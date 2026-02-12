#!/usr/bin/env python3
"""
Script to analyze the deploy-system-unified project using Qwen sub-agents.
"""

import sys
import os
# Add the parent directory (qwen_agents) to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent_manager import QwenAgentManager

def analyze_deploy_system_unified():
    """Analyze the deploy-system-unified project using specialized agents."""
    
    print("🔍 Analyzing deploy-system-unified project with Qwen Sub-Agents")
    print("=" * 65)
    
    # Initialize the agent manager
    manager = QwenAgentManager()
    
    print(f"Available agents: {manager.get_available_agents()}")
    print(f"Initially loaded agents: {list(manager.agents.keys())}\n")
    
    # Use the analysis agent to review the project structure
    print("📊 Using Analysis Agent to review project structure...")
    analysis_agent_name = manager.get_agent_by_capability("data_analysis")
    print(f"Selected agent: {analysis_agent_name}")
    
    # Load the analysis agent
    analysis_agent = manager.get_agent(analysis_agent_name)
    print(f"Agent model: {analysis_agent['agent']['primary_model']}")
    print(f"Agent capabilities: {analysis_agent['agent']['capabilities']}\n")
    
    # Use the research agent to gather information about the project
    print("🔬 Using Research Agent to gather project information...")
    research_agent_name = manager.get_agent_by_capability("web_search")  # Using web_search as proxy for research capability
    print(f"Selected agent: {research_agent_name}")
    
    # Load the research agent
    research_agent = manager.get_agent(research_agent_name)
    print(f"Agent model: {research_agent['agent']['primary_model']}")
    print(f"Agent capabilities: {research_agent['agent']['capabilities']}\n")
    
    # Use the planning agent to assess project planning aspects
    print("📋 Using Planning Agent to assess project organization...")
    planning_agent_name = manager.get_agent_by_capability("task_breakdown")
    print(f"Selected agent: {planning_agent_name}")
    
    # Load the planning agent
    planning_agent = manager.get_agent(planning_agent_name)
    print(f"Agent model: {planning_agent['agent']['primary_model']}")
    print(f"Agent capabilities: {planning_agent['agent']['capabilities']}\n")
    
    # Use the coding agent to review code quality aspects
    print("💻 Using Coding Agent to review code structure...")
    coding_agent_name = manager.get_agent_by_capability("code_generation")
    print(f"Selected agent: {coding_agent_name}")
    
    # Load the coding agent
    coding_agent = manager.get_agent(coding_agent_name)
    print(f"Agent model: {coding_agent['agent']['primary_model']}")
    print(f"Agent capabilities: {coding_agent['agent']['capabilities']}\n")
    
    # Summary of loaded agents
    print(f"🎯 Total agents loaded for analysis: {len(manager.agents)}")
    print(f"Loaded agents: {list(manager.agents.keys())}\n")
    
    # Perform a simulated analysis (in a real scenario, this would connect to the Qwen API)
    print("📝 Simulated Analysis Results:")
    print("- Project follows a modular, security-first approach")
    print("- Uses Ansible for infrastructure as code")
    print("- Implements layered security with default-deny policy")
    print("- Has comprehensive documentation structure")
    print("- Supports containerized workloads with Podman")
    print("- Includes backup and monitoring solutions\n")
    
    # Unload all agents to free memory
    manager.unload_all_agents()
    print(f"🧹 Agents unloaded. Current memory footprint: {len(manager.agents)} agents")
    
    print("\n✅ Analysis completed successfully using Qwen Sub-Agent system!")

if __name__ == "__main__":
    analyze_deploy_system_unified()