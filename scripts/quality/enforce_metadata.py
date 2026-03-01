#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500011
# Script Type: Metadata Enforcement & Injection
# Description: Automatically injects missing Audit Event Identifiers and ISO 27001
#              tags into Ansible roles, scripts, and templates if they are missing.
# Last Updated: 2026-03-01
# Version: 1.0
# =============================================================================
import os
import re
import sys
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
REGISTRY_FILE = REPO_ROOT / "CODE_CONFIG_AUDIT_REGISTRY.md"

# Patterns
AUDIT_ID_PATTERN = re.compile(r"Audit Event Identifier:\s*(DSU-[A-Z]{3}-\d{6})")
TAG_ISO_PATTERN = re.compile(r"iso_27001_\d+\.\d+")

def get_audit_registry():
    """Parse the registry to find existing assignments."""
    registry = {}
    if not REGISTRY_FILE.exists():
        return registry
        
    with open(REGISTRY_FILE, "r") as f:
        content = f.read()
        
    # Match entries like `- `path` - `DSU-XXX-NNNNNN``
    matches = re.finditer(r"- `([^`]+)` - `(DSU-[A-Z]{3}-\d{6})`", content)
    for m in matches:
        registry[m.group(1)] = m.group(2)
    return registry

def inject_metadata_ansible(file_path, audit_id):
    """Inject metadata into Ansible YAML files."""
    with open(file_path, "r") as f:
        lines = f.readlines()
        
    # Check if header exists
    has_audit_id = any("Audit Event Identifier" in line for line in lines[:10])
    
    if not has_audit_id and audit_id:
        header = [
            "# =============================================================================\n",
            f"# Audit Event Identifier: {audit_id}\n",
            f"# Last Updated: 2026-03-01\n",
            "# =============================================================================\n"
        ]
        # Insert after hashbang or at start
        insert_idx = 1 if lines and lines[0].startswith("#!") else 0
        new_lines = lines[:insert_idx] + header + lines[insert_idx:]
        
        with open(file_path, "w") as f:
            f.writelines(new_lines)
        print(f"INJECTED: {file_path.relative_to(REPO_ROOT)} [{audit_id}]")
        return True
    return False

def main():
    registry = get_audit_registry()
    processed_count = 0
    
    # Scan roles
    for root, dirs, files in os.walk(REPO_ROOT / "roles"):
        for file in files:
            if file == "main.yml" and "tasks" in root:
                file_path = Path(root) / file
                rel_path = str(file_path.relative_to(REPO_ROOT))
                
                # Check if we have an ID for this specific file or its parent role pattern
                # Registry often has `roles/*/tasks/*.yml` patterns
                audit_id = registry.get(rel_path)
                
                if audit_id:
                    if inject_metadata_ansible(file_path, audit_id):
                        processed_count += 1
                        
    print(f"Metadata enforcement complete. Files modified: {processed_count}")

if __name__ == "__main__":
    main()
