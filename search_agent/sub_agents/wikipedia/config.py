import os
import configparser
from pathlib import Path
from typing import Optional


class WikipediaConfig:
    
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
        return self._get_value("model", "model_name", env_var="WIKIPEDIA_MODEL_NAME")
    
    @property
    def api_key(self) -> str:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        return api_key
    
    @property
    def api_base(self) -> str:
        return self._get_value("model", "api_base", env_var="WIKIPEDIA_API_BASE")
    
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
    def wikipedia_sentences(self) -> int:
        sentences_str = self._get_value("wikipedia", "sentences", env_var="WIKIPEDIA_SENTENCES")
        return int(sentences_str)


_config: Optional[WikipediaConfig] = None


def get_wikipedia_config() -> WikipediaConfig:
    global _config
    if _config is None:
        _config = WikipediaConfig()
    return _config
