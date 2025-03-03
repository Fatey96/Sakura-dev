"""
Logging utilities for the STIX generator application.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from ..config import LOG_LEVEL, LOG_FILE

def setup_logger(
    name: str = __name__,
    level: str = LOG_LEVEL,
    log_file: str = LOG_FILE,
    console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 3
) -> logging.Logger:
    """
    Set up and configure a logger.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level
        log_file: Path to log file
        console: Whether to log to console
        max_file_size: Maximum size of log file before rotating
        backup_count: Number of backup log files to keep
        
    Returns:
        Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add file handler if log file is specified
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Set up rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

# Create application logger
app_logger = setup_logger("stix_generator")

# Create module-specific loggers
object_generator_logger = setup_logger("stix_generator.object_generator")
relationship_generator_logger = setup_logger("stix_generator.relationship_generator")
bundler_logger = setup_logger("stix_generator.bundler")
metrics_logger = setup_logger("stix_generator.metrics")
api_logger = setup_logger("stix_generator.api")