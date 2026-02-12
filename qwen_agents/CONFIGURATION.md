# Qwen Sub-Agent Configuration

This configuration sets up a multi-agent system using Qwen AI models, with specialized agents for different tasks and on-demand loading for optimal resource usage.

## Architecture Overview

The Qwen sub-agent system consists of:

1. **Main Orchestrator** - Routes tasks to appropriate specialized agents
2. **Specialized Agents** - Each designed for specific types of tasks
3. **Shared Resources** - Common tools and utilities used by all agents
4. **Configuration Layer** - Centralized settings and parameters
5. **On-Demand Loading System** - Efficient memory management

## Agent Types

### Research Agent
- Purpose: Information gathering, research, and analysis
- Model: qwen-plus (optimized for research tasks)
- Capabilities: Web search, document analysis, data extraction, summarization
- Personality: Curious, thorough, detail-oriented

### Coding Agent  
- Purpose: Code generation, debugging, and refactoring
- Model: qwen-coding (optimized for programming tasks)
- Capabilities: Code generation, debugging, testing, code review
- Personality: Precise, logical, follows best practices

### Analysis Agent
- Purpose: Data analysis and insight generation
- Model: qwen-max (for complex analytical tasks)
- Capabilities: Statistical analysis, visualization, trend identification
- Personality: Analytical, objective, insight-driven

### Planning Agent
- Purpose: Project planning and task management
- Model: qwen-max (for complex planning tasks)
- Capabilities: Task breakdown, timeline estimation, risk assessment
- Personality: Organized, strategic, collaborative

## Configuration Files

- `config/main_config.json` - Main configuration with all agent definitions
- `agents/{agent_name}.json` - Individual agent configurations
- `skills/` - Specialized skills and tools for agents
- `examples/` - Example usage scenarios
- `docs/` - Documentation for the agent system

## On-Demand Loading

The system implements on-demand loading to optimize memory usage:

- Agents are only loaded when explicitly accessed
- Capability-based searches don't load agents into memory
- Methods available for managing loaded agents:
  - `get_agent(name)` - Load specific agent
  - `get_agent_by_capability(cap)` - Find agent by capability (without loading)
  - `load_agents_by_capabilities(caps)` - Find multiple agents by capabilities (without loading)
  - `unload_agent(name)` - Free memory for specific agent
  - `unload_all_agents()` - Free memory for all agents

## Usage

The system can be used programmatically via the QwenAgentManager class, which handles:
- Loading agent configurations on-demand
- Routing tasks to appropriate agents
- Managing agent capabilities and constraints
- Optimizing memory usage through selective loading