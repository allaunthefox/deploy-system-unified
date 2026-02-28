#!/bin/bash
# =============================================================================
# Script: rename_uppercase_to_lowercase.sh
# Description: Rename files with uppercase letters to lowercase
# Usage: ./rename_uppercase_to_lowercase.sh [--dry-run]
# =============================================================================

set -e

DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
    echo "=== DRY RUN MODE - No changes will be made ==="
fi

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$PROJECT_ROOT"

# Files to rename (excluding README.md and Chart.yaml which are standard conventions)
files_to_rename=(
    ".reports/MONITORING_MEDIA_DEPLOYMENT_TEST.md"
    ".reports/FULL_DEPLOYMENT_COMPLETE.md"
    ".reports/FORMALIZED_CHANGES.md"
    ".reports/FULL_STACK_DEPLOYMENT_TEST.md"
    ".reports/ZERO_TOUCH_DEPLOYMENT_FORMALIZATION.md"
    ".reports/RANDOM_DEPLOYMENT_TEST_RESULTS.md"
    ".reports/BUG_FIXES_FROM_RANDOM_TEST.md"
    ".reports/NETWORK_STACK_INVESTIGATION.md"
    ".reports/K3S_DNS_FIX_PROJECT_STANDARD.md"
    ".reports/PERMANENT_K3S_FIX.md"
    ".reports/KUBERNETES_SECURITY_WARNINGS_FIX.md"
    ".reports/SECURITY_HARDENING_COMPLETE.md"
    "CHANGELOG.md"
    "IMPLICIT_SETTINGS_IMPLEMENTATION_PLAN.md"
    "LICENSE-COMPLIANCE.md"
    "LICENSE_NOTES.md"
    "Offline_Research/LLM_RESEARCH/Style_Guide.md"
    "Offline_Research/LLM_RESEARCH/planning/CI_MODERNIZATION_PLAN.md"
    "Offline_Research/LLM_RESEARCH/planning/GPU_Slicing_Planning_Document.md"
    "Offline_Research/LLM_RESEARCH/planning/SSH_POLICY.md"
    "PYTHON_ACCESSIBILITY_STANDARDS.md"
    "REPO_SECURITY_CHECKLIST.md"
)

# Find all files with uppercase (excluding README.md and Chart.yaml)
echo "Finding files with uppercase letters (excluding README.md and Chart.yaml)..."
mapfile -t all_uppercase_files < <(find . -type f \( -name "*[A-Z]*.md" -o -name "*[A-Z]*.sh" -o -name "*[A-Z]*.yml" -o -name "*[A-Z]*.yaml" -o -name "*[A-Z]*.py" -o -name "*[A-Z]*.j2" \) 2>/dev/null | grep -v ".git" | grep -v "collections" | grep -vE "README\.md|Chart\.yaml" | sort)

echo "Found ${#all_uppercase_files[@]} files to rename"
echo ""

renamed=0
skipped=0

for file in "${all_uppercase_files[@]}"; do
    # Remove leading ./
    file="${file#./}"
    
    # Get directory and filename
    dir=$(dirname "$file")
    filename=$(basename "$file")
    
    # Convert filename to lowercase
    new_filename=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
    
    # Skip if already lowercase
    if [ "$filename" = "$new_filename" ]; then
        ((skipped++)) || true
        continue
    fi
    
    new_path="$dir/$new_filename"
    
    # Check if target already exists
    if [ -e "$new_path" ]; then
        echo "SKIP: $file (target already exists: $new_path)"
        ((skipped++)) || true
        continue
    fi
    
    if [ "$DRY_RUN" = true ]; then
        echo "WOULD RENAME: $file -> $new_path"
    else
        echo "RENAMING: $file -> $new_path"
        mv "$file" "$new_path"
    fi
    ((renamed++)) || true
done

echo ""
echo "=== Summary ==="
echo "Renamed: $renamed files"
echo "Skipped: $skipped files"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "This was a dry run. Run without --dry-run to actually rename files."
fi
