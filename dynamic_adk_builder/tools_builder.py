import logging
from typing import List, Any

from dynamic_adk_registry import ToolRegistry

logger = logging.getLogger(__name__)


class ToolsBuilder:
    
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self._registry = None
    
    def build(self) -> List[Any]:
        try:
            self._registry = ToolRegistry(self.registry_path)
            tools = self._registry.load_tools()
            logger.info(f"Loaded {len(tools)} tool(s) from registry")
            return tools
        except Exception as e:
            logger.error("Failed to load tools from registry: %s", e)
            raise
