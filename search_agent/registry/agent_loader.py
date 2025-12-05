"""Dynamic agent loader for importing agents from configured modules."""

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
        """Dynamically import and return an agent from a module.
        
        Args:
            module_path: Dotted path to the module (e.g., 'search_agent.sub_agents.wikipedia.wikipedia_agent')
            agent_name: Name of the agent (used for error messages and discovery)
            
        Returns:
            The loaded Agent instance
            
        Raises:
            AgentNotFoundError: If the module cannot be imported
            AgentLoadError: If the agent instance cannot be found in the module
        """
        logger.info("Loading agent '%s' from module: %s", agent_name, module_path)
        
        try:
            # Dynamically import the module
            module = importlib.import_module(module_path)
            logger.debug("Successfully imported module: %s", module_path)
        except ImportError as e:
            raise AgentNotFoundError(
                f"Failed to import module '{module_path}' for agent '{agent_name}': {e}"
            )
        except Exception as e:
            raise AgentLoadError(
                f"Error importing module '{module_path}' for agent '{agent_name}': {e}"
            )
        
        # Try to find the agent instance in the module
        agent = AgentLoader.discover_agent(module, agent_name, module_path)
        
        logger.info("Successfully loaded agent '%s'", agent_name)
        return agent
    
    @staticmethod
    def discover_agent(module: Any, agent_name: str, module_path: str) -> Agent:
        """Find and return the agent instance from a module.
        
        The function looks for an exported agent instance in the following order:
        1. An attribute with the exact agent_name
        2. An attribute ending with '_agent'
        3. Any attribute that is an instance of Agent
        
        Args:
            module: The imported module object
            agent_name: Name of the agent being loaded
            module_path: Path to the module (for error messages)
            
        Returns:
            The discovered Agent instance
            
        Raises:
            AgentLoadError: If no valid agent instance is found
        """
        # Strategy 1: Try exact name match
        if hasattr(module, agent_name):
            candidate = getattr(module, agent_name)
            if isinstance(candidate, Agent):
                logger.debug("Found agent by exact name: %s", agent_name)
                return candidate
        
        # Strategy 2: Look for attributes ending with '_agent'
        agent_candidates = []
        for attr_name in dir(module):
            if attr_name.endswith('_agent') and not attr_name.startswith('_'):
                candidate = getattr(module, attr_name)
                if isinstance(candidate, Agent):
                    agent_candidates.append((attr_name, candidate))
        
        if len(agent_candidates) == 1:
            attr_name, agent = agent_candidates[0]
            logger.debug("Found agent by '_agent' suffix: %s", attr_name)
            return agent
        elif len(agent_candidates) > 1:
            # Multiple agent instances found - try to match by name
            for attr_name, agent in agent_candidates:
                if attr_name == agent_name or agent.name == agent_name:
                    logger.debug("Found agent by matching multiple candidates: %s", attr_name)
                    return agent
            
            # If still ambiguous, raise error
            names = [name for name, _ in agent_candidates]
            raise AgentLoadError(
                f"Multiple agent instances found in '{module_path}': {names}. "
                f"Cannot determine which one to use for '{agent_name}'"
            )
        
        # Strategy 3: Look for any Agent instance
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                candidate = getattr(module, attr_name)
                if isinstance(candidate, Agent):
                    logger.debug("Found agent instance: %s", attr_name)
                    return candidate
        
        # No agent found
        raise AgentLoadError(
            f"No Agent instance found in module '{module_path}' for agent '{agent_name}'. "
            f"The module must export an Agent instance."
        )
