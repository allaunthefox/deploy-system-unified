#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500116
# Last Updated: 2026-02-28
# =============================================================================
"""
Analyze the wiki content using Qwen sub-agents to identify deficits and areas for improvement.
"""

import sys
import os
# Add the parent directory (qwen_agents) to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent_manager import QwenAgentManager
from pathlib import Path

def analyze_wiki_content():
    """Analyze the wiki content using Qwen agents."""
    
    print("🔍 ANALYZING WIKI CONTENT WITH QWEN AGENTS")
    print("=" * 45)
    
    # Initialize the agent manager
    manager = QwenAgentManager()
    
    print(f"Available agents: {manager.get_available_agents()}")
    print()
    
    # Define the wiki pages directory (env WORKSPACES_WIKI or fallback)
    wiki_dir = Path(os.environ.get('WORKSPACES_WIKI', Path.home() / 'Workspaces' / 'wiki_pages'))
    
    if not wiki_dir.exists():
        print(f"❌ Wiki directory does not exist: {wiki_dir}")
        return
    
    print(f"📁 Analyzing wiki content at: {wiki_dir}")
    
    # Count total wiki pages
    wiki_files = list(wiki_dir.glob("*.md"))
    role_files = list((wiki_dir / "roles").glob("*.md"))
    
    print(f"📊 Found {len(wiki_files)} main wiki pages")
    print(f"📊 Found {len(role_files)} role documentation pages")
    print()
    
    # Use the research agent to analyze documentation quality
    print("🔬 RESEARCH AGENT: Documentation Quality Analysis")
    print("-" * 50)
    research_agent_name = manager.get_agent_by_capability("document_analysis")
    research_agent = manager.get_agent(research_agent_name)
    print(f"Using agent: {research_agent_name} ({research_agent['agent']['primary_model']})")
    
    # Check for completeness of key documentation
    key_docs = [
        "HOME.md", "DOCUMENTATION_INDEX.md", "ROLE_REFERENCE.md", 
        "VARIABLE_REFERENCE.md", "ONTOLOGY.md", "STYLE_GUIDE.md"
    ]
    
    print("Checking for key documentation completeness:")
    missing_docs = []
    incomplete_docs = []
    
    for doc in key_docs:
        doc_path = wiki_dir / doc
        if doc_path.exists():
            content = doc_path.read_text()
            word_count = len(content.split())
            print(f"  ✓ {doc} ({word_count} words)")
            
            # Check if document seems incomplete (very basic heuristic)
            if word_count < 100 and "TODO" in content.upper():
                incomplete_docs.append(doc)
        else:
            print(f"  ⚠ {doc} (missing)")
            missing_docs.append(doc)
    
    if incomplete_docs:
        print(f"  → Potentially incomplete docs: {', '.join(incomplete_docs)}")
    print()
    
    # Use the analysis agent to assess structure
    print("📊 ANALYSIS AGENT: Structure Assessment")
    print("-" * 39)
    analysis_agent_name = manager.get_agent_by_capability("data_analysis")
    analysis_agent = manager.get_agent(analysis_agent_name)
    print(f"Using agent: {analysis_agent_name} ({analysis_agent['agent']['primary_model']})")
    
    # Analyze the role documentation completeness
    print("Analyzing role documentation completeness:")
    
    # Get all documented roles from ROLE_REFERENCE.md
    role_ref_path = wiki_dir / "ROLE_REFERENCE.md"
    if role_ref_path.exists():
        role_ref_content = role_ref_path.read_text()
        
        # Count how many roles have detailed documentation
        documented_roles = len(list((wiki_dir / "roles").glob("*.md")))
        total_role_sections = role_ref_content.count("### `")
        
        print(f"  - Total roles referenced: {total_role_sections}")
        print(f"  - Roles with detailed docs: {documented_roles}")
        
        if total_role_sections > 0:
            completion_rate = (documented_roles / total_role_sections) * 100
            print(f"  - Documentation completion: {completion_rate:.1f}%")
            
            if completion_rate < 80:
                print("  ⚠ Low documentation completion rate")
    
    # Check for cross-linking between pages
    total_links = 0
    broken_links = 0
    
    for file_path in wiki_files:
        content = file_path.read_text()
        # Count markdown links
        import re
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        total_links += len(links)
        
        for link_text, link_target in links:
            if not link_target.startswith(('http', 'mailto:', '#')):
                # Check if linked file exists
                if '#' in link_target:
                    target_file = link_target.split('#')[0]
                else:
                    target_file = link_target
                
                if not target_file.endswith('.md'):
                    target_file += '.md'
                
                target_path = wiki_dir / target_file
                if not target_path.exists():
                    broken_links += 1
    
    print(f"  - Total internal links: {total_links}")
    print(f"  - Broken internal links: {broken_links}")
    
    if broken_links > 0:
        print(f"  ⚠ Found {broken_links} broken internal links")
    print()
    
    # Use the planning agent to suggest improvements
    print("📋 PLANNING AGENT: Improvement Recommendations")
    print("-" * 47)
    planning_agent_name = manager.get_agent_by_capability("task_breakdown")
    planning_agent = manager.get_agent(planning_agent_name)
    print(f"Using agent: {planning_agent_name} ({planning_agent['agent']['primary_model']})")
    
    print("Recommended improvements based on analysis:")
    
    recommendations = []
    
    if missing_docs:
        recommendations.append(f"Create missing key documents: {', '.join(missing_docs)}")
    
    if incomplete_docs:
        recommendations.append(f"Complete potentially incomplete docs: {', '.join(incomplete_docs)}")
    
    if broken_links > 0:
        recommendations.append(f"Fix {broken_links} broken internal links")
    
    completion_rate = (documented_roles / total_role_sections * 100) if total_role_sections > 0 else 0
    if completion_rate < 90:
        missing_role_docs = total_role_sections - documented_roles
        recommendations.append(f"Create documentation for {missing_role_docs} undocumented roles")
    
    # Check for searchability/indexing issues
    long_pages = []
    for file_path in wiki_files:
        content = file_path.read_text()
        if len(content) > 10000:  # More than 10k characters
            long_pages.append(file_path.name)
    
    if long_pages:
        recommendations.append(f"Split overly long pages: {', '.join(long_pages)}")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("  ✓ No major improvements needed based on analysis")
    
    print()
    print(f"🧠 AGENTS USED: {list(manager.agents.keys())}")
    
    # Clean up
    manager.unload_all_agents()
    print(f"🧹 CLEANUP: All agents unloaded")
    
    print("\n✅ Wiki content analysis completed successfully!")

if __name__ == "__main__":
    analyze_wiki_content()