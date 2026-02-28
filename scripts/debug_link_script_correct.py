#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500008
# Script Type: Debug/Testing
# Description: Debug script to test link variable reference functionality (corrected)
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
"""Debug script to test the link variable reference functionality."""

import re
from pathlib import Path

# Test the exact logic from the script with correct format
sample_content = """### `containers/anubis`
- `[anubis_enabled](roles/containers_anubis.md#anubis_enabled)`
- `[anubis_port](roles/containers_anubis.md#anubis_port)`
"""

lines = sample_content.splitlines()
current_role_file = None
new_lines = []

for line in lines:
    print(f"Processing line: {repr(line)}")
    
    # Match role header
    m_role = re.match(r'^### `([^`]+)`', line)
    if m_role:
        role_name = m_role.group(1)
        current_role_file = f"roles/{role_name.replace('/', '_')}.md"
        print(f"  Found role: {role_name}, current_role_file: {current_role_file}")
        new_lines.append(line)
        continue

    # Match variable line in format: - [varname](path#anchor)
    m_var = re.match(r'^(\s*-\s+\[)([a-zA-Z0-9_]+)(\].*#)([a-zA-Z0-9_]+)(\).*)$', line)
    if m_var and current_role_file:
        prefix, varname, mid, anchor, suffix = m_var.groups()
        print(f"  Found variable: {varname}, current_role_file: {current_role_file}")
        
        # Link to the anchor in the role page (using slugified version)
        # Use the same slugify function as the linter to match what it expects
        slug_re = re.compile(r'[^a-z0-9 -]')
        def slugify(s):
            s = s.lower()
            s = slug_re.sub('', s)
            s = re.sub(r'\s+', '-', s)
            s = re.sub(r'-+', '-', s)
            return s.strip('-')

        anchor_name = slugify(varname)
        print(f"  Original anchor: {anchor}, slugified anchor: {anchor_name}")
        new_line = f'{prefix}{varname}{mid}{anchor_name}{suffix}'
        print(f"  New line: {new_line}")
        new_lines.append(new_line)
    else:
        print(f"  Line didn't match variable pattern or no current_role_file ({bool(current_role_file)})")
        new_lines.append(line)

print("\nResult:")
for line in new_lines:
    print(repr(line))