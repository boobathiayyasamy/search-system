"""Sub-Agents Module - Contains all sub-agents for the search system."""

from .wikipedia import wikipedia_agent
from .summarizing import summarizing_agent

__all__ = ["wikipedia_agent", "summarizing_agent"]
