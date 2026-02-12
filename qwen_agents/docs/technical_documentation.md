# Qwen Sub-Agent System - Technical Documentation

## System Architecture

The Qwen Sub-Agent System is designed with a modular architecture that allows for easy extension and maintenance. The system consists of several key components:

### Core Components

1. **Agent Manager** (`qwen_agent_manager.py`)
   - Central orchestrator that manages all agents
   - Handles agent registration and retrieval
   - Provides methods for task routing based on capabilities

2. **Configuration Layer** (`config/` directory)
   - Main configuration file defines all available agents
   - Individual agent configuration files specify capabilities and settings
   - JSON-based configuration for easy modification

3. **Agent Definitions** (`agents/` directory)
   - Each agent has its own configuration file
   - Defines model preferences, capabilities, and personality traits
   - Specifies available tools and constraints

4. **Skills Framework** (`skills/` directory)
   - Reusable functions that extend agent capabilities
   - Follow a standardized interface for easy integration
   - Can be added without modifying core agent code

## Agent Configuration Schema

Each agent configuration follows this JSON schema:

```json
{
  "agent": {
    "name": "string",
    "type": "string",
    "description": "string",
    "primary_model": "string",
    "fallback_models": ["string"],
    "max_tokens": "integer",
    "temperature": "float",
    "capabilities": ["string"],
    "tools": ["string"],
    "personality": "string",
    "constraints": ["string"]
  }
}
```

### Field Descriptions

- `name`: Unique identifier for the agent
- `type`: Category of agent (e.g., "specialized", "general")
- `description`: Brief description of the agent's purpose
- `primary_model`: Default model to use for this agent
- `fallback_models`: Models to use if primary model is unavailable
- `max_tokens`: Maximum tokens for model responses
- `temperature`: Temperature setting for model responses
- `capabilities`: List of tasks the agent can perform
- `tools`: Tools available to the agent
- `personality`: Behavioral characteristics of the agent
- `constraints`: Limitations or guidelines for the agent

## Task Routing Logic

The system uses capability-based routing to assign tasks to the most appropriate agent:

1. The system analyzes the task requirements
2. Matches capabilities to available agents
3. Selects the best agent based on specialization
4. Falls back to general agents if no specialized agent is available

## Extending the System

### Adding New Agents

To add a new agent:

1. Create a new JSON configuration file in the `agents/` directory
2. Define the agent's properties according to the schema
3. The agent will be automatically available through the manager

### Adding New Skills

To add a new skill:

1. Create a Python file in the `skills/` directory
2. Implement the skill functionality with a clear interface
3. Update agent configurations to include the new skill in their tools list

### Modifying Agent Behavior

Agent behavior can be adjusted by modifying:

- Personality traits in the configuration
- Constraints that guide decision-making
- Available tools that expand capabilities
- Model preferences for different response characteristics

## Best Practices

1. **Specialization**: Create agents with focused capabilities rather than general-purpose agents
2. **Clear Boundaries**: Define clear responsibilities for each agent to avoid overlap
3. **Consistent Configuration**: Use consistent naming and structure across agent configurations
4. **Documentation**: Maintain clear documentation for each agent's purpose and capabilities
5. **Testing**: Test agents individually and as part of the system to ensure proper behavior