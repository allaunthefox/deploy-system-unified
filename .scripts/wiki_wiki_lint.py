#!/usr/bin/env python3
"""
wiki_wiki_lint.py — enforce GitHub Wiki style and accessibility rules for repo documentation

Usage:
  python3 .scripts/wiki_wiki_lint.py [--paths paths] [--fix-h1] [--create-placeholders] [--json]

By default this scans these folders (if present):
 - wiki_pages
 - wiki_audit
 - wiki_crowdsec_audit
 - wiki_clean_sync
 - projects/deploy-system-unified/docs

Checks performed (errors -> non-zero exit):
 - H1 exists and matches filename (optional auto-fix with --fix-h1)
 - Markdown link targets exist (pages/anchors); missing pages and missing anchors are errors
 - Image files referenced must exist (error)

Warnings (exit code 1) include:
 - Markdown links pointing at YAML files (recommend linking to a wiki page instead)
 - Images with empty alt text
 - Use of raw HTML <img> tags

The script exits:
 - 0 when no problems
 - 1 when only warnings
 - 2 when there are errors

This script is intended to be run when updating the git wiki to avoid broken links
and accessibility regressions.
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_PATHS = [
    Path('wiki_pages'),
    Path('wiki_audit'),
    Path('wiki_crowdsec_audit'),
    Path('wiki_clean_sync'),
    Path('deploy-system-unified/docs'),
]

LINK_RE = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
HEADING_RE = re.compile(r'^(#+)\s*(.+)$', flags=re.M)

slug_re = re.compile(r'[^a-z0-9 -]')
def slugify(s: str) -> str:
    s = s.lower()
    s = slug_re.sub('', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def read_file_safe(path: Path):
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return None


def scan_files(paths, fix_h1=False, create_placeholders=False):
    md_files = []
    for p in paths:
        if p.exists():
            md_files.extend(sorted(p.rglob('*.md')))

    results = {
        'files_scanned': len(md_files),
        'errors': [],
        'warnings': [],
        'fixed': []
    }

    # Build a map of file => headings (slugs)
    headings_map = {}
    for f in md_files:
        txt = read_file_safe(f)
        if txt is None:
            results['warnings'].append(('unreadable', str(f)))
            continue
        headers = [(m.group(1), m.group(2).strip()) for m in HEADING_RE.finditer(txt)]
        headings_map[str(f)] = set(slugify(h) for _, h in headers)

    for f in md_files:
        txt = read_file_safe(f)
        if txt is None:
            continue
        fname = f.stem
        # H1 check
        m = re.search(r'^#\s*(.+)$', txt, flags=re.M)
        h1 = m.group(1).strip() if m else None
        if h1 is None:
            msg = f'MISSING_H1: {f}'
            if fix_h1:
                newtxt = f"# {fname}\n\n" + txt
                f.write_text(newtxt, encoding='utf-8')
                results['fixed'].append(('insert_h1', str(f)))
            else:
                results['errors'].append(('missing_h1', str(f)))
        elif h1 != fname:
            msg = f'MISMATCH_H1: {f} -> "{h1}" vs "{fname}"'
            if fix_h1:
                newtxt = re.sub(r'^(#\s*).+$', r'\1' + fname, txt, count=1, flags=re.M)
                f.write_text(newtxt, encoding='utf-8')
                results['fixed'].append(('fix_h1', str(f)))
            else:
                results['warnings'].append(('h1_mismatch', str(f), h1, fname))

        # Image checks
        for m in IMG_RE.finditer(txt):
            alt = m.group(1).strip()
            target = m.group(2).split()[0]
            if alt == '':
                results['warnings'].append(('img_missing_alt', str(f), target))
            if not re.match(r'https?://', target):
                target_path = (f.parent / target).with_name(Path(target).name)
                if not target_path.exists():
                    results['errors'].append(('img_missing_file', str(f), target))
        if '<img' in txt:
            results['warnings'].append(('html_img_tag', str(f)))

        # Link checks
        for m in LINK_RE.finditer(txt):
            target = m.group(1).strip()
            if re.match(r'https?://', target) or target.startswith('mailto:'):
                continue
            if target.startswith('#'):
                anchor = target[1:]
                if anchor not in headings_map.get(str(f), set()):
                    results['errors'].append(('missing_local_anchor', str(f), target))
                continue
            # split page and anchor
            if '#' in target:
                pagepart, anchor = target.split('#', 1)
            else:
                pagepart, anchor = target, None
            # YAML links are warnings (prefer wiki pages)
            if pagepart.endswith(('.yml', '.yaml')):
                results['warnings'].append(('link_to_yaml', str(f), target))
                # optionally create placeholder page in wiki_pages if asked
                if create_placeholders:
                    # create a placeholder page with same name (without extension) under wiki_pages
                    placeholder = Path('wiki_pages') / (Path(pagepart).stem + '.md')
                    if not placeholder.exists():
                        placeholder.write_text(f"# {placeholder.stem}\n\nPlaceholder for `{pagepart}`. See repository for canonical YAML.", encoding='utf-8')
                        results['fixed'].append(('created_placeholder', str(placeholder)))
                continue
            # normalize page filename
            pagefile = pagepart if pagepart.endswith('.md') else pagepart + '.md'
            # first try relative to current file
            target_path = (f.parent / pagefile)
            if not target_path.exists():
                # try repo-root relative
                target_path = Path(pagefile)
                if not target_path.exists():
                    results['errors'].append(('missing_page', str(f), target))
                    continue
            if anchor:
                ttxt = read_file_safe(target_path)
                if ttxt is None:
                    results['errors'].append(('cannot_read_target', str(f), str(target_path)))
                    continue
                target_headings = set(slugify(h) for _, h in HEADING_RE.findall(ttxt))
                if anchor not in target_headings:
                    results['errors'].append(('missing_anchor_in_target', str(f), target))

    return results


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--paths', help='Comma-separated list of folders to scan', default=None)
    ap.add_argument('--fix-h1', action='store_true', help='Auto-fix missing/mismatched H1s')
    ap.add_argument('--create-placeholders', action='store_true', help='Create placeholder .md pages for YAML links under wiki_pages')
    ap.add_argument('--json', action='store_true', help='Output JSON')
    args = ap.parse_args()

    if args.paths:
        paths=[Path(p.strip()) for p in args.paths.split(',')]
    else:
        paths=[p for p in DEFAULT_PATHS if p.exists()]

    res = scan_files(paths, fix_h1=args.fix_h1, create_placeholders=args.create_placeholders)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Files scanned: {res['files_scanned']}")
        print(f"Errors: {len([e for e in res['errors']])}")
        for e in res['errors'][:200]:
            print('ERROR:', e)
        print(f"Warnings: {len([w for w in res['warnings']])}")
        for w in res['warnings'][:200]:
            print('WARN:', w)
        if res['fixed']:
            print('Auto-fixed items:')
            for f in res['fixed']:
                print('  FIXED:', f)

    if res['errors']:
        sys.exit(2)
    if res['warnings']:
        sys.exit(1)
    sys.exit(0)
