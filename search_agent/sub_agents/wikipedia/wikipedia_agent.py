"""Wikipedia Search Agent."""

import logging

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_wikipedia_config


# Set up logging
logger = logging.getLogger(__name__)


# Initialize the LLM model for Wikipedia agent
try:
    wiki_config = get_wikipedia_config()
    wikipedia_model = LiteLlm(
        model=wiki_config.model_name,
        api_key=wiki_config.api_key,
        api_base=wiki_config.api_base
    )
except Exception as e:
    logger.error("Failed to initialize Wikipedia agent model: %s", e)
    raise


# Initialize the Wikipedia agent
try:
    wikipedia_agent = Agent(
        model=wikipedia_model,
        name=wiki_config.agent_name,
        description=wiki_config.agent_description,
        instruction=wiki_config.agent_instruction,
    )
except Exception as e:
    logger.error("Failed to initialize Wikipedia agent: %s", e)
    raise
