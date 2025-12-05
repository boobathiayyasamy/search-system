"""MCP Client."""

import logging
from typing import Optional

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams, StdioServerParameters

logger = logging.getLogger(__name__)

MCP_SERVER_COMMAND = "python"
MCP_SERVER_ARGS = ["/Users/boobathi/master/studies/ai/responsive/util-mcp/time_server.py"]


def create_mcp_toolset() -> McpToolset:
    """Create and configure the MCP toolset."""
    
    server_params = StdioServerParameters(
        command=MCP_SERVER_COMMAND,
        args=MCP_SERVER_ARGS
    )
    
    connection_params = StdioConnectionParams(
        server_params=server_params
    )
    
    toolset = McpToolset(
        connection_params=connection_params
    )
    
    return toolset
