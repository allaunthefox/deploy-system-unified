#!/bin/sh
# CI Gate Fixes - Collection Cleanup
# This script resolves collection version conflicts

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "=== Deploy-System-Unified Collection Cleanup ==="
echo "Project directory: $PROJECT_DIR"
echo ""

# Remove local collection copies to avoid version conflicts
echo "Removing local collection copies..."
if [ -d "$HOME/.ansible/collections/ansible_collections" ]; then
    rm -rf "$HOME/.ansible/collections/ansible_collections"
    echo "✓ Removed $HOME/.ansible/collections/ansible_collections"
else
    echo "✓ No local collections to remove"
fi

# Install collections from requirements
echo ""
echo "Installing collections from requirements.yml..."
ansible-galaxy collection install -r "$PROJECT_DIR/requirements.yml" --force

echo ""
echo "=== Collection Cleanup Complete ==="
echo ""
echo "To verify collections:"
echo "  ansible-galaxy collection list"
echo ""
echo "To check for conflicts:"
echo "  ansible --version"
