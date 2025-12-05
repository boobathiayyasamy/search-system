"""YAML configuration parser for agents registry."""

import logging
from pathlib import Path
from typing import Any, Dict

import yaml

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class YAMLParser:
    """Parser for agents registry YAML configuration file."""
    
    REQUIRED_FIELDS = {'name', 'module', 'enabled', 'order'}
    FIELD_TYPES = {
        'name': str,
        'module': str,
        'enabled': bool,
        'order': int
    }
    
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
        
        self._validate_config(config)
        return config
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate the configuration structure and required fields."""
        if 'agents' not in config:
            raise ConfigurationError("Configuration must contain 'agents' key")
        
        agents = config['agents']
        if not isinstance(agents, list):
            raise ConfigurationError("'agents' must be a list")
        
        if not agents:
            return
        
        for idx, agent in enumerate(agents):
            self._validate_agent(agent, idx)
    
    def _validate_agent(self, agent: Any, idx: int) -> None:
        """Validate a single agent configuration."""
        if not isinstance(agent, dict):
            raise ConfigurationError(f"Agent at index {idx} must be a dictionary")
        
        agent_name = agent.get('name', f'index {idx}')
        
        missing_fields = self.REQUIRED_FIELDS - set(agent.keys())
        if missing_fields:
            raise ConfigurationError(
                f"Agent '{agent_name}' missing required fields: {missing_fields}"
            )
        
        for field, expected_type in self.FIELD_TYPES.items():
            value = agent[field]
            if not isinstance(value, expected_type):
                raise ConfigurationError(
                    f"Agent '{agent_name}' field '{field}' must be {expected_type.__name__}, "
                    f"got: {type(value).__name__}"
                )
