"""
Flask API routes for STIX generator.
"""

import os
import json
import asyncio
import shutil
from datetime import datetime
from typing import Dict, Any, List, Optional

from flask import Blueprint, request, jsonify, render_template, send_file, current_app
from werkzeug.utils import secure_filename

from ..config import (
    DEFAULT_OBJECT_COUNTS, DISPLAY_TO_STIX_TYPE, OBJECT_TYPE_DISPLAY_NAMES,
    OUTPUT_DIR, CACHE_DIR, CACHE_ENABLED
)
from ..utils.logging_utils import api_logger as logger
from ..core.object_generator import StixObjectGenerator
from ..core.relationship_generator import RelationshipGenerator
from ..core.bundler import create_bundle, serialize_bundle
from ..utils.metrics import analyze_stix_bundle

# Create Blueprint
api_bp = Blueprint('api', __name__)

def distribute_total_count(total_count: int) -> Dict[str, int]:
    """
    Distribute a total count across STIX object types.
    
    Args:
        total_count: Total number of objects to generate
        
    Returns:
        Dictionary mapping object types to counts
    """
    # Define approximate percentages for each type
    distribution = {
        'indicator': 0.20,        # 20%
        'observed-data': 0.15,    # 15%
        'malware': 0.12,          # 12%
        'attack-pattern': 0.10,   # 10%
        'threat-actor': 0.08,     # 8%
        'tool': 0.08,             # 8%
        'vulnerability': 0.07,    # 7%
        'identity': 0.05,         # 5%
        'campaign': 0.05,         # 5%
        'intrusion-set': 0.04,    # 4%
        'course-of-action': 0.03, # 3%
        'report': 0.03            # 3%
    }
    
    # Calculate counts and handle rounding
    counts = {}
    remaining = total_count
    
    for obj_type, percentage in distribution.items():
        count = int(total_count * percentage)
        counts[obj_type] = max(1, count)  # Ensure at least 1 of each type
        remaining -= counts[obj_type]
    
    # Distribute any remaining counts to indicators and observed-data
    if remaining > 0:
        counts['indicator'] += remaining // 2
        counts['observed-data'] += remaining - (remaining // 2)
    
    return counts

@api_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@api_bp.route('/objects', methods=['GET'])
def get_object_types():
    """Get available STIX object types."""
    return jsonify({
        "object_types": OBJECT_TYPE_DISPLAY_NAMES
    })

# This is the main route used by the frontend
@api_bp.route('/generate-graph', methods=['POST'])
def generate_graph():
    """Generate STIX graph with objects and relationships."""
    try:
        data = request.get_json()
        logger.info(f"Received generation request: {data}")
        
        # Get generation method and object counts
        generation_method = data.get('method', 'manual')
        object_counts = {}
        
        # Get cache usage preference
        use_cache = data.get('use_cache', True)
        logger.info(f"Cache usage set to: {use_cache}")
        
        # Get special instructions
        special_instructions = data.get('special_instructions', {})
        logger.info(f"Special instructions received: {special_instructions}")
        
        if generation_method == 'manual':
            # Get counts from the data
            counts = data.get('counts', {})
            if isinstance(counts, dict):
                raw_counts = counts
            else:
                raw_counts = data
            
            # Process object counts
            for display_name, count in raw_counts.items():
                try:
                    stix_type = DISPLAY_TO_STIX_TYPE.get(display_name)
                    if not stix_type:
                        stix_type = display_name  # Try using the name directly
                        
                    if stix_type and int(count) > 0:
                        object_counts[stix_type] = int(count)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid count for {display_name}: {count}")
                    continue
                    
            logger.info(f"Processed object counts: {object_counts}")
            
        else:
            # Handle total count method
            try:
                total_count = int(data.get('totalCount', 0))
                if total_count <= 0:
                    return jsonify({
                        "error": "Total count must be greater than 0",
                        "status": "error"
                    }), 400
                    
                object_counts = distribute_total_count(total_count)
                logger.info(f"Distributed total count {total_count} into: {object_counts}")
                
            except (ValueError, TypeError) as e:
                return jsonify({
                    "error": f"Invalid total count: {data.get('totalCount')}",
                    "status": "error"
                }), 400
        
        # Validate object counts
        if not object_counts:
            logger.error(f"No valid object counts found in request data: {data}")
            return jsonify({
                "error": "No objects selected for generation",
                "status": "error"
            }), 400
        
        # Initialize generators
        seed = data.get('seed', 42)
        object_generator = StixObjectGenerator(seed=seed, use_cache=use_cache)
        relationship_generator = RelationshipGenerator(seed=seed)
        
        # Create the event loop but don't close it immediately
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Generate objects
            logger.info("Generating STIX objects...")
            stix_objects_dict = loop.run_until_complete(object_generator.generate_dataset(object_counts, special_instructions))
            
            # Flatten objects list
            all_stix_objects = []
            for obj_list in stix_objects_dict.values():
                all_stix_objects.extend(obj_list)
            
            # Convert to STIX2 objects
            logger.info("Converting to STIX2 objects...")
            stix2_objects_dict = loop.run_until_complete(object_generator.create_stix2_objects(stix_objects_dict))
            stix2_objects = list(stix2_objects_dict.values())
            
            # Generate relationships
            logger.info("Generating relationships...")
            relationship_output = loop.run_until_complete(relationship_generator.generate_relationships(all_stix_objects))
            
            # Run any pending tasks to allow for proper cleanup
            pending = asyncio.all_tasks(loop)
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            
            # Convert relationships to STIX2 objects
            stix2_relationships = relationship_generator.create_stix2_relationships(
                relationship_output['relationships']
            )
            
            # Create bundle
            logger.info("Creating STIX bundle...")
            stix_bundle = create_bundle(stix2_objects, stix2_relationships)
            
            # Calculate metrics
            logger.info("Calculating metrics...")
            try:
                bundle_json = serialize_bundle(stix_bundle)
                metrics = analyze_stix_bundle(bundle_json)
                
                # Ensure metrics has the expected structure to match frontend expectations
                if "basic_metrics" not in metrics:
                    metrics = {
                        "basic_metrics": {
                            "summary": {
                                "total_objects": len(stix_bundle.objects) if hasattr(stix_bundle, 'objects') else 0,
                                "relationship_count": len(stix2_relationships),
                                "quality_score": 0.0,
                                "completeness_score": 0.0,
                                "consistency_score": 0.0,
                                "relationship_score": 0.0,
                                "relationship_density": 0.0
                            },
                            "object_type_distribution": {},
                            "relationship_type_distribution": {}
                        },
                        "advanced_metrics": {
                            "object_connectivity": 0.0,
                            "relationship_diversity": 0.0,
                            "narrative_coherence": 0.0
                        },
                        "recommendations": []
                    }
                
                # Ensure all required fields exist
                if "summary" not in metrics.get("basic_metrics", {}):
                    metrics["basic_metrics"]["summary"] = {
                        "total_objects": len(stix_bundle.objects) if hasattr(stix_bundle, 'objects') else 0,
                        "relationship_count": len(stix2_relationships),
                        "quality_score": 0.0,
                        "completeness_score": 0.0,
                        "consistency_score": 0.0,
                        "relationship_score": 0.0,
                        "relationship_density": 0.0
                    }
                
                # Make sure relationship_density is defined
                if "relationship_density" not in metrics.get("basic_metrics", {}).get("summary", {}):
                    metrics["basic_metrics"]["summary"]["relationship_density"] = 0.0
                
            except Exception as e:
                logger.error(f"Error calculating metrics: {str(e)}")
                metrics = {
                    "basic_metrics": {
                        "summary": {
                            "total_objects": len(stix_bundle.objects) if hasattr(stix_bundle, 'objects') else 0,
                            "relationship_count": len(stix2_relationships),
                            "quality_score": 0.0,
                            "completeness_score": 0.0,
                            "consistency_score": 0.0,
                            "relationship_score": 0.0,
                            "relationship_density": 0.0
                        },
                        "object_type_distribution": {},
                        "relationship_type_distribution": {}
                    },
                    "advanced_metrics": {
                        "object_connectivity": 0.0,
                        "relationship_diversity": 0.0,
                        "narrative_coherence": 0.0
                    },
                    "recommendations": ["Error calculating metrics"]
                }
            
            # Save bundle to file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"stix_bundle_{timestamp}_{seed}.json"
            filepath = os.path.join(OUTPUT_DIR, secure_filename(filename))
            
            with open(filepath, 'w') as f:
                f.write(bundle_json)
            
            logger.info(f"STIX bundle saved to {filepath}")
            
            # Return result in the format expected by the frontend
            return jsonify({
                "stix_bundle": bundle_json,
                "metrics": metrics,
                "story": relationship_output.get('scenario', ''),
                "status": "success",
                "filename": filename
            })
            
        finally:
            # Properly close the loop after all tasks are done
            try:
                # Cancel any remaining tasks
                for task in asyncio.all_tasks(loop):
                    task.cancel()
                
                # Run the event loop once more to let any callbacks run
                loop.run_until_complete(asyncio.sleep(0.1))
                loop.close()
            except Exception as e:
                logger.warning(f"Error during event loop cleanup: {e}")
        
    except Exception as e:
        logger.error(f"Error in generate_graph: {str(e)}", exc_info=True)
        return jsonify({
            "error": str(e),
            "status": "error",
            "metrics": {
                "basic_metrics": {
                    "summary": {
                        "total_objects": 0,
                        "quality_score": 0.0,
                        "completeness_score": 0.0,
                        "consistency_score": 0.0,
                        "relationship_score": 0.0
                    }
                }
            }
        }), 500

@api_bp.route('/download/<filename>')
def download_file(filename):
    """Download a generated STIX bundle."""
    try:
        filepath = os.path.join(OUTPUT_DIR, secure_filename(filename))
        if not os.path.exists(filepath):
            return jsonify({
                "error": f"File {filename} not found",
                "status": "error"
            }), 404
            
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@api_bp.route('/files')
def list_files():
    """List generated STIX files."""
    try:
        files = []
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(OUTPUT_DIR, filename)
                stats = os.stat(filepath)
                
                # Get object counts and metrics if possible
                metrics = {"object_count": 0, "quality_score": 0}
                try:
                    with open(filepath, 'r') as f:
                        bundle = json.load(f)
                        metrics["object_count"] = len(bundle.get("objects", []))
                except:
                    pass
                
                files.append({
                    "filename": filename,
                    "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "size": stats.st_size,
                    "metrics": metrics,
                    "download_url": f"/api/download/{filename}"
                })
        
        return jsonify({
            "files": sorted(files, key=lambda x: x["created"], reverse=True),
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@api_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the STIX object cache."""
    try:
        if not CACHE_ENABLED:
            return jsonify({
                "status": "success",
                "message": "Cache is disabled, nothing to clear"
            })
            
        if os.path.exists(CACHE_DIR):
            # Remove all files in the cache directory
            for filename in os.listdir(CACHE_DIR):
                file_path = os.path.join(CACHE_DIR, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            
            return jsonify({
                "status": "success",
                "message": "Cache cleared successfully"
            })
        else:
            return jsonify({
                "status": "success",
                "message": "Cache directory does not exist"
            })
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"Failed to clear cache: {str(e)}"
        }), 500