"""Root Agent Builder - Builds the root search agent.

This module contains the builder function for creating the root agent.
"""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

logger = logging.getLogger(__name__)


def build_root_agent(model, config, mcp_toolset, sub_agents):
    """Build and return the root agent.
    
    Args:
        model: The LLM model instance
        config: Configuration object with agent settings
        mcp_toolset: MCP toolset for the agent
        sub_agents: List of sub-agents to include
        
    Returns:
        Agent: The initialized root agent
        
    Raises:
        Exception: If agent initialization fails
    """
    try:
        logger.info("Initializing agent: %s", config.agent_name)
        root_agent = Agent(
            model=model,
            name=config.agent_name,
            description=config.agent_description,
            instruction=config.agent_instruction,
            tools=[mcp_toolset],
            sub_agents=sub_agents
        )
        logger.info("Agent '%s' initialized successfully", config.agent_name)
        return root_agent
    except Exception as e:
        logger.error("Failed to initialize agent: %s", e)
        raise
