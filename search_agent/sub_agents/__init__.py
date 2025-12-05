"""Sub-Agents Module - Contains all sub-agents for the search system.

Note: Sub-agents are now loaded dynamically via the AgentsRegistry.
The imports below are kept for backward compatibility and direct access if needed.
The primary way to load agents is through the build_sub_agents() function
in search_agent.builder.sub_agents_builder, which uses the registry configuration.
"""

from .wikipedia import wikipedia_agent
from .summarizing import summarizing_agent

__all__ = ["wikipedia_agent", "summarizing_agent"]
