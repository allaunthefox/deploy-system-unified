#!/bin/bash

echo "=== Fixing Remaining YAML Issues ==="

# List of files with specific issues
files_with_issues=(
    "roles/security_framework/tasks/enhanced_security_with_required_tools.yml"
    "roles/security_framework/tasks/portable_service_management.yml"
    "roles/security_framework/tasks/directory_verification.yml"
    "roles/security_framework/tasks/tool_verification.yml"
    "roles/security_framework/tasks/secure_time_sync.yml"
    "roles/security_framework/tasks/enhanced_scanning.yml"
    "roles/security_framework/tasks/validation.yml"
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
if [ -f "roles/security_framework/tasks/enhanced_scanning.yml" ]; then
    echo "Fixing long lines in enhanced_scanning.yml..."
    
    # Split long lines by adding line breaks
    sed -i 's/\(.*\)\(line too long.*\)/\1\n\2/' roles/security_framework/tasks/enhanced_scanning.yml
    echo "✓ Fixed long lines in enhanced_scanning.yml"
fi

echo "=== All fixes applied ==="
