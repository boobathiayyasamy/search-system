"""Main agents registry."""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from google.adk.agents.llm_agent import Agent

from .agent_loader import AgentLoader
from .exceptions import AgentLoadError, ConfigurationError
from .yaml_parser import YAMLParser

logger = logging.getLogger(__name__)


class AgentsRegistry:
    """Registry for managing and loading agents from YAML configuration."""
    
    def __init__(self, config_path: str):
        """Initialize the agents registry."""
        self.config_path = config_path
        self.parser = YAMLParser(config_path)
        self.loader = AgentLoader()
        self._config: Optional[Dict] = None
        self._loaded_agents: Optional[List[Agent]] = None
    
    def load_agents(self, force_reload: bool = False) -> List[Agent]:
        """Load and return enabled agents in configured order."""
        if self._loaded_agents is not None and not force_reload:
            return self._loaded_agents
        
        self._config = self.parser.parse()
        
        agent_configs = self._config.get('agents', [])
        
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
        
        self._loaded_agents = loaded_agents
        
        return loaded_agents
    
    def get_agent_config(self, agent_name: str) -> Optional[Dict]:
        """Get configuration for a specific agent by name."""
        if self._config is None:
            self._config = self.parser.parse()
        
        agent_configs = self._config.get('agents', [])
        for config in agent_configs:
            if config.get('name') == agent_name:
                return config
        
        return None
    
    def reload(self) -> List[Agent]:
        """Reload configuration and agents from YAML file."""
        self._config = None
        self._loaded_agents = None
        return self.load_agents(force_reload=True)
    
    def get_loaded_agent_names(self) -> List[str]:
        """Get names of currently loaded agents."""
        if self._loaded_agents is None:
            return []
        return [agent.name for agent in self._loaded_agents]
