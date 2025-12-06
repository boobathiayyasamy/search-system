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
from .builder.root_agent_builder import build_root_agent

try:
    model = LiteLlm(
        model=config.model_name,
        api_key=config.openrouter_api_key,
        api_base=config.api_base
    )
except Exception as e:
    logger.error("Failed to initialize LLM model: %s", e)
    raise

root_agent = build_root_agent(
    model=model,
    config=config
)

