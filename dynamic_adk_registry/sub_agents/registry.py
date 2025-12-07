import logging
from typing import List

from google.adk.agents.llm_agent import Agent

from .loader import SubAgentLoader
from ..exceptions import AgentLoadError
from .parser import SubAgentYAMLParser

logger = logging.getLogger(__name__)


class SubAgentRegistry:
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.parser = SubAgentYAMLParser(config_path)
        self.loader = SubAgentLoader()
    
    def load_agents(self) -> List[Agent]:
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
            tools = config.get('tools', [])
            sub_agents = config.get('sub_agents', [])
            
            try:
                agent = self.loader.load_agent_from_module(module_path, agent_name, tools, sub_agents)
                loaded_agents.append(agent)
            except (AgentLoadError, Exception) as e:
                logger.error(f"Failed to load agent '{agent_name}' from '{module_path}': {e}")
                raise AgentLoadError(f"Failed to load agent '{agent_name}' from '{module_path}': {e}") from e
        
        return loaded_agents
