"""Wikipedia Search Tool."""

import logging
from typing import Dict

import wikipedia


# Set up logging
logger = logging.getLogger(__name__)


def search_wikipedia(query: str) -> Dict[str, str]:
    """Search Wikipedia for information about a topic."""
    
    try:
        # Search Wikipedia for the query
        # Set sentences=3 to get a concise summary
        summary = wikipedia.summary(query, sentences=5, auto_suggest=True)
        
        return {
            "status": "success",
            "query": query,
            "content": summary
        }
        
    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple articles match the query
        options = e.options[:5]  # Limit to first 5 options
        return {
            "status": "disambiguation",
            "query": query,
            "error": f"Multiple articles found. Please be more specific. Options: {', '.join(options)}"
        }
        
    except wikipedia.exceptions.PageError:
        # No article found
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
