"""
Advanced example demonstrating on-demand loading of Qwen Sub-Agents.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent_manager import QwenAgentManager

def main():
    print("Qwen Sub-Agent System - On-Demand Loading Example")
    print("=" * 50)
    
    # Initialize the agent manager
    manager = QwenAgentManager()
    
    print(f"Available agents: {manager.get_available_agents()}")
    print(f"Initially loaded agents: {list(manager.agents.keys())}")
    
    # Initially no agents are loaded
    print("\nInitially, no agents are loaded in memory")
    
    # Request an agent by capability - this will trigger loading
    print("\nRequesting agent with 'code_generation' capability...")
    coding_agent_name = manager.get_agent_by_capability("code_generation")
    print(f"Found agent: {coding_agent_name}")
    
    # The agent is now loaded
    print(f"Loaded agents after capability search: {list(manager.agents.keys())}")
    
    # Access the agent details - no additional loading occurs
    print(f"\nAccessing {coding_agent_name} details...")
    agent_details = manager.get_agent(coding_agent_name)
    print(f"Description: {agent_details['agent']['description']}")
    print(f"Capabilities: {', '.join(agent_details['agent']['capabilities'])}")
    
    # Request another agent
    print(f"\nRequesting agent with 'web_search' capability...")
    research_agent_name = manager.get_agent_by_capability("web_search")
    print(f"Found agent: {research_agent_name}")
    
    # Both agents are now loaded
    print(f"Loaded agents: {list(manager.agents.keys())}")
    
    # Find multiple agents with specific capabilities
    print(f"\nFinding agents with multiple capabilities...")
    multi_agents = manager.load_agents_by_capabilities(["data_analysis", "task_breakdown"])
    print(f"Agents with data_analysis or task_breakdown: {multi_agents}")
    print(f"All loaded agents: {list(manager.agents.keys())}")
    
    # Unload specific agents to free memory
    print(f"\nUnloading {coding_agent_name}...")
    manager.unload_agent(coding_agent_name)
    print(f"Loaded agents after unloading {coding_agent_name}: {list(manager.agents.keys())}")
    
    # Unload all agents
    print(f"\nUnloading all agents...")
    manager.unload_all_agents()
    print(f"Loaded agents after unloading all: {list(manager.agents.keys())}")
    
    print("\nOn-demand loading example completed successfully!")

if __name__ == "__main__":
    main()