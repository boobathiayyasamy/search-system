"""Tools Builder - Reusable builder for loading tools from registry."""

import logging
from typing import List, Any

from custom_adk_registry import ToolRegistry

logger = logging.getLogger(__name__)


class ToolsBuilder:
    """Builder class for loading tools from a registry."""
    
    def __init__(self, registry_path: str):
        """Initialize the ToolsBuilder.
        
        Args:
            registry_path: Path to the tools registry YAML file
        """
        self.registry_path = registry_path
        self._registry = None
    
    def build(self) -> List[Any]:
        """Build and return the tools from registry.
        
        Returns:
            List of tool instances loaded from the registry
            
        Raises:
            Exception: If tools cannot be loaded from registry
        """
        try:
            self._registry = ToolRegistry(self.registry_path)
            tools = self._registry.load_tools()
            logger.info(f"Loaded {len(tools)} tool(s) from registry")
            return tools
        except Exception as e:
            logger.error("Failed to load tools from registry: %s", e)
            raise
