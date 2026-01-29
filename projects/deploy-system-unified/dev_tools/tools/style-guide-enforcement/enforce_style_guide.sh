#!/bin/bash

# Deploy-System-Unified Style Guide Enforcement Tool
# Comprehensive script to enforce project coding standards

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
YAML_LINT_CONFIG="$PROJECT_ROOT/.yamllint.yml"
ANSIBLE_LINT_CONFIG="$PROJECT_ROOT/.ansible-lint.yml"
STYLE_GUIDE="$PROJECT_ROOT/LLM_RESEARCH/Style_Guide.md"

# Counters
TOTAL_ISSUES=0
FIXED_ISSUES=0
UNFIXED_ISSUES=0

# Flags
AUTO_FIX=false
REPORT_ONLY=false

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    log "Checking dependencies..."
    
    local missing_tools=()
    
    command -v yamllint >/dev/null 2>&1 || missing_tools+=("yamllint")
    command -v ansible-lint >/dev/null 2>&1 || missing_tools+=("ansible-lint")
    command -v rg >/dev/null 2>&1 || missing_tools+=("ripgrep")
    command -v awk >/dev/null 2>&1 || missing_tools+=("awk")
    command -v sed >/dev/null 2>&1 || missing_tools+=("sed")
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        error "Missing required tools: ${missing_tools[*]}"
        error "Please install the missing tools and try again."
        exit 1
    fi
    
    success "All dependencies available"
}

# Enforce YAML formatting standards
enforce_yaml_standards() {
    log "Enforcing YAML formatting standards..."
    
    local yaml_files=()
    while IFS= read -r -d '' file; do
        yaml_files+=("$file")
    done < <(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -print0)
    
    if [ ${#yaml_files[@]} -eq 0 ]; then
        warning "No YAML files found"
        return 0
    fi
    
    # Run yamllint
    if [ -f "$YAML_LINT_CONFIG" ]; then
        log "Running yamllint with project configuration..."
        if yamllint -c "$YAML_LINT_CONFIG" "${yaml_files[@]}" 2>&1 | tee /tmp/yamllint_output.txt; then
            success "YAML formatting standards met"
        else
            warning "YAML linting found issues"
            local issue_count=$(grep -E "error|warning" /tmp/yamllint_output.txt | wc -l || echo 0)
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
            
            # Auto-fix trailing spaces and indentation
            if [ "$AUTO_FIX" = true ]; then
                log "Auto-fixing common YAML issues..."
                for file in "${yaml_files[@]}"; do
                    # Fix trailing spaces
                    sed -i 's/[[:space:]]*$//' "$file"

                    # Ensure file ends with newline
                    if [ -s "$file" ] && [ "$(tail -c 1 "$file" | wc -l)" -eq 0 ]; then
                        echo "" >> "$file"
                        FIXED_ISSUES=$((FIXED_ISSUES + 1))
                    fi

                    # Add YAML document start '---' if missing at top of file
                    if ! awk 'NF{print;exit}' "$file" | grep -qE '^---'; then
                        sed -i '1s/^/---\n/' "$file"
                        FIXED_ISSUES=$((FIXED_ISSUES + 1))
                        warning "Inserted YAML document start into: $file"
                    fi

                    # Normalize common boolean values (True/False/Yes/No) to lowercase true/false
                    # Only affects unquoted bare words following a colon
                    perl -i -pe 's/(:\s*)(True|False|TRUE|FALSE|Yes|No|YES|NO|yes|no)\b/$1 . lc($2)/ge' "$file" && FIXED_ISSUES=$((FIXED_ISSUES + 1))

                    # Remove unnecessary spaces inside square brackets (e.g., [ a, b ] -> [a, b])
                    perl -i -0777 -pe 's/\[\s*([^\[\]]*?)\s*\]/[\1]/g' "$file" && FIXED_ISSUES=$((FIXED_ISSUES + 1))
                done
                success "Common YAML issues auto-fixed"
            fi
        fi
    else
        log "Running yamllint with default configuration..."
        if yamllint "${yaml_files[@]}" 2>&1 | tee /tmp/yamllint_output.txt; then
            success "YAML formatting standards met"
        else
            warning "YAML linting found issues"
            local issue_count=$(grep -E "error|warning" /tmp/yamllint_output.txt | wc -l || echo 0)
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce Ansible-specific standards
enforce_ansible_standards() {
    log "Enforcing Ansible-specific standards..."
    
    local ansible_files=()
    while IFS= read -r -d '' file; do
        ansible_files+=("$file")
    done < <(find "$PROJECT_ROOT" -path "*/roles/*" -name "*.yml" -not -path "*/.git/*" -print0)
    
    if [ ${#ansible_files[@]} -eq 0 ]; then
        warning "No Ansible role files found"
        return 0
    fi
    
    # Run ansible-lint
    if [ -f "$ANSIBLE_LINT_CONFIG" ]; then
        log "Running ansible-lint with project configuration..."
        if ansible-lint -c "$ANSIBLE_LINT_CONFIG" "${ansible_files[@]}" 2>&1 | tee /tmp/ansible_lint_output.txt; then
            success "Ansible standards met"
        else
            warning "Ansible linting found issues"
            local issue_count=$(grep -E "error|warning" /tmp/ansible_lint_output.txt | wc -l || echo 0)
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    else
        log "Running ansible-lint with default configuration..."
        if ansible-lint "${ansible_files[@]}" 2>&1 | tee /tmp/ansible_lint_output.txt; then
            success "Ansible standards met"
        else
            warning "Ansible linting found issues"
            local issue_count=$(grep -E "error|warning" /tmp/ansible_lint_output.txt | wc -l || echo 0)
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce naming conventions
enforce_naming_conventions() {
    log "Enforcing naming conventions..."
    
    # Check for files with spaces in names
    local files_with_spaces=()
    while IFS= read -r -d '' file; do
        files_with_spaces+=("$file")
    done < <(find "$PROJECT_ROOT" -name "* *" -not -path "*/.git/*" -print0 2>/dev/null)
    
    if [ ${#files_with_spaces[@]} -gt 0 ]; then
        warning "Found ${#files_with_spaces[@]} files with spaces in names"
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#files_with_spaces[@]}))
        
        if [ "$AUTO_FIX" = true ]; then
            for file in "${files_with_spaces[@]}"; do
                local dir=$(dirname "$file")
                local base=$(basename "$file")
                local new_name="${base// /_}"
                warning "Renaming: $base -> $new_name"
                mv "$file" "$dir/$new_name"
                FIXED_ISSUES=$((FIXED_ISSUES + 1))
            done
        fi
    fi
    
    # Check for uppercase filenames in roles
    local uppercase_files=()
    if [ -d "$PROJECT_ROOT/roles" ]; then
        while IFS= read -r -d '' file; do
            local base=$(basename "$file")
            if [[ "$base" =~ ^[A-Z] ]]; then
                uppercase_files+=("$file")
            fi
        done < <(find "$PROJECT_ROOT/roles" -type f -not -path "*/.git/*" -print0 2>/dev/null)
    fi
    
    if [ ${#uppercase_files[@]} -gt 0 ]; then
        warning "Found ${#uppercase_files[@]} files with uppercase names in roles directory"
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#uppercase_files[@]}))
        
        if [ "$AUTO_FIX" = true ]; then
            for file in "${uppercase_files[@]}"; do
                local dir=$(dirname "$file")
                local base=$(basename "$file")
                local new_name=$(echo "$base" | tr '[:upper:]' '[:lower:]')
                if [ "$base" != "$new_name" ]; then
                    warning "Renaming: $base -> $new_name"
                    mv "$file" "$dir/$new_name"
                    FIXED_ISSUES=$((FIXED_ISSUES + 1))
                fi
            done
        fi
    fi
    
    success "Naming conventions enforced"
}

# Enforce file structure standards
enforce_file_structure() {
    log "Enforcing file structure standards..."
    
    # Check for proper role structure
    local roles_dir="$PROJECT_ROOT/roles"
    
    if [ -d "$roles_dir" ]; then
        for role in "$roles_dir"/*; do
            if [ ! -d "$role" ]; then
                continue
            fi
            
            local role_name=$(basename "$role")
            local role_path="$role"
            
            # Check for required directories
            for dir in "tasks" "handlers" "defaults" "vars" "templates" "files"; do
                if [ ! -d "$role_path/$dir" ]; then
                    warning "Role '$role_name' missing '$dir' directory"
                    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
                fi
            done
            
            # Check for main.yml files
            for main_file in "tasks/main.yml" "handlers/main.yml" "defaults/main.yml" "vars/main.yml"; do
                if [ ! -f "$role_path/$main_file" ]; then
                    warning "Role '$role_name' missing '$main_file'"
                    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
                fi
            done
        done
    fi
    
    success "File structure standards checked"
}

# Enforce security standards
enforce_security_standards() {
    log "Enforcing security standards..."
    
    # Check for hardcoded secrets (with more precise patterns)
    local secret_patterns=(
        'password\s*[:=]'
        'secret\s*[:=]'
        'token\s*[:=]'
        'api_key\s*[:=]'
        'private_key\s*[:=]'
    )
    
    for pattern in "${secret_patterns[@]}"; do
        local matches=()
        while IFS= read -r file; do
            matches+=("$file")
        done < <(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -l -E "$pattern" {} \; 2>/dev/null)
        
        if [ ${#matches[@]} -gt 0 ]; then
            warning "Found ${#matches[@]} file(s) with potential hardcoded secrets matching pattern: $pattern"
            for file in "${matches[@]}"; do
                warning "  - $file"
            done
            TOTAL_ISSUES=$((TOTAL_ISSUES + ${#matches[@]}))
        fi
    done
    
    # Check for unsafe permissions
    local unsafe_perms=()
    while IFS= read -r file; do
        unsafe_perms+=("$file")
    done < <(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -l 'mode:\s*["\x27]\?7[0-9][0-9]' {} \; 2>/dev/null)
    
    if [ ${#unsafe_perms[@]} -gt 0 ]; then
        warning "Found ${#unsafe_perms[@]} file(s) with potentially unsafe permissions (7xx)"
        for file in "${unsafe_perms[@]}"; do
            warning "  - $file"
        done
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#unsafe_perms[@]}))
    fi
    
    success "Security standards checked"
}

# Generate style guide compliance report
generate_report() {
    log "Generating style guide compliance report..."
    
    local report_file="$PROJECT_ROOT/dev_tools/tools/style-guide-enforcement/compliance_report_$(date +%Y%m%d_%H%M%S).md"
    local report_dir=$(dirname "$report_file")
    
    # Create report directory if it doesn't exist
    mkdir -p "$report_dir"
    
    # Calculate unfixed issues
    UNFIXED_ISSUES=$((TOTAL_ISSUES - FIXED_ISSUES))
    
    # Count issues by category
    local yaml_issues=$(grep -E "error|warning" /tmp/yamllint_output.txt 2>/dev/null | wc -l || echo "0")
    local ansible_issues=$(grep -E "error|warning" /tmp/ansible_lint_output.txt 2>/dev/null | wc -l || echo "0")
    local space_files=$(find "$PROJECT_ROOT" -name "* *" -not -path "*/.git/*" 2>/dev/null | wc -l || echo "0")
    local uppercase_files=0
    if [ -d "$PROJECT_ROOT/roles" ]; then
        uppercase_files=$(find "$PROJECT_ROOT/roles" -type f -not -path "*/.git/*" 2>/dev/null | while read -r file; do
            base=$(basename "$file")
            [[ "$base" =~ ^[A-Z] ]] && echo "$file"
        done | wc -l || echo "0")
    fi
    local secret_files=$(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -l -E 'password\s*[:=]' {} \; 2>/dev/null | wc -l || echo "0")
    local unsafe_perm_files=$(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -l 'mode:\s*["\x27]\?7[0-9][0-9]' {} \; 2>/dev/null | wc -l || echo "0")
    
    cat > "$report_file" << EOF
# Style Guide Compliance Report

**Generated:** $(date)
**Project:** Deploy-System-Unified

## Summary

- **Total Issues Found:** $TOTAL_ISSUES
- **Issues Auto-Fixed:** $FIXED_ISSUES
- **Issues Requiring Manual Attention:** $UNFIXED_ISSUES

## Issues by Category

### YAML Formatting
$yaml_issues issues found

### Ansible Standards  
$ansible_issues issues found

### Naming Conventions
$space_files files with spaces in names
$uppercase_files files with uppercase names in roles/

### Security Standards
$secret_files files with potential hardcoded secrets
$unsafe_perm_files files with potentially unsafe permissions

## Recommendations

1. Review and manually fix remaining issues
2. Run this tool regularly as part of development workflow
3. Consider integrating with pre-commit hooks
4. Refer to $STYLE_GUIDE for detailed style guidelines

## Tools Used

- yamllint: YAML linting
- ansible-lint: Ansible-specific linting
- ripgrep/awk/sed: Pattern matching and text processing

EOF

    success "Compliance report generated: $report_file"
}

# Main execution
main() {
    log "Starting style guide enforcement..."
    log "Project root: $PROJECT_ROOT"
    
    check_dependencies
    
    if [ "$REPORT_ONLY" = true ]; then
        log "Report-only mode: generating compliance report..."
        generate_report
        exit 0
    fi
    
    enforce_yaml_standards
    enforce_ansible_standards
    enforce_naming_conventions
    enforce_file_structure
    enforce_security_standards
    
    generate_report
    
    log "Style guide enforcement complete!"
    
    if [ $TOTAL_ISSUES -eq 0 ]; then
        success "✅ No style guide violations found!"
        exit 0
    else
        warning "⚠️  Found $TOTAL_ISSUES style guide violations"
        warning "   $FIXED_ISSUES issues were auto-fixed"
        warning "   $UNFIXED_ISSUES issues require manual attention"
        exit 1
    fi
}

# Script usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
  -h, --help     Show this help message
  -q, --quiet    Suppress output except errors
  -f, --fix      Auto-fix all fixable issues
  -r, --report   Generate compliance report only

Examples:
  $0                    # Run full style guide enforcement
  $0 --fix             # Auto-fix all issues
  $0 --report          # Generate compliance report only
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -q|--quiet)
            exec > /dev/null
            shift
            ;;
        -f|--fix)
            AUTO_FIX=true
            shift
            ;;
        -r|--report)
            REPORT_ONLY=true
            shift
            ;;
        *)
            error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Run main function
main "$@"
