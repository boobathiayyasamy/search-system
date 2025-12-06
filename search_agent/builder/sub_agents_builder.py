"""Sub-agents Builder."""

import logging
from pathlib import Path
from typing import List

from google.adk.agents.llm_agent import Agent
from custom_adk_registry import SubAgentRegistry, AgentLoadError, ConfigurationError

logger = logging.getLogger(__name__)


def build_sub_agents() -> List[Agent]:
    """Build and return the list of sub-agents dynamically from registry."""
    
    try:
        from search_agent.config import get_config
        
        config = get_config()
        builder_dir = Path(__file__).parent
        search_agent_dir = builder_dir.parent
        
        # Get registry path from config and resolve it relative to search_agent directory
        registry_filename = config.sub_agents_registry_path
        registry_path = search_agent_dir / registry_filename
        
        registry = SubAgentRegistry(str(registry_path))
        sub_agents = registry.load_agents()
        logger.info(f"Loaded {len(sub_agents)} sub-agent(s) from registry")
        
        return sub_agents
        
    except (ConfigurationError, AgentLoadError) as e:
        logger.error("Failed to build sub-agents from registry: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error building sub-agents: %s", e)
        raise AgentLoadError(f"Unexpected error building sub-agents: {e}") from e
