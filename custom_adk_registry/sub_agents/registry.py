"""Sub-agents registry for loading agents from YAML configuration."""

import logging
from typing import List

from google.adk.agents.llm_agent import Agent

from .loader import SubAgentLoader
from ..exceptions import AgentLoadError
from .parser import SubAgentYAMLParser

logger = logging.getLogger(__name__)


class SubAgentRegistry:
    """Registry for loading sub-agents from YAML configuration.
    
    This class provides a reusable way to load sub-agents from a YAML configuration file.
    It handles parsing, validation, and dynamic loading of agent modules.
    
    Example:
        registry = SubAgentRegistry('path/to/sub_agents_registry.yaml')
        sub_agents = registry.load_agents()
    """
    
    def __init__(self, config_path: str):
        """Initialize the sub-agents registry.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = config_path
        self.parser = SubAgentYAMLParser(config_path)
        self.loader = SubAgentLoader()
    
    def load_agents(self) -> List[Agent]:
        """Load and return enabled agents in configured order.
        
        Returns:
            List of loaded Agent instances, sorted by order
            
        Raises:
            AgentLoadError: If any agent fails to load
        """
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
            tools = config.get('tools', [])  # Extract tools for this agent
            sub_agents = config.get('sub_agents', [])  # Extract sub_agents for this agent
            
            try:
                agent = self.loader.load_agent_from_module(module_path, agent_name, tools, sub_agents)
                loaded_agents.append(agent)
            except (AgentLoadError, Exception) as e:
                error_msg = f"Failed to load agent '{agent_name}' from '{module_path}': {e}"
                logger.error(error_msg)
                raise AgentLoadError(error_msg) from e
        
        return loaded_agents
