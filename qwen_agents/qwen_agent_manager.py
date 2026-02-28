#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500010
# File Type: Python Module
# Description: Qwen Sub-Agent Manager - loads and manages specialized agents
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
"""
Qwen Sub-Agent Manager

This module provides functionality to load, configure, and manage
multiple specialized Qwen agents for different tasks.
Agents are loaded on-demand to improve performance and resource usage.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List


class QwenAgentManager:
    """Manages multiple specialized Qwen agents with on-demand loading."""
    
    def __init__(self, config_dir: Optional[str] = None):
        # Resolve config directory from argument, env var, or fallback to ~/Workspaces/qwen_agents/config
        default_config = Path(
            os.environ.get(
                "QWEN_AGENTS_CONFIG",
                Path.home() / "Workspaces" / "qwen_agents" / "config",
            )
        ).expanduser().resolve()
        self.config_dir = str(Path(config_dir).expanduser().resolve()) if config_dir else str(default_config)

        # Resolve agents directory from env var or fallback; normalize like config
        default_agents = Path(
            os.environ.get(
                "QWEN_AGENTS_AGENTS_DIR",
                Path.home() / "Workspaces" / "qwen_agents" / "agents",
            )
        ).expanduser().resolve()
        self.agents_dir = str(default_agents)

        self.agents: Dict[str, Any] = {}  # Cache for loaded agents
        self.main_config = self.load_main_config()
        self._available_agents = None  # Lazy-loaded list of available agents
        
    def load_main_config(self) -> Dict[str, Any]:
        """Load the main configuration file.

        If the file does not exist we return an empty dict so the manager
        can still be constructed in environments (e.g. tests) where the
        config directory hasn't been populated yet.
        """
        config_path = os.path.join(self.config_dir, "main_config.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def load_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Load configuration for a specific agent."""
        agent_config_path = os.path.join(self.agents_dir, f"{agent_name}.json")
        with open(agent_config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def register_agent(self, agent_name: str) -> Dict[str, Any]:
        """Register an agent by loading its configuration."""
        if agent_name not in self.agents:
            self.agents[agent_name] = self.load_agent_config(agent_name)
        return self.agents[agent_name]
    
    def get_agent(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get the configuration for a specific agent (loads on-demand)."""
        if agent_name not in self.agents:
            # Check if the agent exists before trying to load
            if agent_name in self.get_available_agents():
                return self.register_agent(agent_name)
            else:
                return None
        return self.agents.get(agent_name)
    
    def get_available_agents(self) -> List[str]:
        """Get a list of available agent names (lazy-loaded)."""
        if self._available_agents is None:
            if not os.path.isdir(self.agents_dir):
                # no agents directory yet; return empty list
                self._available_agents = []
            else:
                agent_files = [f for f in os.listdir(self.agents_dir) if f.endswith('.json')]
                self._available_agents = [os.path.splitext(f)[0] for f in agent_files]
        return self._available_agents
    
    def _get_agent_capabilities(self, agent_name: str) -> List[str]:
        """Get capabilities of an agent without fully loading it into cache."""
        agent_config_path = os.path.join(self.agents_dir, f"{agent_name}.json")
        with open(agent_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config['agent']['capabilities']
    
    def get_agent_by_capability(self, capability: str) -> Optional[str]:
        """Find an agent that has a specific capability without loading all agents."""
        for agent_name in self.get_available_agents():
            # Check capabilities without loading the agent into cache
            try:
                agent_caps = self._get_agent_capabilities(agent_name)
                if capability in agent_caps:
                    return agent_name
            except FileNotFoundError:
                continue  # Agent file doesn't exist
        return None
    
    def load_agents_by_capabilities(self, capabilities: List[str]) -> List[str]:
        """Find agents that have any of the specified capabilities without loading all agents."""
        matching_agents = []
        for agent_name in self.get_available_agents():
            try:
                agent_caps = self._get_agent_capabilities(agent_name)
                if any(cap in agent_caps for cap in capabilities):
                    matching_agents.append(agent_name)
            except FileNotFoundError:
                continue  # Agent file doesn't exist
        return matching_agents
    
    def unload_agent(self, agent_name: str) -> bool:
        """Remove an agent from memory to free resources."""
        if agent_name in self.agents:
            del self.agents[agent_name]
            return True
        return False
    
    def unload_all_agents(self):
        """Unload all loaded agents to free memory."""
        self.agents.clear()


# Example usage
if __name__ == "__main__":
    manager = QwenAgentManager()
    print("Available agents:", manager.get_available_agents())
    
    # Example: Find an agent capable of code generation (agent not loaded yet)
    coding_agent = manager.get_agent_by_capability("code_generation")
    print(f"Agent for code generation: {coding_agent}")
    
    # The agent is now loaded when accessed
    agent_details = manager.get_agent("coding_agent")
    if agent_details:
        print(f"\nCoding agent details:")
        print(f"Description: {agent_details['agent']['description']}")
        print(f"Capabilities: {', '.join(agent_details['agent']['capabilities'])}")
    
    # Show that only the requested agent is loaded
    print(f"\nCurrently loaded agents in memory: {list(manager.agents.keys())}")
    
    # Unload the agent to free memory
    manager.unload_agent("coding_agent")
    print(f"After unloading, loaded agents: {list(manager.agents.keys())}")