import re

line = '- `[anubis_enabled](roles/containers_anubis.md#anubis_enabled)`'
pattern = r'^(\s*-\s+`)(\[)([a-zA-Z0-9_]+)(\])(\()(.*)#([a-zA-Z0-9_]+)(\).*)$'
m_var = re.match(pattern, line)
if m_var:
    print('Match found:', m_var.groups())
    prefix, bracket_open, varname, bracket_close, paren_open, path_part, anchor, suffix = m_var.groups()
    print(f'Prefix: "{prefix}"')
    print(f'Bracket open: "{bracket_open}"')
    print(f'Varname: "{varname}"')
    print(f'Bracket close: "{bracket_close}"')
    print(f'Paren open: "{paren_open}"')
    print(f'Path part: "{path_part}"')
    print(f'Anchor: "{anchor}"')
    print(f'Suffix: "{suffix}"')
    
    # Test slugify
    slug_re = re.compile(r'[^a-z0-9 -]')
    def slugify(s):
        s = s.lower()
        s = slug_re.sub('', s)
        s = re.sub(r'\s+', '-', s)
        s = re.sub(r'-+', '-', s)
        return s.strip('-')

    anchor_name = slugify(varname)
    print(f'Original anchor: {anchor}, slugified: {anchor_name}')
    new_line = f'{prefix}{bracket_open}{varname}{bracket_close}{paren_open}{path_part}#{anchor_name}{suffix}'
    print(f'New line: {new_line}')
else:
    print('No match')
    print('Line format:', repr(line))