"""Sub-agents Builder."""

import logging
from pathlib import Path
from typing import List

from google.adk.agents.llm_agent import Agent
from search_agent.registry import AgentsRegistry, AgentLoadError, ConfigurationError

logger = logging.getLogger(__name__)


def build_sub_agents() -> List[Agent]:
    """Build and return the list of sub-agents dynamically from registry."""
    
    try:
        # Get the path to agents_registry.yaml
        # It should be in the search_agent directory (parent of builder)
        builder_dir = Path(__file__).parent
        search_agent_dir = builder_dir.parent
        registry_path = search_agent_dir / "agents_registry.yaml"
        
        # Initialize registry and load agents
        registry = AgentsRegistry(str(registry_path))
        sub_agents = registry.load_agents()
        
        return sub_agents
        
    except (ConfigurationError, AgentLoadError) as e:
        logger.error("Failed to build sub-agents from registry: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error building sub-agents: %s", e)
        raise AgentLoadError(f"Unexpected error building sub-agents: {e}") from e
