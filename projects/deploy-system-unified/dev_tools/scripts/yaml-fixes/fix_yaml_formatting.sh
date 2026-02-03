#!/usr/bin/env bash

# Script to fix YAML formatting violations using ripgrep and awk

echo "=== Fixing YAML Formatting Violations ==="

# Phase 1: Fix trailing spaces in security/advanced
echo "Phase 1: Fixing trailing spaces..."
if [ -f "roles/security/advanced/tasks/main.yml" ]; then
    # Use sed to remove trailing spaces
    sed -i 's/[[:space:]]*$//' roles/security/advanced/tasks/main.yml
    echo "✓ Fixed trailing spaces in security/advanced/tasks/main.yml"
else
    echo "⚠ File not found: roles/security/advanced/tasks/main.yml"
fi

# Phase 2: Fix indentation issues in security/scanning
echo "Phase 2: Fixing indentation issues in security/scanning..."
if [ -f "roles/security/scanning/tasks/main.yml" ]; then
    # Use awk to fix indentation from 4 spaces to 2 spaces for specific patterns
    # This targets lines that are part of task blocks but incorrectly indented
    awk '
    # Fix indentation for lines that should be at 2 spaces but are at 4
    /^    - / { 
        gsub(/^    - /, "  - "); 
        print; 
        next; 
    }
    # Fix indentation for lines that should be at 4 spaces but are at 6 (nested under tasks)
    /^      / { 
        gsub(/^      /, "    "); 
        print; 
        next; 
    }
    # Fix indentation for lines that should be at 6 spaces but are at 8 (nested under when/args)
    /^        / { 
        gsub(/^        /, "      "); 
        print; 
        next; 
    }
    # Fix indentation for lines that should be at 8 spaces but are at 10 (deeply nested)
    /^          / { 
        gsub(/^          /, "        "); 
        print; 
        next; 
    }
    # Fix indentation for lines that should be at 10 spaces but are at 12 (very deeply nested)
    /^            / { 
        gsub(/^            /, "          "); 
        print; 
        next; 
    }
    # Pass through all other lines unchanged
    { print }
    ' roles/security/scanning/tasks/main.yml > roles/security/scanning/tasks/main.yml.tmp
    
    # Replace original file with fixed version
    mv roles/security/scanning/tasks/main.yml.tmp roles/security/scanning/tasks/main.yml
    echo "✓ Fixed indentation in security/scanning/tasks/main.yml"
else
    echo "⚠ File not found: roles/security/scanning/tasks/main.yml"
fi

# Phase 3: Additional cleanup for any remaining issues
echo "Phase 3: Additional cleanup..."
# Remove any lines with only whitespace
find roles/ -name "*.yml" -exec sed -i '/^[[:space:]]*$/d' {} \;
echo "✓ Removed empty lines with only whitespace"

echo "=== Fixing Complete ==="
