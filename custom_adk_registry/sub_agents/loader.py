"""Dynamic sub-agent loader."""

import importlib
import logging
from typing import Any

from google.adk.agents.llm_agent import Agent

from ..exceptions import AgentLoadError, AgentNotFoundError

logger = logging.getLogger(__name__)


class SubAgentLoader:
    """Dynamically loads sub-agents from Python modules."""
    
    @staticmethod
    def load_agent_from_module(module_path: str, agent_name: str, tools: list = None, sub_agents: list = None) -> Agent:
        """Dynamically import and return an agent from a module.
        
        Args:
            module_path: Full module path (e.g., 'search_agent.sub_agents.wikipedia.wikipedia_agent')
            agent_name: Name of the agent to load
            tools: Optional list of tool configurations to load for this agent
            sub_agents: Optional list of sub_agent configurations to load for this agent
            
        Returns:
            Agent instance
            
        Raises:
            AgentNotFoundError: If module cannot be imported
            AgentLoadError: If agent cannot be loaded from module
        """
        
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise AgentNotFoundError(
                f"Failed to import module '{module_path}' for agent '{agent_name}': {e}"
            )
        except Exception as e:
            raise AgentLoadError(
                f"Error importing module '{module_path}' for agent '{agent_name}': {e}"
            )
        
        # Load tools if specified
        loaded_tools = []
        if tools:
            loaded_tools = SubAgentLoader.load_tools_for_agent(tools, agent_name)
        
        # Load sub_agents if specified
        loaded_sub_agents = []
        if sub_agents:
            loaded_sub_agents = SubAgentLoader.load_sub_agents_for_agent(sub_agents, agent_name)
        
        agent = SubAgentLoader.discover_agent(module, agent_name, module_path, loaded_tools, loaded_sub_agents)
        logger.info(f"Loaded agent '{agent_name}' from module '{module_path}' with {len(loaded_tools)} tool(s) and {len(loaded_sub_agents)} sub-agent(s)")
        
        return agent
    
    @staticmethod
    def discover_agent(module: Any, agent_name: str, module_path: str, tools: list = None, sub_agents: list = None) -> Agent:
        """Find and return the agent instance from a module.
        
        Args:
            module: The imported module
            agent_name: Name of the agent to find
            module_path: Module path (for error messages)
            tools: Optional list of tools to assign to the agent
            sub_agents: Optional list of sub_agents to assign to the agent
            
        Returns:
            Agent instance
            
        Raises:
            AgentLoadError: If agent cannot be found or multiple candidates exist
        """
        if hasattr(module, agent_name):
            candidate = getattr(module, agent_name)
            if isinstance(candidate, Agent):
                return SubAgentLoader._rebuild_agent_with_tools_and_sub_agents(candidate, tools, sub_agents) if (tools or sub_agents) else candidate
        
        agent_candidates = []
        for attr_name in dir(module):
            if attr_name.endswith('_agent') and not attr_name.startswith('_'):
                candidate = getattr(module, attr_name)
                if isinstance(candidate, Agent):
                    agent_candidates.append((attr_name, candidate))
        
        if len(agent_candidates) == 1:
            attr_name, agent = agent_candidates[0]
            return SubAgentLoader._rebuild_agent_with_tools_and_sub_agents(agent, tools, sub_agents) if (tools or sub_agents) else agent
        elif len(agent_candidates) > 1:
            for attr_name, agent in agent_candidates:
                if attr_name == agent_name or agent.name == agent_name:
                    return SubAgentLoader._rebuild_agent_with_tools_and_sub_agents(agent, tools, sub_agents) if (tools or sub_agents) else agent
            
            names = [name for name, _ in agent_candidates]
            raise AgentLoadError(
                f"Multiple agent instances found in '{module_path}': {names}. "
                f"Cannot determine which one to use for '{agent_name}'"
            )
        
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                candidate = getattr(module, attr_name)
                if isinstance(candidate, Agent):
                    return SubAgentLoader._rebuild_agent_with_tools_and_sub_agents(candidate, tools, sub_agents) if (tools or sub_agents) else candidate
        
        raise AgentLoadError(
            f"No Agent instance found in module '{module_path}' for agent '{agent_name}'. "
            f"The module must export an Agent instance."
        )
    
    @staticmethod
    def load_tools_for_agent(tool_configs: list, agent_name: str) -> list:
        """Load tools for an agent from tool configurations.
        
        Args:
            tool_configs: List of tool configuration dictionaries
            agent_name: Name of the agent (for error messages)
            
        Returns:
            List of loaded tool instances
            
        Raises:
            AgentLoadError: If tools cannot be loaded
        """
        from ..exceptions import ToolLoadError
        
        # Filter and sort enabled tools
        enabled_tools = [
            config for config in tool_configs
            if config.get('enabled', False)
        ]
        enabled_tools.sort(key=lambda x: x.get('order', 999))
        
        loaded_tools = []
        for tool_config in enabled_tools:
            tool_name = tool_config.get('name')
            module_path = tool_config.get('module')
            function_name = tool_config.get('function')
            
            if not all([tool_name, module_path, function_name]):
                logger.warning(
                    f"Skipping incomplete tool configuration for agent '{agent_name}': {tool_config}"
                )
                continue
            
            try:
                # Import the tool module
                tool_module = importlib.import_module(module_path)
                
                # Get the tool function
                if not hasattr(tool_module, function_name):
                    raise AgentLoadError(
                        f"Function '{function_name}' not found in module '{module_path}'"
                    )
                
                tool_function = getattr(tool_module, function_name)
                
                # If it's callable and not a class, it's the tool itself
                if callable(tool_function):
                    loaded_tools.append(tool_function)
                    logger.info(
                        f"Loaded tool '{tool_name}' ({function_name}) from '{module_path}' for agent '{agent_name}'"
                    )
                else:
                    raise AgentLoadError(
                        f"'{function_name}' in module '{module_path}' is not callable"
                    )
                    
            except ImportError as e:
                raise AgentLoadError(
                    f"Failed to import tool module '{module_path}' for agent '{agent_name}': {e}"
                )
            except Exception as e:
                raise AgentLoadError(
                    f"Failed to load tool '{tool_name}' for agent '{agent_name}': {e}"
                )
        
        return loaded_tools
    
    @staticmethod
    def load_sub_agents_for_agent(sub_agent_configs: list, parent_agent_name: str) -> list:
        """Load sub_agents for an agent from sub_agent configurations.
        
        Args:
            sub_agent_configs: List of sub_agent configuration dictionaries
            parent_agent_name: Name of the parent agent (for error messages)
            
        Returns:
            List of loaded sub_agent instances
            
        Raises:
            AgentLoadError: If sub_agents cannot be loaded
        """
        # Filter and sort enabled sub_agents
        enabled_sub_agents = [
            config for config in sub_agent_configs
            if config.get('enabled', False)
        ]
        enabled_sub_agents.sort(key=lambda x: x.get('order', 999))
        
        loaded_sub_agents = []
        for sub_agent_config in enabled_sub_agents:
            sub_agent_name = sub_agent_config.get('name')
            module_path = sub_agent_config.get('module')
            tools = sub_agent_config.get('tools', [])
            nested_sub_agents = sub_agent_config.get('sub_agents', [])
            
            if not all([sub_agent_name, module_path]):
                logger.warning(
                    f"Skipping incomplete sub_agent configuration for agent '{parent_agent_name}': {sub_agent_config}"
                )
                continue
            
            try:
                # Recursively load the sub_agent with its own tools and sub_agents
                sub_agent = SubAgentLoader.load_agent_from_module(
                    module_path, 
                    sub_agent_name, 
                    tools=tools,
                    sub_agents=nested_sub_agents
                )
                loaded_sub_agents.append(sub_agent)
                logger.info(
                    f"Loaded sub_agent '{sub_agent_name}' from '{module_path}' for agent '{parent_agent_name}'"
                )
                    
            except Exception as e:
                raise AgentLoadError(
                    f"Failed to load sub_agent '{sub_agent_name}' for agent '{parent_agent_name}': {e}"
                )
        
        return loaded_sub_agents
    
    @staticmethod
    def _rebuild_agent_with_tools_and_sub_agents(agent: Agent, tools: list = None, sub_agents: list = None) -> Agent:
        """Rebuild an agent with new tools and sub_agents.
        
        Args:
            agent: Original agent instance
            tools: Optional list of tools to assign
            sub_agents: Optional list of sub_agents to assign
            
        Returns:
            New Agent instance with tools and sub_agents
        """
        # Get existing values if new ones not provided
        final_tools = tools if tools is not None else (agent.tools if hasattr(agent, 'tools') else [])
        final_sub_agents = sub_agents if sub_agents is not None else (agent.sub_agents if hasattr(agent, 'sub_agents') else [])
        
        # Create a new agent with the same properties but with new tools and sub_agents
        return Agent(
            model=agent.model,
            name=agent.name,
            description=agent.description,
            instruction=agent.instruction,
            tools=final_tools,
            sub_agents=final_sub_agents
        )
