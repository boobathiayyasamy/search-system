"""Search Agent - A helpful assistant.

This module initializes the search agent with proper.
"""

import logging
from pathlib import Path
from datetime import datetime
from .config import get_config, ConfigurationError

# Initialize configuration FIRST
try:
    config = get_config()
except ConfigurationError as e:
    raise RuntimeError(f"Failed to load configuration: {e}") from e


# Set up logging IMMEDIATELY after config, BEFORE other imports
# Create logs directory if it doesn't exist
logs_dir = Path(__file__).parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Create log filename with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = logs_dir / f"search_agent_{timestamp}.log"

# Configure logging with file handler
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format=config.log_format,
    datefmt=config.log_date_format,
    force=True,  # Force reconfiguration even if logging was already configured
    handlers=[
        # File handler - writes to log file
        logging.FileHandler(log_filename, mode='a', encoding='utf-8'),
        # Console handler - also prints to console for immediate feedback
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Logging initialized. Log file: {log_filename}")

# Now import other modules (after logging is configured)
from typing import Dict
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools.mcp import create_mcp_toolset
from .builder.root_agent_builder import build_root_agent
from .builder.sub_agents_builder import build_sub_agents


# Initialize the LLM model
try:
    logger.info("Initializing LLM model: %s", config.model_name)
    logger.debug("api_base: %s", config.api_base)
    
    model = LiteLlm(
        model=config.model_name,
        api_key=config.openrouter_api_key,
        api_base=config.api_base
    )
    logger.info("LLM model initialized successfully")
except Exception as e:
    logger.error("Failed to initialize LLM model: %s", e)
    raise


# Initialize MCP Toolset
try:
    mcp_toolset = create_mcp_toolset()
    logger.info("MCP toolset initialized successfully")
except Exception as e:
    logger.error("Failed to initialize MCP toolset: %s", e)
    # We might want to continue without MCP or raise, depending on requirements.
    # For now, let's raise as it seems critical for this task.
    raise


# Initialize the root agent using builder
root_agent = build_root_agent(
    model=model,
    config=config,
    mcp_toolset=mcp_toolset,
    sub_agents=build_sub_agents()
)

