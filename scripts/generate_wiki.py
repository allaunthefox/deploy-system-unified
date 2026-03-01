#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500100
# Script Type: Wiki Generation
# Description: Generates and prepares wiki pages from documentation and roles
# Last Updated: 2026-03-01
# Version: 1.1
# =============================================================================
import os
import re
import shutil
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROLES_DIR = PROJECT_ROOT / 'roles'
DOCS_DIR = PROJECT_ROOT / 'docs'
WIKI_DIR = PROJECT_ROOT / 'wiki_pages'
STANDARD_DIRS = ['defaults', 'files', 'handlers', 'meta', 'tasks', 'templates', 'vars', 'molecule', 'tests']
SPECIAL_MAPS = {
    'README.md': 'Home',
    'INDEX.md': 'Documentation_Index'
}
STATUS_MAPS = {
    'GPU_SLICING.md': '⚠️ **UNTESTABLE**: This feature is postponed indefinitely until hardware access is secured.',
    'INTEL_GPU_GUIDE.md': '⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.',
    'GPU_ENHANCED_PLAN.md': '⚠️ **UNTESTABLE**: Active development and testing are suspended.',
    'GPU_STACK_SETUP.md': '⚠️ **UNTESTABLE**: Hardware verification gates are currently blocked.',
    'ARCH_ARM64.md': '🧪 **EXPERIMENTAL**: Deployment on aarch64 is currently in early-stage testing.',
    'ARCH_RISCV64.md': '⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.'
}

# Regex Patterns
VAR_PATTERN = re.compile(r'^([a-zA-Z0-9_]+):', re.MULTILINE)
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def extract_role_info(role_path):
    """Extract name and summary from role's readme.md."""
    readme = role_path / 'readme.md'
    if not readme.exists():
        # Try uppercase README.md
        readme = role_path / 'README.md'
    
    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        lines = content.split('\n')
        if not lines:
            return role_path.name, ''
        
        # First line is usually the title
        name = lines[0].strip('# ').strip()
        
        # Summary is the first non-empty line that isn't a header
        summary = ''
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('#'):
                summary = line
                break
        return name, summary
    
    return role_path.name, ''

def extract_variables(role_path):
    """Extract top-level variables from defaults/main.yml."""
    defaults = role_path / 'defaults' / 'main.yml'
    if defaults.exists():
        content = defaults.read_text(encoding='utf-8')
        return VAR_PATTERN.findall(content)
    return []

def generate_references():
    """Generate ROLE_REFERENCE.md and VARIABLE_REFERENCE.md."""
    role_ref = ['# Role Reference\n\n']
    var_ref = ['# Variable Reference\n\n']
    
    if not ROLES_DIR.exists():
        print(f"Warning: Roles directory not found at {ROLES_DIR}")
        return
    
    groups = sorted([d for d in ROLES_DIR.iterdir() if d.is_dir() and not d.name.startswith('.') and d.name not in STANDARD_DIRS])
    
    for group_path in groups:
        group = group_path.name
        role_ref.append(f'## {group.capitalize()} Roles\n\n')
        var_ref.append(f'## {group.capitalize()} Variables\n\n')
        
        roles = sorted([d for d in group_path.iterdir() if d.is_dir() and not d.name.startswith('.') and d.name not in STANDARD_DIRS])
        
        for role_path in roles:
            role = role_path.name
            name, summary = extract_role_info(role_path)
            role_ref.append(f'### `{group}/{role}`\n**{name}**\n\n{summary}\n\n')
            
            vars_list = extract_variables(role_path)
            if vars_list:
                var_ref.append(f'### `{group}/{role}`\n')
                for v in vars_list:
                    var_ref.append(f'- `{v}`\n')
                var_ref.append('\n')
    
    (WIKI_DIR / 'ROLE_REFERENCE.md').write_text(''.join(role_ref), encoding='utf-8')
    (WIKI_DIR / 'VARIABLE_REFERENCE.md').write_text(''.join(var_ref), encoding='utf-8')
    print('References generated successfully.')

def sync_docs():
    """Sync docs and other files to wiki_pages."""
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copy all .md files from docs (depth 2)
    for md_file in DOCS_DIR.glob('**/*.md'):
        # Check depth (relative to docs)
        depth = len(md_file.relative_to(DOCS_DIR).parts)
        if depth <= 2:
            shutil.copy2(md_file, WIKI_DIR / md_file.name)
    
    # Copy special files
    shutil.copy2(PROJECT_ROOT / 'README.md', WIKI_DIR / 'Home.md')
    if (DOCS_DIR / 'INDEX.md').exists():
        shutil.copy2(DOCS_DIR / 'INDEX.md', WIKI_DIR / 'Documentation_Index.md')
    
    print('Documentation files synced.')

def apply_fixes():
    """Apply string replacements and sanitize links."""
    replacements = {
        'preflight_assertions.yml': 'preflight_gate.yml',
        'preflight_validate.yml': 'preflight_gate.yml'
    }
    
    def sanitize_link(match):
        text = match.group(1)
        full_link = match.group(2)
        
        if full_link.startswith(('http', 'mailto:', 'ftp:')):
            return match.group(0)
        
        filename = os.path.basename(full_link)
        anchor = ''
        if '#' in filename:
            filename, anchor = filename.split('#', 1)
            anchor = '#' + anchor
        
        # Use map or strip .md
        wiki_name = SPECIAL_MAPS.get(filename, filename.replace('.md', ''))
        return f'[{text}]({wiki_name}{anchor})'

    for md_file in WIKI_DIR.glob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        
        # Prepend status warning if applicable
        if md_file.name in STATUS_MAPS:
            content = f"> {STATUS_MAPS[md_file.name]}\n\n{content}"
            
        # Apply replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Sanitize links
        content = LINK_PATTERN.sub(sanitize_link, content)
        
        md_file.write_text(content, encoding='utf-8')
    
    print('Fixes and link sanitization applied.')

def generate_sidebar():
    """Generate _Sidebar.md."""
    content = """### [Home](Home)
- [Role Reference](ROLE_REFERENCE)
- [Variable Reference](VARIABLE_REFERENCE)
### [Documentation Index](Documentation_Index)

---

### 🏛️ Architecture
- [Ontology & Profiles](ONTOLOGY)
- [Modular Layers](MODULAR_LAYERS)
- [Layered Security](LAYERED_SECURITY)
- [Ephemeral Design](EPHEMERAL_DESIGN)
- [Core Philosophy](NON_COMINGLING)
- [Virtual Networking](VIRTUAL_NETWORKING)
- [Backup Strategy](BACKUP_STRATEGY)
- [GPU Slicing](GPU_SLICING)

---

### 💻 Development
- [Contributing](CONTRIBUTING)
- [Style Guide](STYLE_GUIDE)
- [Pre-commit Hooks](PRE_COMMIT)
- [Tooling](TOOLING)
- [LLM Context Map](LLM_MAP)

---

### 🚀 Deployment
- [Universal SOP](UNIVERSAL_DEPLOYMENT_GUIDE)
- [Deployment Status](DEPLOYMENT_STATUS)
- [Examples](EXAMPLES)
- [OS Configuration](OS_CONFIGURATION)
- [SSH Idempotence](SSH_IDEMPOTENCE_GUARDRAILS)
- [Security Hybrid Setup](SECURITY_CROWDSEC_HYBRID)

---

### 📅 Planning
- [Stability Plan 2026](STABILITY_EXECUTION_PLAN_2026)
- [Migration Plan](MIGRATION_PLAN)
- [Restructuring Plan](RESTRUCTURING_PLAN_2026)
- [GPU Enhanced Plan](GPU_ENHANCED_PLAN)
"""
    (WIKI_DIR / '_Sidebar.md').write_text(content, encoding='utf-8')
    print('Sidebar generated.')

def main():
    print('Starting Wiki Generation...')
    sync_docs()
    generate_references()
    apply_fixes()
    generate_sidebar()
    print('Wiki Generation Complete!')

if __name__ == '__main__':
    main()
