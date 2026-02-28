#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500014
# Script Type: Repository Maintenance
# Description: Fixes generate_role_pages.py anchor format
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================

with open('.scripts/generate_role_pages.py', 'r') as f:
    content = f.read()

old = "content_lines.append(f'### `{varname}`{#" + '{varname.replace("_", "")}' + "}')"
new = "content_lines.append(f'<a id=\"{varname.replace("_", "-")}"></a>### `{varname}`')"

content = content.replace(old, new)

with open('.scripts/generate_role_pages.py', 'w') as f:
    f.write(content)

print("Fixed!")
