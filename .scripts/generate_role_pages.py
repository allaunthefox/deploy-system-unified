#!/usr/bin/env python3
"""Script to generate role pages from Role_Reference.md."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RR = ROOT / 'wiki_pages' / 'Role_Reference.md'
OUT_DIR = ROOT / 'wiki_pages' / 'roles'
PROJECT_ROLES = ROOT / 'roles'

OUT_DIR.mkdir(parents=True, exist_ok=True)

text = RR.read_text()
lines = text.splitlines()

roles = []
for i, line in enumerate(lines):
    if line.startswith('### `'):
        try:
            role = line.split('`', 1)[1].split('`', 1)[0]
            roles.append((i, role))
        except IndexError:
            continue

role_blocks = {}
for idx, role in roles:
    j = idx + 1
    block_lines = []
    while j < len(lines) and not lines[j].startswith('### `'):
        block_lines.append(lines[j])
        j += 1
    while block_lines and block_lines[0].strip() == '':
        block_lines.pop(0)
    while block_lines and block_lines[-1].strip() == '':
        block_lines.pop()
    role_blocks[role] = '\n'.join(block_lines)


def extract_variables(role_path):
    """Extract variables from defaults/main.yml of a role."""
    defaults_file = PROJECT_ROLES / role_path / 'defaults' / 'main.yml'
    if not defaults_file.exists():
        return []

    vars_found = []
    content = defaults_file.read_text()
    # Simple parser for top-level keys and comments
    # Matches "key: value # comment" or just "key: value"
    # Ignores indented keys (sub-keys) for now to keep it simple
    for line in content.splitlines():
        if line.startswith('#') or line.strip() == '---' or not line.strip():
            continue
        m = re.match(r'^([a-zA-Z0-9_]+):\s*(.*)$', line)
        if m:
            varname = m.group(1)
            val_and_comment = m.group(2)
            comment = ""
            if '#' in val_and_comment:
                comment = val_and_comment.split('#', 1)[1].strip()
            vars_found.append((varname, comment))
    return vars_found


for role, body in role_blocks.items():
    filename = role.replace('/', '_') + '.md'
    filepath = OUT_DIR / filename
    h1 = filename[:-3]

    content_lines = [f'# {h1}', '', f'**role**: `{role}`', '']

    if body:
        content_lines.append(body)
        content_lines.append('')

    # Always try to append Variables section
    vars_list = extract_variables(role)
    if vars_list:
        content_lines.append('## Variables')
        content_lines.append('')
        for varname, comment in vars_list:
            # Create a heading that will slugify to the variable name with underscores removed
            # Since the linter removes underscores during slugification, we need to make sure
            # the links also use the underscore-removed version
            content_lines.append(f'### `{varname}`{{#{varname.replace("_", "")}}}')
            line = f'- `{varname}`'
            if comment:
                line += f' — {comment}'
            content_lines.append(line)
            content_lines.append('')
        content_lines.append('')
    elif not body:
        content_lines.append('TODO: Add role description and examples.')

    content = '\n'.join(content_lines) + "\n"
    filepath.write_text(content)

new_lines = []
for line in lines:
    if line.startswith('### `') and ' — [Read details]' not in line:
        try:
            role = line.split('`', 1)[1].split('`', 1)[0]
            filename = role.replace('/', '_') + '.md'
            new_line = f"{line} — [Read details](roles/{filename})"
            new_lines.append(new_line)
        except IndexError:
            new_lines.append(line)
    else:
        new_lines.append(line)

RR.write_text('\n'.join(new_lines) + '\n')
print('Generated', len(role_blocks), 'role pages with variables and updated Role_Reference.md')
