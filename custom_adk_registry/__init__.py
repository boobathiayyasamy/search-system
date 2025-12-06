"""Custom ADK Registry - Reusable library for loading agents and tools from YAML configurations.

This library provides a flexible, reusable way to load agents, sub-agents, and tools
from YAML configuration files. It can be used by any agent or project that needs
dynamic agent/tool loading capabilities.

Usage:
    from custom_adk_registry import SubAgentRegistry, ToolRegistry
    
    # Load sub-agents
    sub_agent_registry = SubAgentRegistry('path/to/sub_agents_registry.yaml')
    sub_agents = sub_agent_registry.load_agents()
    
    # Load tools
    tool_registry = ToolRegistry('path/to/tools_registry.yaml')
    tools = tool_registry.load_tools()
"""

from .sub_agents.registry import SubAgentRegistry
from .tools.registry import ToolRegistry
from .exceptions import (
    RegistryError,
    ConfigurationError,
    AgentLoadError,
    AgentNotFoundError,
    ToolLoadError,
)

__all__ = [
    "SubAgentRegistry",
    "ToolRegistry",
    "RegistryError",
    "ConfigurationError",
    "AgentLoadError",
    "AgentNotFoundError",
    "ToolLoadError",
]

__version__ = "1.0.0"
