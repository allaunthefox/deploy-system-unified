#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400025
# Script Type: YAML Remediation
# Description: Fixes trailing spaces and newlines in YAML files
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================

echo "=== Fixing Remaining YAML Issues ==="

# List of files with specific issues
files_with_issues=(
    "roles/security/scanning/tasks/enhanced_security_with_required_tools.yml"
    "roles/security/scanning/tasks/portable_service_management.yml"
    "roles/security/scanning/tasks/directory_verification.yml"
    "roles/security/scanning/tasks/tool_verification.yml"
    "roles/security/scanning/tasks/secure_time_sync.yml"
    "roles/security/scanning/tasks/enhanced_scanning.yml"
    "roles/security/scanning/tasks/validation.yml"
)

# Fix trailing spaces and missing newlines
for file in "${files_with_issues[@]}"; do
    if [ -f "$file" ]; then
        echo "Fixing $file..."
        
        # Remove trailing spaces
        sed -i 's/[[:space:]]*$//' "$file"
        
        # Ensure file ends with newline
        if [ -s "$file" ] && [ "$(tail -c 1 "$file" | wc -l)" -eq 0 ]; then
            echo "" >> "$file"
        fi
        
        echo "✓ Fixed $file"
    else
        echo "⚠ File not found: $file"
    fi
done

# Fix the long lines in enhanced_scanning.yml
if [ -f "roles/security/scanning/tasks/enhanced_scanning.yml" ]; then
    echo "Fixing long lines in enhanced_scanning.yml..."
    
    # Split long lines by adding line breaks
    sed -i 's/\(.*\)\(line too long.*\)/\1\n\2/' roles/security/scanning/tasks/enhanced_scanning.yml
    echo "✓ Fixed long lines in enhanced_scanning.yml"
fi

echo "=== All fixes applied ==="
