"""Tool loader for dynamically loading tools from modules."""

import importlib
import logging
from typing import Any, Callable

from .exceptions import ToolLoadError

logger = logging.getLogger(__name__)


class ToolLoader:
    """Loads tools from specified module paths."""
    
    def load_tool_from_module(self, module_path: str, function_name: str) -> Any:
        """Load a tool function from a module.
        
        Args:
            module_path: Full module path (e.g., 'search_agent.tools.mcp')
            function_name: Name of the function to load (e.g., 'create_mcp_toolset')
            
        Returns:
            The loaded tool or toolset
            
        Raises:
            ToolLoadError: If the tool cannot be loaded
        """
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ToolLoadError(f"Failed to import module '{module_path}': {e}")
        
        if not hasattr(module, function_name):
            raise ToolLoadError(
                f"Function '{function_name}' not found in module '{module_path}'"
            )
        
        tool_function = getattr(module, function_name)
        
        if not callable(tool_function):
            raise ToolLoadError(
                f"'{function_name}' in module '{module_path}' is not callable"
            )
        
        try:
            # Call the function to get the actual tool/toolset
            tool = tool_function()
            logger.info("Successfully loaded tool from %s.%s", module_path, function_name)
            return tool
        except Exception as e:
            raise ToolLoadError(
                f"Failed to execute '{function_name}' from '{module_path}': {e}"
            )
