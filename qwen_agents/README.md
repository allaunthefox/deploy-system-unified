# Qwen Sub-Agent System

A modular multi-agent system built on Qwen AI models, designed to handle specialized tasks through dedicated agents with on-demand loading for optimal resource usage.

## Overview

This system implements a multi-agent architecture where different specialized agents handle specific types of tasks:

- **Research Agent**: Handles research and information gathering tasks
- **Coding Agent**: Specialized in code generation and debugging
- **Analysis Agent**: Performs data analysis and generates insights
- **Planning Agent**: Assists with project planning and task management

The system features **on-demand loading**, meaning agents are only loaded into memory when they are actually needed, improving performance and resource efficiency.

## Directory Structure

```
qwen_agents/
├── config/                 # Main configuration files
├── agents/                 # Individual agent configurations
├── skills/                 # Specialized skills for agents
├── examples/               # Usage examples
├── docs/                   # Documentation
├── qwen_agent_manager.py   # Main manager class with on-demand loading
└── CONFIGURATION.md        # System overview
```

## Setup

1. Install required dependencies:
   ```bash
   pip install openai
   ```

2. Configure your Qwen API credentials in environment variables:
   ```bash
   export QWEN_API_KEY="your-api-key-here"
   ```

## Usage

### Using the Agent Manager

```python
from qwen_agent_manager import QwenAgentManager

# Initialize the manager
manager = QwenAgentManager()

# Get available agents (no agents loaded yet)
available_agents = manager.get_available_agents()
print("Available agents:", available_agents)

# Find an agent by capability (no agents loaded yet)
research_agent = manager.get_agent_by_capability("web_search")
print("Agent with web search capability:", research_agent)

# Get a specific agent configuration (loads only this agent into memory)
coding_agent = manager.get_agent("coding_agent")
print("Coding agent capabilities:", coding_agent['agent']['capabilities'])

# Unload specific agents to free memory
manager.unload_agent("coding_agent")

# Unload all agents to free memory
manager.unload_all_agents()
```

### On-Demand Loading Features

The system supports several methods for efficient agent loading:

- `get_agent(agent_name)` - Loads a specific agent on demand
- `get_agent_by_capability(capability)` - Finds an agent with a specific capability without loading others
- `load_agents_by_capabilities(capabilities)` - Finds multiple agents with any of the specified capabilities
- `unload_agent(agent_name)` - Removes an agent from memory
- `unload_all_agents()` - Clears all loaded agents from memory

## Configuration

Each agent has its own configuration file defining:

- Name and description
- Primary and fallback models
- Maximum tokens and temperature settings
- Capabilities and available tools
- Personality traits and constraints

See the individual JSON files in the `agents/` directory for examples.

## Extending the System

The system is designed to be extensible:

- Add new agents by creating configuration files
- Extend capabilities by adding new tools to the tool registry
- Modify agent personalities and constraints as needed
- Leverage on-demand loading to maintain optimal performance