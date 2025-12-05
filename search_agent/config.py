"""Configuration management for the search agent."""

import os
import configparser
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing required values."""
    pass


class Config:
    """Configuration manager for the search agent."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration."""
        # Load environment variables from .env file in the same directory as this module
        env_path = Path(__file__).parent / ".env"
        load_dotenv(dotenv_path=env_path)
        
        # Set up config parser (use RawConfigParser to avoid interpolation issues)
        self.config = configparser.RawConfigParser()
        
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
        default: Optional[str] = None,
        required: bool = False
    ) -> Optional[str]:
        """Get configuration value with fallback chain."""
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
        
        # If required and not found, raise error
        if required:
            raise ConfigurationError(
                f"Required configuration not found: {section}.{key}"
                + (f" (or env var {env_var})" if env_var else "")
            )
        
        return None
    
    @property
    def openrouter_api_key(self) -> str:
        """OpenRouter API key."""
        value = self._get_value(
            "api", 
            "openrouter_api_key",
            env_var="OPENROUTER_API_KEY",
            required=True
        )
        return value
    
    @property
    def api_base(self) -> str:
        """API base URL."""
        return self._get_value(
            "api",
            "api_base",
            env_var="OPENROUTER_API_BASE",
            default="https://openrouter.ai/api/v1"
        )
    
    @property
    def model_name(self) -> str:
        """LLM model name."""
        return self._get_value(
            "api",
            "model_name",
            env_var="MODEL_NAME",
            default="openrouter/x-ai/grok-4.1-fast:free"
        )
    
    @property
    def agent_name(self) -> str:
        """Agent name."""
        return self._get_value(
            "agent",
            "name",
            default="search_agent"
        )
    
    @property
    def agent_description(self) -> str:
        """Agent description."""
        return self._get_value(
            "agent",
            "description",
            default="A helpful assistant for user questions."
        )
    
    @property
    def agent_instruction(self) -> str:
        """Agent instruction."""
        return self._get_value(
            "agent",
            "instruction",
            default="Answer user questions to the best of your knowledge"
        )
    
    @property
    def log_level(self) -> str:
        """Logging level."""
        return self._get_value(
            "logging",
            "level",
            env_var="LOG_LEVEL",
            default="INFO"
        ).upper()
    
    @property
    def log_format(self) -> str:
        """Logging format string."""
        return self._get_value(
            "logging",
            "format",
            default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    @property
    def log_date_format(self) -> str:
        """Logging date format string."""
        return self._get_value(
            "logging",
            "date_format",
            default="%Y-%m-%d %H:%M:%S"
        )


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance.
    
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
