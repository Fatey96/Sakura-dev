"""
Output parsers for LLM responses.
"""

import json
import re
from typing import Dict, Any, List, Optional

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from ..utils.logging_utils import setup_logger
from ..models.schemas import STIXOutput, RelationshipOutput

logger = setup_logger("stix_generator.llm.parser")

class StixOutputParser:
    """Parser for LLM output to STIX objects."""
    
    def __init__(self):
        """Initialize the parser."""
        self.json_parser = JsonOutputParser(pydantic_object=STIXOutput)
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse LLM output text into STIX objects.
        
        Args:
            text: LLM output text
            
        Returns:
            Dictionary containing parsed STIX objects
        """
        try:
            # First try direct JSON parsing
            return json.loads(text)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from markdown
            try:
                json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
                if json_match:
                    return json.loads(json_match.group(1))
            except (json.JSONDecodeError, AttributeError):
                pass
                
            # Try to find JSON-like structure
            try:
                start_idx = text.find('{')
                end_idx = text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = text[start_idx:end_idx]
                    return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                pass
                
            # Last resort: try to create a stix_objects wrapper
            try:
                if '"type":' in text and '"id":' in text:
                    # Seems like we have STIX object(s) but no wrapper
                    if text.strip().startswith('[') and text.strip().endswith(']'):
                        return {"stix_objects": json.loads(text)}
                    elif text.strip().startswith('{') and text.strip().endswith('}'):
                        return {"stix_objects": [json.loads(text)]}
            except json.JSONDecodeError:
                pass
                
            logger.error(f"Failed to parse LLM output as JSON: {text[:200]}...")
            return {"stix_objects": []}

class RelationshipOutputParser:
    """Parser for LLM output to relationships."""
    
    def __init__(self):
        """Initialize the parser."""
        self.json_parser = JsonOutputParser(pydantic_object=RelationshipOutput)
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse LLM output text into relationships.
        
        Args:
            text: LLM output text
            
        Returns:
            Dictionary containing parsed relationships
        """
        try:
            # First try direct JSON parsing
            return json.loads(text)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from markdown
            try:
                json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
                if json_match:
                    return json.loads(json_match.group(1))
            except (json.JSONDecodeError, AttributeError):
                pass
            
            # Try to find JSON-like structure
            try:
                start_idx = text.find('{')
                end_idx = text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = text[start_idx:end_idx]
                    return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                pass
                
            # Extract relationships if we can find them
            relationships = []
            try:
                rel_matches = re.finditer(r'"source_ref":\s*"([^"]+)"[^}]*"target_ref":\s*"([^"]+)"[^}]*"relationship_type":\s*"([^"]+)"', text)
                for match in rel_matches:
                    source, target, rel_type = match.groups()
                    relationships.append({
                        "source_ref": source,
                        "target_ref": target, 
                        "relationship_type": rel_type,
                        "description": f"{source} {rel_type} {target}"
                    })
            except Exception:
                pass
                
            # Extract scenario if present
            scenario = ""
            try:
                scenario_match = re.search(r'"scenario":\s*"([^"]+)"', text)
                if scenario_match:
                    scenario = scenario_match.group(1)
            except Exception:
                pass
                
            logger.error(f"Failed to parse LLM relationship output as JSON: {text[:200]}...")
            return {
                "relationships": relationships,
                "scenario": scenario,
                "evaluation": "Could not properly evaluate relationships due to parsing errors."
            }

def get_stix_output_parser() -> StixOutputParser:
    """
    Get a STIX output parser.
    
    Returns:
        STIX output parser
    """
    return StixOutputParser()

def get_relationship_output_parser() -> RelationshipOutputParser:
    """
    Get a relationship output parser.
    
    Returns:
        Relationship output parser
    """
    return RelationshipOutputParser()