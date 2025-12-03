"""Search Agent - A helpful assistant powered by LLM.

This module initializes and configures the search agent with proper
configuration management and logging.
"""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_config, ConfigurationError
from .wikipedia_agent import search_wikipedia
from .summarizing_agent import summarize_content



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
    model = LiteLlm(
        model=config.model_name,
        api_key=config.openrouter_api_key,
        api_base=config.api_base
    )
    logger.info("LLM model initialized successfully")
except Exception as e:
    logger.error("Failed to initialize LLM model: %s", e)
    raise


def get_current_time(city: str) -> Dict[str, str]:
    """Returns the current time in a specified city.
    
    Args:
        city: Name of the city to get the time for
        
    Returns:
        Dictionary with status, city, and time information
        
    Note:
        This is a placeholder implementation. In production, this should
        integrate with a real time API or library.
    """
    logger.debug("Getting current time for city: %s", city)
    # TODO: Implement actual time lookup functionality
    result = {"status": "success", "city": city, "time": "10:30 AM"}
    logger.debug("Time lookup result: %s", result)
    return result


# Initialize the root agent
try:
    logger.info("Initializing agent: %s", config.agent_name)
    root_agent = Agent(
        model=model,
        name=config.agent_name,
        description=config.agent_description,
        instruction=config.agent_instruction,
        tools=[get_current_time, search_wikipedia, summarize_content],
    )
    logger.info("Agent '%s' initialized successfully", config.agent_name)
except Exception as e:
    logger.error("Failed to initialize agent: %s", e)
    raise

