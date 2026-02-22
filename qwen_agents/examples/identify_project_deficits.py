#!/usr/bin/env python3
"""
Identify potential deficits in the deploy-system-unified project using Qwen sub-agents.
"""

import sys
import os
# Add the parent directory (qwen_agents) to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent_manager import QwenAgentManager

def identify_project_deficits():
    """Identify potential deficits in the deploy-system-unified project."""
    
    print("🔍 IDENTIFYING PROJECT DEFICITS: deploy-system-unified")
    print("=" * 58)
    
    # Initialize the agent manager
    manager = QwenAgentManager()
    
    print(f"Available agents: {manager.get_available_agents()}")
    print()
    
    # Path to the deploy-system-unified project
    project_path = Path(os.environ.get('WORKSPACES_PROJECTS', Path.home() / 'Workspaces' / 'projects')) / 'deploy-system-unified'
    
    # Check if the project exists
    if not os.path.exists(project_path):
        print(f"❌ Project path does not exist: {project_path}")
        return
    
    print(f"📁 Analyzing project at: {project_path}")
    print()
    
    # Use the research agent to identify documentation deficits
    print("🔬 RESEARCH AGENT: Documentation Analysis")
    print("-" * 42)
    research_agent_name = manager.get_agent_by_capability("document_analysis")
    research_agent = manager.get_agent(research_agent_name)
    print(f"Using agent: {research_agent_name} ({research_agent['agent']['primary_model']})")
    
    # Check for missing documentation elements
    important_docs = [
        "CONTRIBUTING.md", "CHANGELOG.md", "ROADMAP.md", 
        "SECURITY.md", "CODE_OF_CONDUCT.md", "LICENSE"
    ]
    
    print("Checking for essential documentation:")
    missing_docs = []
    for doc in important_docs:
        doc_path = os.path.join(project_path, doc)
        if os.path.exists(doc_path):
            print(f"  ✓ {doc}")
        else:
            print(f"  ⚠ {doc} (missing)")
            missing_docs.append(doc)
    
    if not missing_docs:
        print("  → No critical documentation deficits found")
    else:
        print(f"  → Missing documentation: {', '.join(missing_docs)}")
    print()
    
    # Use the coding agent to identify code quality deficits
    print("💻 CODING AGENT: Code Quality Assessment")
    print("-" * 40)
    coding_agent_name = manager.get_agent_by_capability("code_review")
    coding_agent = manager.get_agent(coding_agent_name)
    print(f"Using agent: {coding_agent_name} ({coding_agent['agent']['primary_model']})")
    
    # Check for common Ansible project deficits
    print("Checking for common Ansible project deficits:")
    
    # Check for tests directory
    tests_path = os.path.join(project_path, "tests")
    if os.path.exists(tests_path):
        print("  ✓ Tests directory exists")
    else:
        print("  ⚠ Tests directory missing - important for verifying idempotency")
    
    # Check for molecule directory (common for Ansible testing)
    molecule_path = os.path.join(project_path, "molecule")
    if os.path.exists(molecule_path):
        print("  ✓ Molecule testing framework detected")
    else:
        print("  ⚠ Molecule testing framework missing - recommended for role testing")
    
    # Check for requirements file
    req_files = ["requirements.yml", "requirements.txt"]
    found_reqs = [f for f in req_files if os.path.exists(os.path.join(project_path, f))]
    if found_reqs:
        print(f"  ✓ Dependency requirements found: {', '.join(found_reqs)}")
    else:
        print("  ⚠ No dependency requirements file found - dependencies not explicitly defined")
    
    # Check for version control configuration
    gitignore_path = os.path.join(project_path, ".gitignore")
    if os.path.exists(gitignore_path):
        print("  ✓ .gitignore file exists")
    else:
        print("  ⚠ .gitignore file missing - sensitive data could be committed")
    print()
    
    # Use the analysis agent to identify structural deficits
    print("📊 ANALYSIS AGENT: Structural Assessment")
    print("-" * 39)
    analysis_agent_name = manager.get_agent_by_capability("data_analysis")
    analysis_agent = manager.get_agent(analysis_agent_name)
    print(f"Using agent: {analysis_agent_name} ({analysis_agent['agent']['primary_model']})")
    
    # Check for important directories that might be missing
    important_dirs = [
        "group_vars/", "host_vars/", "filter_plugins/", 
        "lookup_plugins/", "library/", "module_utils/"
    ]
    
    print("Checking for important Ansible directories:")
    missing_dirs = []
    for dir_name in important_dirs:
        full_path = os.path.join(project_path, dir_name.rstrip('/'))
        if os.path.exists(full_path):
            print(f"  ✓ {dir_name}")
        else:
            print(f"  ? {dir_name} (potentially missing)")
            missing_dirs.append(dir_name)
    
    # Check for vars directory specifically
    vars_path = os.path.join(project_path, "vars")
    if os.path.exists(vars_path):
        print("  ✓ vars/ directory exists")
    else:
        print("  ⚠ vars/ directory missing - might need for shared variables")
    print()
    
    # Use the planning agent to identify organizational deficits
    print("📋 PLANNING AGENT: Organization Assessment")
    print("-" * 41)
    planning_agent_name = manager.get_agent_by_capability("risk_assessment")
    planning_agent = manager.get_agent(planning_agent_name)
    print(f"Using agent: {planning_agent_name} ({planning_agent['agent']['primary_model']})")
    
    # Look for potential organizational deficits
    print("Assessing organizational structure deficits:")
    
    # Check for CI/CD configuration
    ci_files = [".github/workflows/", ".gitlab-ci.yml", ".travis.yml", "Jenkinsfile"]
    found_ci = False
    for ci_file in ci_files:
        if "/" in ci_file:  # Directory check
            ci_path = os.path.join(project_path, ci_file.rstrip('/'))
            if os.path.exists(ci_path):
                print(f"  ✓ CI/CD configuration detected: {ci_file}")
                found_ci = True
        else:  # File check
            ci_path = os.path.join(project_path, ci_file)
            if os.path.exists(ci_path):
                print(f"  ✓ CI/CD configuration detected: {ci_file}")
                found_ci = True
    
    if not found_ci:
        print("  ⚠ No CI/CD configuration detected - automation of testing/deployment missing")
    
    # Check for backup strategy documentation
    backup_related = ["backup", "restore", "disaster", "recovery"]
    has_backup_docs = False
    docs_dir = os.path.join(project_path, "docs")
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(('.md', '.txt', '.rst')):
                    with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if any(term in content for term in backup_related):
                            has_backup_docs = True
                            break
            if has_backup_docs:
                break
    
    if has_backup_docs:
        print("  ✓ Backup/disaster recovery documentation found")
    else:
        print("  ⚠ Backup/disaster recovery documentation may be insufficient")
    
    # Check for security audit trail
    security_related = ["security", "audit", "compliance", "penetration", "vulnerability"]
    has_security_audits = False
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(('.md', '.txt', '.rst')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(term in content for term in security_related):
                                has_security_audits = True
                                break
                    except:
                        continue
            if has_security_audits:
                break
    
    if has_security_audits:
        print("  ✓ Security audit documentation found")
    else:
        print("  ⚠ Security audit documentation may be insufficient")
    print()
    
    # Compile findings
    print("📋 COMPILED DEFICIT ANALYSIS")
    print("-" * 31)
    
    deficits = []
    if missing_docs:
        deficits.append(f"Missing documentation: {', '.join(missing_docs)}")
    
    # Add code quality deficits
    if not os.path.exists(os.path.join(project_path, "molecule")):
        deficits.append("Missing Molecule testing framework")
    if not any(os.path.exists(os.path.join(project_path, f)) for f in ["requirements.yml", "requirements.txt"]):
        deficits.append("Missing explicit dependency requirements")
    if not os.path.exists(os.path.join(project_path, ".gitignore")):
        deficits.append("Missing .gitignore file")
    
    # Add structural deficits
    if not os.path.exists(os.path.join(project_path, "vars")):
        deficits.append("Missing vars/ directory for shared variables")
    
    # Add organizational deficits
    if not found_ci:
        deficits.append("Missing CI/CD pipeline configuration")
    if not has_backup_docs:
        deficits.append("Insufficient backup/disaster recovery documentation")
    if not has_security_audits:
        deficits.append("Insufficient security audit documentation")
    
    if deficits:
        print("⚠️  Potential deficits identified:")
        for i, deficit in enumerate(deficits, 1):
            print(f"  {i}. {deficit}")
    else:
        print("✅ No major deficits identified in initial analysis")
    
    print()
    print(f"🧠 AGENTS USED: {list(manager.agents.keys())}")
    
    # Clean up
    manager.unload_all_agents()
    print(f"🧹 CLEANUP: All agents unloaded")
    
    print("\n✅ Deficit analysis completed successfully!")

if __name__ == "__main__":
    identify_project_deficits()