"""Configuration management for the Wikipedia sub-agent.

This module provides configuration management specific to the Wikipedia agent,
using config.ini for non-sensitive data and environment variables for API keys.
"""

import os
import configparser
from pathlib import Path
from typing import Optional


class WikipediaConfig:
    """Configuration manager for the Wikipedia sub-agent.
    
    Configuration priority (highest to lowest):
    1. Environment variables
    2. Configuration file (config.ini)
    3. Default values
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize Wikipedia agent configuration.
        
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
        """LLM model name for Wikipedia agent."""
        return self._get_value(
            "model",
            "model_name",
            env_var="WIKIPEDIA_MODEL_NAME",
            default="openrouter/x-ai/grok-4.1-fast:free"
        )
    
    @property
    def api_key(self) -> str:
        """API key for Wikipedia agent model.
        
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
        """API base URL for Wikipedia agent model."""
        return self._get_value(
            "model",
            "api_base",
            env_var="WIKIPEDIA_API_BASE",
            default="https://openrouter.ai/api/v1"
        )
    
    @property
    def agent_name(self) -> str:
        """Wikipedia agent name."""
        return self._get_value(
            "agent",
            "name",
            default="wikipedia_agent"
        )
    
    @property
    def agent_description(self) -> str:
        """Wikipedia agent description."""
        return self._get_value(
            "agent",
            "description",
            default="An agent that searches Wikipedia to answer questions about various topics."
        )
    
    @property
    def agent_instruction(self) -> str:
        """Wikipedia agent instruction."""
        return self._get_value(
            "agent",
            "instruction",
            default="Search Wikipedia to find accurate and relevant information to answer user questions. Provide concise summaries from Wikipedia articles."
        )
    
    @property
    def wikipedia_sentences(self) -> int:
        """Number of sentences to retrieve from Wikipedia summaries."""
        sentences_str = self._get_value(
            "wikipedia",
            "sentences",
            env_var="WIKIPEDIA_SENTENCES",
            default="5"
        )
        return int(sentences_str)


# Global config instance
_config: Optional[WikipediaConfig] = None


def get_wikipedia_config() -> WikipediaConfig:
    """Get the global Wikipedia configuration instance.
    
    Returns:
        WikipediaConfig instance
    """
    global _config
    if _config is None:
        _config = WikipediaConfig()
    return _config
