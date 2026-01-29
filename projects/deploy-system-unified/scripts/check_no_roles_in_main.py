#!/usr/bin/env python3
import sys
import os

try:
    import yaml
except Exception as e:
    print("ERROR: PyYAML is required to run this script. Install it with 'pip install PyYAML' or ensure ansible/ansible-lint is installed in CI.")
    sys.exit(2)


def main():
    if len(sys.argv) != 2:
        print("Usage: check_no_roles_in_main.py <playbook_path>")
        return 2
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"ERROR: file not found: {path}")
        return 2
    with open(path, 'r') as fh:
        try:
            docs = yaml.safe_load(fh)
        except Exception as exc:
            print(f"ERROR: failed to parse YAML: {exc}")
            return 2

    if docs is None:
        docs = []
    if not isinstance(docs, list):
        docs = [docs]

    for idx, play in enumerate(docs):
        if isinstance(play, dict) and 'roles' in play and play.get('roles'):
            print(f"ERROR: 'roles:' found at top-level in {path} (play index {idx}). main.yml must remain a pristine base; use branch_templates/*.yml")
            return 1

    print("OK: no top-level 'roles' key found in", path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
