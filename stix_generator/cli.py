"""
Command-line interface for STIX generation.
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from stix_generator.config import (
    DEFAULT_OBJECT_COUNTS, OUTPUT_DIR, OPENAI_API_KEY
)
from stix_generator.core.object_generator import StixObjectGenerator
from stix_generator.core.relationship_generator import RelationshipGenerator
from stix_generator.core.bundler import create_bundle, serialize_bundle
from stix_generator.utils.metrics import analyze_stix_bundle
from stix_generator.utils.logging_utils import setup_logger

# Set up logger
logger = setup_logger("stix_generator.cli")

async def generate_stix_data(
    object_counts, 
    output_file=None, 
    seed=42, 
    analyze=True
):
    """
    Generate STIX data from the command line.
    
    Args:
        object_counts: Dictionary mapping object types to counts
        output_file: Path to output file (None for auto-generated)
        seed: Random seed for generation
        analyze: Whether to analyze and print metrics
    """
    try:
        logger.info(f"Starting STIX data generation with seed {seed}")
        start_time = datetime.now()
        
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Generate output filename if not provided
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(OUTPUT_DIR, f"stix_bundle_{timestamp}_{seed}.json")
        
        # Initialize generators
        object_generator = StixObjectGenerator(seed=seed)
        relationship_generator = RelationshipGenerator(seed=seed)
        
        # Generate objects
        logger.info("Generating STIX objects...")
        stix_objects_dict = await object_generator.generate_dataset(object_counts)
        
        # Flatten objects list
        all_stix_objects = []
        for obj_list in stix_objects_dict.values():
            all_stix_objects.extend(obj_list)
        
        # Convert to STIX2 objects
        logger.info("Converting to STIX2 objects...")
        stix2_objects_dict = await object_generator.create_stix2_objects(stix_objects_dict)
        stix2_objects = list(stix2_objects_dict.values())
        
        # Generate relationships
        logger.info("Generating relationships...")
        relationship_output = await relationship_generator.generate_relationships(all_stix_objects)
        
        # Convert relationships to STIX2 objects
        stix2_relationships = relationship_generator.create_stix2_relationships(
            relationship_output['relationships']
        )
        
        # Create bundle
        logger.info("Creating STIX bundle...")
        stix_bundle = create_bundle(stix2_objects, stix2_relationships)
        
        # Serialize and save bundle
        bundle_json = serialize_bundle(stix_bundle)
        with open(output_file, 'w') as f:
            f.write(bundle_json)
        
        logger.info(f"STIX bundle saved to {output_file}")
        
        # Calculate and print metrics if requested
        if analyze:
            logger.info("Analyzing STIX bundle...")
            metrics = analyze_stix_bundle(bundle_json)
            
            # Print summary metrics
            summary = metrics["basic_metrics"]["summary"]
            print("\nSTIX Bundle Metrics:")
            print(f"  Total Objects: {summary['total_objects']}")
            print(f"  Quality Score: {summary['quality_score']}%")
            print(f"  Completeness Score: {summary['completeness_score']}%")
            print(f"  Consistency Score: {summary['consistency_score']}%")
            print(f"  Relationship Score: {summary['relationship_score']}%")
            
            # Print object distribution
            print("\nObject Distribution:")
            for obj_type, count in metrics["basic_metrics"]["object_distribution"].items():
                print(f"  {obj_type}: {count}")
        
        # Print generation time
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"Generation completed in {duration:.2f} seconds")
        
        return True, output_file
        
    except Exception as e:
        logger.error(f"Error generating STIX data: {str(e)}", exc_info=True)
        return False, str(e)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate synthetic STIX data")
    
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: auto-generated)",
        default=None
    )
    
    parser.add_argument(
        "--seed", "-s",
        help="Random seed for reproducibility (default: 42)",
        type=int,
        default=42
    )
    
    parser.add_argument(
        "--config", "-c",
        help="Path to JSON config file with object counts",
        default=None
    )
    
    parser.add_argument(
        "--counts", "-n",
        help="Object counts in format 'type1:count1,type2:count2'",
        default=None
    )
    
    parser.add_argument(
        "--total", "-t",
        help="Total number of objects to generate with automatic distribution",
        type=int,
        default=None
    )
    
    parser.add_argument(
        "--no-metrics",
        help="Disable metrics calculation and display",
        action="store_true"
    )