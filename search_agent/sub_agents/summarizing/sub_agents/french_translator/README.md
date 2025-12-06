# French Translator Sub-Agent

A dedicated agent for translating content to French, implemented as a sub-agent of the Summarizing Agent.

## Overview

The French Translator Agent is a specialized LLM-based agent that translates content to French while maintaining the original formatting and structure.

## Architecture

```
search_agent/sub_agents/summarizing/
├── summarizing_agent.py          # Main summarizing agent
├── config.py                      # Summarizing config
├── config.ini                     # Summarizing settings
└── sub_agents/                    # Sub-agents directory
    └── french_translator/         # French translator sub-agent
        ├── __init__.py
        ├── config.py              # Configuration class
        ├── config.ini             # Agent settings
        ├── french_translator_agent.py  # Main agent implementation
        └── example_usage.py       # Usage examples
```

## Features

- **Dedicated LLM Agent**: Has its own Agent instance with specialized instructions for French translation
- **Configurable**: Settings can be customized via `config.ini` or environment variables
- **Error Handling**: Robust error handling with detailed error messages
- **Consistent API**: Follows the same pattern as other agents in the system

## Usage

### Method 1: Using the Helper Function

```python
from search_agent.sub_agents.summarizing.sub_agents.french_translator import translate_to_french

content = "Hello, how are you today?"
result = translate_to_french(content)

if result["status"] == "success":
    print(result["translation"])
else:
    print(result["error"])
```

### Method 2: Using the Agent Directly

```python
from search_agent.sub_agents.summarizing import french_translator_agent

content = "Hello, how are you today?"
translation = french_translator_agent.run(f"Translate to French: {content}")
print(translation)
```

### Method 3: Importing from Parent Module

```python
from search_agent.sub_agents.summarizing import french_translator_agent

# Use the agent
response = french_translator_agent.run("Translate this to French: Good morning!")
```

## Configuration

### config.ini Settings

```ini
[agent]
name = french_translator_agent
description = An agent that translates content to French
instruction = Translate the provided content to French...

[model]
model_name = openrouter/google/gemini-2.0-flash-001
api_base = https://openrouter.ai/api/v1

[translation]
target_language = French
preserve_formatting = true
```

### Environment Variables

You can override settings using environment variables:

- `FRENCH_TRANSLATOR_MODEL_NAME`: Override the model name
- `FRENCH_TRANSLATOR_API_BASE`: Override the API base URL
- `OPENROUTER_API_KEY`: API key (required)
- `TRANSLATION_TARGET_LANGUAGE`: Target language
- `TRANSLATION_PRESERVE_FORMATTING`: Whether to preserve formatting

## Response Format

The `translate_to_french()` function returns a dictionary:

**Success:**
```python
{
    "status": "success",
    "translation": "Bonjour, comment allez-vous aujourd'hui?"
}
```

**Error:**
```python
{
    "status": "error",
    "error": "Error message here"
}
```

## Examples

See `example_usage.py` for complete working examples.

## Integration with Summarizing Agent

The French Translator Agent is a sub-agent of the Summarizing Agent, meaning:

1. It lives in the `summarizing/sub_agents/` directory
2. It can be accessed through the summarizing module
3. It has its own independent configuration and LLM instance
4. It follows the same architectural patterns as the parent agent

## Development

To add more translation languages or features:

1. Create a new sub-agent in `sub_agents/` directory
2. Follow the same structure (config.py, config.ini, agent.py, __init__.py)
3. Update the parent `sub_agents/__init__.py` to expose the new agent
