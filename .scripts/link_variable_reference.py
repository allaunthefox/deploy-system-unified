#!/usr/bin/env python3
"""Script to link Variable_Reference.md to role pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VR = ROOT / 'wiki_pages' / 'Variable_Reference.md'

text = VR.read_text()
lines = text.splitlines()

current_role_file = None
new_lines = []

for line in lines:
    # Match role header
    m_role = re.match(r'^### `([^`]+)`', line)
    if m_role:
        role_name = m_role.group(1)
        current_role_file = f"roles/{role_name.replace('/', '_')}.md"
        new_lines.append(line)
        continue

    # Match variable line
    m_var = re.match(r'^(\s*-\s+`)([a-zA-Z0-9_]+)(`.*)$', line)
    if m_var and current_role_file:
        indent, varname, rest = m_var.groups()
        # Link to the anchor in the role page
        new_line = f'{indent}[{varname}]({current_role_file}#{varname}){rest}'
        new_lines.append(new_line)
    else:
        new_lines.append(line)

VR.write_text('\n'.join(new_lines) + '\n')
print("Linked Variable_Reference.md to role pages.")
