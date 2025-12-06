"""Root Tools Builder."""

import logging
from ..tools.mcp import create_mcp_toolset

logger = logging.getLogger(__name__)


def build_root_tools():
    """Build and return the root agent tools."""
    try:
        time_tool = create_mcp_toolset()
        return [time_tool]
    except Exception as e:
        logger.error("Failed to initialize root tools: %s", e)
        raise
