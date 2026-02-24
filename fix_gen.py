#!/usr/bin/env python3

with open('.scripts/generate_role_pages.py', 'r') as f:
    content = f.read()

old = "content_lines.append(f'### `{varname}`{#" + '{varname.replace("_", "")}' + "}')"
new = "content_lines.append(f'<a id=\"{varname.replace("_", "-")}"></a>### `{varname}`')"

content = content.replace(old, new)

with open('.scripts/generate_role_pages.py', 'w') as f:
    f.write(content)

print("Fixed!")
