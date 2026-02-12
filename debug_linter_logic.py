#!/usr/bin/env python3
"""Debug script to test the linter logic directly."""

import re
from pathlib import Path

# Replicate the linter logic
def slugify(s):
    slug_re = re.compile(r'[^a-z0-9 -]')
    s = s.lower()
    s = slug_re.sub('', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

# Read the role file
role_file = Path('/home/prod/Workspaces/wiki_pages/roles/containers_anubis.md')
role_content = role_file.read_text()

# Extract headings like the linter does
HEADING_RE = re.compile(r'^(#+)\s*(.+)$', flags=re.M)
headers = [(m.group(1), m.group(2).strip()) for m in HEADING_RE.finditer(role_content)]
headings_slugs = set(slugify(h) for _, h in headers)

print("All heading slugs in containers_anubis.md:")
for slug in sorted(headings_slugs):
    if 'anubis' in slug or 'enable' in slug or 'port' in slug:
        print(f"  {slug}")

print("\nChecking for specific anchors:")
test_anchors = ['anubisenabled', 'anubisport', 'anubisdifficulty']
for anchor in test_anchors:
    exists = anchor in headings_slugs
    print(f"  {anchor}: {'FOUND' if exists else 'MISSING'}")

# Read the variable reference file
var_file = Path('/home/prod/Workspaces/wiki_pages/Variable_Reference_Containers.md')
var_content = var_file.read_text()

print("\nLinks found in Variable_Reference_Containers.md with 'anubis':")
for line in var_content.splitlines():
    if 'anubis' in line and '#' in line:
        # Extract anchor from link
        import re as regex
        link_match = regex.search(r'#([a-zA-Z0-9_]+)[\'"()]', line + "'")  # Add quote to ensure closing
        if not link_match:
            link_match = regex.search(r'#([a-zA-Z0-9_]+)\)', line)  # Look for closing parenthesis
        if link_match:
            anchor = link_match.group(1)
            exists = anchor in headings_slugs
            print(f"  {anchor}: {'FOUND' if exists else 'MISSING'} -> {line.strip()}")