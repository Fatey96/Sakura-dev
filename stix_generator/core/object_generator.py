"""
STIX object generator module.
"""

import os
import json
import uuid
import random
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import re

import stix2
from stix2 import (
    AttackPattern, Campaign, CourseOfAction, Grouping, Identity, Indicator,
    Infrastructure, IntrusionSet, Location, Malware, MalwareAnalysis, Note,
    ObservedData, Opinion, Report, ThreatActor, Tool, Vulnerability, Incident,
    Sighting, MarkingDefinition, LanguageContent
)

from ..config import (
    OPENAI_API_KEY, LLM_MODEL, LLM_OBJECT_TEMPERATURE, 
    DEFAULT_BATCH_SIZE, MAX_CONCURRENT_REQUESTS, CACHE_ENABLED, CACHE_DIR
)
from ..utils.logging_utils import object_generator_logger as logger
from ..llm.client import get_llm_client
from ..llm.prompts import get_object_generation_prompt_template, get_stix_output_parser, get_stix_object_prompt_template
from ..models.schemas import get_schema_for_type
from ..models.stix_templates import get_examples_for_type

class StixObjectGenerator:
    """
    Generator for STIX objects using LLM.
    """
    
    def __init__(self, api_key: str = OPENAI_API_KEY, seed: int = 42, use_cache: bool = True):
        """
        Initialize the STIX object generator.
        
        Args:
            api_key: OpenAI API key
            seed: Random seed for reproducibility
            use_cache: Whether to use cached objects
        """
        self.api_key = api_key
        self.seed = seed
        self.use_cache = use_cache
        
        # Create cache directory if it doesn't exist and cache is enabled
        if CACHE_ENABLED and self.use_cache and not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
            
        # Initialize LLM client
        self.llm_client = get_llm_client(api_key)
        
        # Set random seed
        random.seed(seed)
        
        logger.info(f"Initialized StixObjectGenerator with seed {seed} and cache usage set to {use_cache}")
        
        self.context = []
    
    async def _generate_stix_objects_batch(self, object_type: str, count: int, context: List[Any], batch_seed: int, special_instructions: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate a batch of STIX objects.
        
        Args:
            object_type: STIX object type
            count: Number of objects to generate
            context: Context for generation
            batch_seed: Random seed for this batch
            special_instructions: Special instructions for object generation
            
        Returns:
            List of generated STIX objects
        """
        try:
            # Set seed for this batch
            random.seed(batch_seed)
            
            # Get LLM client and output parser
            llm = self.llm_client
            output_parser = get_stix_output_parser()
            
            # Get prompt template
            prompt_template = get_stix_object_prompt_template(object_type)
            
            # Add special instructions to the prompt if provided
            if special_instructions:
                prompt_template = prompt_template.replace(
                    "Generate a valid STIX", 
                    f"Generate a valid STIX {object_type} object following these special instructions: {special_instructions}\n\nGenerate a valid STIX"
                )
            
            # Create prompt
            prompt = prompt_template.format(
                object_type=object_type,
                count=count
            )
            
            # Generate objects
            response = await llm.agenerate([prompt])
            
            # Parse response
            try:
                result = response.generations[0][0].text
                objects = output_parser.parse(result)
                
                # Ensure we have the right number of objects
                if len(objects) < count:
                    logger.warning(f"Generated {len(objects)} {object_type} objects, but requested {count}")
                
                # Process each object
                for obj in objects:
                    # Add ID if missing
                    if "id" not in obj:
                        obj["id"] = f"{object_type}--{str(uuid.uuid4())}"
                    
                    # Add type if missing
                    if "type" not in obj:
                        obj["type"] = object_type
                    
                    # Add created/modified timestamps if missing
                    if "created" not in obj:
                        obj["created"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
                    if "modified" not in obj:
                        obj["modified"] = obj["created"]
                
                return objects[:count]  # Ensure we return exactly the requested count
                
            except Exception as e:
                logger.error(f"Error parsing LLM response: {str(e)}")
                return []
                
        except Exception as e:
            logger.error(f"Error generating {object_type} objects: {str(e)}")
            return []
    
    # The rest of the methods remain the same as in the original file
    
    def get_stix_class(self, obj_type: str):
        """
        Get the STIX class for a given object type.
        
        Args:
            obj_type: STIX object type
            
        Returns:
            STIX class or None if not found
        """
        type_map = {
            'attack-pattern': AttackPattern,
            'campaign': Campaign,
            'course-of-action': CourseOfAction,
            'grouping': Grouping,
            'identity': Identity,
            'indicator': Indicator,
            'infrastructure': Infrastructure,
            'intrusion-set': IntrusionSet,
            'location': Location,
            'malware': Malware,
            'malware-analysis': MalwareAnalysis,
            'note': Note,
            'observed-data': ObservedData,
            'opinion': Opinion,
            'report': Report,
            'threat-actor': ThreatActor,
            'tool': Tool,
            'vulnerability': Vulnerability,
            'incident': Incident,
            'sighting': Sighting,
            'marking-definition': MarkingDefinition,
            'language-content': LanguageContent
        }
        return type_map.get(obj_type)
    
    def _save_to_cache(self, obj: Dict[str, Any], obj_type: str) -> None:
        """
        Save an object to cache.
        
        Args:
            obj: STIX object as dictionary
            obj_type: STIX object type
        """
        if not CACHE_ENABLED or not self.use_cache:
            return
            
        cache_path = os.path.join(CACHE_DIR, f"{obj_type}.json")
        
        try:
            # Load existing cache if it exists
            if os.path.exists(cache_path):
                with open(cache_path, 'r') as f:
                    cache = json.load(f)
            else:
                cache = []
            
            # Add new object to cache
            cache.append(obj)
            
            # Save updated cache
            with open(cache_path, 'w') as f:
                json.dump(cache, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving to cache: {str(e)}")
    
    def _load_from_cache(self, obj_type: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Load objects from cache.
        
        Args:
            obj_type: STIX object type
            limit: Maximum number of objects to load
            
        Returns:
            List of cached STIX objects
        """
        if not CACHE_ENABLED or not self.use_cache:
            return []
            
        cache_path = os.path.join(CACHE_DIR, f"{obj_type}.json")
        
        if not os.path.exists(cache_path):
            return []
            
        try:
            with open(cache_path, 'r') as f:
                cache = json.load(f)
                
            if limit is not None:
                return cache[:limit]
            return cache
                
        except Exception as e:
            logger.error(f"Error loading from cache: {str(e)}")
            return []
    
    def get_reference(self, context: List[Any], obj_type: str) -> str:
        """
        Get a reference to an existing object of the specified type.
        
        Args:
            context: List of existing STIX objects
            obj_type: STIX object type
            
        Returns:
            ID of a matching object or a newly generated ID
        """
        matching_objects = []
        
        for obj in context:
            if isinstance(obj, dict) and obj.get('type') == obj_type:
                matching_objects.append(obj)
            elif hasattr(obj, 'type') and obj.type == obj_type:
                matching_objects.append(obj)
        
        if matching_objects:
            selected = random.choice(matching_objects)
            if isinstance(selected, dict):
                return selected['id']
            else:
                return selected.id
        
        # Generate a fallback ID if no matching objects found
        return f"{obj_type}--{uuid.uuid4()}"
    
    def get_references(self, context: List[Any], obj_type: str, count: int) -> List[str]:
        """
        Get references to multiple existing objects of the specified type.
        
        Args:
            context: List of existing STIX objects
            obj_type: STIX object type
            count: Number of references to get
            
        Returns:
            List of object IDs
        """
        matching_objects = []
        
        for obj in context:
            if isinstance(obj, dict) and obj.get('type') == obj_type:
                matching_objects.append(obj)
            elif hasattr(obj, 'type') and obj.type == obj_type:
                matching_objects.append(obj)
        
        if not matching_objects:
            return [f"{obj_type}--{uuid.uuid4()}" for _ in range(count)]
        
        sample_count = min(count, len(matching_objects))
        selected = random.sample(matching_objects, sample_count)
        
        return [obj['id'] if isinstance(obj, dict) else obj.id for obj in selected]
    
    def get_mixed_references(self, context: List[Any], count: int) -> List[str]:
        """
        Get references to multiple existing objects of any type.
        
        Args:
            context: List of existing STIX objects
            count: Number of references to get
            
        Returns:
            List of object IDs
        """
        valid_objects = []
        
        for obj in context:
            if isinstance(obj, dict) and 'id' in obj:
                valid_objects.append(obj)
            elif hasattr(obj, 'id'):
                valid_objects.append(obj)
        
        if not valid_objects:
            types = ["attack-pattern", "indicator", "malware", "threat-actor"]
            return [f"{random.choice(types)}--{uuid.uuid4()}" for _ in range(count)]
        
        sample_count = min(count, len(valid_objects))
        selected = random.sample(valid_objects, sample_count)
        
        return [obj['id'] if isinstance(obj, dict) else obj.id for obj in selected]
    
    def _prepare_object(self, obj: Dict[str, Any], context: List[Any]) -> Dict[str, Any]:
        """
        Prepare a STIX object by ensuring all fields are valid.
        
        Args:
            obj: STIX object as dictionary
            context: Context for generation
            
        Returns:
            Prepared STIX object
        """
        # Ensure ID is in the correct format
        if 'type' in obj and 'id' in obj:
            obj_type = obj['type']
            # Check if ID is in the correct format
            if not re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', obj['id']):
                # Replace with a properly formatted ID
                obj['id'] = f"{obj_type}--{str(uuid.uuid4())}"
        
        # Process references to ensure they are valid
        for key, value in list(obj.items()):
            # Handle reference fields
            if key.endswith('_ref') and isinstance(value, str):
                # Check if the reference is valid
                if not re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', value):
                    # Try to find a valid reference in context
                    ref_type = value.split('--')[0] if '--' in value else None
                    if ref_type:
                        # Find objects of this type in context
                        matching_objects = [c for c in context if isinstance(c, dict) and c.get('type') == ref_type]
                        if matching_objects:
                            # Use a valid ID from context
                            obj[key] = matching_objects[0]['id']
                        else:
                            # Remove invalid reference
                            del obj[key]
                    else:
                        # Remove invalid reference
                        del obj[key]
            
            # Handle reference lists
            elif key.endswith('_refs') and isinstance(value, list):
                valid_refs = []
                for ref in value:
                    if isinstance(ref, str):
                        # Check if the reference is valid
                        if re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', ref):
                            valid_refs.append(ref)
                        else:
                            # Try to find a valid reference in context
                            ref_type = ref.split('--')[0] if '--' in ref else None
                            if ref_type:
                                # Find objects of this type in context
                                matching_objects = [c for c in context if isinstance(c, dict) and c.get('type') == ref_type]
                                if matching_objects:
                                    # Use a valid ID from context
                                    valid_refs.append(matching_objects[0]['id'])
                
                # Update with valid references only
                if valid_refs:
                    obj[key] = valid_refs
                else:
                    # Remove empty reference list
                    del obj[key]
        
        # Ensure created and modified timestamps are in the correct format
        for timestamp_field in ['created', 'modified']:
            if timestamp_field in obj:
                try:
                    # Try to parse the timestamp
                    datetime.fromisoformat(obj[timestamp_field].replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    # Replace with a valid timestamp
                    obj[timestamp_field] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        # Special handling for specific object types
        obj_type = obj.get('type')
        
        # Special handling for observed-data
        if obj_type == 'observed-data':
            self._sanitize_observed_data(obj)
        
        # Special handling for sighting
        elif obj_type == 'sighting':
            # Ensure sighting_of_ref is valid
            if 'sighting_of_ref' in obj and not re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', obj['sighting_of_ref']):
                # Try to find a valid indicator or other observable
                for ref_type in ['indicator', 'malware', 'tool', 'attack-pattern']:
                    matching_objects = [c for c in context if isinstance(c, dict) and c.get('type') == ref_type]
                    if matching_objects:
                        obj['sighting_of_ref'] = matching_objects[0]['id']
                        break
                else:
                    # If no valid reference found, remove the field
                    if 'sighting_of_ref' in obj:
                        del obj['sighting_of_ref']
        
        # Special handling for marking-definition
        elif obj_type == 'marking-definition':
            # Ensure definition_type is valid
            if 'definition_type' not in obj:
                obj['definition_type'] = 'statement'
            
            # Ensure definition is present
            if 'definition' not in obj:
                obj['definition'] = {'statement': 'Copyright. All rights reserved.'}
        
        # Special handling for language-content
        elif obj_type == 'language-content':
            # Ensure object_ref is valid
            if 'object_ref' in obj and not re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', obj['object_ref']):
                # Try to find any valid object
                if context:
                    for c in context:
                        if isinstance(c, dict) and 'id' in c:
                            obj['object_ref'] = c['id']
                            break
                    else:
                        # If no valid reference found, remove the field
                        if 'object_ref' in obj:
                            del obj['object_ref']
            
            # Ensure contents is present
            if 'contents' not in obj:
                obj['contents'] = {'en': {'name': 'English content'}}
        
        return obj
    
    def _sanitize_observed_data(self, obj: Dict[str, Any]) -> None:
        """
        Sanitize observed data to ensure it is valid.
        
        Args:
            obj: Observed data object to sanitize
        """
        if 'objects' not in obj:
            return
            
        sanitized = {}
        for key, value in obj['objects'].items():
            if isinstance(value, dict):
                if 'type' in value:
                    if value['type'] == 'file':
                        value.pop('created', None)
                    elif value['type'] == 'process':
                        value.pop('created', None)
                    elif value['type'] == 'network-traffic':
                        if 'src_ref' in value and not isinstance(value['src_ref'], str):
                            value['src_ref'] = str(value['src_ref'])
                        if 'dst_ref' in value and not isinstance(value['dst_ref'], str):
                            value['dst_ref'] = str(value['dst_ref'])
                sanitized[key] = value
        
        obj['objects'] = sanitized
    
    def convert_to_stix2_object(self, obj: Dict[str, Any]) -> Optional[Any]:
        """
        Convert a dictionary to a STIX2 object.
        
        Args:
            obj: STIX object as dictionary
            
        Returns:
            STIX2 object or None if conversion fails
        """
        try:
            # Get the STIX class for this object type
            obj_type = obj.get('type')
            if not obj_type:
                logger.error(f"Object missing 'type' field: {obj}")
                return None
                
            stix_class = self.get_stix_class(obj_type)
            if not stix_class:
                logger.error(f"Unsupported STIX object type: {obj_type}")
                return None
            
            # Fix common issues before conversion
            obj_copy = obj.copy()
            
            # Ensure ID is in the correct format
            if 'id' in obj_copy:
                if not re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', obj_copy['id']):
                    obj_copy['id'] = f"{obj_type}--{str(uuid.uuid4())}"
            
            # Fix reference fields
            for key, value in list(obj_copy.items()):
                # Handle reference fields
                if key.endswith('_ref') and isinstance(value, str):
                    # Check if the reference is valid
                    if not re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', value):
                        # Remove invalid reference
                        del obj_copy[key]
                
                # Handle reference lists
                elif key.endswith('_refs') and isinstance(value, list):
                    valid_refs = []
                    for ref in value:
                        if isinstance(ref, str) and re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', ref):
                            valid_refs.append(ref)
                    
                    # Update with valid references only
                    if valid_refs:
                        obj_copy[key] = valid_refs
                    else:
                        # Remove empty reference list
                        del obj_copy[key]
            
            # Ensure timestamps are in the correct format
            for timestamp_field in ['created', 'modified']:
                if timestamp_field in obj_copy:
                    try:
                        # Try to parse the timestamp
                        datetime.fromisoformat(obj_copy[timestamp_field].replace('Z', '+00:00'))
                    except (ValueError, TypeError):
                        # Replace with a valid timestamp
                        obj_copy[timestamp_field] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            
            # Special handling for observed-data
            if obj_type == 'observed-data':
                self._sanitize_observed_data(obj_copy)
            
            # Convert to STIX2 object
            return stix_class(**obj_copy)
            
        except Exception as e:
            logger.error(f"Error converting to STIX2 object: {str(e)}")
            return None
    
    async def generate_stix_objects(self, object_type: str, count: int, special_instructions: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate STIX objects of a specific type.
        
        Args:
            object_type: STIX object type
            count: Number of objects to generate
            special_instructions: Special instructions for object generation
            
        Returns:
            List of generated STIX objects
        """
        logger.info(f"Generating {count} {object_type} objects")
        
        # Check if we can load from cache
        cached_objects = self._load_from_cache(object_type, count)
        if cached_objects and len(cached_objects) >= count and not special_instructions:
            logger.info(f"Loaded {len(cached_objects[:count])} {object_type} objects from cache")
            return cached_objects[:count]
        
        # Initialize result list
        result = []
        
        # Add cached objects if available and no special instructions
        if cached_objects and not special_instructions:
            result.extend(cached_objects)
            count -= len(cached_objects)
            logger.info(f"Loaded {len(cached_objects)} {object_type} objects from cache, generating {count} more")
        
        # If we still need to generate objects
        if count > 0:
            # Determine batch size
            batch_size = min(DEFAULT_BATCH_SIZE, count)
            
            # Calculate number of batches
            num_batches = (count + batch_size - 1) // batch_size
            
            # Generate objects in batches
            for i in range(num_batches):
                # Calculate batch count
                batch_count = min(batch_size, count - i * batch_size)
                
                # Generate batch
                batch_seed = self.seed + i
                batch = await self._generate_stix_objects_batch(
                    object_type, 
                    batch_count, 
                    self.context, 
                    batch_seed,
                    special_instructions
                )
                
                # Process and add to result
                for obj in batch:
                    # Prepare object
                    obj = self._prepare_object(obj, self.context)
                    
                    # Add to result
                    result.append(obj)
                    
                    # Save to cache if no special instructions
                    if not special_instructions:
                        self._save_to_cache(obj, object_type)
                    
                # Add to context
                self.context.extend(batch)
        
        return result
    
    async def generate_dataset(self, object_counts: Dict[str, int], special_instructions: Optional[Dict[str, str]] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate a dataset of STIX objects in a phased approach to ensure proper references.
        
        Args:
            object_counts: Dictionary mapping object types to counts
            special_instructions: Dictionary mapping object types to special instructions
            
        Returns:
            Dictionary mapping object types to lists of generated objects
        """
        if special_instructions is None:
            special_instructions = {}
            
        logger.info(f"Generating dataset with counts: {object_counts}")
        logger.info(f"Special instructions: {special_instructions}")
        
        # Initialize result dictionary
        result = {}
        
        # Define generation phases to ensure proper references
        # Phase 1: Generate independent objects that don't typically reference others
        phase1_types = [
            'identity',
            'location',
            'vulnerability',
            'attack-pattern',
            'marking-definition',
            'language-content'
        ]
        
        # Phase 2: Generate objects that reference Phase 1 objects
        phase2_types = [
            'threat-actor',
            'malware',
            'tool',
            'course-of-action',
            'infrastructure',
            'malware-analysis'
        ]
        
        # Phase 3: Generate objects that reference Phase 1 and Phase 2 objects
        phase3_types = [
            'campaign',
            'intrusion-set',
            'indicator',
            'opinion',
            'note'
        ]
        
        # Phase 4: Generate objects that reference all previous phases
        phase4_types = [
            'observed-data',
            'report',
            'grouping',
            'incident',
            'sighting'
        ]
        
        # All supported STIX object types
        all_stix_types = phase1_types + phase2_types + phase3_types + phase4_types
        
        # Process each phase
        for phase_num, phase_types in enumerate([phase1_types, phase2_types, phase3_types, phase4_types], 1):
            logger.info(f"Starting generation phase {phase_num} with object types: {phase_types}")
            phase_objects = {}
            
            # Generate objects for each type in this phase
            for obj_type in phase_types:
                if obj_type in object_counts and object_counts[obj_type] > 0:
                    # Get special instructions for this object type if available
                    obj_instructions = special_instructions.get(obj_type, None)
                    if obj_instructions:
                        logger.info(f"Using special instructions for {obj_type}: {obj_instructions}")
                    
                    # Generate objects
                    objects = await self.generate_stix_objects(obj_type, object_counts[obj_type], obj_instructions)
                    
                    # Process generated objects to ensure valid IDs
                    processed_objects = []
                    for obj in objects:
                        # Ensure ID is a valid UUID format
                        if 'id' in obj:
                            # Check if ID is in the correct format
                            if not re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', obj['id']):
                                # Replace with a properly formatted ID
                                obj['id'] = f"{obj_type}--{str(uuid.uuid4())}"
                        else:
                            obj['id'] = f"{obj_type}--{str(uuid.uuid4())}"
                        
                        # Add to processed objects
                        processed_objects.append(obj)
                    
                    # Add to phase objects
                    phase_objects[obj_type] = processed_objects
                    
                    # Add to result
                    result[obj_type] = processed_objects
                    
                    logger.info(f"Generated {len(processed_objects)} {obj_type} objects in phase {phase_num}")
            
            # Add all objects from this phase to context before moving to next phase
            for obj_list in phase_objects.values():
                self.context.extend(obj_list)
            
            logger.info(f"Completed generation phase {phase_num}")
        
        # Process any remaining object types not covered in the phases
        remaining_types = [obj_type for obj_type in object_counts.keys() 
                          if obj_type not in all_stix_types]
        
        if remaining_types:
            logger.info(f"Processing remaining object types: {remaining_types}")
            
            for obj_type in remaining_types:
                if object_counts[obj_type] > 0:
                    # Get special instructions for this object type if available
                    obj_instructions = special_instructions.get(obj_type, None)
                    if obj_instructions:
                        logger.info(f"Using special instructions for {obj_type}: {obj_instructions}")
                    
                    # Generate objects
                    objects = await self.generate_stix_objects(obj_type, object_counts[obj_type], obj_instructions)
                    
                    # Process generated objects to ensure valid IDs
                    processed_objects = []
                    for obj in objects:
                        # Ensure ID is a valid UUID format
                        if 'id' in obj:
                            # Check if ID is in the correct format
                            if not re.match(r'^[a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', obj['id']):
                                # Replace with a properly formatted ID
                                obj['id'] = f"{obj_type}--{str(uuid.uuid4())}"
                        else:
                            obj['id'] = f"{obj_type}--{str(uuid.uuid4())}"
                        
                        # Add to processed objects
                        processed_objects.append(obj)
                    
                    # Add to result
                    result[obj_type] = processed_objects
                    
                    # Add to context
                    self.context.extend(processed_objects)
                    
                    logger.info(f"Generated {len(processed_objects)} {obj_type} objects (custom type)")
        
        logger.info(f"Dataset generation complete with {sum(len(objs) for objs in result.values())} total objects")
        return result
    
    async def create_stix2_objects(self, all_objects: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Convert all generated objects to STIX2 objects.
        
        Args:
            all_objects: Dictionary mapping object types to lists of objects
            
        Returns:
            Dictionary mapping object IDs to STIX2 objects
        """
        logger.info(f"Converting {sum(len(objs) for objs in all_objects.values())} objects to STIX2 format")
        
        # Initialize result dictionary
        result = {}
        
        # Define conversion order to ensure proper references
        # Phase 1: Independent objects
        phase1_types = [
            'identity',
            'location',
            'vulnerability',
            'attack-pattern',
            'marking-definition',
            'language-content'
        ]
        
        # Phase 2: Objects that reference Phase 1 objects
        phase2_types = [
            'threat-actor',
            'malware',
            'tool',
            'course-of-action',
            'infrastructure',
            'malware-analysis'
        ]
        
        # Phase 3: Objects that reference Phase 1 and Phase 2 objects
        phase3_types = [
            'campaign',
            'intrusion-set',
            'indicator',
            'opinion',
            'note'
        ]
        
        # Phase 4: Objects that reference all previous phases
        phase4_types = [
            'observed-data',
            'report',
            'grouping',
            'incident',
            'sighting'
        ]
        
        # All supported STIX object types
        all_stix_types = phase1_types + phase2_types + phase3_types + phase4_types
        
        # Process each phase
        for phase_num, phase_types in enumerate([phase1_types, phase2_types, phase3_types, phase4_types], 1):
            logger.info(f"Converting phase {phase_num} objects: {phase_types}")
            
            # Convert objects for each type in this phase
            for obj_type in phase_types:
                if obj_type in all_objects:
                    objects = all_objects[obj_type]
                    logger.info(f"Converting {len(objects)} {obj_type} objects")
                    
                    # Convert each object
                    for obj in objects:
                        stix2_obj = self.convert_to_stix2_object(obj)
                        if stix2_obj:
                            result[obj['id']] = stix2_obj
                        else:
                            logger.warning(f"Failed to convert {obj_type} object: {obj.get('id', 'unknown')}")
        
        # Process any remaining object types
        remaining_types = [obj_type for obj_type in all_objects.keys() 
                          if obj_type not in all_stix_types]
        
        if remaining_types:
            logger.info(f"Converting remaining object types: {remaining_types}")
            
            for obj_type in remaining_types:
                if obj_type in all_objects:
                    objects = all_objects[obj_type]
                    logger.info(f"Converting {len(objects)} {obj_type} objects")
                    
                    # Convert each object
                    for obj in objects:
                        stix2_obj = self.convert_to_stix2_object(obj)
                        if stix2_obj:
                            result[obj['id']] = stix2_obj
                        else:
                            logger.warning(f"Failed to convert {obj_type} object: {obj.get('id', 'unknown')}")
        
        logger.info(f"Successfully converted {len(result)} objects to STIX2 format")
        return result