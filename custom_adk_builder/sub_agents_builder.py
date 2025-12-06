"""Sub-agents Builder - Reusable builder for loading sub-agents from registry."""

import logging
from typing import List

from google.adk.agents.llm_agent import Agent
from custom_adk_registry import SubAgentRegistry, AgentLoadError, ConfigurationError

logger = logging.getLogger(__name__)


class SubAgentsBuilder:
    """Builder class for loading sub-agents from a registry."""
    
    def __init__(self, registry_path: str):
        """Initialize the SubAgentsBuilder.
        
        Args:
            registry_path: Path to the sub-agents registry YAML file
        """
        self.registry_path = registry_path
        self._registry = None
    
    def build(self) -> List[Agent]:
        """Build and return the list of sub-agents from registry.
        
        Returns:
            List of Agent instances loaded from the registry
            
        Raises:
            ConfigurationError: If registry configuration is invalid
            AgentLoadError: If agents cannot be loaded from registry
        """
        try:
            self._registry = SubAgentRegistry(self.registry_path)
            sub_agents = self._registry.load_agents()
            logger.info(f"Loaded {len(sub_agents)} sub-agent(s) from registry")
            return sub_agents
        except (ConfigurationError, AgentLoadError) as e:
            logger.error("Failed to build sub-agents from registry: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error building sub-agents: %s", e)
            raise AgentLoadError(f"Unexpected error building sub-agents: {e}") from e
