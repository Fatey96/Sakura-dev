"""
STIX bundling utilities.
"""

import json
import traceback
from typing import List, Dict, Any, Union, Optional

from stix2 import Bundle

from ..utils.logging_utils import bundler_logger as logger

def create_bundle(
    stix_objects: List[Any], 
    relationships: List[Any] = None, 
    validate: bool = True
) -> Bundle:
    """
    Create a STIX bundle from objects and relationships.
    
    Args:
        stix_objects: List of STIX objects
        relationships: List of STIX relationships (optional)
        validate: Whether to validate objects before bundling
        
    Returns:
        STIX Bundle
    """
    try:
        relationships = relationships or []
        logger.info(f"Creating bundle with {len(stix_objects)} objects and {len(relationships)} relationships")
        
        # Validate inputs
        if not isinstance(stix_objects, list) or not isinstance(relationships, list):
            raise ValueError("Both stix_objects and relationships must be lists")

        # Combine objects
        all_objects = []
        
        # Add STIX objects
        for obj in stix_objects:
            try:
                if validate:
                    if not hasattr(obj, 'serialize'):
                        logger.warning(f"Invalid STIX object (missing serialize method): {type(obj)}")
                        continue
                    if not getattr(obj, 'id', None):
                        logger.warning(f"Invalid STIX object (missing id): {obj}")
                        continue
                all_objects.append(obj)
            except Exception as e:
                logger.error(f"Error processing STIX object: {str(e)}")
                continue
                
        # Add relationships
        for rel in relationships:
            try:
                if validate:
                    if not hasattr(rel, 'serialize'):
                        logger.warning(f"Invalid relationship object: {type(rel)}")
                        continue
                all_objects.append(rel)
            except Exception as e:
                logger.error(f"Error processing relationship: {str(e)}")
                continue

        # Create and return bundle
        bundle = Bundle(objects=all_objects)
        logger.info(f"Successfully created bundle with {len(all_objects)} total objects")
        return bundle

    except Exception as e:
        logger.error(f"Error creating bundle: {str(e)}\n{traceback.format_exc()}")
        # Return an empty bundle rather than raising an exception
        return Bundle(objects=[])

def create_bundle_batches(
    stix_objects: List[Any], 
    relationships: List[Any] = None, 
    batch_size: int = 1000
) -> List[Bundle]:
    """
    Create multiple bundles for large datasets.
    
    Args:
        stix_objects: List of STIX objects
        relationships: List of STIX relationships (optional)
        batch_size: Maximum number of objects per bundle
        
    Returns:
        List of STIX Bundles
    """
    try:
        relationships = relationships or []
        total_objects = len(stix_objects) + len(relationships)
        
        if total_objects <= batch_size:
            return [create_bundle(stix_objects, relationships)]

        bundles = []
        
        # Process objects in batches
        for i in range(0, len(stix_objects), batch_size):
            batch_objects = stix_objects[i:i + batch_size]
            
            # Calculate how many relationships to include
            rels_per_batch = min(
                len(relationships),
                max(1, batch_size - len(batch_objects))
            )
            
            # Use a copy to avoid modifying the original list
            batch_relationships = relationships[:rels_per_batch]
            relationships = relationships[rels_per_batch:]  # Remove used relationships
            
            try:
                bundle = create_bundle(batch_objects, batch_relationships)
                bundles.append(bundle)
                logger.info(f"Created batch bundle {len(bundles)} with {len(batch_objects)} objects and {rels_per_batch} relationships")
            except Exception as e:
                logger.error(f"Error creating batch bundle: {str(e)}")
                continue

        return bundles

    except Exception as e:
        logger.error(f"Error in create_bundle_batches: {str(e)}\n{traceback.format_exc()}")
        return []

def merge_bundles(bundles: List[Bundle]) -> Bundle:
    """
    Merge multiple STIX bundles into a single bundle.
    
    Args:
        bundles: List of STIX Bundles
        
    Returns:
        Merged STIX Bundle
    """
    try:
        all_objects = []
        seen_ids = set()

        for bundle in bundles:
            try:
                for obj in bundle.objects:
                    # Avoid duplicate objects
                    if obj.id not in seen_ids:
                        all_objects.append(obj)
                        seen_ids.add(obj.id)
            except Exception as e:
                logger.error(f"Error processing bundle: {str(e)}")
                continue

        merged_bundle = Bundle(objects=all_objects)
        logger.info(f"Successfully merged {len(bundles)} bundles into one with {len(all_objects)} objects")
        return merged_bundle

    except Exception as e:
        logger.error(f"Error merging bundles: {str(e)}\n{traceback.format_exc()}")
        return Bundle(objects=[])

def serialize_bundle(bundle: Bundle, pretty: bool = True) -> str:
    """
    Serialize a STIX bundle to JSON.
    
    Args:
        bundle: STIX Bundle
        pretty: Whether to format the JSON with indentation
        
    Returns:
        JSON string
    """
    try:
        return bundle.serialize(pretty=pretty)
    except Exception as e:
        logger.error(f"Error serializing bundle: {str(e)}")
        return json.dumps({"type": "bundle", "id": f"bundle--error", "objects": []})

def load_bundle(bundle_json: str) -> Optional[Bundle]:
    """
    Load a STIX bundle from JSON.
    
    Args:
        bundle_json: JSON string
        
    Returns:
        STIX Bundle or None if loading fails
    """
    try:
        return Bundle.parse(bundle_json)
    except Exception as e:
        logger.error(f"Error loading bundle: {str(e)}")
        return None