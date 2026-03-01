#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500010
# Script Type: Documentation Link Repair Script (ISO 27001 §12.4 | Quality Control)
# Last Updated: 2026-03-01
# Version: 1.0
# =============================================================================

import os
import re
import sys

# Configuration
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
SKIP_DIRS = [".git", ".venv", ".ansible", "venv", "Offline_Research", "brain", "_agent", "_agents", ".gemini"]

# Manual fixes for known moves/renames
MANUAL_FIXES = {
    "./docs/development/BASE_LAYER_IMPLEMENTATION_STATUS.md": "./docs/deployment/DEPLOYMENT_STATUS.md"
}

def get_all_wiki_pages():
    """Build a map of uppercase basenames to actual filenames for case-insensitive matching."""
    pages = {}
    wiki_dir = os.path.join(REPO_ROOT, "wiki_pages")
    if os.path.exists(wiki_dir):
        for f in os.listdir(wiki_dir):
            if f.endswith(".md"):
                pages[f[:-3].upper()] = f
    return pages

WIKI_PAGES = get_all_wiki_pages()

def check_link(filepath, link):
    """Verify if a link is valid, returns False if it should be fixed."""
    if link.startswith(("http", "mailto:", "#")):
        return True
    
    if link in MANUAL_FIXES:
        return False
    
    link_path = link.split("#")[0]
    if not link_path:
        return True
    
    dir_path = os.path.dirname(os.path.join(REPO_ROOT, filepath))
    target_path = os.path.join(dir_path, link_path)
    
    if os.path.exists(target_path):
        return True
    
    # Check for missing .md extension
    if not link_path.endswith(".md"):
        if os.path.exists(target_path + ".md"):
            return False # Fixable
            
        # Check wiki pages if it's a bare name (common in wiki contexts)
        if link_path.upper() in WIKI_PAGES:
            return False # Fixable
            
    return False

def fix_link(filepath, link):
    """Propose a fix for a broken link."""
    if link in MANUAL_FIXES:
        return MANUAL_FIXES[link]
    
    link_path = link.split("#")[0]
    hash_part = "#" + link.split("#")[1] if "#" in link else ""
    
    dir_path = os.path.dirname(os.path.join(REPO_ROOT, filepath))
    target_path = os.path.join(dir_path, link_path)

    # 1. Try adding .md
    if not link_path.endswith(".md"):
        if os.path.exists(target_path + ".md"):
            return link_path + ".md" + hash_part
            
        # 2. Try wiki mapping
        if link_path.upper() in WIKI_PAGES:
            # Calculate relative path to wiki_pages from current file
            target_wiki = os.path.join(REPO_ROOT, "wiki_pages", WIKI_PAGES[link_path.upper()])
            rel_path = os.path.relpath(target_wiki, dir_path)
            return rel_path + hash_part
    
    return link

def process_file(filepath):
    """Read, scan, and update a markdown file."""
    abs_path = os.path.join(REPO_ROOT, filepath)
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return
    
    new_content = content
    # Find all potential links
    matches = LINK_PATTERN.findall(content)
    
    for text, link in matches:
        if not check_link(filepath, link):
            fixed_link = fix_link(filepath, link)
            if fixed_link != link:
                # Use string replacement for the exact (link) literal
                # This handles common occurrences without regex escaping complexity for every link
                old_str = f"({link})"
                new_str = f"({fixed_link})"
                if old_str in new_content:
                    new_content = new_content.replace(old_str, new_str)
                    print(f"[{filepath}] FIXED: {link} -> {fixed_link}")
    
    if new_content != content:
        try:
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            print(f"Error writing {filepath}: {e}")

def main():
    os.chdir(REPO_ROOT)
    for root, dirs, files in os.walk("."):
        # Prune invisible and skipped directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), ".")
                process_file(rel_path)

if __name__ == "__main__":
    main()
