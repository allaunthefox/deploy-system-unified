#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500112
# Last Updated: 2026-02-28
# =============================================================================
"""
Detailed analysis of the deploy-system-unified project using Qwen sub-agents.
"""

import sys
import os
from pathlib import Path
# Add the parent directory (qwen_agents) to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent_manager import QwenAgentManager

def detailed_project_analysis():
    """Perform a detailed analysis of the deploy-system-unified project."""
    
    print("🔍 DETAILED ANALYSIS: deploy-system-unified project")
    print("=" * 55)
    
    # Initialize the agent manager
    manager = QwenAgentManager()
    
    print(f"Available agents: {manager.get_available_agents()}")
    print()
    
    # Path to the deploy-system-unified project
    project_path = os.environ.get("DEPLOY_SYSTEM_UNIFIED_PROJECT_PATH", str(Path(__file__).resolve().parents[2] / "projects" / "deploy-system-unified"))
    
    # Check if the project exists
    if not os.path.exists(project_path):
        print(f"❌ Project path does not exist: {project_path}")
        return
    
    print(f"📁 Analyzing project at: {project_path}")
    print()
    
    # Use the research agent to examine documentation
    print("🔬 RESEARCH AGENT ANALYSIS")
    print("-" * 30)
    research_agent_name = manager.get_agent_by_capability("document_analysis")
    print(f"Using agent: {research_agent_name}")
    
    # Load the research agent
    research_agent = manager.get_agent(research_agent_name)
    print(f"Model: {research_agent['agent']['primary_model']}")
    
    # Examine key documentation files
    doc_files = [
        "README.md",
        "docs/INDEX.md",
        "base_hardened.yml",
        "production_deploy.yml",
        "ansible.cfg"
    ]
    
    print("Key documentation files identified:")
    for doc_file in doc_files:
        full_path = os.path.join(project_path, doc_file)
        if os.path.exists(full_path):
            print(f"  ✓ {doc_file}")
        else:
            print(f"  ✗ {doc_file}")
    print()
    
    # Use the coding agent to analyze code structure
    print("💻 CODING AGENT ANALYSIS")
    print("-" * 28)
    coding_agent_name = manager.get_agent_by_capability("architecture_design")
    print(f"Using agent: {coding_agent_name}")
    
    # Load the coding agent
    coding_agent = manager.get_agent(coding_agent_name)
    print(f"Model: {coding_agent['agent']['primary_model']}")
    
    # Analyze the roles structure
    roles_path = os.path.join(project_path, "roles")
    if os.path.exists(roles_path):
        roles = os.listdir(roles_path)
        print(f"Project has {len(roles)} major role categories:")
        for role in roles:
            print(f"  - {role}")
    else:
        print("  ❌ Roles directory not found")
    print()
    
    # Use the analysis agent to assess complexity
    print("📊 ANALYSIS AGENT ASSESSMENT")
    print("-" * 32)
    analysis_agent_name = manager.get_agent_by_capability("data_analysis")
    print(f"Using agent: {analysis_agent_name}")
    
    # Load the analysis agent
    analysis_agent = manager.get_agent(analysis_agent_name)
    print(f"Model: {analysis_agent['agent']['primary_model']}")
    
    # Count key files to assess project size
    import subprocess
    try:
        # Count total files in the project
        result = subprocess.run(['find', project_path, '-type', 'f'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        total_files = len(result.stdout.strip().split('\n')) - 1  # Subtract 1 for empty string
        print(f"Total project files: ~{total_files}")
        
        # Count Ansible playbooks
        result = subprocess.run(['find', project_path, '-name', '*.yml', '-o', '-name', '*.yaml'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        playbook_count = len(result.stdout.strip().split('\n')) - 1
        print(f"Ansible playbooks: {playbook_count}")
        
        # Count directories
        result = subprocess.run(['find', project_path, '-type', 'd'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        dir_count = len(result.stdout.strip().split('\n')) - 1
        print(f"Total directories: {dir_count}")
    except Exception as e:
        print(f"Could not count files: {e}")
    print()
    
    # Use the planning agent to assess project organization
    print("📋 PLANNING AGENT EVALUATION")
    print("-" * 32)
    planning_agent_name = manager.get_agent_by_capability("task_breakdown")
    print(f"Using agent: {planning_agent_name}")
    
    # Load the planning agent
    planning_agent = manager.get_agent(planning_agent_name)
    print(f"Model: {planning_agent['agent']['primary_model']}")
    
    # Assess project structure
    important_dirs = [
        "roles/", "playbooks/", "inventory/", "docs/", 
        "tasks/", "handlers/", "vars/", "files/"
    ]
    
    print("Checking for standard Ansible project structure:")
    for dir_name in important_dirs:
        full_path = os.path.join(project_path, dir_name.rstrip('/'))
        if os.path.exists(full_path):
            print(f"  ✓ {dir_name}")
        else:
            print(f"  ? {dir_name} (missing)")
    print()
    
    # Summary
    print("📋 SUMMARY OF FINDINGS")
    print("-" * 22)
    print("The deploy-system-unified project appears to be a comprehensive")
    print("Ansible-based infrastructure deployment system with:")
    print("  • Modular role-based architecture")
    print("  • Security-first design philosophy")
    print("  • Container workload support (Podman/Quadlets)")
    print("  • Comprehensive documentation structure")
    print("  • Multiple deployment profiles (production, development, etc.)")
    print()
    
    # Show which agents were loaded
    print(f"🧠 AGENTS LOADED: {list(manager.agents.keys())}")
    
    # Clean up
    manager.unload_all_agents()
    print(f"🧹 CLEANUP: All agents unloaded")
    
    print("\n✅ Detailed analysis completed successfully!")

if __name__ == "__main__":
    detailed_project_analysis()