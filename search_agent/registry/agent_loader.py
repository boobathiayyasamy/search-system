"""Dynamic agent loader."""

import importlib
import logging
from typing import Any

from google.adk.agents.llm_agent import Agent

from .exceptions import AgentLoadError, AgentNotFoundError

logger = logging.getLogger(__name__)


class AgentLoader:
    """Dynamically loads agents from Python modules."""
    
    @staticmethod
    def load_agent_from_module(module_path: str, agent_name: str) -> Agent:
        """Dynamically import and return an agent from a module."""
        
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise AgentNotFoundError(
                f"Failed to import module '{module_path}' for agent '{agent_name}': {e}"
            )
        except Exception as e:
            raise AgentLoadError(
                f"Error importing module '{module_path}' for agent '{agent_name}': {e}"
            )
        
        agent = AgentLoader.discover_agent(module, agent_name, module_path)
        
        return agent
    
    @staticmethod
    def discover_agent(module: Any, agent_name: str, module_path: str) -> Agent:
        """Find and return the agent instance from a module."""
        if hasattr(module, agent_name):
            candidate = getattr(module, agent_name)
            if isinstance(candidate, Agent):
                return candidate
        
        agent_candidates = []
        for attr_name in dir(module):
            if attr_name.endswith('_agent') and not attr_name.startswith('_'):
                candidate = getattr(module, attr_name)
                if isinstance(candidate, Agent):
                    agent_candidates.append((attr_name, candidate))
        
        if len(agent_candidates) == 1:
            attr_name, agent = agent_candidates[0]
            return agent
        elif len(agent_candidates) > 1:
            for attr_name, agent in agent_candidates:
                if attr_name == agent_name or agent.name == agent_name:
                    return agent
            
            names = [name for name, _ in agent_candidates]
            raise AgentLoadError(
                f"Multiple agent instances found in '{module_path}': {names}. "
                f"Cannot determine which one to use for '{agent_name}'"
            )
        
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                candidate = getattr(module, attr_name)
                if isinstance(candidate, Agent):
                    return candidate
        
        raise AgentLoadError(
            f"No Agent instance found in module '{module_path}' for agent '{agent_name}'. "
            f"The module must export an Agent instance."
        )
