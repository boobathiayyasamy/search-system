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
        
        prompt = f"""Analyze the sentiment of the following summary and provide a single sentence response that describes the sentiment.

Summary to analyze:
{summary}

Instructions:
- If POSITIVE: Explain why the content expresses favorable, optimistic, or encouraging views
- If NEUTRAL: Explain why the content is factual, balanced, or objective without strong emotional tone
- If NEGATIVE: Explain why the content expresses unfavorable, critical, or pessimistic views

Provide a single, concise sentence that describes the sentiment of the summary with proper context.
Example responses:
- "This summary conveys a positive sentiment as it highlights successful achievements and optimistic outcomes."
- "The summary maintains a neutral tone by presenting factual information without emotional bias."
- "This content reflects a negative sentiment due to its focus on challenges and unfavorable circumstances."

Your response:
"""
        
        response = verifying_agent.run(prompt).strip()
        
        # Extract sentiment classification from the response
        response_lower = response.lower()
        sentiment = "neutral"
        if "positive" in response_lower:
            sentiment = "positive"
        elif "negative" in response_lower:
            sentiment = "negative"
        
        # Return sentiment analysis with the full sentence response
        final_content = f"{summary}\n\nSentiment Analysis: {response}"
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
