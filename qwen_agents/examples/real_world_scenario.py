"""
Real-world scenario example using Qwen Sub-Agents.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent_manager import QwenAgentManager

def simulate_task_processing():
    """Simulate processing different types of tasks using appropriate agents."""
    manager = QwenAgentManager()
    
    # Simulated tasks with different requirements
    tasks = [
        {"type": "research", "query": "Find information about quantum computing"},
        {"type": "coding", "query": "Generate a Python function to sort an array"},
        {"type": "analysis", "query": "Analyze sales data trends"},
        {"type": "planning", "query": "Create a project plan for launching a new product"}
    ]
    
    print("Processing tasks with appropriate agents:\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"{i}. Task: {task['query']}")
        
        # Find the appropriate agent for the task
        if task['type'] == 'research':
            agent_name = manager.get_agent_by_capability('web_search')
        elif task['type'] == 'coding':
            agent_name = manager.get_agent_by_capability('code_generation')
        elif task['type'] == 'analysis':
            agent_name = manager.get_agent_by_capability('data_analysis')
        elif task['type'] == 'planning':
            agent_name = manager.get_agent_by_capability('task_breakdown')
        else:
            agent_name = 'general'
        
        print(f"   → Assigned to: {agent_name}")
        
        # Load the agent configuration to get its details
        agent_config = manager.get_agent(agent_name)
        if agent_config:
            print(f"   → Model: {agent_config['agent']['primary_model']}")
            print(f"   → Personality: {agent_config['agent']['personality']}")
        
        # Show which agents are currently loaded in memory
        loaded_agents = list(manager.agents.keys())
        print(f"   → Agents currently loaded: {loaded_agents if loaded_agents else 'None'}")
        print()
    
    # Clean up by unloading all agents
    manager.unload_all_agents()
    print("All agents unloaded. Memory freed.")

def demonstrate_dynamic_loading():
    """Demonstrate dynamic loading based on changing requirements."""
    manager = QwenAgentManager()
    
    print("Dynamic loading demonstration:\n")
    
    # Initially no agents loaded
    print(f"Initially loaded: {list(manager.agents.keys())}")
    
    # Process a sequence of tasks requiring different agents
    task_sequence = [
        "Need to research AI trends",  # Requires research_agent
        "Write a JavaScript function",  # Requires coding_agent
        "Analyze dataset",              # Requires analysis_agent
        "Plan a project timeline"       # Requires planning_agent
    ]
    
    for i, task_desc in enumerate(task_sequence, 1):
        print(f"{i}. Processing: {task_desc}")
        
        # Determine required capability based on task description
        if "research" in task_desc.lower() or "information" in task_desc.lower():
            required_capability = "web_search"
        elif "write" in task_desc.lower() or "function" in task_desc.lower() or "code" in task_desc.lower():
            required_capability = "code_generation"
        elif "analyze" in task_desc.lower() or "dataset" in task_desc.lower():
            required_capability = "data_analysis"
        elif "plan" in task_desc.lower() or "timeline" in task_desc.lower():
            required_capability = "task_breakdown"
        else:
            required_capability = "web_search"  # Default
        
        # Find and load the appropriate agent
        agent_name = manager.get_agent_by_capability(required_capability)
        if agent_name:
            print(f"   → Found agent: {agent_name}")
            
            # Actually load the agent to work with it
            agent_config = manager.get_agent(agent_name)
            print(f"   → Agent loaded: {agent_name}")
        
        print(f"   → Currently loaded agents: {list(manager.agents.keys())}")
        print()

if __name__ == "__main__":
    print("Qwen Sub-Agent System - Real-World Scenario Example")
    print("=" * 55)
    
    print("\n1. Task Processing Simulation")
    print("-" * 30)
    simulate_task_processing()
    
    print("\n2. Dynamic Loading Demonstration")
    print("-" * 35)
    demonstrate_dynamic_loading()
    
    print("\nReal-world scenario example completed successfully!")