"""Agent Builder - Reusable builder for constructing agents with sub-agents and tools."""

import logging
from typing import Any, List

from google.adk.agents.llm_agent import Agent
from .sub_agents_builder import SubAgentsBuilder
from .tools_builder import ToolsBuilder

logger = logging.getLogger(__name__)


class AgentBuilder:
    """Builder class for constructing agents with sub-agents and tools."""
    
    def __init__(self, model: Any, name: str, description: str, instruction: str,
                 sub_agents_registry_path: str = None, tools_registry_path: str = None):
        """Initialize the AgentBuilder.
        
        Args:
            model: The LLM model instance to use for the agent
            name: Name of the agent
            description: Description of the agent
            instruction: Instructions for the agent
            sub_agents_registry_path: Optional path to sub-agents registry YAML file
            tools_registry_path: Optional path to tools registry YAML file
        """
        self.model = model
        self.name = name
        self.description = description
        self.instruction = instruction
        self.sub_agents_registry_path = sub_agents_registry_path
        self.tools_registry_path = tools_registry_path
    
    def build(self) -> Agent:
        """Build and return the agent with sub-agents and tools.
        
        Returns:
            Configured Agent instance
            
        Raises:
            Exception: If agent cannot be built
        """
        try:
            # Build sub-agents if registry path provided
            sub_agents = []
            if self.sub_agents_registry_path:
                sub_agents_builder = SubAgentsBuilder(self.sub_agents_registry_path)
                sub_agents = sub_agents_builder.build()
            
            # Build tools if registry path provided
            tools = []
            if self.tools_registry_path:
                tools_builder = ToolsBuilder(self.tools_registry_path)
                tools = tools_builder.build()
            
            # Construct the agent
            agent = Agent(
                model=self.model,
                name=self.name,
                description=self.description,
                instruction=self.instruction,
                tools=tools,
                sub_agents=sub_agents
            )
            
            logger.info(f"Successfully built agent '{self.name}' with {len(sub_agents)} sub-agent(s) and {len(tools)} tool(s)")
            return agent
            
        except Exception as e:
            logger.error("Failed to build agent: %s", e)
            raise
