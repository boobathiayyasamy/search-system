"""Search Agent - A helpful assistant.

This module initializes the search agent with proper.
"""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_config, ConfigurationError
from .sub_agents import wikipedia_agent, summarizing_agent
from .tools.mcp import create_mcp_toolset
from builder.root_agent_builder import build_root_agent


# ... (existing imports)

# Initialize configuration
try:
    config = get_config()
except ConfigurationError as e:
    raise RuntimeError(f"Failed to load configuration: {e}") from e


# Set up logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format=config.log_format,
    datefmt=config.log_date_format
)
logger = logging.getLogger(__name__)


# Initialize the LLM model
try:
    logger.info("Initializing LLM model: %s", config.model_name)
    logger.debug("api_base: %s", config.api_base)
    
    model = LiteLlm(
        model=config.model_name,
        api_key=config.openrouter_api_key,
        api_base=config.api_base
    )
    logger.info("LLM model initialized successfully")
except Exception as e:
    logger.error("Failed to initialize LLM model: %s", e)
    raise


# Initialize MCP Toolset
try:
    mcp_toolset = create_mcp_toolset()
    logger.info("MCP toolset initialized successfully")
except Exception as e:
    logger.error("Failed to initialize MCP toolset: %s", e)
    # We might want to continue without MCP or raise, depending on requirements.
    # For now, let's raise as it seems critical for this task.
    raise


# Initialize the root agent using builder
root_agent = build_root_agent(
    model=model,
    config=config,
    mcp_toolset=mcp_toolset,
    sub_agents=[wikipedia_agent, summarizing_agent]
)

