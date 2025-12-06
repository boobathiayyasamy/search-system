import os
import configparser
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class ConfigurationError(Exception):
    pass


class Config:
    
    def __init__(self, config_file: Optional[str] = None):
        env_path = Path(__file__).parent / ".env"
        load_dotenv(dotenv_path=env_path)
        
        self.config = configparser.RawConfigParser()
        
        if config_file is None:
            config_file = Path(__file__).parent / "config.ini"
        
        self.config_file = Path(config_file)
        
        if self.config_file.exists():
            self.config.read(self.config_file)
    
    def _get_value(
        self, 
        section: str, 
        key: str, 
        env_var: Optional[str] = None,
        required: bool = False
    ) -> Optional[str]:
        if env_var:
            value = os.environ.get(env_var)
            if value:
                return value
        
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        
        if required:
            raise ConfigurationError(
                f"Required configuration not found: {section}.{key}"
                + (f" (or env var {env_var})" if env_var else "")
            )
        
        return None
    
    @property
    def openrouter_api_key(self) -> str:
        value = self._get_value("api", "openrouter_api_key", env_var="OPENROUTER_API_KEY", required=True)
        return value
    
    @property
    def api_base(self) -> str:
        return self._get_value("api", "api_base", env_var="OPENROUTER_API_BASE")
    
    @property
    def model_name(self) -> str:
        return self._get_value("api", "model_name", env_var="MODEL_NAME")
    
    @property
    def agent_name(self) -> str:
        return self._get_value("agent", "name")
    
    @property
    def agent_description(self) -> str:
        return self._get_value("agent", "description")
    
    @property
    def agent_instruction(self) -> str:
        return self._get_value("agent", "instruction")
    
    @property
    def log_level(self) -> str:
        return self._get_value("logging", "level", env_var="LOG_LEVEL").upper()
    
    @property
    def log_format(self) -> str:
        return self._get_value("logging", "format")
    
    @property
    def log_date_format(self) -> str:
        return self._get_value("logging", "date_format")
    
    @property
    def registry_path(self) -> str:
        return self._get_value("registry", "registry_path")





_config: Optional[Config] = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config
