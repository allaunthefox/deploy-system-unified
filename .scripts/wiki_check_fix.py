#!/usr/bin/env python3
import re, sys
from pathlib import Path
root = Path("wiki_pages")
mds = sorted([p for p in root.glob("*.md") if p.name != "_Sidebar.md"])
slug_re = re.compile(r'[^a-z0-9 -]')

def slugify(s):
    s = s.lower()
    s = slug_re.sub('', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

missing_pages = set()
missing_anchors = []
modified = []

# Preload headers for each file
file_headers = {}
for p in mds:
    txt = p.read_text(encoding='utf-8')
    headers = re.findall(r'^(#+)\s*(.+)$', txt, flags=re.M)
    file_headers[p.name] = [ (h,l.strip()) for h,l in headers ]

for p in mds:
    name = p.stem
    txt = p.read_text(encoding='utf-8')
    # find first H1
    m = re.search(r'^#\s*(.+)$', txt, flags=re.M)
    h1 = m.group(1).strip() if m else None
    need_change = False
    if h1 is None:
        # insert H1 at top
        newtxt = f"# {name}\n\n" + txt
        txt = newtxt
        need_change = True
        print(f"MISSING_H1: {p.name} -> inserted '# {name}'")
    elif h1 != name:
        # replace only the first H1 line
        newtxt = re.sub(r'^(#\s*).+$', r'\1' + name, txt, count=1, flags=re.M)
        txt = newtxt
        need_change = True
        print(f"MISMATCH_H1: {p.name} -> changed H1 '{h1}' to '# {name}'")
    # collect header slugs for anchors in this file (after possible change)
    headers = re.findall(r'^(#+)\s*(.+)$', txt, flags=re.M)
    slugs = set(slugify(h.strip()) for _,h in headers)

    # link checking
    for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', txt):
        target = link.strip()
        if re.match(r'^[a-z]+://', target) or target.startswith('mailto:'):
            continue
        if target.startswith('#'):
            anchor = target[1:]
            if anchor not in slugs:
                missing_anchors.append((p.name, target, 'local'))
        else:
            if '#' in target:
                pagepart, anchorpart = target.split('#',1)
            else:
                pagepart, anchorpart = target, None
            # normalize pagepart
            pagefile = pagepart if pagepart.endswith('.md') else pagepart + '.md'
            if not (root / pagefile).exists():
                missing_pages.add((p.name, target))
            else:
                if anchorpart:
                    other_headers = [h for _,h in file_headers.get(pagefile, [])]
                    other_slugs = set(slugify(h.strip()) for h in other_headers)
                    if anchorpart not in other_slugs:
                        missing_anchors.append((p.name, target, 'external'))
    if need_change:
        p.write_text(txt, encoding='utf-8')
        modified.append(p.name)

print('\nSummary:')
print(f'Files scanned: {len(mds)}')
print(f'Files modified (H1 fixes): {len(modified)}')
if modified:
    for m in modified: print('  -', m)

if missing_pages:
    print('\nMissing page links detected:')
    for src,t in sorted(missing_pages):
        print(f'  - In {src}: link to missing page "{t}"')
else:
    print('\nNo missing page links found.')

if missing_anchors:
    print('\nMissing anchors detected:')
    for src,t,kind in missing_anchors:
        print(f'  - In {src}: link "{t}" -> missing anchor ({kind})')
else:
    print('\nNo missing anchors found.')

# exit with non-zero if broken links present
if missing_pages or missing_anchors:
    sys.exit(2)
else:
    sys.exit(0)
