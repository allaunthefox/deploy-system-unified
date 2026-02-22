#!/usr/bin/env python3
"""
Initializer script for Qwen Sub-Agent System
"""

import os
from .qwen_agent_manager import QwenAgentManager

def initialize_qwen_agents():
    """Initialize the Qwen agent system."""
    print("Initializing Qwen Sub-Agent System...")
    
    # Create the agent manager
    manager = QwenAgentManager()
    
    # Load all available agents
    available_agents = manager.get_available_agents()
    
    print(f"✓ Loaded {len(available_agents)} agents:")
    for agent_name in available_agents:
        agent_config = manager.get_agent(agent_name)
        print(f"  - {agent_name}: {agent_config['agent']['description']}")
    
    print("\nQwen Sub-Agent System initialized successfully!")
    print("You can now use the agents through the QwenAgentManager.")
    
    return manager

if __name__ == "__main__":
    initialize_qwen_agents()