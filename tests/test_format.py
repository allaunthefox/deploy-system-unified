#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-TST-1000102
# File Type: Python Test Script
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
import re
from pathlib import Path

# Test the actual format
line = "- `[anubis_enabled](roles/containers_anubis.md#anubis_enabled)`"
# Pattern to match: - `[varname]`(path#anchor) - but wait, that's not right
# Looking at the actual format: - `[anubis_enabled](roles/containers_anubis.md#anubis_enabled)`
# So it's: - [varname](path#anchor) with no backticks around the variable name
line = "- [anubis_enabled](roles/containers_anubis.md#anubis_enabled)"

# Pattern to match: - [varname](path#anchor)
pattern = r'^(\s*-\s+\[)([a-zA-Z0-9_]+)(\].*#)([a-zA-Z0-9_]+)(\).*)$'
m_var = re.match(pattern, line)
if m_var:
    print('Match found:', m_var.groups())
    prefix, varname, mid, anchor, suffix = m_var.groups()
    print(f'Prefix: "{prefix}"')
    print(f'Varname: "{varname}"')
    print(f'Mid: "{mid}"')
    print(f'Anchor: "{anchor}"')
    print(f'Suffix: "{suffix}"')
else:
    print('No match')
    print('Line format:', repr(line))
    
# Let's also try the format with backticks around variable names
line_with_backticks = "- `[anubis_enabled](roles/containers_anubis.md#anubis_enabled)`"
pattern_with_backticks = r'^(\s*-\s+`)(\[)([a-zA-Z0-9_]+)(\])(\].*#)([a-zA-Z0-9_]+)(\).*)$'
m_var_bt = re.match(pattern_with_backticks, line_with_backticks)
if m_var_bt:
    print('Match with backticks found:', m_var_bt.groups())
else:
    print('No match with backticks pattern')
    print('Line with backticks format:', repr(line_with_backticks))
    
# Actually, let me look at the actual format again
print("\nActual format from file:")
repo_root = Path(__file__).resolve().parent
with open(repo_root / 'wiki_pages' / 'Variable_Reference_Containers.md', 'r') as f:
    content = f.read()
    import re
    # Find a line with the pattern
    for line in content.splitlines():
        if '[anubis' in line and 'roles/containers_anubis' in line:
            print(repr(line))
            break