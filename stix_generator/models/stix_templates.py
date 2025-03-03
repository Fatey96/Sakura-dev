"""
Templates for STIX objects.
"""

from typing import Dict, List, Any

# Attack Pattern Examples
ATTACK_PATTERN_EXAMPLES = [
    {
        "type": "attack-pattern",
        "spec_version": "2.1",
        "id": "attack-pattern--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061",
        "created": "2022-08-15T15:12:20.000Z",
        "modified": "2022-08-15T15:12:20.000Z",
        "name": "Phishing",
        "description": "Phishing is a technique for attempting to acquire sensitive credentials, such as usernames, passwords, credit card details, etc. by masquerading as a trustworthy entity in an electronic communication.",
        "aliases": ["Email Phishing", "Spear Phishing"],
        "kill_chain_phases": [
            {
                "kill_chain_name": "lockheed-martin-cyber-kill-chain",
                "phase_name": "delivery"
            }
        ]
    }
]

# Campaign Examples
CAMPAIGN_EXAMPLES = [
    {
        "type": "campaign",
        "spec_version": "2.1",
        "id": "campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c",
        "created": "2022-09-01T13:11:00.000Z",
        "modified": "2022-09-01T13:11:00.000Z",
        "name": "Operation Dragon Fury",
        "description": "A series of coordinated attacks targeting financial institutions in Southeast Asia.",
        "aliases": ["OpDragonFury", "Asian Bank Heist"],
        "first_seen": "2022-07-01T00:00:00Z",
        "last_seen": "2022-08-31T23:59:59Z",
        "objective": "Steal financial data and credentials from major banks"
    }
]

# Course of Action Examples
COURSE_OF_ACTION_EXAMPLES = [
    {
        "type": "course-of-action",
        "spec_version": "2.1",
        "id": "course-of-action--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
        "created": "2022-10-05T09:22:30.000Z",
        "modified": "2022-10-05T09:22:30.000Z",
        "name": "Block Malicious IPs",
        "description": "Block a list of known malicious IP addresses at the network firewall level."
    }
]

# Identity Examples
IDENTITY_EXAMPLES = [
    {
        "type": "identity",
        "spec_version": "2.1",
        "id": "identity--023d105b-752e-4e3c-941c-7d3f3cb15e9e",
        "created": "2022-04-06T20:03:00.000Z",
        "modified": "2022-04-06T20:03:00.000Z",
        "name": "ACME Cybersecurity, Inc.",
        "description": "ACME Cybersecurity is a leading provider of threat intelligence and security solutions.",
        "roles": ["cybersecurity-vendor", "threat-intelligence-provider"],
        "identity_class": "organization",
        "sectors": ["technology"],
        "contact_information": "info@acmecyber.example.com"
    }
]

# Indicator Examples
INDICATOR_EXAMPLES = [
    {
        "type": "indicator",
        "spec_version": "2.1",
        "id": "indicator--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
        "created": "2022-12-15T09:45:00.000Z",
        "modified": "2022-12-15T09:45:00.000Z",
        "name": "Malicious IP for Operation Dragon Fury",
        "description": "This IP address is associated with command and control activities of Operation Dragon Fury.",
        "indicator_types": ["malicious-activity"],
        "pattern": "[ipv4-addr:value = '203.0.113.100']",
        "pattern_type": "stix",
        "pattern_version": "2.1",
        "valid_from": "2022-12-15T09:45:00Z",
        "valid_until": "2023-12-15T09:45:00Z",
        "kill_chain_phases": [
            {
                "kill_chain_name": "lockheed-martin-cyber-kill-chain",
                "phase_name": "command-and-control"
            }
        ]
    }
]

# Intrusion Set Examples
INTRUSION_SET_EXAMPLES = [
    {
        "type": "intrusion-set",
        "spec_version": "2.1",
        "id": "intrusion-set--4e78f46f-a023-4e5f-bc24-71b3ca22ec29",
        "created": "2023-02-10T08:17:27.000Z",
        "modified": "2023-02-10T08:17:27.000Z",
        "name": "Dragon Fury Group",
        "description": "Dragon Fury Group is a sophisticated cyber espionage group targeting financial institutions in Southeast Asia.",
        "aliases": ["DFG", "Asian Bank Hackers"],
        "first_seen": "2022-06-01T00:00:00Z",
        "last_seen": "2023-02-09T23:59:59Z",
        "goals": ["financial theft", "espionage"],
        "resource_level": "organization",
        "primary_motivation": "organizational-gain",
        "secondary_motivations": ["financial-gain"]
    }
]

# Malware Examples
MALWARE_EXAMPLES = [
    {
        "type": "malware",
        "spec_version": "2.1",
        "id": "malware--3a41e552-999b-4ad3-bedc-332b6d9ff80c",
        "created": "2023-06-01T10:31:44.000Z",
        "modified": "2023-06-01T10:31:44.000Z",
        "name": "Emotet",
        "description": "Emotet is a modular malware variant which functions as a downloader or dropper of other banking malware.",
        "malware_types": ["trojan", "dropper"],
        "is_family": True,
        "aliases": ["Geodo", "Mealybug"],
        "kill_chain_phases": [
            {"kill_chain_name": "lockheed-martin-cyber-kill-chain", "phase_name": "delivery"}
        ],
        "architecture_execution_envs": ["x86", "x64"],
        "implementation_languages": ["Visual Basic", "C++"],
        "capabilities": ["spamming", "credential-theft", "downloader"]
    }
]

# Tool Examples
TOOL_EXAMPLES = [
    {
        "type": "tool",
        "spec_version": "2.1",
        "id": "tool--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
        "created": "2023-07-01T14:20:00.000Z",
        "modified": "2023-07-01T14:20:00.000Z",
        "name": "Dragon Scanner",
        "description": "Dragon Scanner is a custom network vulnerability scanner used by the Dragon Fury Group to identify potential targets.",
        "tool_types": ["vulnerability-scanner"],
        "aliases": ["DFScanner"],
        "kill_chain_phases": [
            {
                "kill_chain_name": "lockheed-martin-cyber-kill-chain",
                "phase_name": "reconnaissance"
            }
        ],
        "tool_version": "2.1.3"
    }
]

# Threat Actor Examples
THREAT_ACTOR_EXAMPLES = [
    {
        "type": "threat-actor",
        "spec_version": "2.1",
        "id": "threat-actor--56f3f0db-b5d5-431c-ae56-c18c1e8b9ba4",
        "created": "2023-05-14T08:17:27.000Z",
        "modified": "2023-05-14T08:17:27.000Z",
        "name": "DragonFly",
        "description": "DragonFly is a sophisticated threat actor known for targeting energy sector organizations.",
        "aliases": ["Energetic Bear", "Crouching Yeti"],
        "threat_actor_types": ["nation-state", "spy"],
        "roles": ["agent", "director", "infrastructure-architect"],
        "goals": ["espionage", "sabotage"],
        "sophistication": "advanced",
        "resource_level": "government",
        "primary_motivation": "strategic-advantage",
        "secondary_motivations": ["dominance", "organizational-gain"]
    }
]

# Vulnerability Examples
VULNERABILITY_EXAMPLES = [
    {
        "type": "vulnerability",
        "spec_version": "2.1",
        "id": "vulnerability--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061",
        "created": "2023-07-15T09:15:00.000Z",
        "modified": "2023-07-15T09:15:00.000Z",
        "name": "CVE-2023-1234",
        "description": "A buffer overflow vulnerability in XYZ Banking Software versions 2.0 to 2.5 allows remote attackers to execute arbitrary code via a crafted network packet.",
        "external_references": [
            {
                "source_name": "cve",
                "external_id": "CVE-2023-1234"
            }
        ]
    }
]

# Observed Data Examples
OBSERVED_DATA_EXAMPLES = [
    {
        "type": "observed-data",
        "spec_version": "2.1",
        "id": "observed-data--b67d30ff-02ac-498a-92f9-32f845f448cf",
        "created": "2023-05-10T15:20:00.000Z",
        "modified": "2023-05-10T15:20:00.000Z",
        "first_observed": "2023-05-10T14:00:00Z",
        "last_observed": "2023-05-10T15:00:00Z",
        "number_observed": 50,
        "object_refs": [
            "ipv4-addr--efcd5e80-570d-4131-b213-62cb18eaa6a8",
            "network-traffic--2568d22a-8998-58eb-99ec-3c8ca74f527d"
        ]
    }
]

# Report Examples
REPORT_EXAMPLES = [
    {
        "type": "report",
        "spec_version": "2.1",
        "id": "report--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
        "created": "2023-06-01T09:00:00.000Z",
        "modified": "2023-06-01T09:00:00.000Z",
        "name": "Dragon Fury Group: Tactics, Techniques, and Procedures",
        "description": "This report provides a comprehensive overview of the Dragon Fury Group's TTPs based on recent cyber attacks against financial institutions in Southeast Asia.",
        "report_types": ["threat-actor", "attack-pattern"],
        "published": "2023-06-01T12:00:00Z",
        "object_refs": [
            "threat-actor--4e78f46f-a023-4e5f-bc24-71b3ca22ec29",
            "attack-pattern--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061",
            "malware--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061"
        ]
    }
]

# Infrastructure Examples
INFRASTRUCTURE_EXAMPLES = [
    {
        "type": "infrastructure",
        "spec_version": "2.1",
        "id": "infrastructure--78cc7b4b-c6ab-40d1-82eb-95a3059641da",
        "created": "2023-01-20T14:11:00.000Z",
        "modified": "2023-01-20T14:11:00.000Z",
        "name": "Dragon Fury C2 Server",
        "description": "Command and Control server used in Operation Dragon Fury campaign.",
        "infrastructure_types": ["command-and-control"],
        "aliases": ["DF-C2", "Dragon-Control"],
        "first_seen": "2023-01-01T00:00:00Z",
        "last_seen": "2023-01-19T23:59:59Z"
    }
]

# Location Examples
LOCATION_EXAMPLES = [
    {
        "type": "location",
        "spec_version": "2.1",
        "id": "location--a6e9345f-5a15-4c29-8bb3-7dcc5d168d64",
        "created": "2023-03-01T12:00:00.000Z",
        "modified": "2023-03-01T12:00:00.000Z",
        "name": "Bangkok, Thailand",
        "description": "Capital city of Thailand",
        "latitude": 13.7563,
        "longitude": 100.5018,
        "precision": 0.1,
        "region": "south-eastern-asia",
        "country": "TH",
        "administrative_area": "Bangkok",
        "city": "Bangkok",
        "postal_code": "10100"
    }
]

# Maps object types to their examples
EXAMPLES_MAP = {
    "attack-pattern": ATTACK_PATTERN_EXAMPLES,
    "campaign": CAMPAIGN_EXAMPLES,
    "course-of-action": COURSE_OF_ACTION_EXAMPLES,
    "identity": IDENTITY_EXAMPLES,
    "indicator": INDICATOR_EXAMPLES,
    "intrusion-set": INTRUSION_SET_EXAMPLES,
    "malware": MALWARE_EXAMPLES,
    "tool": TOOL_EXAMPLES,
    "threat-actor": THREAT_ACTOR_EXAMPLES,
    "vulnerability": VULNERABILITY_EXAMPLES,
    "observed-data": OBSERVED_DATA_EXAMPLES,
    "report": REPORT_EXAMPLES,
    "infrastructure": INFRASTRUCTURE_EXAMPLES,
    "location": LOCATION_EXAMPLES
}

def get_examples_for_type(object_type: str) -> List[Dict[str, Any]]:
    """
    Get examples for a specific STIX object type.
    
    Args:
        object_type: The type of STIX object
        
    Returns:
        List of example objects for the specified type
    """
    return EXAMPLES_MAP.get(object_type, [])