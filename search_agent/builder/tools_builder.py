"""Root Tools Builder."""

import logging
from pathlib import Path
from typing import List, Any

from custom_adk_registry import ToolRegistry

logger = logging.getLogger(__name__)


def build_tools() -> List[Any]:
    """Build and return the agent tools."""
    try:
        from search_agent.config import get_config
        
        config = get_config()
        builder_dir = Path(__file__).parent
        search_agent_dir = builder_dir.parent
        
        # Get registry path from config and resolve it relative to search_agent directory
        registry_relative_path = config.tools_registry_path
        registry_path = search_agent_dir / registry_relative_path
        
        # Load tools from registry
        tools_registry = ToolRegistry(str(registry_path))
        tools = tools_registry.load_tools()
        logger.info(f"Loaded {len(tools)} tool(s) from registry")
        
        return tools
    except Exception as e:
        logger.error("Failed to initialize tools: %s", e)
        raise
