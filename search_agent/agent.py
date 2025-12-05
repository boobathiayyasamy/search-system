"""Search Agent - A helpful assistant."""

from .config import get_config, ConfigurationError
from .utils import setup_logging

try:
    config = get_config()
except ConfigurationError as e:
    raise RuntimeError(f"Failed to load configuration: {e}") from e

logger = setup_logging(config)

from typing import Dict
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools.mcp import create_mcp_toolset
from .builder.root_agent_builder import build_root_agent
from .builder.sub_agents_builder import build_sub_agents

try:
    model = LiteLlm(
        model=config.model_name,
        api_key=config.openrouter_api_key,
        api_base=config.api_base
    )
except Exception as e:
    logger.error("Failed to initialize LLM model: %s", e)
    raise

try:
    mcp_toolset = create_mcp_toolset()
except Exception as e:
    logger.error("Failed to initialize MCP toolset: %s", e)
    raise

root_agent = build_root_agent(
    model=model,
    config=config,
    mcp_toolset=mcp_toolset,
    sub_agents=build_sub_agents()
)

