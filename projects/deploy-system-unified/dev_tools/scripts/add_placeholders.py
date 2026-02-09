#!/usr/bin/env python3
from pathlib import Path
import sys

def add_placeholders(group):
    base = Path('roles')/group
    if not base.exists():
        print(f"Group {group} not found")
        return
    for r in base.iterdir():
        if r.is_dir():
            t = r/'tasks'/'main.yml'
            if not t.exists():
                t.parent.mkdir(parents=True, exist_ok=True)
                t.write_text('---\n- name: placeholder task (no-op)\n  debug:\n    msg: "Placeholder: no action"\n')
            d = r/'defaults'/'main.yml'
            if not d.exists():
                d.parent.mkdir(parents=True, exist_ok=True)
                d.write_text('---\n# Placeholder defaults\n# Intentionally empty\n')
            f = r/'files'
            if not f.exists():
                f.mkdir(parents=True, exist_ok=True)
                (f/'README.md').write_text('# Placeholder directory\nThis directory intentionally left empty for packaging purposes.')
    print(f"Placeholders added for group: {group}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: add_placeholders.py <group>')
        sys.exit(1)
    add_placeholders(sys.argv[1])
