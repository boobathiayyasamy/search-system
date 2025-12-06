"""Tools registry for loading tools from YAML configuration."""

import logging
from typing import List, Any

from .loader import ToolLoader
from ..exceptions import ToolLoadError
from .parser import ToolYAMLParser

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry for loading tools from YAML configuration.
    
    This class provides a reusable way to load tools from a YAML configuration file.
    It handles parsing, validation, and dynamic loading of tool modules.
    
    Example:
        registry = ToolRegistry('path/to/tools_registry.yaml')
        tools = registry.load_tools()
    """
    
    def __init__(self, config_path: str):
        """Initialize the tools registry.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = config_path
        self.parser = ToolYAMLParser(config_path)
        self.loader = ToolLoader()
    
    def load_tools(self) -> List[Any]:
        """Load and return enabled tools in configured order.
        
        Returns:
            List of loaded tools, sorted by order
            
        Raises:
            ToolLoadError: If any tool fails to load
        """
        config = self.parser.parse()
        tool_configs = config.get('tools', [])
        
        enabled_configs = [
            config for config in tool_configs 
            if config.get('enabled', False)
        ]
        enabled_configs.sort(key=lambda x: x.get('order', 999))
        
        loaded_tools = []
        for config in enabled_configs:
            tool_name = config['name']
            module_path = config['module']
            function_name = config['function']
            
            try:
                tool = self.loader.load_tool_from_module(module_path, function_name)
                loaded_tools.append(tool)
            except (ToolLoadError, Exception) as e:
                error_msg = f"Failed to load tool '{tool_name}' from '{module_path}.{function_name}': {e}"
                logger.error(error_msg)
                raise ToolLoadError(error_msg) from e
        
        return loaded_tools
