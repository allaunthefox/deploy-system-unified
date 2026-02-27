import os
import re
from pathlib import Path

ROOT = Path('.').resolve()
WIKI_DIR = ROOT / 'wiki_pages'
PROJECT_ROLES = ROOT / 'deploy-system-unified' / 'roles'
ROLE_REF = WIKI_DIR / 'ROLE_REFERENCE.md'

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

def get_roles_by_category():
    """Build a map of category => [roles] from ROLE_REFERENCE.md."""
    if not ROLE_REF.exists():
        return {}
    
    content = ROLE_REF.read_text()
    categories = {}
    current_category = None
    
    for line in content.splitlines():
        # Match ## Category Roles
        m_cat = re.match(r'^##\s+(.+)\s+Roles', line)
        if m_cat:
            current_category = m_cat.group(1).strip()
            categories[current_category] = []
            continue
            
        # Match ### `subsystem/role`
        m_role = re.match(r'^###\s+`([^`]+)`', line)
        if m_role and current_category:
            categories[current_category].append(m_role.group(1).strip())
            
    return categories

def process_categories():
    roles_map = get_roles_by_category()
    
    # Category-to-file mapping must follow the canonical
    # SCREAMING_SNAKE_CASE naming that the wiki now uses.  Older commits
    # attempted to reference `REF_Vars_*` variants, which no longer
    # exist.
    categories_to_files = {
        'Containers': 'REF_VARS_CONTAINERS.md',
        'Core': 'REF_VARS_CORE.md',
        'Security': 'REF_VARS_SECURITY.md',
        'Networking': 'REF_VARS_NETWORKING.md',
        'Storage': 'REF_VARS_STORAGE.md'
    }
    
    for cat_name, filename in categories_to_files.items():
        print(f"Processing {filename} ({cat_name})...")
        file_path = WIKI_DIR / filename
        roles = roles_map.get(cat_name, [])
        
        if not roles:
            print(f"  WARNING: No roles found for category {cat_name}")
        
        new_lines = [f"# {filename[:-3]}", "", f"## {cat_name} Variables", ""]
        
        for role_name in sorted(roles):
            new_lines.append(f"### `{role_name}`")
            role_vars = extract_variables(role_name)
            
            if role_vars:
                role_md_file = role_name.replace('/', '_') + '.md'
                for v in role_vars:
                    anchor = slugify(v)
                    new_lines.append(f'- [`{v}`](roles/{role_md_file}#{anchor})')
                new_lines.append('')
            else:
                new_lines.append('- *No variables defined in defaults/main.yml*')
                new_lines.append('')
                
        file_path.write_text('\n'.join(new_lines) + '\n')

process_categories()
print("Synchronization complete.")
