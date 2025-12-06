"""Summarizing Agent."""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_summarizing_config

try:
    config = get_summarizing_config()
except Exception as e:
    raise RuntimeError(f"Failed to load summarizing configuration: {e}") from e

logger = logging.getLogger(__name__)

try:
    summarizing_model = LiteLlm(
        model=config.model_name,
        api_key=config.api_key,
        api_base=config.api_base
    )
except Exception as e:
    logger.error("Failed to initialize summarizing agent model: %s", e)
    raise

# Import the french translator function as a tool
# Note: This import must happen after the config is loaded
from .sub_agents.french_translator import french_translator_agent

try:
    summarizing_agent = Agent(
        model=summarizing_model,
        name=config.agent_name,
        description=config.agent_description,
        instruction=config.agent_instruction,
        sub_agents=[french_translator_agent]
    )
except Exception as e:
    logger.error("Failed to initialize summarizing agent: %s", e)
    raise



def summarize_content(content: str) -> Dict[str, str]:
    """Summarize content into 3-5 concise bullet points."""
    
    try:
        if not content or not content.strip():
            return {
                "status": "error",
                "error": "No content provided to summarize"
            }
        
        prompt = f"""Please summarize the following content into 3-5 concise bullet points:

{content}"""
        
        response = summarizing_agent.run(prompt)
        
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

