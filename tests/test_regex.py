#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-TST-1000106
# File Type: Python Test Script
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
import re
from pathlib import Path

# Test the regex pattern with a sample line
sample_line = '- [anubis_enabled](roles/containers_anubis.md#anubis_enabled)'
m_var = re.match(r'^(\s*-\s+`)([a-zA-Z0-9_]+)(`.*)$', sample_line)
if m_var:
    print('Groups found:', m_var.groups())
    indent, varname, rest = m_var.groups()
    print(f'Indent: "{indent}"')
    print(f'Varname: "{varname}"')
    print(f'Rest: "{rest}"')
    
    # Apply slugify function
    slug_re = re.compile(r'[^a-z0-9 -]')
    def slugify(s):
        s = s.lower()
        s = slug_re.sub('', s)
        s = re.sub(r'\s+', '-', s)
        s = re.sub(r'-+', '-', s)
        return s.strip('-')

    anchor_name = slugify(varname)
    print(f'Slugified anchor: "{anchor_name}"')
    
    # Construct new line
    new_line = f'{indent}[{varname}](roles/containers_anubis.md#{anchor_name}){rest}'
    print(f'New line: {new_line}')
else:
    print('Regex did not match')
    print('Sample line:', repr(sample_line))
    # The actual format is different: - [varname](path#anchor)
    # So let's try a different pattern
    m_var2 = re.match(r'^(\s*-\s+\[)([a-zA-Z0-9_]+)(\].*#)([a-zA-Z0-9_]+)(\).*)$', sample_line)
    if m_var2:
        print('Alternative pattern matched:', m_var2.groups())
        prefix, varname, mid, anchor, suffix = m_var2.groups()
        print(f'Prefix: "{prefix}", Varname: "{varname}", Mid: "{mid}", Anchor: "{anchor}", Suffix: "{suffix}"')
    else:
        print('Even alternative pattern did not match')
        # Try the exact format
        m_var3 = re.match(r'^(\s*-\s+\[)([a-zA-Z0-9_]+)(\]\()(.*#)([a-zA-Z0-9_]+)(\).*)$', sample_line)
        if m_var3:
            print('Third pattern matched:', m_var3.groups())
        else:
            print('No pattern matched')