#!/bin/sh
# =============================================================================
# Audit Event Identifier: DSU-SHS-400024
# Script Type: Style Enforcement
# Description: Comprehensive script to enforce project coding standards
# Last Updated: 2026-03-01
# Version: 1.7
# =============================================================================

# Configuration
PROJECT_ROOT=$(git rev-parse --show-toplevel)
REPORT_DIR="$PROJECT_ROOT/dev_tools/reports"
DATE_STR=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$REPORT_DIR/compliance_report_$DATE_STR.md"
TOTAL_ISSUES=0
FIXED_ISSUES=0
AUTO_FIX=false
REPORT_ONLY=false

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() { echo "[$(date +%H:%M:%S)] $1"; }
success() { echo "${GREEN}[SUCCESS] $1${NC}"; }
warning() { echo "${YELLOW}[WARNING] $1${NC}"; }
error() { echo "${RED}[ERROR] $1${NC}"; exit 1; }

# Parse arguments
for arg in "$@"; do
    case $arg in
        --fix) AUTO_FIX=true ;;
        --report) REPORT_ONLY=true ;;
    esac
done

# Ensure report directory exists
mkdir -p "$REPORT_DIR"

# Check dependencies
check_dependencies() {
    log "Checking dependencies..."
    
    deps="rg fd flake8 bandit safety trufflehog checkov trivy lynis rkhunter"
    for dep in $deps; do
        if command -v "$dep" >/dev/null 2>&1; then
            success "Dependency available: $dep"
        else
            warning "Dependency NOT found: $dep"
        fi
    done
    
    if ! command -v codeql >/dev/null 2>&1; then
        warning "codeql not found. For deep security analysis, install CodeQL CLI."
    fi
}

# Enforce Security Audit (Bandit + Safety + TruffleHog + Checkov + Trivy + Lynis + RKHunter)
enforce_security_audit() {
    log "Enforcing Security Audit..."

    # 1. Bandit (Local static analysis)
    if command -v bandit >/dev/null 2>&1; then
        log "Running Bandit security scan..."
        if bandit -r "$PROJECT_ROOT" -ll --exclude "$PROJECT_ROOT/venv,$PROJECT_ROOT/.venv,$PROJECT_ROOT/.ansible,$PROJECT_ROOT/Offline_Research" 2>&1 | tee "$REPORT_DIR/bandit_output.txt"; then
            success "Bandit security scan passed"
        else
            warning "Bandit detected potential security issues"
            issue_count=$(grep -c "Issue:" "$REPORT_DIR/bandit_output.txt" 2>/dev/null || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi

    # 2. Safety (Dependency vulnerability scan)
    if command -v safety >/dev/null 2>&1; then
        if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
            log "Running Safety dependency scan..."
            if safety scan -r "$PROJECT_ROOT/requirements.txt" --non-interactive --project deploy-system-unified 2>&1 | tee "$REPORT_DIR/safety_output.txt"; then
                success "Python dependencies pass safety check"
            else
                warning "Safety detected vulnerable dependencies"
                TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
            fi
        fi
    fi

    # 3. TruffleHog (Git History Secret Scanning - v2 syntax)
    if command -v trufflehog >/dev/null 2>&1; then
        log "Running TruffleHog secret scan (last commit)..."
        # Note: Using v2 syntax as detected in environment
        if trufflehog --json --regex --repo_path "$PROJECT_ROOT" --max_depth 1 . 2>&1 | tee "$REPORT_DIR/trufflehog_output.txt"; then
            if [ -s "$REPORT_DIR/trufflehog_output.txt" ]; then
                warning "TruffleHog detected secrets in Git history!"
                TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
            else
                success "TruffleHog secret scan passed"
            fi
        else
            warning "TruffleHog execution encountered an error"
        fi
    fi

    # 4. Checkov (IaC Security)
    if command -v checkov >/dev/null 2>&1; then
        log "Running Checkov IaC scan..."
        # Exclude vendor and research dirs
        if checkov --directory "$PROJECT_ROOT" --compact --soft-fail --framework ansible,dockerfile,kubernetes --skip-path "$PROJECT_ROOT/venv" --skip-path "$PROJECT_ROOT/.ansible" 2>&1 | tee "$REPORT_DIR/checkov_output.txt"; then
            success "Checkov IaC scan completed"
        fi
    fi

    # 5. Trivy (Vulnerability Scanner)
    if command -v trivy >/dev/null 2>&1; then
        log "Running Trivy filesystem scan..."
        # Scan only our roles and playbooks to avoid venv noise and long scans
        if trivy fs "$PROJECT_ROOT" --severity HIGH,CRITICAL --security-checks vuln,config --exit-code 0 --skip-dirs venv,.ansible,Offline_Research 2>&1 | tee "$REPORT_DIR/trivy_output.txt"; then
            success "Trivy vulnerability scan completed"
        fi
    fi

    # 6. Lynis (System Auditing)
    if command -v lynis >/dev/null 2>&1; then
        log "Running Lynis system audit (light mode)..."
        # Run a non-privileged scan for basic configuration checks
        if lynis audit system --quick --pentest 2>&1 | tee "$REPORT_DIR/lynis_output.txt"; then
            success "Lynis audit completed"
        else
            warning "Lynis reported issues (see $REPORT_DIR/lynis_output.txt)"
            # Lynis always exits non-zero if suggestions found, so we don't increment TOTAL_ISSUES hard
        fi
    fi

    # 7. RKHunter (Rootkit Detection)
    if command -v rkhunter >/dev/null 2>&1; then
        log "Running RKHunter check (local system)..."
        # Warning: This scans the RUNNER/HOST, not the project code. 
        # Included for completeness with the 'enhanced_scanning' role definition.
        if sudo rkhunter --check --sk --rwo 2>&1 | tee "$REPORT_DIR/rkhunter_output.txt"; then
            success "RKHunter scan completed"
        else
            warning "RKHunter found warnings (see $REPORT_DIR/rkhunter_output.txt)"
        fi
    fi

    # 8. Custom Forensic Integrity Checks
    log "Checking for insecure image patterns..."
    insecure_images=$(grep -r "image:" "$PROJECT_ROOT/roles" --include="main.yml" | grep "latest" | grep -v "@sha256" || true)
    if [ -n "$insecure_images" ]; then
        warning "Insecure 'latest' tag without digest found in roles!"
        echo "$insecure_images"
        TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
    fi
}

# Enforce Python standards
enforce_python_standards() {
    log "Enforcing Python coding standards..."
    py_files=$(find "$PROJECT_ROOT" -name "*.py" -not -path "*/.git/*" -not -path "*/.venv/*" -not -path "*/venv/*" -not -path "*/.ansible/*" -not -path "*/Offline_Research/*")
    if [ -z "$py_files" ]; then
        warning "No local Python files found"
        return 0
    fi
    if command -v flake8 >/dev/null 2>&1; then
        log "Running flake8..."
        if flake8 --max-line-length=120 --ignore=E501,W503 $py_files 2>&1 | tee "$REPORT_DIR/flake8_output.txt"; then
            success "Python scripts pass flake8"
        else
            warning "flake8 found issues"
            issue_count=$(grep -cE "^.*:[0-9]+:[0-9]+:" "$REPORT_DIR/flake8_output.txt" 2>/dev/null || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce YAML standards
enforce_yaml_standards() {
    log "Enforcing YAML formatting standards..."
    if command -v yamllint >/dev/null 2>&1; then
        log "Running yamllint..."
        if yamllint -c "$PROJECT_ROOT/.yamllint.yml" "$PROJECT_ROOT/roles" "$PROJECT_ROOT/playbooks" 2>&1 | tee "$REPORT_DIR/yaml_output.txt"; then
            success "YAML files pass yamllint"
        else
            warning "yamllint found issues"
            issue_count=$(grep -cE "^.*:[0-9]+:[0-9]+:" "$REPORT_DIR/yaml_output.txt" 2>/dev/null || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce Ansible standards
enforce_ansible_standards() {
    log "Enforcing Ansible best practices..."
    if command -v ansible-lint >/dev/null 2>&1; then
        log "Running ansible-lint..."
        if ansible-lint -x internal-error "$PROJECT_ROOT" 2>&1 | tee "$REPORT_DIR/ansible_output.txt"; then
            success "Ansible roles pass ansible-lint"
        else
            warning "ansible-lint found issues"
            issue_count=$(grep -cE "^.*:[0-9]+:" "$REPORT_DIR/ansible_output.txt" 2>/dev/null || echo "0")
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce Shell standards
enforce_shell_standards() {
    log "Enforcing Shell scripting standards..."
    if command -v shellcheck >/dev/null 2>&1; then
        log "Running shellcheck..."
        sh_files=$(find "$PROJECT_ROOT" -maxdepth 2 -name "*.sh" -not -path "*/.git/*" && find "$PROJECT_ROOT/scripts" -name "*.sh")
        if [ -n "$sh_files" ]; then
            if shellcheck $sh_files 2>&1 | tee "$REPORT_DIR/shell_output.txt"; then
                success "Shell scripts pass shellcheck"
            else
                warning "shellcheck found issues"
                issue_count=$(grep -cE "^In .* line [0-9]+:" "$REPORT_DIR/shell_output.txt" 2>/dev/null || echo "0")
                TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
            fi
        fi
    fi
}

# Check naming conventions
check_naming_conventions() {
    log "Checking forensic naming conventions..."
    local errors=0
    # Use -wholename or robust exclusions to avoid find warnings
    while IFS= read -r file; do
        non_compliant=$(grep -n -E "^[[:space:]]*- name:" "$file" | \
          grep -v '^[[:space:]]*#' | \
          grep -v -E " - name:[[:space:]]*[\"'][^|]+[|][[:space:]]*([^|]+[|][[:space:]]*)?([0-9]{6}|[DSU]|Audit Code|Audit Code [0-9]{6})[[:space:]]*[|]" || true)
        
        if [ -n "$non_compliant" ]; then
          filtered_non_compliant=""
          while IFS= read -r line; do
            indent=$(echo "$line" | sed -E 's/^([[:space:]]*).*/\1/' | wc -c)
            if [ "$indent" -le 6 ]; then
              filtered_non_compliant="${filtered_non_compliant}${line}\n"
            fi
          done <<< "$non_compliant"
          
          if [ -n "$filtered_non_compliant" ] && [ "$filtered_non_compliant" != "\n" ]; then
            errors=$((errors + 1))
          fi
        fi
    done < <(find roles playbooks -name "*.yml" -not -path "*/molecule/*" -not -path "*/meta/main.yml" -not -path "*/venv/*" -not -path "*/.ansible/*" -not -path "*/Offline_Research/*")
    
    if [ "$errors" -gt 0 ]; then
        warning "$errors files have tasks missing forensic Audit IDs"
        TOTAL_ISSUES=$((TOTAL_ISSUES + errors))
    else
        success "Forensic naming conventions verified"
    fi
}

# Check for secrets
check_secrets() {
    log "Checking for exposed secrets (detect-secrets)..."
    if command -v detect-secrets >/dev/null 2>&1; then
        if detect-secrets scan "$PROJECT_ROOT" --exclude-files ".secrets.baseline" --exclude-files ".ansible" --exclude-files "venv" --exclude-files "Offline_Research" 2>&1 | tee "$REPORT_DIR/secrets_output.txt"; then
            success "No new secrets detected"
        else
            warning "Potential secrets detected!"
            TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
        fi
    fi
}

# Check file permissions
check_permissions() {
    log "Checking critical file permissions..."
    if [ -f "$PROJECT_ROOT/.vault_pass" ]; then
        perm=$(stat -c "%a" "$PROJECT_ROOT/.vault_pass")
        if [ "$perm" != "600" ]; then
            warning "Incorrect permissions on .vault_pass: $perm (expected 600)"
            TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
            if [ "$AUTO_FIX" = true ]; then
                chmod 600 "$PROJECT_ROOT/.vault_pass"
                success "Permissions corrected"
                FIXED_ISSUES=$((FIXED_ISSUES + 1))
            fi
        fi
    fi
    success "Permissions verified"
}

# Main function
main() {
    echo "========================================"
    echo "  Style Guide Enforcement Tool (v1.7)"
    echo "========================================"
    echo ""

    check_dependencies

    if [ "$REPORT_ONLY" = false ]; then
        enforce_security_audit
        enforce_python_standards
        enforce_yaml_standards
        enforce_ansible_standards
        enforce_shell_standards
        check_naming_conventions
        check_secrets
        check_permissions
    fi

    echo ""
    echo "========================================"
    echo "           Final Summary"
    echo "========================================"
    echo "Total Issues:   $TOTAL_ISSUES"
    echo "Fixed Issues:   $FIXED_ISSUES"
    echo "Remaining:      $((TOTAL_ISSUES - FIXED_ISSUES))"
    echo "========================================"

    if [ "$TOTAL_ISSUES" -gt 0 ] && [ "$((TOTAL_ISSUES - FIXED_ISSUES))" -gt 0 ]; then
        warning "Issues found. Review the reports in $REPORT_DIR for details."
        exit 1
    else
        success "All style and security checks passed!"
        exit 0
    fi
}

main
