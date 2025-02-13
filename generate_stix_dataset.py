from stix_object_generator import STIXObjectGenerator
from typing import Dict, List
from stix_object_builder import generate_high_quality_stix_dataset

def generate_stix_dataset(object_counts: Dict[str, int]) -> Dict[str, List[dict]]:
    """
    Generate a STIX dataset with specified object counts
    
    Args:
        object_counts: Dictionary mapping object types to counts
        
    Returns:
        Dictionary mapping object types to lists of generated objects
    """
    generator = STIXObjectGenerator()
    return generator.generate_objects(object_counts)

if __name__ == "__main__":
    # Example usage
    counts = {
        "identity": 2,
        "threat-actor": 3,
        "malware": 4,
        "indicator": 5,
        "report": 2
    }
    
    dataset = generate_stix_dataset(counts)
    
    # Print summary
    for obj_type, objects in dataset.items():
        print(f"Generated {len(objects)} {obj_type} objects") 