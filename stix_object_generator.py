from typing import Dict, List, Optional

import json
import os
from datetime import datetime
from uuid import uuid4
import random
from pathlib import Path
from stix_generation_workflow import GENERATION_WORKFLOW
class STIXObjectGenerator:
    def __init__(self, examples_dir: str = "examples"):
        self.examples_dir = Path(examples_dir)
        self.examples_cache = {}
        self.generated_objects = {}
        self._load_examples()

    def _load_examples(self):
        """Load example objects from JSON files"""
        if not self.examples_dir.exists():
            self.examples_dir.mkdir(parents=True)
            
        for file in self.examples_dir.glob("*.json"):
            with open(file) as f:
                self.examples_cache[file.stem.lower()] = json.load(f)

    def _get_template(self, obj_type: str) -> dict:
        """Get a random template from examples"""
        templates = self.examples_cache.get(obj_type.lower(), [])
        return random.choice(templates) if templates else {}

    def _generate_timestamp(self) -> str:
        """Generate a current timestamp in STIX format"""
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def _generate_base_object(self, obj_type: str) -> dict:
        """Generate a base STIX object with required fields"""
        timestamp = self._generate_timestamp()
        return {
            "type": obj_type,
            "id": f"{obj_type}--{uuid4()}",
            "created": timestamp,
            "modified": timestamp,
            "spec_version": "2.1"
        }

    def generate_objects(self, counts: Dict[str, int]) -> Dict[str, List[dict]]:
        """Generate STIX objects according to workflow phases"""
        self.generated_objects = {}
        
        # Generate objects according to workflow
        for phase in GENERATION_WORKFLOW.values():
            for obj_type in phase:
                if obj_type in counts:
                    self._generate_type(obj_type, counts[obj_type])

        return self.generated_objects

    def _generate_type(self, obj_type: str, count: int):
        """Generate specified number of objects of given type"""
        self.generated_objects[obj_type] = []
        
        for _ in range(count):
            template = self._get_template(obj_type)
            obj = self._generate_base_object(obj_type)
            
            # Merge template with generated fields
            if template:
                obj.update(self._adapt_template(template, obj_type))
            
            # Add references if needed
            self._add_references(obj, obj_type)
            
            self.generated_objects[obj_type].append(obj)

    def _adapt_template(self, template: dict, obj_type: str) -> dict:
        """Adapt template by removing ID/timestamp fields and varying content"""
        adapted = template.copy()
        adapted.pop('id', None)
        adapted.pop('created', None)
        adapted.pop('modified', None)
        
        # Vary some fields to create diversity
        if 'name' in adapted:
            adapted['name'] = f"{adapted['name']}_{random.randint(1000,9999)}"
            
        return adapted

    def _add_references(self, obj: dict, obj_type: str):
        """Add references to other objects based on type"""
        if obj_type in GENERATION_WORKFLOW['phase2']:
            self._add_identity_ref(obj)
            
        elif obj_type in GENERATION_WORKFLOW['phase3']:
            self._add_identity_ref(obj)
            self._add_object_refs(obj, ['malware', 'tool'], 1, 2)
            
        elif obj_type in GENERATION_WORKFLOW['phase4']:
            self._add_identity_ref(obj)
            self._add_object_refs(obj, ['indicator', 'malware', 'threat-actor'], 2, 4)

    def _add_identity_ref(self, obj: dict):
        """Add reference to an identity object"""
        if 'identity' in self.generated_objects and self.generated_objects['identity']:
            obj['created_by_ref'] = random.choice(self.generated_objects['identity'])['id']

    def _add_object_refs(self, obj: dict, ref_types: List[str], min_refs: int, max_refs: int):
        """Add references to other objects"""
        available_refs = []
        for ref_type in ref_types:
            if ref_type in self.generated_objects:
                available_refs.extend([o['id'] for o in self.generated_objects[ref_type]])
                
        if available_refs:
            num_refs = random.randint(min_refs, min(max_refs, len(available_refs)))
            obj['object_refs'] = random.sample(available_refs, num_refs) 