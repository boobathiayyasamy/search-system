import os
import configparser
from pathlib import Path
from typing import Optional


class SummarizingConfig:
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = configparser.ConfigParser()
        
        if config_file is None:
            config_file = Path(__file__).parent / "config.ini"
        
        self.config_file = Path(config_file)
        
        if self.config_file.exists():
            self.config.read(self.config_file)
    
    def _get_value(
        self,
        section: str,
        key: str,
        env_var: Optional[str] = None
    ) -> str:
        if env_var:
            value = os.environ.get(env_var)
            if value:
                return value
        
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        
        return ""
    
    @property
    def model_name(self) -> str:
        return self._get_value("model", "model_name", env_var="SUMMARIZING_MODEL_NAME")
    
    @property
    def api_key(self) -> str:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        return api_key
    
    @property
    def api_base(self) -> str:
        return self._get_value("model", "api_base", env_var="SUMMARIZING_API_BASE")
    
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
    def min_bullet_points(self) -> int:
        min_str = self._get_value("summarizing", "min_bullet_points", env_var="SUMMARIZING_MIN_BULLETS")
        return int(min_str)
    
    @property
    def max_bullet_points(self) -> int:
        max_str = self._get_value("summarizing", "max_bullet_points", env_var="SUMMARIZING_MAX_BULLETS")
        return int(max_str)


_config: Optional[SummarizingConfig] = None


def get_summarizing_config() -> SummarizingConfig:
    global _config
    if _config is None:
        _config = SummarizingConfig()
    return _config
