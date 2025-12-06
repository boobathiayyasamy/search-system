"""YAML configuration parser for agents registry."""

import logging
from pathlib import Path
from typing import Any, Dict

import yaml

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class YAMLParser:
    """Parser for agents registry YAML configuration file."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.file_exists = self.config_path.exists()
        if not self.file_exists:
            logger.info(f"Configuration file not found: {config_path}. Sub-agents registration will be skipped.")
    
    def parse(self) -> Dict[str, Any]:
        """Parse and validate the YAML configuration file."""
        if not self.file_exists:
            return {'agents': []}
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Failed to parse YAML file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error reading configuration file: {e}")
        
        if not config:
            raise ConfigurationError("Configuration file is empty")
        
        if 'agents' not in config:
            raise ConfigurationError("Configuration must contain 'agents' key")
        
        if not isinstance(config['agents'], list):
            raise ConfigurationError("'agents' must be a list")
        
        self._validate_agents(config['agents'])
        
        return config
    
    def _validate_agents(self, agents: list) -> None:
        """Validate agents configuration for duplicates."""
        self._validate_duplicate_name_module(agents)
        self._validate_duplicate_order(agents)
    
    def _validate_duplicate_name_module(self, agents: list) -> None:
        """Check for duplicate agent name and module combinations."""
        seen = {}
        for idx, agent in enumerate(agents):
            name = agent.get('name')
            module = agent.get('module')
            
            if not name or not module:
                continue
            
            key = (name, module)
            if key in seen:
                raise ConfigurationError(
                    f"Duplicate agent configuration found: agent '{name}' "
                    f"with module '{module}' is defined at positions {seen[key]} and {idx}"
                )
            seen[key] = idx
    
    def _validate_duplicate_order(self, agents: list) -> None:
        """Check for duplicate order values among enabled agents."""
        enabled_agents = [
            agent for agent in agents 
            if agent.get('enabled', False)
        ]
        
        order_map = {}
        for agent in enabled_agents:
            order = agent.get('order')
            name = agent.get('name', 'unknown')
            
            if order is None:
                continue
            
            if order in order_map:
                raise ConfigurationError(
                    f"Duplicate order value {order} found for enabled agents: "
                    f"'{order_map[order]}' and '{name}'"
                )
            order_map[order] = name

