"""Custom ADK Builder - Reusable library for building agents with sub-agents and tools.

This library provides a flexible, reusable way to build agents with sub-agents and tools
loaded from YAML configuration files via the custom_adk_registry library.

Usage:
    from custom_adk_builder import AgentBuilder
    
    # Build an agent with sub-agents and tools
    builder = AgentBuilder(
        model=model,
        name="My Agent",
        description="A helpful agent",
        instruction="You are a helpful assistant",
        sub_agents_registry_path="path/to/sub_agents_registry.yaml",
        tools_registry_path="path/to/tools_registry.yaml"
    )
    agent = builder.build()
    
    # Or use individual builders
    from custom_adk_builder import SubAgentsBuilder, ToolsBuilder
    
    sub_agents_builder = SubAgentsBuilder('path/to/sub_agents_registry.yaml')
    sub_agents = sub_agents_builder.build()
    
    tools_builder = ToolsBuilder('path/to/tools_registry.yaml')
    tools = tools_builder.build()
"""

from .agent_builder import AgentBuilder
from .sub_agents_builder import SubAgentsBuilder
from .tools_builder import ToolsBuilder

__all__ = [
    "AgentBuilder",
    "SubAgentsBuilder",
    "ToolsBuilder",
]

__version__ = "1.0.0"
