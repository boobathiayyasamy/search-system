"""Verifying Agent - Provides sentiment analysis capabilities for summarized content.
"""

import logging
from typing import Dict

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_verifying_config


# Initialize configuration
try:
    config = get_verifying_config()
except Exception as e:
    raise RuntimeError(f"Failed to load verifying configuration: {e}") from e


# Set up logging
logger = logging.getLogger(__name__)


# Initialize the LLM model for verifying agent
try:
    logger.info("Initializing verifying agent model")
    verifying_model = LiteLlm(
        model=config.model_name,
        api_key=config.api_key,
        api_base=config.api_base
    )
    logger.info("Verifying agent model initialized successfully")
except Exception as e:
    logger.error("Failed to initialize verifying agent model: %s", e)
    raise


# Initialize the verifying agent without tools (sentiment analysis uses only LLM)
try:
    logger.info("Initializing verifying agent")
    verifying_agent = Agent(
        model=verifying_model,
        name=config.agent_name,
        description=config.agent_description,
        instruction=config.agent_instruction,
        tools=[],
    )
    logger.info("Verifying agent initialized successfully")
except Exception as e:
    logger.error("Failed to initialize verifying agent: %s", e)
    raise


def analyze_sentiment(summary: str, original_content: str = "") -> Dict[str, str]:
    """Analyze the sentiment of summarized content.
    
    This function analyzes the sentiment of a summary and classifies it as
    positive, neutral, or negative. If the sentiment is negative, it triggers
    the summarizing agent to regenerate the content with a positive or neutral tone.
    
    Args:
        summary: The summary to analyze (typically bullet points)
        original_content: Optional original content for context in regeneration
        
    Returns:
        Dictionary with status, sentiment classification, and final content
        Keys:
        - status: 'success' or 'error'
        - sentiment: 'positive', 'neutral', or 'negative'
        - content: The final content (original if positive/neutral, regenerated if negative)
        - regenerated: Boolean indicating if content was regenerated
        
    Example:
        >>> summary = "• Python is a terrible language\\n• It has poor performance"
        >>> result = analyze_sentiment(summary, "original content...")
        >>> print(result['sentiment'])
        'negative'
        >>> print(result['regenerated'])
        True
    """
    logger.info("Analyzing sentiment of summary (length: %d characters)", len(summary))
    
    try:
        if not summary or not summary.strip():
            logger.warning("Empty summary provided for sentiment analysis")
            return {
                "status": "error",
                "error": "No summary provided to analyze"
            }
        
        # Build sentiment analysis prompt
        prompt = f"""Analyze the sentiment of the following summary and classify it as POSITIVE, NEUTRAL, or NEGATIVE.

Summary to analyze:
{summary}

Instructions:
- POSITIVE: Content expresses favorable, optimistic, or encouraging views
- NEUTRAL: Content is factual, balanced, or objective without strong emotional tone
- NEGATIVE: Content expresses unfavorable, critical, or pessimistic views

Respond with ONLY ONE WORD: POSITIVE, NEUTRAL, or NEGATIVE
"""
        
        # Use the verifying agent to analyze sentiment
        response = verifying_agent.run(prompt).strip().upper()
        
        # Extract sentiment from response (handle cases where LLM adds extra text)
        sentiment = "neutral"  # default
        if "POSITIVE" in response:
            sentiment = "positive"
        elif "NEGATIVE" in response:
            sentiment = "negative"
        elif "NEUTRAL" in response:
            sentiment = "neutral"
        
        logger.info("Detected sentiment: %s", sentiment)
        
        # If sentiment is positive or neutral, return original content with sentiment info
        if sentiment in ["positive", "neutral"]:
            logger.info("Sentiment is %s, returning original content", sentiment)
            final_content = f"{summary}\n\nSentiment Analysis: {sentiment.upper()}"
            return {
                "status": "success",
                "sentiment": sentiment,
                "content": final_content,
                "regenerated": False
            }
        
        # If sentiment is negative, trigger regeneration
        logger.info("Sentiment is negative, triggering regeneration")
        
        # Import summarizing agent here to avoid circular dependency
        try:
            from ..summarizing.summarizing_agent import regenerate_with_positive_tone
        except ImportError as e:
            logger.error("Failed to import regenerate_with_positive_tone: %s", e)
            return {
                "status": "error",
                "error": "Failed to trigger regeneration: summarizing agent not available"
            }
        
        # Call summarizing agent to regenerate with positive/neutral tone
        regeneration_result = regenerate_with_positive_tone(summary, original_content)
        
        if regeneration_result["status"] == "error":
            logger.error("Regeneration failed: %s", regeneration_result.get("error"))
            return {
                "status": "error",
                "error": f"Regeneration failed: {regeneration_result.get('error')}"
            }
        
        logger.info("Successfully regenerated content with positive/neutral tone")
        final_content = f"{regeneration_result['summary']}\n\nSentiment Analysis: NEGATIVE (Regenerated to NEUTRAL/POSITIVE)"
        return {
            "status": "success",
            "sentiment": "negative",
            "content": final_content,
            "regenerated": True,
            "original_content": summary
        }
        
    except Exception as e:
        logger.error("Error analyzing sentiment: %s", e)
        return {
            "status": "error",
            "error": f"An error occurred while analyzing sentiment: {str(e)}"
        }
