"""
Configuration settings for the STIX generator application.
"""

import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys and credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    import warnings
    warnings.warn("OPENAI_API_KEY not found in environment variables. LLM features will be unavailable.")

# LLM settings
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_OBJECT_TEMPERATURE = float(os.getenv("LLM_OBJECT_TEMPERATURE", "0.7"))
LLM_RELATIONSHIP_TEMPERATURE = float(os.getenv("LLM_RELATIONSHIP_TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))

# Generation settings
DEFAULT_BATCH_SIZE = 5
MAX_BATCH_SIZE = 10
MAX_CONCURRENT_REQUESTS = 5
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
CACHE_DIR = os.getenv("CACHE_DIR", "./stix_cache")

# Default distribution of STIX objects
DEFAULT_OBJECT_COUNTS = {
    "threat-actor": 5,
    "identity": 8,
    "malware": 10,
    "tool": 8,
    "attack-pattern": 10,
    "campaign": 5,
    "course-of-action": 5,
    "indicator": 15,
    "report": 5,
    "intrusion-set": 5,
    "observed-data": 10,
    "vulnerability": 10,
    "infrastructure": 5,
    "location": 10
}

# Object type display names mapping
OBJECT_TYPE_DISPLAY_NAMES = {
    "threat-actor": "Threat Actor",
    "identity": "Identity",
    "malware": "Malware",
    "tool": "Tool",
    "attack-pattern": "Attack Pattern",
    "campaign": "Campaign",
    "course-of-action": "Course of Action",
    "indicator": "Indicator",
    "report": "Report",
    "intrusion-set": "Intrusion Set",
    "observed-data": "Observed Data",
    "vulnerability": "Vulnerability",
    "infrastructure": "Infrastructure",
    "location": "Location",
    "opinion": "Opinion",
    "malware-analysis": "Malware Analysis",
    "note": "Note",
    "grouping": "Grouping"
}

# Reverse mapping for UI to STIX type conversion
DISPLAY_TO_STIX_TYPE = {v: k for k, v in OBJECT_TYPE_DISPLAY_NAMES.items()}

# Valid relationship types between STIX objects
RELATIONSHIP_MAP = {
    "threat-actor": {"identity": ["attributed-to"], "attack-pattern": ["uses"], "malware": ["uses"], "tool": ["uses"], "vulnerability": ["targets"]},
    "identity": {"threat-actor": ["attributed-to"], "campaign": ["attributed-to", "targets"]},
    "malware": {"vulnerability": ["exploits"], "tool": ["uses"], "attack-pattern": ["uses"], "campaign": ["originates-from"], "threat-actor": ["authored-by"]},
    "indicator": {"campaign": ["indicates"], "malware": ["indicates"], "threat-actor": ["indicates"], "tool": ["indicates"], "intrusion-set": ["indicates"]},
    "campaign": {"threat-actor": ["attributed-to"], "intrusion-set": ["attributed-to"], "identity": ["targets"], "vulnerability": ["targets"], "tool": ["uses"], "malware": ["uses"]},
    "intrusion-set": {"campaign": ["part-of"], "threat-actor": ["attributed-to"]},
    "tool": {"threat-actor": ["uses"], "malware": ["uses"]},
    "course-of-action": {"indicator": ["investigates", "mitigates"], "observed-data": ["based-on"], "attack-pattern": ["mitigates"], "malware": ["remediates"], "vulnerability": ["remediates"], "tool": ["mitigates"]},
    "location": {"identity": ["located-at"], "threat-actor": ["located-at"], "campaign": ["originates-from", "targets"], "malware": ["originates-from", "targets"], "intrusion-set": ["originates-from", "targets"], "attack-pattern": ["targets"], "tool": ["targets"]},
    "malware-analysis": {"malware": ["characterizes", "analysis-of", "static-analysis-of", "dynamic-analysis-of"]},
    "infrastructure": {"threat-actor": ["compromised-by"], "infrastructure": ["consists-of"], "tool": ["hosts"], "malware": ["hosts"], "campaign": ["used-by", "hosts"]},
    "opinion": {"indicator": ["related-to"], "threat-actor": ["related-to"], "attack-pattern": ["related-to"], "campaign": ["related-to"], "incident": ["related-to"], "malware": ["related-to"], "tool": ["related-to"], "vulnerability": ["related-to"], "infrastructure": ["related-to"], "intrusion-set": ["related-to"], "malware-analysis": ["related-to"], "threat-report": ["related-to"], "identity": ["related-to"]},
    "vulnerability": {"attack-pattern": ["targets"], "campaign": ["targets"], "intrusion-set": ["targets"], "malware": ["targets", "exploits"], "threat-actor": ["targets"], "tool": ["targets"], "course-of-action": ["mitigates"], "infrastructure": ["has"]}
}

# Flask settings
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "development-key-change-in-production")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "stix_generator.log")

# Output directory
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./stix_output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)