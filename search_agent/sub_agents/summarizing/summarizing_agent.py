"""Summarizing Agent - Provides content summarization capabilities.
"""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_summarizing_config


# Initialize configuration
try:
    config = get_summarizing_config()
except Exception as e:
    raise RuntimeError(f"Failed to load summarizing configuration: {e}") from e


# Set up logging
logger = logging.getLogger(__name__)


# Initialize the LLM model for summarizing agent
try:
    logger.info("Initializing summarizing agent model")
    summarizing_model = LiteLlm(
        model=config.model_name,
        api_key=config.api_key,
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
        name=config.agent_name,
        description=config.agent_description,
        instruction=config.agent_instruction,
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


def regenerate_with_positive_tone(summary: str, original_content: str = "") -> Dict[str, str]:
    """Regenerate summary with positive or neutral tone.
    
    This function takes a summary with negative sentiment and regenerates it
    to have a positive or neutral tone while maintaining factual accuracy.
    
    Args:
        summary: The negative sentiment summary to regenerate
        original_content: Optional original content for additional context
        
    Returns:
        Dictionary with status and regenerated summary or error message
        
    Example:
        >>> summary = "• Python is a terrible language\\n• It has poor performance"
        >>> result = regenerate_with_positive_tone(summary)
        >>> print(result['status'])
        'success'
        >>> print(result['summary'])
        '• Python is a versatile programming language\\n• It prioritizes readability...'
    """
    logger.info("Regenerating summary with positive/neutral tone (length: %d characters)", len(summary))
    
    try:
        if not summary or not summary.strip():
            logger.warning("Empty summary provided for regeneration")
            return {
                "status": "error",
                "error": "No summary provided to regenerate"
            }
        
        # Build regeneration prompt
        prompt = f"""The following summary has negative sentiment. Please rewrite it to have a POSITIVE or NEUTRAL tone while maintaining factual accuracy.

Original summary:
{summary}
"""
        
        if original_content:
            prompt += f"""\nOriginal content for context:
{original_content[:500]}...
"""
        
        prompt += """
Requirements:
1. Rewrite into 3-5 concise bullet points
2. Use positive or neutral language
3. Maintain factual accuracy
4. Keep the same general topics/themes
5. Avoid negative, critical, or pessimistic phrasing

Provide ONLY the regenerated bullet points, no explanations.
"""
        
        # Use the summarizing agent to regenerate with positive tone
        response = summarizing_agent.run(prompt)
        
        logger.info("Successfully regenerated summary with positive/neutral tone")
        return {
            "status": "success",
            "summary": response.strip()
        }
        
    except Exception as e:
        logger.error("Error regenerating summary: %s", e)
        return {
            "status": "error",
            "error": f"An error occurred while regenerating: {str(e)}"
        }

