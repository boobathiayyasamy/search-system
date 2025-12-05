"""Sub-agents Builder - Builds and returns sub-agents for the root agent.

This module dynamically loads sub-agents based on the agents_registry.yaml configuration.
"""

import logging
from pathlib import Path
from typing import List

from google.adk.agents.llm_agent import Agent
from search_agent.registry import AgentsRegistry, AgentLoadError, ConfigurationError

logger = logging.getLogger(__name__)


def build_sub_agents() -> List[Agent]:
    """Build and return the list of sub-agents dynamically from registry.
    
    The agents are loaded based on the configuration in agents_registry.yaml.
    Only enabled agents will be loaded, in the order specified by the 'order' field.
    
    Returns:
        List[Agent]: List of dynamically loaded enabled agents
        
    Raises:
        ConfigurationError: If the registry configuration is invalid
        AgentLoadError: If an agent fails to load
        
    Note:
        The agents are loaded from modules specified in:
        search_agent/agents_registry.yaml
    """
    logger.info("Building sub-agents list from registry")
    
    try:
        # Get the path to agents_registry.yaml
        # It should be in the search_agent directory (parent of builder)
        builder_dir = Path(__file__).parent
        search_agent_dir = builder_dir.parent
        registry_path = search_agent_dir / "agents_registry.yaml"
        
        logger.debug("Registry path: %s", registry_path)
        
        # Initialize registry and load agents
        registry = AgentsRegistry(str(registry_path))
        sub_agents = registry.load_agents()
        
        logger.info("Sub-agents list built with %d agents: %s", 
                    len(sub_agents), 
                    [agent.name for agent in sub_agents])
        
        return sub_agents
        
    except (ConfigurationError, AgentLoadError) as e:
        logger.error("Failed to build sub-agents from registry: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error building sub-agents: %s", e)
        raise AgentLoadError(f"Unexpected error building sub-agents: {e}") from e
