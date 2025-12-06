"""Summarizing Agent Module - Provides content summarization capabilities."""

from .summarizing_agent import summarize_content, summarizing_agent
from .sub_agents.french_translator import french_translator_agent, translate_to_french

__all__ = [
    "summarize_content", 
    "summarizing_agent", 
    "french_translator_agent",
    "translate_to_french"
]
