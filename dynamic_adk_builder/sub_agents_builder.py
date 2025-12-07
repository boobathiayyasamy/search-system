import logging
from typing import List

from google.adk.agents.llm_agent import Agent
from dynamic_adk_registry import SubAgentRegistry, AgentLoadError, ConfigurationError

logger = logging.getLogger(__name__)


class SubAgentsBuilder:
    
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self._registry = None
    
    def build(self) -> List[Agent]:
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
