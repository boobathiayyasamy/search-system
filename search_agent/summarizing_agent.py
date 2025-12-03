"""Summarizing Agent - Provides content summarization capabilities.

This module implements a summarizing agent that can take content (typically from
Wikipedia searches) and format it into concise bullet points (3-5 bullets).
"""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_config, ConfigurationError


# Initialize configuration
try:
    config = get_config()
except ConfigurationError as e:
    raise RuntimeError(f"Failed to load configuration: {e}") from e


# Set up logging
logger = logging.getLogger(__name__)


# Initialize the LLM model for summarizing agent
try:
    logger.info("Initializing summarizing agent model")
    summarizing_model = LiteLlm(
        model=config.model_name,
        api_key=config.openrouter_api_key,
        api_base=config.api_base
    )
    logger.info("Summarizing agent model initialized successfully")
except Exception as e:
    logger.error("Failed to initialize summarizing agent model: %s", e)
    raise


# Initialize the summarizing agent (without tools, it will just use the LLM)
try:
    logger.info("Initializing summarizing agent")
    summarizing_agent = Agent(
        model=summarizing_model,
        name="summarizing_agent",
        description="An agent that summarizes content into 3-5 concise bullet points.",
        instruction="Take the provided content and create a clear, concise summary with 3-5 bullet points. Each bullet should capture a key piece of information. Use the '•' character for bullets. Provide ONLY the bullet points, nothing else.",
        tools=[],
    )
    logger.info("Summarizing agent initialized successfully")
except Exception as e:
    logger.error("Failed to initialize summarizing agent: %s", e)
    raise


def summarize_content(content: str) -> Dict[str, str]:
    """Summarize content into 3-5 concise bullet points.
    
    Args:
        content: The content to summarize (typically from Wikipedia search)
        
    Returns:
        Dictionary with status and either formatted bullets or error message
        
    Example:
        >>> result = summarize_content("Long Wikipedia article text...")
        >>> print(result['status'])
        'success'
        >>> print(result['summary'])
        '• Point 1\n• Point 2\n• Point 3'
    """
    logger.info("Summarizing content (length: %d characters)", len(content))
    
    try:
        if not content or not content.strip():
            logger.warning("Empty content provided for summarization")
            return {
                "status": "error",
                "error": "No content provided to summarize"
            }
        
        # Use the summarizing agent to generate bullet points
        prompt = f"""Please summarize the following content into 3-5 concise bullet points:

{content}"""
        
        response = summarizing_agent.run(prompt)
        
        logger.info("Successfully generated summary")
        return {
            "status": "success",
            "summary": response.strip()
        }
        
    except Exception as e:
        logger.error("Error summarizing content: %s", e)
        return {
            "status": "error",
            "error": f"An error occurred while summarizing: {str(e)}"
        }
