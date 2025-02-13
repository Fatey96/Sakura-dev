# Define generation order based on dependencies
GENERATION_WORKFLOW = {
    'phase1': [  # Objects with no dependencies
        'identity',
        'location', 
        'vulnerability',
        'attack-pattern',
        'malware',
        'tool'
    ],
    'phase2': [  # Objects that reference phase1
        'threat-actor',
        'infrastructure',
        'intrusion-set',
        'campaign'
    ],
    'phase3': [  # Objects that need multiple references
        'indicator',
        'observed-data',
        'malware-analysis',
        'course-of-action'
    ],
    'phase4': [  # Objects that aggregate/reference others
        'grouping',
        'report',
        'note',
        'opinion'
    ]
} 