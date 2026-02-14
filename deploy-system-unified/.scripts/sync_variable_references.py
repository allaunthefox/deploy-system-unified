import os
import re
from pathlib import Path

ROOT = Path('.').resolve()
WIKI_DIR = ROOT / 'wiki_pages'
PROJECT_ROLES = ROOT / 'projects' / 'deploy-system-unified' / 'roles'

def slugify(s):
    # Using the same slugify as the linter
    s = s.lower()
    s = re.sub(r'[^a-z0-9 -]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def extract_variables(role_path):
    defaults_file = PROJECT_ROLES / role_path / 'defaults' / 'main.yml'
    if not defaults_file.exists():
        return []

    vars_found = []
    content = defaults_file.read_text()
    for line in content.splitlines():
        if line.startswith('#') or line.strip() == '---' or not line.strip():
            continue
        m = re.match(r'^([a-zA-Z0-9_]+):', line)
        if m:
            vars_found.append(m.group(1))
    return vars_found

def process_file(file_path):
    print(f"Processing {file_path.name}...")
    content = file_path.read_text()
    lines = content.splitlines()
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Match role header: ### `subsystem/role`
        m_role = re.match(r'^### `([^`]+)`', line)
        if m_role:
            role_name = m_role.group(1)
            role_vars = extract_variables(role_name)
            
            # Skip existing variable list
            i += 1
            # Skip lines that are links or empty or "No variables" placeholders
            # Matches both: - `[var](link)` and - [`var`](link)
            while i < len(lines) and (lines[i].strip().startswith('-') or not lines[i].strip()):
                if lines[i].strip().startswith('###'): # Don't skip next header
                    break
                i += 1
            
            # Add new variable list
            if role_vars:
                role_md_file = role_name.replace('/', '_') + '.md'
                for v in role_vars:
                    anchor = slugify(v)
                    new_lines.append(f'- [`{v}`](roles/{role_md_file}#{anchor})')
                new_lines.append('')
            else:
                new_lines.append('- *No variables defined in defaults/main.yml*')
                new_lines.append('')
            
            # Since we incremented i, we need to continue without adding the line again
            continue
        
        i += 1
        
    file_path.write_text('
'.join(new_lines) + '
')

vr_files = [
    'Variable_Reference_Containers.md',
    'Variable_Reference_Core.md',
    'Variable_Reference_Security.md',
    'Variable_Reference_Networking.md',
    'Variable_Reference_Storage.md'
]

for filename in vr_files:
    p = WIKI_DIR / filename
    if p.exists():
        process_file(p)

print("Synchronization complete.")
