"""
Example usage of the French Translator sub-agent.

This demonstrates how to use the French translator agent that is
a sub-agent of the summarizing agent.
"""

from search_agent.sub_agents.summarizing import french_translator_agent
from search_agent.sub_agents.summarizing.sub_agents.french_translator import translate_to_french


def example_direct_agent_usage():
    """Example: Using the agent directly."""
    content = "Hello, how are you today? I hope you're having a wonderful day!"
    
    # Use the agent directly
    response = french_translator_agent.run(f"Translate to French: {content}")
    print("Direct agent response:")
    print(response)
    print()


def example_helper_function():
    """Example: Using the helper function."""
    content = """
    Welcome to our application!
    
    Features:
    • Fast and reliable
    • Easy to use
    • Secure and private
    """
    
    # Use the helper function
    result = translate_to_french(content)
    
    if result["status"] == "success":
        print("Translation successful:")
        print(result["translation"])
    else:
        print("Translation failed:")
        print(result["error"])
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("French Translator Sub-Agent Examples")
    print("=" * 60)
    print()
    
    example_direct_agent_usage()
    example_helper_function()
