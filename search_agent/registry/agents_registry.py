"""Main agents registry for managing dynamic agent loading."""

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
        """Initialize the agents registry.
        
        Args:
            config_path: Path to the agents_registry.yaml file
        """
        self.config_path = config_path
        self.parser = YAMLParser(config_path)
        self.loader = AgentLoader()
        self._config: Optional[Dict] = None
        self._loaded_agents: Optional[List[Agent]] = None
        
        logger.info("Initialized AgentsRegistry with config: %s", config_path)
    
    def load_agents(self, force_reload: bool = False) -> List[Agent]:
        """Load and return enabled agents in configured order.
        
        Args:
            force_reload: If True, reload agents even if already cached
            
        Returns:
            List of loaded Agent instances, sorted by order
            
        Raises:
            ConfigurationError: If configuration is invalid
            AgentLoadError: If an agent fails to load
        """
        # Return cached agents if available and not forcing reload
        if self._loaded_agents is not None and not force_reload:
            logger.debug("Returning cached agents (%d agents)", len(self._loaded_agents))
            return self._loaded_agents
        
        logger.info("Loading agents from registry")
        
        # Parse configuration
        self._config = self.parser.parse()
        
        # Get agent configurations
        agent_configs = self._config.get('agents', [])
        
        # Filter enabled agents and sort by order
        enabled_configs = [
            config for config in agent_configs 
            if config.get('enabled', False)
        ]
        enabled_configs.sort(key=lambda x: x.get('order', 999))
        
        logger.info("Found %d enabled agents out of %d total", 
                   len(enabled_configs), len(agent_configs))
        
        # Load each enabled agent
        loaded_agents = []
        for config in enabled_configs:
            agent_name = config['name']
            module_path = config['module']
            
            try:
                agent = self.loader.load_agent_from_module(module_path, agent_name)
                loaded_agents.append(agent)
                logger.info("Loaded agent: %s (order: %d)", agent_name, config['order'])
            except (AgentLoadError, Exception) as e:
                error_msg = f"Failed to load agent '{agent_name}' from '{module_path}': {e}"
                logger.error(error_msg)
                raise AgentLoadError(error_msg) from e
        
        # Cache loaded agents
        self._loaded_agents = loaded_agents
        
        logger.info("Successfully loaded %d agents: %s", 
                   len(loaded_agents),
                   [agent.name for agent in loaded_agents])
        
        return loaded_agents
    
    def get_agent_config(self, agent_name: str) -> Optional[Dict]:
        """Get configuration for a specific agent by name.
        
        Args:
            agent_name: Name of the agent to lookup
            
        Returns:
            Agent configuration dictionary, or None if not found
        """
        if self._config is None:
            self._config = self.parser.parse()
        
        agent_configs = self._config.get('agents', [])
        for config in agent_configs:
            if config.get('name') == agent_name:
                return config
        
        return None
    
    def reload(self) -> List[Agent]:
        """Reload configuration and agents from YAML file.
        
        Returns:
            List of newly loaded Agent instances
        """
        logger.info("Reloading agents registry")
        self._config = None
        self._loaded_agents = None
        return self.load_agents(force_reload=True)
    
    def get_loaded_agent_names(self) -> List[str]:
        """Get names of currently loaded agents.
        
        Returns:
            List of agent names
        """
        if self._loaded_agents is None:
            return []
        return [agent.name for agent in self._loaded_agents]
