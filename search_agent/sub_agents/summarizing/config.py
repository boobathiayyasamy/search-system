"""Configuration management for the Summarizing sub-agent.

This module provides configuration management specific to the Summarizing agent,
using config.ini for non-sensitive data and environment variables for API keys.
"""

import os
import configparser
from pathlib import Path
from typing import Optional


class SummarizingConfig:
    """Configuration manager for the Summarizing sub-agent.
    
    Configuration priority (highest to lowest):
    1. Environment variables
    2. Configuration file (config.ini)
    3. Default values
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize Summarizing agent configuration.
        
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
        """LLM model name for Summarizing agent."""
        return self._get_value(
            "model",
            "model_name",
            env_var="SUMMARIZING_MODEL_NAME",
            default="openrouter/x-ai/grok-4.1-fast:free"
        )
    
    @property
    def api_key(self) -> str:
        """API key for Summarizing agent model.
        
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
        """API base URL for Summarizing agent model."""
        return self._get_value(
            "model",
            "api_base",
            env_var="SUMMARIZING_API_BASE",
            default="https://openrouter.ai/api/v1"
        )
    
    @property
    def agent_name(self) -> str:
        """Summarizing agent name."""
        return self._get_value(
            "agent",
            "name",
            default="summarizing_agent"
        )
    
    @property
    def agent_description(self) -> str:
        """Summarizing agent description."""
        return self._get_value(
            "agent",
            "description",
            default="An agent that summarizes content into 3-5 concise bullet points."
        )
    
    @property
    def agent_instruction(self) -> str:
        """Summarizing agent instruction."""
        return self._get_value(
            "agent",
            "instruction",
            default="Take the provided content and create a clear, concise summary with 3-5 bullet points. Each bullet should capture a key piece of information. Use the '•' character for bullets. Provide ONLY the bullet points, nothing else."
        )
    
    @property
    def min_bullet_points(self) -> int:
        """Minimum number of bullet points for summaries."""
        min_str = self._get_value(
            "summarizing",
            "min_bullet_points",
            env_var="SUMMARIZING_MIN_BULLETS",
            default="3"
        )
        return int(min_str)
    
    @property
    def max_bullet_points(self) -> int:
        """Maximum number of bullet points for summaries."""
        max_str = self._get_value(
            "summarizing",
            "max_bullet_points",
            env_var="SUMMARIZING_MAX_BULLETS",
            default="5"
        )
        return int(max_str)


# Global config instance
_config: Optional[SummarizingConfig] = None


def get_summarizing_config() -> SummarizingConfig:
    """Get the global Summarizing configuration instance.
    
    Returns:
        SummarizingConfig instance
    """
    global _config
    if _config is None:
        _config = SummarizingConfig()
    return _config
