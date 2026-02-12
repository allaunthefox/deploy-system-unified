# Qwen Sub-Agent Examples

This directory contains examples demonstrating various aspects of the Qwen sub-agent system.

## Available Examples

### Basic Examples
- `basic_example.py` - Demonstrates basic initialization and usage of the agent manager
- `on_demand_loading_example.py` - Shows how agents are loaded only when needed
- `real_world_scenario.py` - Simulates real-world usage with multiple tasks

### Example Descriptions

#### basic_example.py
Shows how to initialize the agent manager, list available agents, and access agent configurations. Demonstrates the basic API for working with agents.

#### on_demand_loading_example.py
Demonstrates the on-demand loading feature where agents are only loaded into memory when explicitly accessed. Shows how to find agents by capability without loading them, and how to manage memory usage.

#### real_world_scenario.py
Simulates a real-world scenario where different types of tasks are processed using appropriate agents. Demonstrates dynamic agent selection and loading based on task requirements.

## Running Examples

To run any example:

```bash
cd /home/prod/Workspaces/qwen_agents
python examples/example_name.py
```

Make sure your Qwen API key is set in the environment variable `QWEN_API_KEY` if you plan to actually call the Qwen API (though the examples here only demonstrate the configuration and loading system).