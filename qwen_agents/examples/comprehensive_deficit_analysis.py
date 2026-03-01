#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500111
# Last Updated: 2026-02-28
# =============================================================================
"""
Comprehensive deficit analysis of the deploy-system-unified project using Qwen sub-agents.
"""

import sys
import os
from pathlib import Path
# Add the parent directory (qwen_agents) to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent_manager import QwenAgentManager

def comprehensive_deficit_analysis():
    """Comprehensive deficit analysis of the deploy-system-unified project."""
    
    print("🔍 COMPREHENSIVE DEFICIT ANALYSIS: deploy-system-unified")
    print("=" * 58)
    
    # Initialize the agent manager
    manager = QwenAgentManager()
    
    print(f"Available agents: {manager.get_available_agents()}")
    print()
    
    # Path to the deploy-system-unified project (env var or default). Normalize to an absolute path.
    project_path = Path(
        os.environ.get(
            "DEPLOY_SYSTEM_UNIFIED_PROJECT_PATH",
            Path(__file__).resolve().parents[2] / "projects" / "deploy-system-unified",
        )
    ).expanduser().resolve()
    
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
        "SECURITY.md", "CODE_OF_CONDUCT.md"
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
    req_files = ["requirements.yml", "requirements.txt", "galaxy.yml"]
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
    print("Checking for important Ansible directories:")
    
    # Check for vars directories (which actually exist in this project)
    vars_dirs = []
    for root, dirs, files in os.walk(project_path):
        for d in dirs:
            if 'vars' in d.lower():
                vars_dirs.append(os.path.relpath(os.path.join(root, d), project_path))
    
    if vars_dirs:
        print(f"  ✓ Multiple vars directories found ({len(vars_dirs)}):")
        # Show a sample of the vars directories
        for vdir in vars_dirs[:5]:  # Show first 5
            print(f"    - {vdir}")
        if len(vars_dirs) > 5:
            print(f"    ... and {len(vars_dirs)-5} more")
    else:
        print("  ⚠ No vars directories found - might need for shared variables")
    
    # Check for group_vars and host_vars at project level
    group_vars_path = os.path.join(project_path, "group_vars")
    host_vars_path = os.path.join(project_path, "host_vars")
    
    if os.path.exists(group_vars_path):
        print(f"  ✓ group_vars directory exists at project level")
    else:
        print(f"  ? group_vars directory missing at project level (found in roles)")
    
    if os.path.exists(host_vars_path):
        print(f"  ✓ host_vars directory exists at project level")
    else:
        print(f"  ? host_vars directory missing at project level (found in roles)")
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
    ci_exists = os.path.exists(os.path.join(project_path, ".github"))
    if ci_exists:
        print("  ✓ CI/CD configuration detected (.github directory)")
    else:
        print("  ⚠ No CI/CD configuration detected - automation of testing/deployment missing")
    
    # Check for backup strategy documentation
    backup_related = ["backup", "restore", "disaster", "recovery"]
    has_backup_docs = False
    docs_dir = os.path.join(project_path, "docs")
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(('.md', '.txt', '.rst')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(term in content for term in backup_related):
                                has_backup_docs = True
                                break
                    except:
                        continue
                if has_backup_docs:
                    break
            if has_backup_docs:
                break
    
    if has_backup_docs:
        print("  ✓ Backup/disaster recovery documentation found")
    else:
        print("  ⚠ Backup/disaster recovery documentation may be insufficient")
    
    # Check for security audit trail
    security_related = ["security", "audit", "compliance", "penetration", "vulnerability", "hardening"]
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
                break
    
    if has_security_audits:
        print("  ✓ Security audit documentation found")
    else:
        print("  ⚠ Security audit documentation may be insufficient")
    
    # Check for performance monitoring documentation
    perf_related = ["performance", "monitoring", "metrics", "observability", "telemetry"]
    has_perf_docs = False
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(('.md', '.txt', '.rst')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(term in content for term in perf_related):
                                has_perf_docs = True
                                break
                    except:
                        continue
                if has_perf_docs:
                    break
            if has_perf_docs:
                break
    
    if has_perf_docs:
        print("  ✓ Performance monitoring documentation found")
    else:
        print("  ⚠ Performance monitoring documentation may be insufficient")
    print()
    
    # Check for upgrade/migration documentation
    print("Checking for upgrade/migration documentation:")
    migration_related = ["migration", "upgrade", "update", "transition", "evolution"]
    has_migration_docs = False
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(('.md', '.txt', '.rst')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(term in content for term in migration_related):
                                has_migration_docs = True
                                break
                    except:
                        continue
                if has_migration_docs:
                    break
            if has_migration_docs:
                break
    
    if has_migration_docs:
        print("  ✓ Upgrade/migration documentation found")
    else:
        print("  ⚠ Upgrade/migration documentation may be insufficient")
    print()
    
    # Compile findings
    print("📋 COMPREHENSIVE DEFICIT ANALYSIS")
    print("-" * 35)
    
    deficits = []
    if missing_docs:
        deficits.append(f"Missing documentation: {', '.join(missing_docs)}")
    
    # Add code quality deficits
    if not os.path.exists(os.path.join(project_path, "molecule")):
        deficits.append("Missing Molecule testing framework")
    if not any(os.path.exists(os.path.join(project_path, f)) for f in ["requirements.yml", "requirements.txt", "galaxy.yml"]):
        deficits.append("Missing explicit dependency requirements")
    if not os.path.exists(os.path.join(project_path, ".gitignore")):
        deficits.append("Missing .gitignore file")
    if not os.path.exists(os.path.join(project_path, "tests")):
        deficits.append("Missing dedicated tests directory")
    
    # Add organizational deficits
    if not ci_exists:
        deficits.append("Missing CI/CD pipeline configuration")
    if not has_backup_docs:
        deficits.append("Insufficient backup/disaster recovery documentation")
    if not has_security_audits:
        deficits.append("Insufficient security audit documentation")
    if not has_perf_docs:
        deficits.append("Insufficient performance monitoring documentation")
    if not has_migration_docs:
        deficits.append("Insufficient upgrade/migration documentation")
    
    if deficits:
        print("⚠️  Potential deficits identified:")
        for i, deficit in enumerate(deficits, 1):
            print(f"  {i}. {deficit}")
    else:
        print("✅ No major deficits identified in comprehensive analysis")
    
    print()
    print(f"🧠 AGENTS USED: {list(manager.agents.keys())}")
    
    # Clean up
    manager.unload_all_agents()
    print(f"🧹 CLEANUP: All agents unloaded")
    
    print("\n✅ Comprehensive deficit analysis completed successfully!")

if __name__ == "__main__":
    comprehensive_deficit_analysis()