"""Verifying sub-agent package.

This package provides the verifying agent which uses Google search
to verify the accuracy of summarized content.
"""

from .verifying_agent import verifying_agent, analyze_sentiment

__all__ = ["verifying_agent", "analyze_sentiment"]
