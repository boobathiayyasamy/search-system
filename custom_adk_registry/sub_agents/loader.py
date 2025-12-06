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
    def load_agent_from_module(module_path: str, agent_name: str, tools: list = None) -> Agent:
        """Dynamically import and return an agent from a module.
        
        Args:
            module_path: Full module path (e.g., 'search_agent.sub_agents.wikipedia.wikipedia_agent')
            agent_name: Name of the agent to load
            tools: Optional list of tool configurations to load for this agent
            
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
        
        agent = SubAgentLoader.discover_agent(module, agent_name, module_path, loaded_tools)
        logger.info(f"Loaded agent '{agent_name}' from module '{module_path}' with {len(loaded_tools)} tool(s)")
        
        return agent
    
    @staticmethod
    def discover_agent(module: Any, agent_name: str, module_path: str, tools: list = None) -> Agent:
        """Find and return the agent instance from a module.
        
        Args:
            module: The imported module
            agent_name: Name of the agent to find
            module_path: Module path (for error messages)
            tools: Optional list of tools to assign to the agent
            
        Returns:
            Agent instance
            
        Raises:
            AgentLoadError: If agent cannot be found or multiple candidates exist
        """
        if hasattr(module, agent_name):
            candidate = getattr(module, agent_name)
            if isinstance(candidate, Agent):
                return SubAgentLoader._rebuild_agent_with_tools(candidate, tools) if tools else candidate
        
        agent_candidates = []
        for attr_name in dir(module):
            if attr_name.endswith('_agent') and not attr_name.startswith('_'):
                candidate = getattr(module, attr_name)
                if isinstance(candidate, Agent):
                    agent_candidates.append((attr_name, candidate))
        
        if len(agent_candidates) == 1:
            attr_name, agent = agent_candidates[0]
            return SubAgentLoader._rebuild_agent_with_tools(agent, tools) if tools else agent
        elif len(agent_candidates) > 1:
            for attr_name, agent in agent_candidates:
                if attr_name == agent_name or agent.name == agent_name:
                    return SubAgentLoader._rebuild_agent_with_tools(agent, tools) if tools else agent
            
            names = [name for name, _ in agent_candidates]
            raise AgentLoadError(
                f"Multiple agent instances found in '{module_path}': {names}. "
                f"Cannot determine which one to use for '{agent_name}'"
            )
        
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                candidate = getattr(module, attr_name)
                if isinstance(candidate, Agent):
                    return SubAgentLoader._rebuild_agent_with_tools(candidate, tools) if tools else candidate
        
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
    def _rebuild_agent_with_tools(agent: Agent, tools: list) -> Agent:
        """Rebuild an agent with new tools.
        
        Args:
            agent: Original agent instance
            tools: List of tools to assign
            
        Returns:
            New Agent instance with tools
        """
        # Create a new agent with the same properties but with new tools
        return Agent(
            model=agent.model,
            name=agent.name,
            description=agent.description,
            instruction=agent.instruction,
            tools=tools,
            sub_agents=agent.sub_agents if hasattr(agent, 'sub_agents') else []
        )
