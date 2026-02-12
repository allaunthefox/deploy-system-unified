#!/usr/bin/env python3
"""Test the exact logic from the script."""

import re

# Read the actual content from the file
with open('/home/prod/Workspaces/wiki_pages/Variable_Reference_Containers.md', 'r') as f:
    content = f.read()

lines = content.splitlines()
current_role_file = None
new_lines = []

for line_num, line in enumerate(lines[:10]):  # Just first 10 lines for testing
    print(f"Line {line_num}: {repr(line)}")
    
    # Match role header
    m_role = re.match(r'^### `([^`]+)`', line)
    if m_role:
        role_name = m_role.group(1)
        current_role_file = f"roles/{role_name.replace('/', '_')}.md"
        print(f"  -> Found role: {role_name}, current_role_file: {current_role_file}")
        new_lines.append(line)
        continue

    # Match variable line in format: - `[varname]`(path#anchor)
    m_var = re.match(r'^(\s*-\s+`)(\[)([a-zA-Z0-9_]+)(\])(\].*#)([a-zA-Z0-9_]+)(\).*)$', line)
    if m_var and current_role_file:
        prefix, bracket_open, varname, bracket_close, mid, anchor, suffix = m_var.groups()
        print(f"  -> Found variable: {varname}, anchor: {anchor}")
        
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
        print(f"  -> Original anchor: {anchor}, slugified anchor: {anchor_name}")
        new_line = f'{prefix}{bracket_open}{varname}{bracket_close}{mid}{anchor_name}{suffix}'
        print(f"  -> New line: {new_line}")
        new_lines.append(new_line)
    else:
        if m_var:
            print(f"  -> Match found but no current_role_file: {bool(current_role_file)}")
        else:
            print(f"  -> No match for variable pattern")
        new_lines.append(line)

print("\nFirst few lines of result:")
for i, line in enumerate(new_lines):
    if i < 10:
        print(f"{i}: {repr(line)}")