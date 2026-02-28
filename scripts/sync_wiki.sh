#!/bin/sh
# =============================================================================
# Audit Event Identifier: DSU-SHS-400020
# Script Type: Wiki Synchronization
# Description: Syncs wiki_pages/ to GitHub Wiki repository
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Wiki Sync Script - Sync wiki_pages/ to GitHub Wiki
#
# This script syncs the wiki_pages/ directory to the GitHub wiki repository.
# The GitHub wiki is a separate git repository at:
#   github.com:allaunthefox/deploy-system-unified.wiki.git

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

WIKI_PAGES_DIR="$PROJECT_DIR/wiki_pages"
WIKI_TEMP_DIR="/tmp/github-wiki-sync-$$"
WIKI_REPO="git@github.com:allaunthefox/deploy-system-unified.wiki.git"

echo "=== GitHub Wiki Sync ==="
echo "Source: $WIKI_PAGES_DIR"
echo "Target: $WIKI_REPO"
echo ""

# Check if wiki_pages directory exists
if [ ! -d "$WIKI_PAGES_DIR" ]; then
    echo "ERROR: wiki_pages directory not found at $WIKI_PAGES_DIR"
    exit 1
fi

# Clean up temp directory if it exists
rm -rf "$WIKI_TEMP_DIR"

# Clone the wiki repository
echo "Cloning wiki repository..."
git clone --quiet "$WIKI_REPO" "$WIKI_TEMP_DIR" 2>/dev/null || {
    echo "ERROR: Failed to clone wiki repository. Ensure SSH key is configured."
    exit 1
}

# Sync files
echo "Syncing wiki pages..."

# Copy all files from wiki_pages/ to wiki temp dir
cp -r "$WIKI_PAGES_DIR"/* "$WIKI_TEMP_DIR"/

# Remove files in wiki that don't exist in wiki_pages/
cd "$WIKI_TEMP_DIR"
for file in *; do
    if [ "$file" != ".git" ] && [ ! -e "$WIKI_PAGES_DIR/$file" ]; then
        echo "Removing: $file"
        rm -rf "$file"
    fi
done

# Check for changes
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes detected. Wiki is up to date."
    cd "$PROJECT_DIR"
    rm -rf "$WIKI_TEMP_DIR"
    exit 0
fi

# Commit and push changes
echo "Committing changes..."
git add -A
git commit -m "Sync wiki pages from wiki_pages/ directory

Automated sync from wiki_pages/ directory.
Commit: $(cd "$PROJECT_DIR" && git rev-parse HEAD 2>/dev/null || echo 'unknown')
Date: $(date -Iseconds)
"

echo "Pushing to GitHub wiki..."
git push origin master

# Clean up
cd "$PROJECT_DIR"
rm -rf "$WIKI_TEMP_DIR"

echo ""
echo "=== Wiki Sync Complete ==="
echo "GitHub wiki has been updated."
