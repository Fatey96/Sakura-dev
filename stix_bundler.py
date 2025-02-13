import logging
import traceback
import uuid
from typing import List, Union, Dict, Any
from stix2 import Bundle
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_bundle(stix_objects: List[Any], relationships: List[Any], validate: bool = True) -> str:
    """
    Create a STIX bundle from objects and relationships.
    
    Args:
        stix_objects: List of STIX objects
        relationships: List of STIX relationships
        validate: Whether to validate objects before bundling (default: True)
    
    Returns:
        Serialized STIX bundle as a string
    """
    try:
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
                        logger.warning(f"Invalid STIX object (missing serialize method): {obj}")
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
                        logger.warning(f"Invalid relationship (missing serialize method): {rel}")
                        continue
                    if not all(hasattr(rel, attr) for attr in ['source_ref', 'target_ref', 'relationship_type']):
                        logger.warning(f"Invalid relationship (missing required attributes): {rel}")
                        continue
                all_objects.append(rel)
            except Exception as e:
                logger.error(f"Error processing relationship: {str(e)}")
                continue

        # Create bundle
        bundle = Bundle(
            id=f"bundle--{uuid.uuid4()}",
            objects=all_objects
        )

        # Serialize with error handling
        try:
            serialized_bundle = bundle.serialize(pretty=True)
            
            # Validate JSON structure
            json.loads(serialized_bundle)  # This will raise an error if the JSON is invalid
            
            logger.info(f"Successfully created bundle with {len(all_objects)} total objects")
            return serialized_bundle
            
        except json.JSONDecodeError as je:
            logger.error(f"Invalid JSON produced: {str(je)}")
            raise
        except Exception as e:
            logger.error(f"Error serializing bundle: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Error creating bundle: {str(e)}\n{traceback.format_exc()}")
        raise

def create_bundles_batch(stix_objects: List[Any], relationships: List[Any], batch_size: int = 1000) -> List[str]:
    """
    Create multiple bundles for large datasets.
    
    Args:
        stix_objects: List of STIX objects
        relationships: List of STIX relationships
        batch_size: Maximum number of objects per bundle
    
    Returns:
        List of serialized STIX bundles
    """
    try:
        total_objects = len(stix_objects) + len(relationships)
        if total_objects <= batch_size:
            return [create_bundle(stix_objects, relationships)]

        bundles = []
        for i in range(0, len(stix_objects), batch_size):
            batch_objects = stix_objects[i:i + batch_size]
            
            # Calculate how many relationships to include
            rels_per_batch = min(
                len(relationships),
                max(1, batch_size - len(batch_objects))
            )
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
        logger.error(f"Error in create_bundles_batch: {str(e)}\n{traceback.format_exc()}")
        return []

def merge_bundles(bundles: List[str]) -> str:
    """
    Merge multiple STIX bundles into a single bundle.
    
    Args:
        bundles: List of serialized STIX bundles
    
    Returns:
        Single merged STIX bundle as a string
    """
    try:
        all_objects = []
        seen_ids = set()

        for bundle_str in bundles:
            try:
                bundle_data = json.loads(bundle_str)
                for obj in bundle_data.get('objects', []):
                    # Avoid duplicate objects
                    if obj.get('id') not in seen_ids:
                        all_objects.append(obj)
                        seen_ids.add(obj.get('id'))
            except json.JSONDecodeError as je:
                logger.error(f"Invalid bundle JSON: {str(je)}")
                continue
            except Exception as e:
                logger.error(f"Error processing bundle: {str(e)}")
                continue

        merged_bundle = Bundle(objects=all_objects)
        return merged_bundle.serialize(pretty=True)

    except Exception as e:
        logger.error(f"Error merging bundles: {str(e)}\n{traceback.format_exc()}")
        raise