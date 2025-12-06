"""YAML configuration parser for tools registry."""

import logging
from pathlib import Path
from typing import Any, Dict

import yaml

from ..exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class ToolYAMLParser:
    """Parser for tools registry YAML configuration file."""
    
    def __init__(self, config_path: str):
        """Initialize the parser with a configuration file path.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.file_exists = self.config_path.exists()
        if not self.file_exists:
            logger.info(f"Configuration file not found: {config_path}. Tools registration will be skipped.")
    
    def parse(self) -> Dict[str, Any]:
        """Parse and validate the YAML configuration file.
        
        Returns:
            Parsed configuration dictionary
            
        Raises:
            ConfigurationError: If the configuration is invalid
        """
        if not self.file_exists:
            return {'tools': []}
        
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
        
        self._validate_tools(config['tools'])
        
        return config
    
    def _validate_tools(self, tools: list) -> None:
        """Validate tools configuration for duplicates.
        
        Args:
            tools: List of tool configurations
            
        Raises:
            ConfigurationError: If validation fails
        """
        self._validate_duplicate_name_module(tools)
        self._validate_duplicate_order(tools)
    
    def _validate_duplicate_name_module(self, tools: list) -> None:
        """Check for duplicate tool name and module combinations.
        
        Args:
            tools: List of tool configurations
            
        Raises:
            ConfigurationError: If duplicates are found
        """
        seen = {}
        for idx, tool in enumerate(tools):
            name = tool.get('name')
            module = tool.get('module')
            
            if not name or not module:
                continue
            
            key = (name, module)
            if key in seen:
                raise ConfigurationError(
                    f"Duplicate tool configuration found: tool '{name}' "
                    f"with module '{module}' is defined at positions {seen[key]} and {idx}"
                )
            seen[key] = idx
    
    def _validate_duplicate_order(self, tools: list) -> None:
        """Check for duplicate order values among enabled tools.
        
        Args:
            tools: List of tool configurations
            
        Raises:
            ConfigurationError: If duplicate order values are found
        """
        enabled_tools = [
            tool for tool in tools 
            if tool.get('enabled', False)
        ]
        
        order_map = {}
        for tool in enabled_tools:
            order = tool.get('order')
            name = tool.get('name', 'unknown')
            
            if order is None:
                continue
            
            if order in order_map:
                raise ConfigurationError(
                    f"Duplicate order value {order} found for enabled tools: "
                    f"'{order_map[order]}' and '{name}'"
                )
            order_map[order] = name
