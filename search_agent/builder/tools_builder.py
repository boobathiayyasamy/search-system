"""Root Tools Builder."""

import logging
from pathlib import Path
from typing import List, Any

from ..registry import ToolsRegistry

logger = logging.getLogger(__name__)


def build_tools() -> List[Any]:
    """Build and return the agent tools."""
    try:
        # Get the path to tools_registry.yaml
        registry_path = Path(__file__).parent.parent / "tools_registry.yaml"
        
        # Load tools from registry
        tools_registry = ToolsRegistry(str(registry_path))
        tools = tools_registry.load_tools()
        logger.info(f"Loaded {len(tools)} tool(s) from registry")
        
        return tools
    except Exception as e:
        logger.error("Failed to initialize tools: %s", e)
        raise
