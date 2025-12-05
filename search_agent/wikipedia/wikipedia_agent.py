"""Wikipedia Search Agent - Provides Wikipedia search capabilities.
"""

import logging
from typing import Dict

import wikipedia
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from ..config import get_config, ConfigurationError


# Initialize configuration
try:
    config = get_config()
except ConfigurationError as e:
    raise RuntimeError(f"Failed to load configuration: {e}") from e


# Set up logging
logger = logging.getLogger(__name__)


def search_wikipedia(query: str) -> Dict[str, str]:
    """Search Wikipedia for information about a topic.
    
    Args:
        query: The search query or topic to look up on Wikipedia
        
    Returns:
        Dictionary with status and either content (summary) or error message
        
    Example:
        >>> result = search_wikipedia("Python programming")
        >>> print(result['status'])
        'success'
    """
    logger.info("Searching Wikipedia for: %s", query)
    
    try:
        # Search Wikipedia for the query
        # Set sentences=3 to get a concise summary
        summary = wikipedia.summary(query, sentences=5, auto_suggest=True)
        
        logger.info("Successfully retrieved Wikipedia summary for: %s", query)
        return {
            "status": "success",
            "query": query,
            "content": summary
        }
        
    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple articles match the query
        logger.warning("Disambiguation needed for query '%s': %s", query, e.options[:5])
        options = e.options[:5]  # Limit to first 5 options
        return {
            "status": "disambiguation",
            "query": query,
            "error": f"Multiple articles found. Please be more specific. Options: {', '.join(options)}"
        }
        
    except wikipedia.exceptions.PageError:
        # No article found
        logger.warning("No Wikipedia page found for query: %s", query)
        return {
            "status": "not_found",
            "query": query,
            "error": f"No Wikipedia article found for '{query}'. Please try a different search term."
        }
        
    except Exception as e:
        # Other errors
        logger.error("Error searching Wikipedia for '%s': %s", query, e)
        return {
            "status": "error",
            "query": query,
            "error": f"An error occurred while searching Wikipedia: {str(e)}"
        }


# Initialize the LLM model for Wikipedia agent
try:
    logger.info("Initializing Wikipedia agent model")
    wikipedia_model = LiteLlm(
        model=config.model_name,
        api_key=config.openrouter_api_key,
        api_base=config.api_base
    )
    logger.info("Wikipedia agent model initialized successfully")
except Exception as e:
    logger.error("Failed to initialize Wikipedia agent model: %s", e)
    raise


# Initialize the Wikipedia agent
try:
    logger.info("Initializing Wikipedia agent")
    wikipedia_agent = Agent(
        model=wikipedia_model,
        name="wikipedia_agent",
        description="An agent that searches Wikipedia to answer questions about various topics.",
        instruction="Search Wikipedia to find accurate and relevant information to answer user questions. Provide concise summaries from Wikipedia articles.",
        tools=[search_wikipedia],
    )
    logger.info("Wikipedia agent initialized successfully")
except Exception as e:
    logger.error("Failed to initialize Wikipedia agent: %s", e)
    raise
