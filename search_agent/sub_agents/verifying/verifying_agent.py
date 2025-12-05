"""Verifying Agent."""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_verifying_config

try:
    config = get_verifying_config()
except Exception as e:
    raise RuntimeError(f"Failed to load verifying configuration: {e}") from e

logger = logging.getLogger(__name__)

try:
    verifying_model = LiteLlm(
        model=config.model_name,
        api_key=config.api_key,
        api_base=config.api_base
    )
except Exception as e:
    logger.error("Failed to initialize verifying agent model: %s", e)
    raise

try:
    verifying_agent = Agent(
        model=verifying_model,
        name=config.agent_name,
        description=config.agent_description,
        instruction=config.agent_instruction,
        tools=[],
    )
except Exception as e:
    logger.error("Failed to initialize verifying agent: %s", e)
    raise


def analyze_sentiment(summary: str, original_content: str = "") -> Dict[str, str]:
    """Analyze the sentiment of summarized content."""
    
    try:
        if not summary or not summary.strip():
            return {
                "status": "error",
                "error": "No summary provided to analyze"
            }
        
        prompt = f"""Analyze the sentiment of the following summary and classify it as POSITIVE, NEUTRAL, or NEGATIVE.

Summary to analyze:
{summary}

Instructions:
- POSITIVE: Content expresses favorable, optimistic, or encouraging views
- NEUTRAL: Content is factual, balanced, or objective without strong emotional tone
- NEGATIVE: Content expresses unfavorable, critical, or pessimistic views

Respond with ONLY ONE WORD: POSITIVE, NEUTRAL, or NEGATIVE
"""
        
        response = verifying_agent.run(prompt).strip().upper()
        
        sentiment = "neutral"
        if "POSITIVE" in response:
            sentiment = "positive"
        elif "NEGATIVE" in response:
            sentiment = "negative"
        elif "NEUTRAL" in response:
            sentiment = "neutral"
        
        # Return sentiment analysis for all sentiment types
        final_content = f"{summary}\n\nSentiment Analysis: {sentiment.upper()}"
        return {
            "status": "success",
            "sentiment": sentiment,
            "content": final_content,
        }
        
    except Exception as e:
        logger.error("Error analyzing sentiment: %s", e)
        return {
            "status": "error",
            "error": f"An error occurred while analyzing sentiment: {str(e)}"
        }
