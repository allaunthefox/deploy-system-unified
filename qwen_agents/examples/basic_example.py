"""
Basic example demonstrating the Qwen Sub-Agent system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent_manager import QwenAgentManager

def main():
    # Initialize the agent manager
    manager = QwenAgentManager()
    
    print("Qwen Sub-Agent System - Basic Example")
    print("=" * 40)
    
    # Show available agents
    available_agents = manager.get_available_agents()
    print(f"Available agents: {available_agents}")
    
    print("\nAgent details:")
    for agent_name in available_agents:
        agent_config = manager.get_agent(agent_name)
        if agent_config:
            desc = agent_config['agent']['description']
            caps = ', '.join(agent_config['agent']['capabilities'][:3])  # Show first 3 capabilities
            print(f"- {agent_name}: {desc}")
            print(f"  Capabilities: {caps}...")
    
    # Demonstrate finding an agent by capability
    print("\nFinding agents by capability:")
    web_search_agent = manager.get_agent_by_capability("web_search")
    print(f"Agent with web search capability: {web_search_agent}")
    
    coding_agent = manager.get_agent_by_capability("code_generation")
    print(f"Agent with code generation capability: {coding_agent}")
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main()