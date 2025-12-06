"""Root Agent Builder."""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from .sub_agents_builder import build_sub_agents
from .root_tools_builder import build_root_tools

logger = logging.getLogger(__name__)


def build_root_agent(model, config):
    """Build and return the root agent."""
    try:
        sub_agents = build_sub_agents()
        tools = build_root_tools()
        root_agent = Agent(
            model=model,
            name=config.agent_name,
            description=config.agent_description,
            instruction=config.agent_instruction,
            tools=tools,
            sub_agents=sub_agents
        )
        return root_agent
    except Exception as e:
        logger.error("Failed to initialize agent: %s", e)
        raise
