"""
STIX relationship generator module.
"""

import uuid
import json
import random
from typing import List, Dict, Any, Optional, Union

from stix2 import Relationship

from ..config import (
    OPENAI_API_KEY, LLM_MODEL, LLM_RELATIONSHIP_TEMPERATURE, 
    RELATIONSHIP_MAP
)
from ..utils.logging_utils import relationship_generator_logger as logger
from ..llm.client import get_llm_client
from ..llm.prompts import get_relationship_generation_prompt_template, get_relationship_output_parser

class RelationshipGenerator:
    """STIX relationship generator class."""
    
    def __init__(self, api_key: str = OPENAI_API_KEY, seed: int = 42):
        """
        Initialize the relationship generator.
        
        Args:
            api_key: OpenAI API key
            seed: Random seed for reproducibility
        """
        self.api_key = api_key
        self.seed = seed
        random.seed(seed)
    
    def _validate_relationship(
        self, relationship: Dict[str, Any], stix_objects: List[Dict[str, Any]]
    ) -> bool:
        """
        Validate a relationship.
        
        Args:
            relationship: Relationship to validate
            stix_objects: List of STIX objects
            
        Returns:
            True if the relationship is valid, False otherwise
        """
        try:
            source_ref = relationship.get('source_ref', '')
            target_ref = relationship.get('target_ref', '')
            
            if not source_ref or not target_ref:
                return False
                
            # Extract types from references
            source_type = source_ref.split('--')[0]
            target_type = target_ref.split('--')[0]
            relationship_type = relationship.get('relationship_type', '')
            
            # Check if relationship type is valid for these object types
            if source_type not in RELATIONSHIP_MAP:
                return False
            if target_type not in RELATIONSHIP_MAP.get(source_type, {}):
                return False
            if relationship_type not in RELATIONSHIP_MAP.get(source_type, {}).get(target_type, []):
                return False
            
            # Check if referenced objects exist
            object_ids = {obj['id'] for obj in stix_objects}
            if source_ref not in object_ids:
                return False
            if target_ref not in object_ids:
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating relationship: {str(e)}")
            return False
    
    def _generate_relationship_description(
        self, source_obj: Dict[str, Any], target_obj: Dict[str, Any], relationship_type: str
    ) -> str:
        """
        Generate a meaningful description for a relationship.
        
        Args:
            source_obj: Source object
            target_obj: Target object
            relationship_type: Type of relationship
            
        Returns:
            Description of the relationship
        """
        templates = {
            "uses": [
                "{source_name} utilizes {target_name} in their operations",
                "{source_name} has been observed using {target_name}",
                "{source_name} leverages {target_name} for their activities"
            ],
            "targets": [
                "{source_name} specifically targets {target_name}",
                "{source_name} has been known to target {target_name}",
                "{source_name} focuses attacks on {target_name}"
            ],
            "indicates": [
                "{source_name} provides evidence of {target_name}",
                "{source_name} has been associated with {target_name}",
                "{source_name} suggests the presence of {target_name}"
            ],
            "mitigates": [
                "{source_name} helps prevent {target_name}",
                "{source_name} is effective against {target_name}",
                "{source_name} can be used to counter {target_name}"
            ],
            "attributed-to": [
                "{source_name} is attributed to {target_name}",
                "{source_name} is believed to be operated by {target_name}",
                "{source_name} is connected to {target_name}"
            ],
            "exploits": [
                "{source_name} exploits {target_name} to gain unauthorized access",
                "{source_name} takes advantage of {target_name}",
                "{source_name} leverages {target_name} as an attack vector"
            ]
        }
        
        template_list = templates.get(relationship_type, ["{source_name} {relationship_type} {target_name}"])
        template = random.choice(template_list)
        
        return template.format(
            source_name=source_obj.get('name', source_obj['type']),
            target_name=target_obj.get('name', target_obj['type']),
            relationship_type=relationship_type
        )
    
    def _generate_rules_based_relationships(
        self, stix_objects: List[Dict[str, Any]], min_relationships_per_object: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Generate relationships based on predefined rules.
        
        Args:
            stix_objects: List of STIX objects
            min_relationships_per_object: Minimum number of relationships per object
            
        Returns:
            List of generated relationships
        """
        # Group objects by type for efficient access
        objects_by_type = {}
        for obj in stix_objects:
            obj_type = obj['type']
            if obj_type not in objects_by_type:
                objects_by_type[obj_type] = []
            objects_by_type[obj_type].append(obj)
        
        relationships = []
        
        # Try to create at least one relationship for each object
        for source_obj in stix_objects:
            source_type = source_obj['type']
            
            # Skip relationship objects
            if source_type == 'relationship':
                continue
                
            # Get allowed target types for this source type
            target_types = RELATIONSHIP_MAP.get(source_type, {})
            if not target_types:
                continue
            
            potential_relationships = []
            
            # Find all potential relationships
            for target_type, rel_types in target_types.items():
                if target_type not in objects_by_type:
                    continue
                    
                for target_obj in objects_by_type[target_type]:
                    for rel_type in rel_types:
                        potential_relationships.append((target_obj, rel_type))
            
            # If there are potential relationships, create at least one
            if potential_relationships:
                # Decide how many relationships to create
                num_relationships = min(
                    random.randint(min_relationships_per_object, 3),
                    len(potential_relationships)
                )
                
                selected_relationships = random.sample(potential_relationships, num_relationships)
                
                for target_obj, rel_type in selected_relationships:
                    relationship = {
                        "type": "relationship",
                        "spec_version": "2.1",
                        "id": f"relationship--{uuid.uuid4()}",
                        "source_ref": source_obj['id'],
                        "target_ref": target_obj['id'],
                        "relationship_type": rel_type,
                        "description": self._generate_relationship_description(
                            source_obj, target_obj, rel_type
                        )
                    }
                    
                    if self._validate_relationship(relationship, stix_objects):
                        relationships.append(relationship)
        
        return relationships
    
    def _generate_threat_scenario(
        self, objects: List[Dict[str, Any]], relationships: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a comprehensive threat scenario narrative.
        
        Args:
            objects: List of STIX objects
            relationships: List of relationships
            
        Returns:
            Narrative describing the threat scenario
        """
        # Group objects by type
        objects_by_type = {}
        for obj in objects:
            obj_type = obj['type']
            if obj_type not in objects_by_type:
                objects_by_type[obj_type] = []
            objects_by_type[obj_type].append(obj)
        
        # Build scenario components
        components = []
        
        # Start with threat actors if present
        if 'threat-actor' in objects_by_type:
            actors = objects_by_type['threat-actor']
            components.append(f"The threat landscape involves {len(actors)} threat actors, "
                           f"including {', '.join(a.get('name', 'Unknown Actor') for a in actors)}.")
        
        # Add campaign information
        if 'campaign' in objects_by_type:
            campaigns = objects_by_type['campaign']
            components.append(f"These actors are involved in {len(campaigns)} campaigns, "
                           f"notably {', '.join(c.get('name', 'Unknown Campaign') for c in campaigns)}.")
        
        # Describe tools and malware
        tools_malware = []
        if 'tool' in objects_by_type:
            tools_malware.extend(objects_by_type['tool'])
        if 'malware' in objects_by_type:
            tools_malware.extend(objects_by_type['malware'])
        if tools_malware:
            components.append(f"The adversaries utilize various tools and malware, including "
                           f"{', '.join(t.get('name', 'Unknown Tool') for t in tools_malware)}.")
        
        # Add attack patterns
        if 'attack-pattern' in objects_by_type:
            attack_patterns = objects_by_type['attack-pattern']
            components.append(f"Common techniques employed include "
                           f"{', '.join(a.get('name', 'Unknown Technique') for a in attack_patterns[:3])}.")
        
        # Add targeted identities
        if 'identity' in objects_by_type:
            identities = objects_by_type['identity']
            components.append(f"The primary targets include "
                           f"{', '.join(i.get('name', 'Unknown Identity') for i in identities[:3])}.")
        
        # Add mitigation information
        if 'course-of-action' in objects_by_type:
            mitigations = objects_by_type['course-of-action']
            components.append(f"Recommended mitigations include "
                           f"{', '.join(m.get('name', 'Unknown Mitigation') for m in mitigations)}.")
        
        # Describe indicators
        if 'indicator' in objects_by_type:
            indicators = objects_by_type['indicator']
            components.append(f"The activity can be detected by monitoring for "
                           f"{len(indicators)} indicators of compromise.")
        
        # Combine components into a coherent narrative
        scenario = " ".join(components)
        if not scenario:
            scenario = "No comprehensive scenario could be generated from the available objects."
        
        return scenario
    
    def _evaluate_relationships(
        self, relationships: List[Dict[str, Any]], objects: List[Dict[str, Any]]
    ) -> str:
        """
        Evaluate the quality and consistency of generated relationships.
        
        Args:
            relationships: List of relationships
            objects: List of STIX objects
            
        Returns:
            Evaluation of the relationships
        """
        from collections import Counter
        
        if not relationships:
            return "No relationships were generated."
        
        # Count objects by type (excluding relationships)
        object_types = Counter(
            obj['type'] for obj in objects if obj['type'] != 'relationship'
        )
        
        # Count relationship types
        relationship_types = Counter(r['relationship_type'] for r in relationships)
        
        # Check relationship distribution
        non_relationship_count = sum(object_types.values())
        relationship_count = len(relationships)
        
        relationship_ratio = relationship_count / non_relationship_count if non_relationship_count > 0 else 0
        
        # Evaluate relationship quality
        evaluation_points = []
        
        # Check relationship density
        if relationship_ratio < 0.5:
            evaluation_points.append("Low relationship density - consider generating more relationships.")
        elif relationship_ratio > 2:
            evaluation_points.append("High relationship density - consider reducing number of relationships.")
        else:
            evaluation_points.append("Good relationship density.")
        
        # Check relationship type diversity
        if len(relationship_types) < 3:
            evaluation_points.append("Limited relationship type diversity.")
        else:
            evaluation_points.append(f"Good relationship type diversity with {len(relationship_types)} different types.")
        
        # Check for relationship balance
        if relationship_types:
            most_common_type = relationship_types.most_common(1)[0]
            if most_common_type[1] / relationship_count > 0.5:
                evaluation_points.append(f"Relationship type '{most_common_type[0]}' is overrepresented.")
        
        return " ".join(evaluation_points)
    
    async def generate_relationships(self, stix_objects: List[Any]) -> Dict[str, Any]:
        """
        Generate relationships between STIX objects.
        
        Args:
            stix_objects: List of STIX objects
            
        Returns:
            Dictionary containing relationships, scenario, and evaluation
        """
        try:
            # Convert objects to dictionaries for consistent handling
            object_dicts = []
            for obj in stix_objects:
                if hasattr(obj, 'serialize'):
                    obj_dict = json.loads(obj.serialize())
                else:
                    obj_dict = obj
                object_dicts.append(obj_dict)
            
            # Generate rules-based relationships
            relationships = self._generate_rules_based_relationships(object_dicts)
            
            # For larger datasets or more complex scenarios, use LLM-based generation
            if len(object_dicts) >= 10 and self.api_key:
                try:
                    # Get LLM client
                    llm = get_llm_client(temperature=LLM_RELATIONSHIP_TEMPERATURE)
                    
                    # Get output parser
                    output_parser = get_relationship_output_parser()
                    
                    # Get prompt template
                    prompt_template = get_relationship_generation_prompt_template()
                    
                    # Create chain
                    chain = llm.create_chain(prompt_template, output_parser)
                    
                    # Prepare simplified object representations for LLM
                    simplified_objects = []
                    for obj in object_dicts:
                        simplified = {
                            "id": obj['id'],
                            "type": obj['type'],
                            "name": obj.get('name', obj['type']),
                            "description": obj.get('description', 'No description provided')
                        }
                        simplified_objects.append(simplified)
                    
                    # Create chain input
                    chain_input = {
                        "stix_objects": json.dumps(simplified_objects, indent=2),
                        "relationship_map": json.dumps(RELATIONSHIP_MAP, indent=2),
                        "format_instructions": output_parser.get_format_instructions()
                    }
                    
                    # Generate using LLM
                    result = await llm.ainvoke_chain(chain, chain_input)
                    
                    # Extract LLM-generated relationships and merge with rules-based
                    if result and 'relationships' in result:
                        llm_relationships = []
                        for rel in result['relationships']:
                            relationship = {
                                "type": "relationship",
                                "spec_version": "2.1",
                                "id": f"relationship--{uuid.uuid4()}",
                                "source_ref": rel['source_ref'],
                                "target_ref": rel['target_ref'],
                                "relationship_type": rel['relationship_type'],
                                "description": rel['description']
                            }
                            
                            if self._validate_relationship(relationship, object_dicts):
                                llm_relationships.append(relationship)
                        
                        # Combine relationships, avoiding duplicates
                        existing_relations = set(
                            (r['source_ref'], r['target_ref'], r['relationship_type'])
                            for r in relationships
                        )
                        
                        for rel in llm_relationships:
                            relation_key = (rel['source_ref'], rel['target_ref'], rel['relationship_type'])
                            if relation_key not in existing_relations:
                                relationships.append(rel)
                                existing_relations.add(relation_key)
                        
                        # Use LLM-generated scenario if provided
                        scenario = result.get('scenario')
                        evaluation = result.get('evaluation')
                    else:
                        scenario = self._generate_threat_scenario(object_dicts, relationships)
                        evaluation = self._evaluate_relationships(relationships, object_dicts)
                        
                except Exception as e:
                    logger.error(f"Error in LLM relationship generation: {str(e)}")
                    scenario = self._generate_threat_scenario(object_dicts, relationships)
                    evaluation = self._evaluate_relationships(relationships, object_dicts)
            else:
                # Generate scenario and evaluation using rule-based methods
                scenario = self._generate_threat_scenario(object_dicts, relationships)
                evaluation = self._evaluate_relationships(relationships, object_dicts)
            
            logger.info(f"Generated {len(relationships)} relationships between {len(object_dicts)} objects")
            
            return {
                "relationships": relationships,
                "scenario": scenario,
                "evaluation": evaluation
            }
            
        except Exception as e:
            logger.error(f"Error generating relationships: {str(e)}")
            return {
                "relationships": [],
                "scenario": "Error generating scenario",
                "evaluation": "Error evaluating relationships"
            }
    
    def create_stix2_relationships(self, relationships: List[Dict[str, Any]]) -> List[Relationship]:
        """
        Convert relationship dictionaries to STIX2 Relationship objects.
        
        Args:
            relationships: List of relationship dictionaries
            
        Returns:
            List of STIX2 Relationship objects
        """
        stix2_relationships = []
        
        for rel in relationships:
            try:
                # Ensure source_ref and target_ref are valid STIX IDs
                if not (isinstance(rel['source_ref'], str) and '--' in rel['source_ref']):
                    continue
                if not (isinstance(rel['target_ref'], str) and '--' in rel['target_ref']):
                    continue
                    
                stix2_rel = Relationship(
                    id=rel.get('id', f"relationship--{uuid.uuid4()}"),
                    relationship_type=rel['relationship_type'],
                    source_ref=rel['source_ref'],
                    target_ref=rel['target_ref'],
                    description=rel.get('description', '')
                )
                stix2_relationships.append(stix2_rel)
            except Exception as e:
                logger.error(f"Error creating STIX2 Relationship: {str(e)}")
        
        return stix2_relationships