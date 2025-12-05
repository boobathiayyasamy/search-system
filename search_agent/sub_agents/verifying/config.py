"""Configuration management for the Verifying sub-agent.

This module provides configuration management specific to the Verifying agent
for sentiment analysis functionality, using config.ini for non-sensitive data
and environment variables for API keys.
"""

import os
import configparser
from pathlib import Path
from typing import Optional


class VerifyingConfig:
    """Configuration manager for the Verifying sub-agent.
    
    Configuration priority (highest to lowest):
    1. Environment variables
    2. Configuration file (config.ini)
    3. Default values
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize Verifying agent configuration.
        
        Args:
            config_file: Path to config.ini file. If None, looks for config.ini
                        in the same directory as this module.
        """
        # Set up config parser
        self.config = configparser.ConfigParser()
        
        # Determine config file path
        if config_file is None:
            config_file = Path(__file__).parent / "config.ini"
        
        self.config_file = Path(config_file)
        
        # Load config file if it exists
        if self.config_file.exists():
            self.config.read(self.config_file)
    
    def _get_value(
        self,
        section: str,
        key: str,
        env_var: Optional[str] = None,
        default: Optional[str] = None
    ) -> str:
        """Get configuration value with fallback chain.
        
        Args:
            section: Config file section name
            key: Config file key name
            env_var: Environment variable name to check first
            default: Default value if not found elsewhere
            
        Returns:
            Configuration value
        """
        # Priority 1: Environment variable
        if env_var:
            value = os.environ.get(env_var)
            if value:
                return value
        
        # Priority 2: Config file
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        
        # Priority 3: Default value
        if default is not None:
            return default
        
        # Return empty string if nothing found
        return ""
    
    @property
    def model_name(self) -> str:
        """LLM model name for Verifying agent."""
        return self._get_value(
            "model",
            "model_name",
            env_var="VERIFYING_MODEL_NAME",
            default="openrouter/google/gemini-2.0-flash-001"
        )
    
    @property
    def api_key(self) -> str:
        """API key for Verifying agent model.
        
        Raises:
            ValueError: If API key is not found in environment variables
        """
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable is required"
            )
        return api_key
    
    @property
    def api_base(self) -> str:
        """API base URL for Verifying agent model."""
        return self._get_value(
            "model",
            "api_base",
            env_var="VERIFYING_API_BASE",
            default="https://openrouter.ai/api/v1"
        )
    
    @property
    def agent_name(self) -> str:
        """Verifying agent name."""
        return self._get_value(
            "agent",
            "name",
            default="verifying_agent"
        )
    
    @property
    def agent_description(self) -> str:
        """Verifying agent description."""
        return self._get_value(
            "agent",
            "description",
            default="An agent that analyzes sentiment of summarized content and ensures positive or neutral tone."
        )
    
    @property
    def agent_instruction(self) -> str:
        """Verifying agent instruction."""
        return self._get_value(
            "agent",
            "instruction",
            default="Analyze the sentiment of the provided summary and classify it as POSITIVE, NEUTRAL, or NEGATIVE."
        )
    
    @property
    def confidence_threshold(self) -> float:
        """Confidence threshold for sentiment classification (0.0-1.0)."""
        threshold_str = self._get_value(
            "sentiment",
            "confidence_threshold",
            env_var="SENTIMENT_CONFIDENCE_THRESHOLD",
            default="0.7"
        )
        return float(threshold_str)


# Global config instance
_config: Optional[VerifyingConfig] = None


def get_verifying_config() -> VerifyingConfig:
    """Get the global Verifying configuration instance.
    
    Returns:
        VerifyingConfig instance
    """
    global _config
    if _config is None:
        _config = VerifyingConfig()
    return _config
