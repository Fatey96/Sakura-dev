"""
LLM prompts for STIX generation.
"""

from typing import Dict, Any, List, Optional, Union

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Define output schemas for parsing
class STIXOutput(BaseModel):
    stix_objects: List[Dict[str, Any]] = Field(description="List of generated STIX objects")

class RelationshipOutput(BaseModel):
    relationships: List[Dict[str, Any]] = Field(description="The generated STIX relationships")
    evaluation: str = Field(description="Evaluation of the generated relationships")
    scenario: str = Field(description="A comprehensive scenario describing the relationships")

def get_object_generation_prompt_template() -> str:
    """
    Get the prompt template for generating STIX objects.
    
    Returns:
        String prompt template
    """
    return """You are an expert in Cyber Threat Intelligence (CTI) and STIX (Structured Threat Information Expression). 
    Your task is to generate high-quality, realistic STIX objects based on the provided schema and context.
    
    Object Type: {object_type}

    Schema:
    {schema}

    Examples:
    {examples}

    Context (existing objects to reference or relate to):
    {context}

    Seed: {seed}

    Please generate {count} realistic and detailed {object_type} objects. Ensure that:
    1. All fields are filled with realistic and contextually appropriate information.
    2. The objects are diverse and represent a range of real-world scenarios.
    3. Where applicable, reference existing objects from the context to create meaningful relationships.
    4. Use realistic naming conventions, descriptions, and technical details.
    5. Ensure consistency in timestamps and other relational data.
    6. For Malware objects, use generic strings for operating_system_refs (e.g., "windows", "linux", "macos") instead of object references.
    7. Use the provided seed value to guide your generation and ensure consistency.

    {format_instructions}
    """

def get_relationship_generation_prompt_template() -> str:
    """
    Get the prompt template for generating relationships.
    
    Returns:
        String prompt template
    """
    return """You are an expert in cyber threat intelligence and STIX (Structured Threat Information Expression). 
    Your task is to create realistic and meaningful relationships between multiple STIX Domain Objects (SDOs), 
    evaluate these relationships, and generate a comprehensive threat intelligence scenario.
    
    STIX Objects:
    {stix_objects}
    
    Relationship Map:
    {relationship_map}
    
    Based on these STIX objects and the relationship map, please:
    1. Generate realistic and meaningful relationships between the objects.
    2. Evaluate the generated relationships for consistency and realism.
    3. Create a comprehensive threat intelligence scenario that incorporates all these relationships.
    
    Ensure that:
    - The relationships you create are valid according to the relationship map.
    - The relationships are realistic and relevant to current cyber threat landscapes.
    - There are no contradicting or nonsensical relationships.
    - The scenario is detailed and incorporates all the provided STIX objects.
    
    {format_instructions}
    """

def get_stix_output_parser() -> JsonOutputParser:
    """
    Get a JSON output parser for STIX objects.
    
    Returns:
        JsonOutputParser for STIX objects
    """
    return JsonOutputParser(pydantic_object=STIXOutput)

def get_relationship_output_parser() -> JsonOutputParser:
    """
    Get a JSON output parser for relationships.
    
    Returns:
        JsonOutputParser for relationships
    """
    return JsonOutputParser(pydantic_object=RelationshipOutput)

def get_stix_object_prompt_template(object_type: str) -> str:
    """
    Get the prompt template for generating STIX objects with support for special instructions.
    
    Args:
        object_type: The type of STIX object to generate
        
    Returns:
        String prompt template
    """
    return f"""You are an expert in Cyber Threat Intelligence (CTI) and STIX (Structured Threat Information Expression).
    
    Generate a valid STIX {object_type} object. Create {{count}} realistic and detailed instances.
    
    IMPORTANT REQUIREMENTS:
    1. All fields must be filled with realistic and contextually appropriate information.
    2. The objects must be diverse and represent a range of real-world scenarios.
    3. Use realistic naming conventions, descriptions, and technical details.
    4. Ensure consistency in timestamps and other relational data.
    5. For Malware objects, use generic strings for operating_system_refs (e.g., "windows", "linux", "macos").
    
    CRITICAL UUID FORMAT REQUIREMENTS:
    1. All IDs MUST follow the format: "{object_type}--" followed by a valid UUID v4 (e.g., "{object_type}--550e8400-e29b-41d4-a716-446655440000").
    2. All references to other objects (_ref or _refs fields) MUST use valid UUIDs in the same format.
    3. DO NOT use placeholder UUIDs like "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6" - these are invalid.
    4. Valid UUIDs only contain hexadecimal characters (0-9, a-f) in the pattern: 8-4-4-4-12 characters.
    
    Format your response as a JSON array of objects. Each object should be a valid STIX {object_type} object.
    
    Example format with VALID UUID:
    [
      {{
        "type": "{object_type}",
        "id": "{object_type}--550e8400-e29b-41d4-a716-446655440000",
        "created": "2023-01-01T00:00:00.000Z",
        "modified": "2023-01-01T00:00:00.000Z",
        // other fields specific to {object_type}
      }},
      // more objects...
    ]
    """