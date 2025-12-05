"""Sub-agents Builder - Builds and returns sub-agents for the root agent.

This module contains the builder function for creating and returning sub-agents.
"""

import logging
from typing import List

from google.adk.agents.llm_agent import Agent
from search_agent.sub_agents import wikipedia_agent, summarizing_agent

logger = logging.getLogger(__name__)


def build_sub_agents() -> List[Agent]:
    """Build and return the list of sub-agents.
    
    Returns:
        List[Agent]: List containing wikipedia_agent and summarizing_agent
        
    Note:
        The sub-agents are initialized in their respective modules:
        - wikipedia_agent: search_agent/sub_agents/wikipedia/wikipedia_agent.py
        - summarizing_agent: search_agent/sub_agents/summarizing/summarizing_agent.py
    """
    logger.info("Building sub-agents list")
    
    sub_agents = [wikipedia_agent, summarizing_agent]
    
    logger.info("Sub-agents list built with %d agents: %s", 
                len(sub_agents), 
                [agent.name for agent in sub_agents])
    
    return sub_agents
