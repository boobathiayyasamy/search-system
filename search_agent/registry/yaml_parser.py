"""YAML configuration parser."""

import logging
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class YAMLParser:
    """Parser for agents registry YAML configuration file."""
    
    REQUIRED_FIELDS = {'name', 'module', 'enabled', 'order'}
    
    def __init__(self, config_path: str):
        """Initialize the YAML parser."""
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
        
        self.validate_config(config)
        
        return config
    
    def validate_config(self, config: Dict[str, Any]) -> None:
        """Validate the configuration structure and required fields."""
        # Check for agents list
        if 'agents' not in config:
            raise ConfigurationError("Configuration must contain 'agents' key")
        
        agents = config['agents']
        if not isinstance(agents, list):
            raise ConfigurationError("'agents' must be a list")
        
        if not agents:
            return
        
        # Validate each agent configuration
        for idx, agent in enumerate(agents):
            if not isinstance(agent, dict):
                raise ConfigurationError(f"Agent at index {idx} must be a dictionary")
            
            # Check required fields
            missing_fields = self.REQUIRED_FIELDS - set(agent.keys())
            if missing_fields:
                agent_name = agent.get('name', f'index {idx}')
                raise ConfigurationError(
                    f"Agent '{agent_name}' missing required fields: {missing_fields}"
                )
            
            # Validate field types
            if not isinstance(agent['name'], str):
                raise ConfigurationError(f"Agent name must be a string, got: {type(agent['name'])}")
            
            if not isinstance(agent['module'], str):
                raise ConfigurationError(
                    f"Agent '{agent['name']}' module must be a string, got: {type(agent['module'])}"
                )
            
            if not isinstance(agent['enabled'], bool):
                raise ConfigurationError(
                    f"Agent '{agent['name']}' enabled must be a boolean, got: {type(agent['enabled'])}"
                )
            
            if not isinstance(agent['order'], int):
                raise ConfigurationError(
                    f"Agent '{agent['name']}' order must be an integer, got: {type(agent['order'])}"
                )
