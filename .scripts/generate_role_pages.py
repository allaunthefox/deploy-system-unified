#!/usr/bin/env python3
"""Generate per-role pages from Role_Reference.md and add 'Read details' links.

Behavior:
- Parse wiki_pages/Role_Reference.md for lines starting with "### `role/name`".
- Capture the following paragraph(s) (until next "### " or EOF).
- Create wiki_pages/roles/<role_with_slash_replaced_by_underscore>.md with H1 equal to the filename (without .md) to match linter rules.
- Update Role_Reference.md to append a ' — [Read details](roles/<file>.md)' link on the same header line.

Run this script from the repo root.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RR = ROOT / 'wiki_pages' / 'Role_Reference.md'
OUT_DIR = ROOT / 'wiki_pages' / 'roles'
OUT_DIR.mkdir(parents=True, exist_ok=True)

text = RR.read_text()
lines = text.splitlines()

roles = []
for i, line in enumerate(lines):
    if line.startswith('### `') and line.endswith('`'):
        role = line.split('### `',1)[1].rsplit('`',1)[0]
        roles.append((i, role))

# Extract content blocks
role_blocks = {}
for idx, role in roles:
    # Start from next line
    j = idx+1
    block_lines = []
    while j < len(lines) and not lines[j].startswith('### `'):
        block_lines.append(lines[j])
        j += 1
    # Trim leading/trailing blank lines
    while block_lines and block_lines[0].strip() == '':
        block_lines.pop(0)
    while block_lines and block_lines[-1].strip() == '':
        block_lines.pop()
    role_blocks[role] = '\n'.join(block_lines)

# Create role pages
for role, body in role_blocks.items():
    filename = role.replace('/', '_') + '.md'
    filepath = OUT_DIR / filename
    h1 = filename[:-3]
    content_lines = [f'# {h1}', '', f'**role**: `{role}`', '']
    if body:
        content_lines.append(body)
    else:
        content_lines.append('TODO: Add role description and examples.')
    content = '\n'.join(content_lines)+"\n"
    if filepath.exists():
        # don't overwrite existing content, but if file was only a placeholder, we may update
        existing = filepath.read_text()
        if 'TODO: Add role description' in existing:
            filepath.write_text(content)
    else:
        filepath.write_text(content)

# Update Role_Reference.md: add link next to each header line
new_lines = []
for line in lines:
    if line.startswith('### `') and line.endswith('`'):
        role = line.split('### `',1)[1].rsplit('`',1)[0]
        filename = role.replace('/', '_') + '.md'
        new_line = f"{line} — [Read details](roles/{filename})"
        new_lines.append(new_line)
    else:
        new_lines.append(line)

RR.write_text('\n'.join(new_lines) + '\n')
print('Generated', len(role_blocks), 'role pages and updated Role_Reference.md')
