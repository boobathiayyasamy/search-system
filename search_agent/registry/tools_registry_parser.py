"""YAML configuration parser for tools registry."""

import logging
from pathlib import Path
from typing import Any, Dict

import yaml

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class ToolsYAMLParser:
    """Parser for tools registry YAML configuration file."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")
    
    def parse(self) -> Dict[str, Any]:
        """Parse and validate the YAML configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Failed to parse YAML file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error reading configuration file: {e}")
        
        if not config:
            raise ConfigurationError("Configuration file is empty")
        
        if 'tools' not in config:
            raise ConfigurationError("Configuration must contain 'tools' key")
        
        if not isinstance(config['tools'], list):
            raise ConfigurationError("'tools' must be a list")
        
        return config
