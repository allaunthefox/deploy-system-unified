#!/usr/bin/env python3
"""Script to link Variable_Reference.md and its split counterparts to role pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Use the same slugify function as the linter to match what it expects
slug_re = re.compile(r'[^a-z0-9 -]')
def slugify(s):
    s = s.lower()
    s = slug_re.sub('', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def process_file(filepath):
    """Process a variable reference file to update anchors to match linter's slugify."""
    if not filepath.exists():
        return False
    
    text = filepath.read_text()
    lines = text.splitlines()

    current_role_file = None
    new_lines = []
    modified = False

    for line in lines:
        # Match role header
        m_role = re.match(r'^### `([^`]+)`', line)
        if m_role:
            role_name = m_role.group(1)
            current_role_file = f"roles/{role_name.replace('/', '_')}.md"
            new_lines.append(line)
            continue

        # Match variable line in format: - `[varname](path#anchor)`
        # Updated regex to allow hyphens in anchor (existing files may have them)
        m_var = re.match(r'^(\s*-\s+\[\`)([a-zA-Z0-9_]+)(\`\]\()(.*)#([a-zA-Z0-9_-]+)(\).*)$', line)
        if m_var and current_role_file:
            prefix, varname, middle, path_part, old_anchor, suffix = m_var.groups()
            # Generate the correct anchor using slugify
            anchor_name = slugify(varname)
            if old_anchor != anchor_name:
                modified = True
                new_line = f'{prefix}{varname}{middle}{path_part}#{anchor_name}{suffix}'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if modified:
        filepath.write_text('\n'.join(new_lines) + '\n')
        return True
    return False


# Handle the main Variable_Reference.md file
VR = ROOT / 'wiki_pages' / 'Variable_Reference.md'
if process_file(VR):
    print("Linked Variable_Reference.md to role pages.")
else:
    print("Variable_Reference.md already up to date.")

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
    if process_file(vr_split):
        print(f"Linked {filename} to role pages.")
    else:
        print(f"{filename} already up to date.")

print("All variable reference files linked to role pages.")
