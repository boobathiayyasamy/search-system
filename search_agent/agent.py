"""Search Agent - A helpful assistant."""

from .config import get_config, ConfigurationError
from utils import setup_logging

try:
    config = get_config()
except ConfigurationError as e:
    raise RuntimeError(f"Failed to load configuration: {e}") from e

logger = setup_logging(config)

from pathlib import Path
from google.adk.models.lite_llm import LiteLlm
from custom_adk_builder import AgentBuilder

try:
    model = LiteLlm(
        model=config.model_name,
        api_key=config.openrouter_api_key,
        api_base=config.api_base
    )
except Exception as e:
    logger.error("Failed to initialize LLM model: %s", e)
    raise

search_agent_dir = Path(__file__).parent
registry_path = search_agent_dir / config.registry_path

agent_builder = AgentBuilder(
    model=model,
    name=config.agent_name,
    description=config.agent_description,
    instruction=config.agent_instruction,
    registry_path=str(registry_path)
)

root_agent = agent_builder.build()


