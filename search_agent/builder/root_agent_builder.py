"""Root Agent Builder."""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

logger = logging.getLogger(__name__)


def build_root_agent(model, config, mcp_toolset, sub_agents):
    """Build and return the root agent."""
    try:
        root_agent = Agent(
            model=model,
            name=config.agent_name,
            description=config.agent_description,
            instruction=config.agent_instruction,
            tools=[mcp_toolset],
            sub_agents=sub_agents
        )
        return root_agent
    except Exception as e:
        logger.error("Failed to initialize agent: %s", e)
        raise
