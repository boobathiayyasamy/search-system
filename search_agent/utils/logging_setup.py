"""Logging setup utility for search agent."""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(config) -> logging.Logger:
    """
    Configure and setup logging for the search agent.
    
    Args:
        config: Configuration object containing log settings
        
    Returns:
        Configured logger instance
    """
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = logs_dir / f"search_agent_{timestamp}.log"
    
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format=config.log_format,
        datefmt=config.log_date_format,
        force=True,
        handlers=[
            logging.FileHandler(log_filename, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
