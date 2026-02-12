#!/usr/bin/env python3
"""Test script to debug the linter's anchor processing."""

import re
from pathlib import Path

# Read the role file
role_file = Path('/home/prod/Workspaces/wiki_pages/roles/containers_anubis.md')
role_content = role_file.read_text()

# Extract headings using the same pattern as the linter
HEADING_RE = re.compile(r'^(#+)\s*(.+)$', flags=re.M)
headers = [(m.group(1), m.group(2).strip()) for m in HEADING_RE.finditer(role_content)]

# Apply slugify function as linter does
slug_re = re.compile(r'[^a-z0-9 -]')
def slugify(s):
    s = s.lower()
    s = slug_re.sub('', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

target_headings = set(slugify(h) for _, h in headers)
print('All headings in containers_anubis.md:')
for h in sorted([h for _, h in headers]):
    if 'anubis' in h.lower():
        slug = slugify(h)
        print(f'  - "{h}" -> "{slug}"')

print()
print('Target headings containing anubis:')
for h in sorted(target_headings):
    if 'anubis' in h:
        print(f'  - {h}')

# Check if specific anchors exist
test_anchors = ['anubisenabled', 'anubisport', 'anubisdifficulty']
print()
print('Checking specific anchors:')
for anchor in test_anchors:
    exists = anchor in target_headings
    print(f'  - {anchor}: {"EXISTS" if exists else "MISSING"}')

# Also check the variable reference file
var_file = Path('/home/prod/Workspaces/wiki_pages/Variable_Reference_Containers.md')
var_content = var_file.read_text()

print()
print('Links in Variable_Reference_Containers.md containing anubis:')
for line in var_content.splitlines():
    if 'anubis' in line and '#' in line and 'containers_anubis.md' in line:
        # Extract the anchor part
        import re as regex
        match = regex.search(r'#([a-zA-Z0-9_]+)[\'"()]', line + "'")  # Add quote to ensure closing
        if not match:
            match = regex.search(r'#([a-zA-Z0-9_]+)\)', line)  # Look for closing parenthesis
        if match:
            anchor = match.group(1)
            exists = anchor in target_headings
            print(f'  - #{anchor} in containers_anubis.md: {"EXISTS" if exists else "MISSING"} -> {line.strip()}')