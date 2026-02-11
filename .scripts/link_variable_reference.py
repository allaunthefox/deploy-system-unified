#!/usr/bin/env python3
"""Script to link Variable_Reference.md and its split counterparts to role pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Handle the main Variable_Reference.md file
VR = ROOT / 'wiki_pages' / 'Variable_Reference.md'
if VR.exists():
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

        # Match variable line in format: - `[varname](path#anchor)`
        m_var = re.match(r'^(\s*-\s+`)(\[)([a-zA-Z0-9_]+)(\])(\()(.*)#([a-zA-Z0-9_]+)(\).*)$', line)
        if m_var and current_role_file:
            prefix, bracket_open, varname, bracket_close, paren_open, path_part, anchor, suffix = m_var.groups()
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
            new_line = f'{prefix}{bracket_open}{varname}{bracket_close}{paren_open}{path_part}#{anchor_name}{suffix}'
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    VR.write_text('\n'.join(new_lines) + '\n')
    print("Linked Variable_Reference.md to role pages.")

# Handle the split variable reference files
split_files = [
    'Variable_Reference_Containers.md',
    'Variable_Reference_Core.md', 
    'Variable_Reference_Security.md',
    'Variable_Reference_Networking.md',
    'Variable_Reference_Storage.md'
]

for filename in split_files:
    vr_split = ROOT / 'wiki_pages' / filename
    if vr_split.exists():
        text = vr_split.read_text()
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

            # Match variable line in format: - `[varname](path#anchor)`
            m_var = re.match(r'^(\s*-\s+`)(\[)([a-zA-Z0-9_]+)(\])(\()(.*)#([a-zA-Z0-9_]+)(\).*)$', line)
            if m_var and current_role_file:
                prefix, bracket_open, varname, bracket_close, paren_open, path_part, anchor, suffix = m_var.groups()
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
                new_line = f'{prefix}{bracket_open}{varname}{bracket_close}{paren_open}{path_part}#{anchor_name}{suffix}'
                new_lines.append(new_line)
            else:
                new_lines.append(line)

        vr_split.write_text('\n'.join(new_lines) + '\n')
        print(f"Linked {filename} to role pages.")

print("All variable reference files linked to role pages.")