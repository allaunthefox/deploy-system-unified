#!/bin/sh
# Deploy-System-Unified Style Guide Enforcement Tool
# Comprehensive script to enforce project coding standards
# Fully POSIX compliant

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
YAML_LINT_CONFIG="$PROJECT_ROOT/.yamllint.yml"
ANSIBLE_LINT_CONFIG="$PROJECT_ROOT/.ansible-lint.yml"
STYLE_IGNORE="$PROJECT_ROOT/dev_tools/tools/style-guide-enforcement/.styleignore"
VENV_DIR="$PROJECT_ROOT/.venv"

# Ensure relative paths resolve consistently
cd "$PROJECT_ROOT"

# Prefer project-local virtualenv if available
if [ -x "$VENV_DIR/bin/ansible-lint" ]; then
    export PATH="$VENV_DIR/bin:$PATH"
    unset ANSIBLE_COLLECTIONS_PATHS
    export ANSIBLE_CONFIG="$PROJECT_ROOT/ansible.cfg"
fi

# Check style ignore patterns
is_ignored() {
    path="$1"
    [ ! -f "$STYLE_IGNORE" ] && return 1

    ignored=0
    while read -r line || [ -n "$line" ]; do
        case "$line" in
            "") continue ;;
            \#*) continue ;;
        esac

        neg=0
        pat="$line"
        case "${pat%"${pat#?}"}" in
            !)
                neg=1
                pat="${pat#?}"
                ;;
        esac

        match=0
        case "$pat" in
            re:*)
                regex="${pat#re:}"
                if printf '%s' "$path" | grep -Eq -- "$regex"; then
                    match=1
                fi
                ;;
            *)
                case "$path" in
                    $pat) match=1 ;;
                esac
                ;;
        esac

        if [ $match -eq 1 ]; then
            if [ $neg -eq 1 ]; then
                ignored=0
            else
                ignored=1
            fi
        fi
    done < "$STYLE_IGNORE"

    [ $ignored -eq 1 ] && return 0 || return 1
}

# Counters
TOTAL_ISSUES=0
FIXED_ISSUES=0

# Flags
AUTO_FIX=false
LOW_RISK_REPAIR=false
REPORT_ONLY=false

# Logging functions
log() { printf "${BLUE}[%s]${NC} %s\n" "$(date +'%H:%M:%S')" "$1"; }
error() { printf "${RED}[ERROR]${NC} %s\n" "$1"; }
warning() { printf "${YELLOW}[WARNING]${NC} %s\n" "$1"; }
success() { printf "${GREEN}[SUCCESS]${NC} %s\n" "$1"; }

# Perform safe repairs
perform_safe_repairs() {
    file="$1"
    fixed=0

    if grep -q "[[:space:]]$" "$file"; then
        sed -i 's/[[:space:]]*$//' "$file"
        fixed=1
    fi

    if [ -s "$file" ] && [ "$(tail -c 1 "$file" | wc -l)" -eq 0 ]; then
        echo "" >> "$file"
        fixed=1
    fi

    case "$file" in
        *.yml|*.yaml)
            if ! awk 'NF{print;exit}' "$file" | grep -qE '^---'; then
                sed -i '1s/^/---\n/' "$file"
                fixed=1
            fi
            ;;
    esac

    if [ $fixed -eq 1 ]; then
        FIXED_ISSUES=$((FIXED_ISSUES + 1))
        return 0
    else
        return 1
    fi
}

# Check dependencies
check_dependencies() {
    log "Checking dependencies..."

    missing_tools=""

    command -v yamllint >/dev/null 2>&1 || missing_tools="$missing_tools yamllint"
    command -v ansible-lint >/dev/null 2>&1 || missing_tools="$missing_tools ansible-lint"
    command -v awk >/dev/null 2>&1 || missing_tools="$missing_tools awk"
    command -v sed >/dev/null 2>&1 || missing_tools="$missing_tools sed"

    if [ -n "$missing_tools" ]; then
        error "Missing required tools:$missing_tools"
        error "Please install the missing tools and try again."
        exit 1
    fi

    if command -v rg >/dev/null 2>&1; then
        success "All dependencies available (including ripgrep)"
    else
        warning "ripgrep not found, falling back to standard grep (processing may be slower)"
    fi

    if command -v fd >/dev/null 2>&1 || command -v fdfind >/dev/null 2>&1; then
        success "All dependencies available (including fd)"
    else
        warning "fd not found, falling back to standard find (processing may be slower)"
    fi

    if command -v shellcheck >/dev/null 2>&1; then
        success "All dependencies available (including shellcheck)"
    else
        warning "shellcheck not found, internal shell scripts will not be audited"
    fi
}

# Enforce YAML standards
enforce_yaml_standards() {
    log "Enforcing YAML formatting standards..."

    yaml_count=0
    yaml_issues=0

    # Find YAML files
    if command -v fd >/dev/null 2>&1; then
        yaml_count=$(fd . "$PROJECT_ROOT" -e yml -e yaml --exclude .git 2>/dev/null | wc -l)
    elif command -v fdfind >/dev/null 2>&1; then
        yaml_count=$(fdfind . "$PROJECT_ROOT" -e yml -e yaml --exclude .git 2>/dev/null | wc -l)
    else
        yaml_count=$(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" | wc -l)
    fi

    if [ "$yaml_count" -eq 0 ]; then
        warning "No YAML files found"
        return 0
    fi

    # Run yamllint
    if [ -f "$YAML_LINT_CONFIG" ]; then
        log "Running yamllint with project configuration..."
        if yamllint -c "$YAML_LINT_CONFIG" "$PROJECT_ROOT" 2>&1 | tee /tmp/yamllint_output.txt; then
            success "YAML formatting standards met"
        else
            warning "YAML linting found issues"
            issue_count=$(grep -E -c "error|warning" /tmp/yamllint_output.txt 2>/dev/null || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))

            if [ "$AUTO_FIX" = true ] || [ "$LOW_RISK_REPAIR" = true ]; then
                log "Applying safe repairs to YAML files..."
                if command -v fd >/dev/null 2>&1; then
                    fd . "$PROJECT_ROOT" -e yml -e yaml --exclude .git -X sh -c 'sed -i "s/[[:space:]]*$//"; echo "" >> "{}"' 2>/dev/null || true
                else
                    find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec sh -c 'sed -i "s/[[:space:]]*$//"; echo "" >> "$1"' _ {} \; 2>/dev/null || true
                fi
                success "YAML repairs complete"
            fi
        fi
    else
        log "Running yamllint with default configuration..."
        if yamllint "$PROJECT_ROOT" 2>&1 | tee /tmp/yamllint_output.txt; then
            success "YAML formatting standards met"
        else
            warning "YAML linting found issues"
            issue_count=$(grep -E -c "error|warning" /tmp/yamllint_output.txt 2>/dev/null || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce Ansible standards
enforce_ansible_standards() {
    log "Enforcing Ansible best practices..."

    if [ -f "$ANSIBLE_LINT_CONFIG" ]; then
        log "Running ansible-lint with project configuration..."
        if ansible-lint -c "$ANSIBLE_LINT_CONFIG" "$PROJECT_ROOT" 2>&1 | tee /tmp/ansible_lint_output.txt; then
            success "Ansible best practices met"
        else
            warning "Ansible linting found issues"
            issue_count=$(grep -E -c "error|warning" /tmp/ansible_lint_output.txt 2>/dev/null || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    else
        log "Running ansible-lint with default configuration..."
        if ansible-lint "$PROJECT_ROOT" 2>&1 | tee /tmp/ansible_lint_output.txt; then
            success "Ansible best practices met"
        else
            warning "Ansible linting found issues"
            issue_count=$(grep -E -c "error|warning" /tmp/ansible_lint_output.txt 2>/dev/null || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce shell script standards
enforce_shell_standards() {
    log "Enforcing shell script standards..."

    shell_count=0
    shell_issues=0

    if command -v fd >/dev/null 2>&1; then
        shell_count=$(fd . "$PROJECT_ROOT" -e sh --exclude .git 2>/dev/null | wc -l)
    else
        shell_count=$(find "$PROJECT_ROOT" -name "*.sh" -not -path "*/.git/*" | wc -l)
    fi

    if [ "$shell_count" -eq 0 ]; then
        warning "No shell files found"
        return 0
    fi

    if command -v shellcheck >/dev/null 2>&1; then
        log "Running shellcheck..."
        if command -v fd >/dev/null 2>&1; then
            if fd . "$PROJECT_ROOT" -e sh --exclude .git -X shellcheck 2>&1 | tee /tmp/shellcheck_output.txt; then
                success "Shell scripts pass shellcheck"
            else
                warning "Shellcheck found issues"
                issue_count=$(grep -E -c "^In " /tmp/shellcheck_output.txt 2>/dev/null || echo "0")
                shell_issues=$issue_count
                TOTAL_ISSUES=$((TOTAL_ISSUES + shell_issues))
            fi
        else
            if find "$PROJECT_ROOT" -name "*.sh" -not -path "*/.git/*" -exec shellcheck {} + 2>&1 | tee /tmp/shellcheck_output.txt; then
                success "Shell scripts pass shellcheck"
            else
                warning "Shellcheck found issues"
                issue_count=$(grep -E -c "^In " /tmp/shellcheck_output.txt 2>/dev/null || echo "0")
                shell_issues=$issue_count
                TOTAL_ISSUES=$((TOTAL_ISSUES + shell_issues))
            fi
        fi
    else
        warning "shellcheck not installed, skipping shell script validation"
    fi
}

# Check file naming conventions
check_naming_conventions() {
    log "Checking file naming conventions..."

    space_files=0
    uppercase_files=0

    # Check for spaces in filenames
    if command -v fd >/dev/null 2>&1; then
        space_files=$(fd . "$PROJECT_ROOT" --exclude .git 2>/dev/null | grep -c " " || echo "0")
    else
        space_files=$(find "$PROJECT_ROOT" -not -path "*/.git/*" | grep -c " " || echo "0")
    fi

    if [ "$space_files" -gt 0 ]; then
        warning "$space_files files have spaces in names"
        TOTAL_ISSUES=$((TOTAL_ISSUES + space_files))
    fi

    # Check for uppercase in roles/
    if [ -d "$PROJECT_ROOT/roles" ]; then
        if command -v fd >/dev/null 2>&1; then
            uppercase_files=$(fd . "$PROJECT_ROOT/roles" --exclude .git 2>/dev/null | grep -cE "/[A-Z]" || echo "0")
        else
            uppercase_files=$(find "$PROJECT_ROOT/roles" -not -path "*/.git/*" | grep -cE "/[A-Z]" || echo "0")
        fi

        if [ "$uppercase_files" -gt 0 ]; then
            warning "$uppercase_files files in roles/ have uppercase letters"
            TOTAL_ISSUES=$((TOTAL_ISSUES + uppercase_files))
        fi
    fi

    if [ "$space_files" -eq 0 ] && [ "$uppercase_files" -eq 0 ]; then
        success "File naming conventions met"
    fi
}

# Check for hardcoded secrets
check_secrets() {
    log "Checking for hardcoded secrets..."

    secret_files=0
    secret_patterns="password[[:space:]]*[:=]|secret[[:space:]]*[:=]|token[[:space:]]*[:=]|api_key[[:space:]]*[:=]|private_key[[:space:]]*[:=]"

    if command -v rg >/dev/null 2>&1; then
        secret_files=$(rg -l "$secret_patterns" "$PROJECT_ROOT" --glob "!.git/*" --glob "!*.secrets.baseline" 2>/dev/null | wc -l || echo "0")
    else
        secret_files=$(grep -rlE "$secret_patterns" "$PROJECT_ROOT" --exclude-dir=.git --exclude="*.secrets.baseline" 2>/dev/null | wc -l || echo "0")
    fi

    if [ "$secret_files" -gt 0 ]; then
        warning "$secret_files files may contain hardcoded secrets"
        TOTAL_ISSUES=$((TOTAL_ISSUES + secret_files))
    else
        success "No hardcoded secrets detected"
    fi
}

# Check unsafe file permissions
check_permissions() {
    log "Checking file permissions..."

    unsafe_perms=0
    perm_pattern='mode:[[:space:]]*(0?777|0?666)'

    if command -v rg >/dev/null 2>&1; then
        unsafe_perms=$(rg -l "$perm_pattern" "$PROJECT_ROOT" --glob "*.yml" --glob "*.yaml" 2>/dev/null | wc -l || echo "0")
    else
        unsafe_perms=$(grep -rlE "$perm_pattern" "$PROJECT_ROOT" --include="*.yml" --include="*.yaml" 2>/dev/null | wc -l || echo "0")
    fi

    if [ "$unsafe_perms" -gt 0 ]; then
        warning "$unsafe_perms files have potentially unsafe permissions (777/666)"
        TOTAL_ISSUES=$((TOTAL_ISSUES + unsafe_perms))
    else
        success "No unsafe file permissions detected"
    fi
}

# Generate compliance report
generate_report() {
    report_file="$PROJECT_ROOT/dev_tools/tools/style-guide-enforcement/compliance_report_$(date +%Y%m%d_%H%M%S).md"

    cat > "$report_file" << EOF
# Style Guide Compliance Report

**Generated:** $(date)
**Project:** Deploy-System-Unified

## Summary

- **Total Issues:** $TOTAL_ISSUES
- **Fixed Issues:** $FIXED_ISSUES
- **Remaining Issues:** $((TOTAL_ISSUES - FIXED_ISSUES))

## Categories

### YAML Formatting
Issues found in YAML files

### Ansible Best Practices
Issues found in Ansible playbooks/roles

### Shell Scripting
Issues found in shell scripts

### File Naming
Files with spaces or uppercase in roles/

### Security
Potential hardcoded secrets or unsafe permissions

## Recommendations

1. Review and fix remaining issues
2. Run this tool regularly during development
3. Integrate with CI/CD pipeline
4. Refer to STYLE_GUIDE for detailed guidelines

## Tools Used

- yamllint: YAML linting
- ansible-lint: Ansible linting
- shellcheck: Shell script linting
- ripgrep/grep: Pattern matching
- fd/find: File discovery
EOF

    echo ""
    success "Report saved to: $report_file"
}

# Print usage
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --fix          Automatically fix issues where safe"
    echo "  --low-risk     Apply only low-risk automatic fixes"
    echo "  --report       Generate compliance report only"
    echo "  --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --fix       Fix all auto-fixable issues"
    echo "  $0 --report    Generate report without fixing"
}

# Parse command line arguments
while [ $# -gt 0 ]; do
    case $1 in
        --fix)
            AUTO_FIX=true
            shift
            ;;
        --low-risk)
            LOW_RISK_REPAIR=true
            shift
            ;;
        --report)
            REPORT_ONLY=true
            shift
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    echo "========================================"
    echo "  Style Guide Enforcement Tool"
    echo "========================================"
    echo ""

    check_dependencies

    if [ "$REPORT_ONLY" = false ]; then
        enforce_yaml_standards
        enforce_ansible_standards
        enforce_shell_standards
        check_naming_conventions
        check_secrets
        check_permissions
    fi

    generate_report

    echo ""
    echo "========================================"
    echo "           Final Summary"
    echo "========================================"
    echo "Total Issues:   $TOTAL_ISSUES"
    echo "Fixed Issues:   $FIXED_ISSUES"
    echo "Remaining:      $((TOTAL_ISSUES - FIXED_ISSUES))"
    echo "========================================"

    if [ "$TOTAL_ISSUES" -gt 0 ]; then
        warning "Issues found. Review the report for details."
        exit 1
    else
        success "All style checks passed!"
        exit 0
    fi
}

# Run main function
main
