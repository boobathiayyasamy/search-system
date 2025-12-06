"""Main agents registry."""

import logging
from typing import List

from google.adk.agents.llm_agent import Agent

from .sub_agents_loader import AgentLoader
from .exceptions import AgentLoadError
from .sub_agents_registry_parser import YAMLParser

logger = logging.getLogger(__name__)


class AgentsRegistry:
    """Registry for loading agents from YAML configuration."""
    
    def __init__(self, config_path: str):
        """Initialize the agents registry."""
        self.config_path = config_path
        self.parser = YAMLParser(config_path)
        self.loader = AgentLoader()
    
    def load_agents(self) -> List[Agent]:
        """Load and return enabled agents in configured order."""
        config = self.parser.parse()
        agent_configs = config.get('agents', [])
        
        enabled_configs = [
            config for config in agent_configs 
            if config.get('enabled', False)
        ]
        enabled_configs.sort(key=lambda x: x.get('order', 999))
        
        loaded_agents = []
        for config in enabled_configs:
            agent_name = config['name']
            module_path = config['module']
            
            try:
                agent = self.loader.load_agent_from_module(module_path, agent_name)
                loaded_agents.append(agent)
            except (AgentLoadError, Exception) as e:
                error_msg = f"Failed to load agent '{agent_name}' from '{module_path}': {e}"
                logger.error(error_msg)
                raise AgentLoadError(error_msg) from e
        
        return loaded_agents
