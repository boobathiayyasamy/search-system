"""Main tools registry."""

import logging
from typing import List, Any

from .tool_loader import ToolLoader
from .exceptions import ToolLoadError
from .tools_registry_parser import ToolsYAMLParser

logger = logging.getLogger(__name__)


class ToolsRegistry:
    """Registry for loading tools from YAML configuration."""
    
    def __init__(self, config_path: str):
        """Initialize the tools registry."""
        self.config_path = config_path
        self.parser = ToolsYAMLParser(config_path)
        self.loader = ToolLoader()
    
    def load_tools(self) -> List[Any]:
        """Load and return enabled tools in configured order."""
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
