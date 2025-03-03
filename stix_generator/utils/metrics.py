"""
STIX quality metrics calculation module.
"""

import json
from typing import Dict, Any, List, Optional

from ..utils.logging_utils import setup_logger

logger = setup_logger("stix_generator.metrics")

def analyze_stix_bundle(stix_bundle: str) -> Dict[str, Any]:
    """
    Analyze a STIX bundle and calculate quality metrics.
    
    Args:
        stix_bundle: STIX bundle in JSON string format
        
    Returns:
        Dictionary of metrics
    """
    try:
        # Parse the STIX bundle
        bundle_data = json.loads(stix_bundle)
        objects = bundle_data.get('objects', [])
        
        if not objects:
            logger.warning("Empty STIX bundle provided for analysis")
            # Return default metrics structure to prevent frontend errors
            return {
                "basic_metrics": {
                    "summary": {
                        "total_objects": 0,
                        "relationship_count": 0,
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
        
        # Basic metrics
        total_objects = len(objects)
        object_types = {}
        relationship_types = {}
        relationship_count = 0
        domain_objects = 0
        
        # Analyze objects
        for obj in objects:
            obj_type = obj.get('type', 'unknown')
            
            # Track object types
            object_types[obj_type] = object_types.get(obj_type, 0) + 1
            
            # Count relationships
            if obj_type == 'relationship':
                relationship_count += 1
                rel_type = obj.get('relationship_type', 'unknown')
                relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
            else:
                domain_objects += 1
        
        # Calculate relationship density (relationships per domain object)
        relationship_density = relationship_count / domain_objects if domain_objects > 0 else 0
        
        # Calculate completeness score (percentage of objects with all required properties)
        required_props = {
            'indicator': ['pattern', 'valid_from'],
            'malware': ['name', 'malware_types'],
            'threat-actor': ['name', 'threat_actor_types'],
            'attack-pattern': ['name'],
            'relationship': ['source_ref', 'target_ref', 'relationship_type'],
            # Add more as needed
        }
        
        complete_objects = 0
        for obj in objects:
            obj_type = obj.get('type', '')
            if obj_type in required_props:
                if all(prop in obj for prop in required_props[obj_type]):
                    complete_objects += 1
                    
        completeness_score = (complete_objects / total_objects * 100) if total_objects > 0 else 0
        
        # Calculate consistency score based on reference validity
        valid_references = 0
        total_references = 0
        
        all_ids = set(obj.get('id', '') for obj in objects)
        
        for obj in objects:
            if obj.get('type') == 'relationship':
                total_references += 2  # source_ref and target_ref
                
                source_ref = obj.get('source_ref', '')
                target_ref = obj.get('target_ref', '')
                
                if source_ref in all_ids:
                    valid_references += 1
                    
                if target_ref in all_ids:
                    valid_references += 1
        
        consistency_score = (valid_references / total_references * 100) if total_references > 0 else 100
        
        # Calculate relationship score based on density and distribution
        relationship_diversity = len(relationship_types) / len(object_types) if object_types else 0
        relationship_score = min(100, (relationship_density * 10 + relationship_diversity * 5) * 10)
        
        # Overall quality score
        quality_score = (completeness_score * 0.4 + consistency_score * 0.3 + relationship_score * 0.3)
        
        # Generate recommendations
        recommendations = []
        
        if completeness_score < 70:
            recommendations.append("Add more details to objects to improve completeness")
            
        if consistency_score < 70:
            recommendations.append("Fix invalid references between objects")
            
        if relationship_score < 50:
            recommendations.append("Add more diverse relationships between objects")
            
        if relationship_density < 0.5:
            recommendations.append("Increase the number of relationships between objects")
            
        # Construct and return metrics
        return {
            "basic_metrics": {
                "summary": {
                    "total_objects": total_objects,
                    "relationship_count": relationship_count,
                    "quality_score": round(quality_score, 1),
                    "completeness_score": round(completeness_score, 1),
                    "consistency_score": round(consistency_score, 1),
                    "relationship_score": round(relationship_score, 1),
                    "relationship_density": round(relationship_density, 2)
                },
                "object_type_distribution": object_types,
                "relationship_type_distribution": relationship_types
            },
            "advanced_metrics": {
                "object_connectivity": round(relationship_density * 100, 1),
                "relationship_diversity": round(relationship_diversity * 100, 1),
                "narrative_coherence": round(consistency_score * 0.8, 1)  # Simplified estimate
            },
            "recommendations": recommendations
        }
            
    except Exception as e:
        logger.error(f"Error analyzing STIX bundle: {str(e)}")
        # Return default metrics structure on error
        return {
            "basic_metrics": {
                "summary": {
                    "total_objects": 0,
                    "relationship_count": 0,
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
            "recommendations": ["Error analyzing STIX bundle"]
        }