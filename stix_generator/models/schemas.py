"""
Pydantic models for LLM generation.
"""

from typing import List, Dict, Any, Optional
from langchain_core.pydantic_v1 import BaseModel, Field

# STIX Object Schemas for LLM generation

class AttackPatternSTIX(BaseModel):
    type: str = Field(default="attack-pattern")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the attack pattern")
    created: str = Field(description="The time at which the attack pattern was created")
    modified: str = Field(description="The time at which this particular version of the attack pattern was last modified")
    name: str = Field(description="A name used to identify this Attack Pattern")
    description: Optional[str] = Field(description="A description that provides more details and context about the Attack Pattern")
    aliases: Optional[List[str]] = Field(description="Alternative names used to identify this Attack Pattern")
    kill_chain_phases: Optional[List[Dict[str, str]]] = Field(description="List of kill chain phases this attack pattern is used in")

class CampaignSTIX(BaseModel):
    type: str = Field(default="campaign")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the campaign")
    created: str = Field(description="The time at which the campaign was created")
    modified: str = Field(description="The time at which this particular version of the campaign was last modified")
    name: str = Field(description="A name used to identify this Campaign")
    description: Optional[str] = Field(description="A description that provides more details and context about the Campaign")
    aliases: Optional[List[str]] = Field(description="Alternative names used to identify this Campaign")
    first_seen: Optional[str] = Field(description="The time that this Campaign was first seen")
    last_seen: Optional[str] = Field(description="The time that this Campaign was last seen")
    objective: Optional[str] = Field(description="The Campaign's primary goal, objective, desired outcome, or intended effect")

class CourseOfActionSTIX(BaseModel):
    type: str = Field(default="course-of-action")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the course of action")
    created: str = Field(description="The time at which the course of action was created")
    modified: str = Field(description="The time at which this particular version of the course of action was last modified")
    name: str = Field(description="A name used to identify this Course of Action")
    description: Optional[str] = Field(description="A description that provides more details and context about the Course of Action")
    action_type: Optional[str] = Field(description="The type of action to be taken")
    os_execution_envs: Optional[List[str]] = Field(description="A list of Operating System execution environments the Course of Action can be applied to")
    action_bin: Optional[str] = Field(description="Base64 encoded binary data for the action")
    action_reference: Optional[Dict[str, str]] = Field(description="An external reference to the action to be taken")

class GroupingSTIX(BaseModel):
    type: str = Field(default="grouping")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the grouping")
    created: str = Field(description="The time at which the grouping was created")
    modified: str = Field(description="The time at which this particular version of the grouping was last modified")
    name: Optional[str] = Field(description="A name used to identify this Grouping")
    description: Optional[str] = Field(description="A description that provides more details and context about the Grouping")
    context: str = Field(description="A short descriptor of the particular context shared by the content referenced by the Grouping")
    object_refs: List[str] = Field(description="Specifies the STIX Objects that are referred to by this Grouping")

class IdentitySTIX(BaseModel):
    type: str = Field(default="identity")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the identity")
    created: str = Field(description="The time at which the identity was created")
    modified: str = Field(description="The time at which this particular version of the identity was last modified")
    name: str = Field(description="A name used to identify this Identity")
    description: Optional[str] = Field(description="A description that provides more details and context about the Identity")
    roles: Optional[List[str]] = Field(description="A list of roles this Identity has")
    identity_class: str = Field(description="The type of entity that this Identity describes")
    sectors: Optional[List[str]] = Field(description="A list of industry sectors this Identity belongs to")
    contact_information: Optional[str] = Field(description="Contact information for this Identity")

class IndicatorSTIX(BaseModel):
    type: str = Field(default="indicator")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the indicator")
    created: str = Field(description="The time at which the indicator was created")
    modified: str = Field(description="The time at which this particular version of the indicator was last modified")
    name: Optional[str] = Field(description="A name used to identify this Indicator")
    description: Optional[str] = Field(description="A description that provides more details and context about the Indicator")
    indicator_types: List[str] = Field(description="A set of categorizations for this indicator")
    pattern: str = Field(description="The detection pattern for this Indicator")
    pattern_type: str = Field(description="The pattern language used in this Indicator")
    pattern_version: Optional[str] = Field(description="The version of the pattern language used")
    valid_from: str = Field(description="The time from which this Indicator is considered valid")
    valid_until: Optional[str] = Field(description="The time at which this Indicator should no longer be considered valid")
    kill_chain_phases: Optional[List[Dict[str, str]]] = Field(description="List of kill chain phases this indicator is used in")

class InfrastructureSTIX(BaseModel):
    type: str = Field(default="infrastructure")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the infrastructure")
    created: str = Field(description="The time at which the infrastructure was created")
    modified: str = Field(description="The time at which this particular version of the infrastructure was last modified")
    name: str = Field(description="A name used to identify this Infrastructure")
    description: Optional[str] = Field(description="A description that provides more details and context about the Infrastructure")
    infrastructure_types: List[str] = Field(description="The type of infrastructure being described")
    aliases: Optional[List[str]] = Field(description="Alternative names used to identify this Infrastructure")
    kill_chain_phases: Optional[List[Dict[str, str]]] = Field(description="List of kill chain phases this infrastructure is used in")
    first_seen: Optional[str] = Field(description="The time that this Infrastructure was first seen")
    last_seen: Optional[str] = Field(description="The time that this Infrastructure was last seen")

class IntrusionSetSTIX(BaseModel):
    type: str = Field(default="intrusion-set")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the intrusion set")
    created: str = Field(description="The time at which the intrusion set was created")
    modified: str = Field(description="The time at which this particular version of the intrusion set was last modified")
    name: str = Field(description="A name used to identify this Intrusion Set")
    description: Optional[str] = Field(description="A description that provides more details and context about the Intrusion Set")
    aliases: Optional[List[str]] = Field(description="Alternative names used to identify this Intrusion Set")
    first_seen: Optional[str] = Field(description="The time that this Intrusion Set was first seen")
    last_seen: Optional[str] = Field(description="The time that this Intrusion Set was last seen")
    goals: Optional[List[str]] = Field(description="The high-level goals of this Intrusion Set")
    resource_level: Optional[str] = Field(description="The organizational level at which this Intrusion Set typically works")
    primary_motivation: Optional[str] = Field(description="The primary reason, motivation, or purpose behind this Intrusion Set")
    secondary_motivations: Optional[List[str]] = Field(description="The secondary reasons, motivations, or purposes behind this Intrusion Set")

class LocationSTIX(BaseModel):
    type: str = Field(default="location")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the location")
    created: str = Field(description="The time at which the location was created")
    modified: str = Field(description="The time at which this particular version of the location was last modified")
    name: Optional[str] = Field(description="A name used to identify this Location")
    description: Optional[str] = Field(description="A description that provides more details and context about the Location")
    latitude: Optional[float] = Field(description="The latitude of the Location")
    longitude: Optional[float] = Field(description="The longitude of the Location")
    precision: Optional[float] = Field(description="Defines the precision of the coordinates")
    region: Optional[str] = Field(description="The region that this Location describes")
    country: Optional[str] = Field(description="The country that this Location describes")
    administrative_area: Optional[str] = Field(description="The administrative area that this Location describes")
    city: Optional[str] = Field(description="The city that this Location describes")
    street_address: Optional[str] = Field(description="The street address that this Location describes")
    postal_code: Optional[str] = Field(description="The postal code for this Location")

class MalwareSTIX(BaseModel):
    type: str = Field(default="malware")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the malware")
    created: str = Field(description="The time at which the malware was created")
    modified: str = Field(description="The time at which this particular version of the malware was last modified")
    name: str = Field(description="A name used to identify this Malware")
    description: Optional[str] = Field(description="A description that provides more details and context about the Malware")
    malware_types: List[str] = Field(description="A list of malware types for this malware")
    is_family: bool = Field(description="Whether this object represents a malware family")
    aliases: Optional[List[str]] = Field(description="Alternative names used to identify this Malware")
    kill_chain_phases: Optional[List[Dict[str, str]]] = Field(description="List of kill chain phases this malware is used in")
    architecture_execution_envs: Optional[List[str]] = Field(description="The processor architectures that the malware has been observed to run on")
    implementation_languages: Optional[List[str]] = Field(description="The programming languages implemented by this malware")
    capabilities: Optional[List[str]] = Field(description="Any capabilities identified for the malware instance")

class MalwareAnalysisSTIX(BaseModel):
    type: str = Field(default="malware-analysis")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the malware analysis")
    created: str = Field(description="The time at which the malware analysis was created")
    modified: str = Field(description="The time at which this particular version of the malware analysis was last modified")
    product: str = Field(description="The name of the analysis engine or product that was used")
    version: Optional[str] = Field(description="The version of the analysis product that was used to perform the analysis")
    host_vm_ref: Optional[str] = Field(description="Reference to a virtual machine environment used for dynamic analysis")
    operating_system_ref: Optional[str] = Field(description="Reference to the operating system used for dynamic analysis")
    installed_software_refs: Optional[List[str]] = Field(description="References to software installed on the dynamic analysis environment")
    configuration_version: Optional[str] = Field(description="The named configuration of additional product configuration parameters")
    modules: Optional[List[str]] = Field(description="The specific analysis modules that were used")
    analysis_engine_version: Optional[str] = Field(description="The version of the analysis engine used")
    analysis_definition_version: Optional[str] = Field(description="The version of the analysis definitions used")
    submitted: Optional[str] = Field(description="The date and time the malware was first submitted for scanning or analysis")
    analysis_started: Optional[str] = Field(description="The date and time the analysis was initiated")
    analysis_ended: Optional[str] = Field(description="The date and time the analysis ended")
    result_name: Optional[str] = Field(description="The classification result or name assigned to the malware")
    analysis_sco_refs: Optional[List[str]] = Field(description="References to STIX Cyber-observable Objects captured during the analysis")

class NoteSTIX(BaseModel):
    type: str = Field(default="note")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the note")
    created: str = Field(description="The time at which the note was created")
    modified: str = Field(description="The time at which this particular version of the note was last modified")
    abstract: Optional[str] = Field(description="A brief summary of the note content")
    content: str = Field(description="The content of the note")
    authors: Optional[List[str]] = Field(description="The names of the authors of this note")
    object_refs: List[str] = Field(description="The STIX Objects that the note is being applied to")

class ObservedDataSTIX(BaseModel):
    type: str = Field(default="observed-data")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the observed data")
    created: str = Field(description="The time at which the observed data was created")
    modified: str = Field(description="The time at which this particular version of the observed data was last modified")
    first_observed: str = Field(description="The beginning of the time window during which the data was observed")
    last_observed: str = Field(description="The end of the time window during which the data was observed")
    number_observed: int = Field(description="The number of times the data was observed")
    objects: Optional[Dict[str, Dict]] = Field(description="A dictionary of SCO representing the observation")
    object_refs: Optional[List[str]] = Field(description="A list of SCOs and SROs representing the observation")

class OpinionSTIX(BaseModel):
    type: str = Field(default="opinion")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the opinion")
    created: str = Field(description="The time at which the opinion was created")
    modified: str = Field(description="The time at which this particular version of the opinion was last modified")
    explanation: Optional[str] = Field(description="An explanation of why the producer has this Opinion")
    authors: Optional[List[str]] = Field(description="The names of the authors of this Opinion")
    opinion: str = Field(description="The opinion that the producer has about all of the STIX Object(s) listed in the object_refs property")
    object_refs: List[str] = Field(description="The STIX Objects that the Opinion is being applied to")

class ReportSTIX(BaseModel):
    type: str = Field(default="report")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the report")
    created: str = Field(description="The time at which the report was created")
    modified: str = Field(description="The time at which this particular version of the report was last modified")
    name: str = Field(description="A name used to identify this Report")
    description: Optional[str] = Field(description="A description that provides more details and context about the Report")
    report_types: List[str] = Field(description="The primary subject(s) of this report")
    published: str = Field(description="The date that this Report was officially published")
    object_refs: List[str] = Field(description="Specifies the STIX Objects that are referred to by this Report")

class ThreatActorSTIX(BaseModel):
    type: str = Field(default="threat-actor")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the threat actor")
    created: str = Field(description="The time at which the threat actor was created")
    modified: str = Field(description="The time at which this particular version of the threat actor was last modified")
    name: str = Field(description="A name used to identify this Threat Actor")
    description: Optional[str] = Field(description="A description that provides more details and context about the Threat Actor")
    aliases: Optional[List[str]] = Field(description="Alternative names used to identify this Threat Actor")
    threat_actor_types: List[str] = Field(description="The type of this Threat Actor")
    roles: Optional[List[str]] = Field(description="A list of roles the Threat Actor plays")
    goals: Optional[List[str]] = Field(description="The high-level goals of this Threat Actor")
    sophistication: Optional[str] = Field(description="The skill, specific knowledge, resources, and capabilities this Threat Actor possesses")
    resource_level: Optional[str] = Field(description="The organizational level at which this Threat Actor typically works")
    primary_motivation: Optional[str] = Field(description="The primary reason, motivation, or purpose behind this Threat Actor's activities")
    secondary_motivations: Optional[List[str]] = Field(description="The secondary reasons, motivations, or purposes behind this Threat Actor's activities")
    personal_motivations: Optional[List[str]] = Field(description="The personal reasons, motivations, or purposes of the Threat Actor regardless of organizational goals")

class ToolSTIX(BaseModel):
    type: str = Field(default="tool")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the tool")
    created: str = Field(description="The time at which the tool was created")
    modified: str = Field(description="The time at which this particular version of the tool was last modified")
    name: str = Field(description="A name used to identify this Tool")
    description: Optional[str] = Field(description="A description that provides more details and context about the Tool")
    tool_types: List[str] = Field(description="The kind(s) of tool(s) being described")
    aliases: Optional[List[str]] = Field(description="Alternative names used to identify this Tool")
    kill_chain_phases: Optional[List[Dict[str, str]]] = Field(description="List of kill chain phases this tool is used in")
    tool_version: Optional[str] = Field(description="The version identifier associated with the Tool")

class VulnerabilitySTIX(BaseModel):
    type: str = Field(default="vulnerability")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the vulnerability")
    created: str = Field(description="The time at which the vulnerability was created")
    modified: str = Field(description="The time at which this particular version of the vulnerability was last modified")
    name: str = Field(description="A name used to identify this Vulnerability")
    description: Optional[str] = Field(description="A description that provides more details and context about the Vulnerability")
    external_references: Optional[List[Dict[str, str]]] = Field(description="A list of external references which refer to non-STIX information")

class RelationshipSTIX(BaseModel):
    type: str = Field(default="relationship")
    spec_version: str = Field(default="2.1")
    id: str = Field(description="Unique identifier for the relationship")
    created: str = Field(description="The time at which the relationship was created")
    modified: str = Field(description="The time at which this particular version of the relationship was last modified")
    relationship_type: str = Field(description="The type of relationship")
    source_ref: str = Field(description="The ID of the source object")
    target_ref: str = Field(description="The ID of the target object")
    description: Optional[str] = Field(description="A description that provides more details about the relationship")

class STIXOutput(BaseModel):
    stix_objects: List[Dict[str, Any]] = Field(description="List of generated STIX objects")

class RelationshipOutput(BaseModel):
    relationships: List[Dict[str, Any]] = Field(description="The generated STIX relationships")
    evaluation: str = Field(description="Evaluation of the generated relationships")
    scenario: str = Field(description="A comprehensive scenario describing the relationships")

# Function to get the schema for a specific STIX object type
def get_schema_for_type(object_type: str) -> Dict[str, Any]:
    """
    Get the schema for a specific STIX object type.
    
    Args:
        object_type: The type of STIX object
        
    Returns:
        Dictionary containing the schema for the specified object type
    """
    type_map = {
        "attack-pattern": AttackPatternSTIX,
        "campaign": CampaignSTIX,
        "course-of-action": CourseOfActionSTIX,
        "grouping": GroupingSTIX,
        "identity": IdentitySTIX,
        "indicator": IndicatorSTIX,
        "infrastructure": InfrastructureSTIX,
        "intrusion-set": IntrusionSetSTIX,
        "location": LocationSTIX,
        "malware": MalwareSTIX,
        "malware-analysis": MalwareAnalysisSTIX,
        "note": NoteSTIX,
        "observed-data": ObservedDataSTIX,
        "opinion": OpinionSTIX,
        "report": ReportSTIX,
        "threat-actor": ThreatActorSTIX,
        "tool": ToolSTIX,
        "vulnerability": VulnerabilitySTIX,
        "relationship": RelationshipSTIX
    }
    
    model_class = type_map.get(object_type)
    if not model_class:
        raise ValueError(f"Unknown STIX object type: {object_type}")
        
    return model_class.schema()