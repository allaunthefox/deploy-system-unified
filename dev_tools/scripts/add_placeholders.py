#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500011
# Script Type: Repository Maintenance
# Description: Adds .gitkeep placeholders to role directories
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
from pathlib import Path
import sys

def add_placeholders(group):
    base = Path('roles')/group
    if not base.exists():
        print(f"Group {group} not found")
        return
    
    # Standard Ansible directories to ignore if found at the group level
    ignored_dirs = {
        'defaults', 'files', 'handlers', 'meta', 
        'tasks', 'templates', 'vars', 'molecule', 'tests'
    }

    for r in base.iterdir():
        if r.is_dir():
            # Skip hidden directories and standard Ansible subdirectories
            if r.name.startswith('.') or r.name in ignored_dirs:
                continue

            t = r/'tasks'/'main.yml'
            if not t.exists():
                t.parent.mkdir(parents=True, exist_ok=True)
                t.write_text('---\n- name: placeholder task (no-op)\n  ansible.builtin.debug:\n    msg: "Placeholder: no action"\n')
            d = r/'defaults'/'main.yml'
            if not d.exists():
                d.parent.mkdir(parents=True, exist_ok=True)
                d.write_text('---\n# Placeholder defaults\n# Intentionally empty\n')
            # Add handlers placeholder where missing
            h = r/'handlers'/'main.yml'
            if not h.exists():
                h.parent.mkdir(parents=True, exist_ok=True)
                h.write_text('---\n# Placeholder handlers file\n# Intentionally empty\n')
            # Add vars placeholder where missing
            v = r/'vars'/'main.yml'
            if not v.exists():
                v.parent.mkdir(parents=True, exist_ok=True)
                v.write_text('---\n# Placeholder vars file\n# Intentionally empty\n')
            # Add templates placeholder where missing (lowercase readme)
            tpls = r/'templates'
            if not tpls.exists():
                tpls.mkdir(parents=True, exist_ok=True)
                (tpls/'readme.md').write_text('# Placeholder templates directory\nThis directory intentionally left empty (no templates required).')
            f = r/'files'
            if not f.exists():
                f.mkdir(parents=True, exist_ok=True)
                (f/'readme.md').write_text('# Placeholder directory\nThis directory intentionally left empty for packaging purposes.')
    print(f"Placeholders added for group: {group}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: add_placeholders.py <group>')
        sys.exit(1)
    add_placeholders(sys.argv[1])
