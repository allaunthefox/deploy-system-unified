#!/usr/bin/env python3
"""Test script to replicate the exact linter logic."""

import re
from pathlib import Path

# Replicate the exact linter logic
root = Path('wiki_pages')
mds = sorted([p for p in root.rglob('*.md') if p.name != '_Sidebar.md'])

# Preload headers for each file (like the linter does)
file_headers = {}
for p in mds:
    # Store the relative path from root as the key
    relative_path = p.relative_to(root)
    txt = p.read_text(encoding='utf-8')
    headers = re.findall(r'^(#+)\s*(.+)$', txt, flags=re.M)
    file_headers[str(relative_path)] = [(h, l.strip()) for h, l in headers]

print("File headers map for roles/containers_anubis.md:")
if 'roles/containers_anubis.md' in file_headers:
    headers = file_headers['roles/containers_anubis.md']
    print(f"Found {len(headers)} headers:")
    for i, (level, header) in enumerate(headers):
        print(f"  {i+1}. Level {len(level)}: '{header}'")
        
    # Apply the exact same slugify as the linter
    slug_re = re.compile(r'[^a-z0-9 -]')
    def slugify(s):
        s = s.lower()
        s = slug_re.sub('', s)
        s = re.sub(r'\s+', '-', s)
        s = re.sub(r'-+', '-', s)
        return s.strip('-')
    
    slugs = set(slugify(h.strip()) for _, h in headers)
    print(f"\nGenerated slugs:")
    for slug in sorted(slugs):
        if 'anubis' in slug:
            print(f"  - {slug}")
    
    # Check specific anchors
    test_anchors = ['anubisenabled', 'anubisport', 'anubisdifficulty']
    print(f"\nChecking specific anchors:")
    for anchor in test_anchors:
        exists = anchor in slugs
        print(f"  - {anchor}: {'EXISTS' if exists else 'MISSING'}")
else:
    print("File roles/containers_anubis.md not found in file_headers")
    print("Available keys with 'anubis':")
    for key in file_headers:
        if 'anubis' in key:
            print(f"  - {key}")

# Also test the variable reference file link processing
var_ref_file = root / 'Variable_Reference_Containers.md'
if var_ref_file.exists():
    var_content = var_ref_file.read_text()
    print(f"\nLinks found in Variable_Reference_Containers.md pointing to containers_anubis.md:")
    for link in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', var_content):
        link_text, link_target = link
        if 'containers_anubis.md#' in link_target:
            if '#' in link_target:
                pagepart, anchorpart = link_target.split('#', 1)
            else:
                continue
            # normalize pagepart
            pagefile = pagepart if pagepart.endswith('.md') else pagepart + '.md'
            
            print(f"  - Link: [{link_text}]({link_target}) -> pagefile: {pagefile}, anchor: {anchorpart}")
            
            # Check if target file exists in headers map
            if pagefile in file_headers:
                other_headers = [h for _, h in file_headers[pagefile]]
                other_slugs = set(slugify(h.strip()) for h in other_headers)
                anchor_exists = anchorpart in other_slugs
                print(f"    Target file exists with {len(other_headers)} headers, anchor '{anchorpart}': {'EXISTS' if anchor_exists else 'MISSING'}")
            else:
                print(f"    ERROR: Target file {pagefile} not found in file_headers")