import logging
from typing import Any, List

from google.adk.agents.llm_agent import Agent
from .sub_agents_builder import SubAgentsBuilder
from .tools_builder import ToolsBuilder

logger = logging.getLogger(__name__)


class AgentBuilder:
    
    def __init__(self, model: Any, name: str, description: str, instruction: str,
                 registry_path: str = None):
        self.model = model
        self.name = name
        self.description = description
        self.instruction = instruction
        self.registry_path = registry_path
    
    def build(self) -> Agent:
        try:
            sub_agents = []
            if self.registry_path:
                sub_agents_builder = SubAgentsBuilder(self.registry_path)
                sub_agents = sub_agents_builder.build()
            
            tools = []
            if self.registry_path:
                tools_builder = ToolsBuilder(self.registry_path)
                tools = tools_builder.build()
            
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
