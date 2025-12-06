"""Root Agent Builder."""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from .sub_agents_builder import build_sub_agents

logger = logging.getLogger(__name__)


def build_root_agent(model, config, tool):
    """Build and return the root agent."""
    try:
        sub_agents = build_sub_agents()
        root_agent = Agent(
            model=model,
            name=config.agent_name,
            description=config.agent_description,
            instruction=config.agent_instruction,
            tools=[tool],
            sub_agents=sub_agents
        )
        return root_agent
    except Exception as e:
        logger.error("Failed to initialize agent: %s", e)
        raise
