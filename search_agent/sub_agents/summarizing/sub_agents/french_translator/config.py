import os
import configparser
from pathlib import Path
from typing import Optional


class FrenchTranslatorConfig:
    
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
        return self._get_value("model", "model_name", env_var="FRENCH_TRANSLATOR_MODEL_NAME")
    
    @property
    def api_key(self) -> str:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        return api_key
    
    @property
    def api_base(self) -> str:
        return self._get_value("model", "api_base", env_var="FRENCH_TRANSLATOR_API_BASE")
    
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
    def target_language(self) -> str:
        return self._get_value("translation", "target_language", env_var="TRANSLATION_TARGET_LANGUAGE")
    
    @property
    def preserve_formatting(self) -> bool:
        preserve_str = self._get_value("translation", "preserve_formatting", env_var="TRANSLATION_PRESERVE_FORMATTING")
        return preserve_str.lower() in ("true", "1", "yes")


_config: Optional[FrenchTranslatorConfig] = None


def get_french_translator_config() -> FrenchTranslatorConfig:
    global _config
    if _config is None:
        _config = FrenchTranslatorConfig()
    return _config
