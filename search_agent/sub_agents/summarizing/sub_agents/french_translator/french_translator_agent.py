"""French Translator Agent."""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_french_translator_config

try:
    config = get_french_translator_config()
except Exception as e:
    raise RuntimeError(f"Failed to load French translator configuration: {e}") from e

logger = logging.getLogger(__name__)

try:
    french_translator_model = LiteLlm(
        model=config.model_name,
        api_key=config.api_key,
        api_base=config.api_base
    )
except Exception as e:
    logger.error("Failed to initialize French translator agent model: %s", e)
    raise

try:
    french_translator_agent = Agent(
        model=french_translator_model,
        name=config.agent_name,
        description=config.agent_description,
        instruction=config.agent_instruction,
        tools=[],
    )
except Exception as e:
    logger.error("Failed to initialize French translator agent: %s", e)
    raise


def translate_to_french(content: str) -> Dict[str, str]:
    """Translate content to French using the French translator agent.
    
    Args:
        content: The content to translate to French
        
    Returns:
        A dictionary with status and translation (or error message)
    """
    
    try:
        if not content or not content.strip():
            return {
                "status": "error",
                "error": "No content provided to translate"
            }
        
        prompt = f"""Please translate the following content to French. Maintain the original formatting and structure.

Content to translate:
{content}

Provide ONLY the French translation, no explanations or additional text."""
        
        response = french_translator_agent.run(prompt)
        
        return {
            "status": "success",
            "translation": response.strip()
        }
        
    except Exception as e:
        logger.error("Error translating to French: %s", e)
        return {
            "status": "error",
            "error": f"An error occurred while translating: {str(e)}"
        }
