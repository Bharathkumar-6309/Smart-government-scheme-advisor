import logging
import sys
from typing import Optional
from datetime import datetime


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name. If None, returns the root logger.
        
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name or __name__)
    
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)
        
        # Prevent propagation to avoid duplicate logs
        logger.propagate = False
    
    return logger
