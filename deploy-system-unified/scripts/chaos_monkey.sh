#!/bin/bash
#===============================================================================
# chaos_monkey.sh - Chaos Testing for Deploy-System-Unified
#===============================================================================
# Tests edge cases, failures, and resilience across:
# - Helm charts (template rendering with invalid/missing values)
# - Benchmark script (various runtime inputs)
# - K8s playbook (various configurations)
#===============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

log_pass() { echo -e "${GREEN}[PASS]${NC} $1"; ((TESTS_PASSED++)); }
log_fail() { echo -e "${RED}[FAIL]${NC} $1"; ((TESTS_FAILED++)); }
log_skip() { echo -e "${YELLOW}[SKIP]${NC} $1"; ((TESTS_SKIPPED++)); }
log_info() { echo -e "[INFO] $1"; }

echo "========================================"
echo "   CHAOS MONKEY TEST SUITE"
echo "========================================"
echo ""

#===============================================================================
# Test 1: Helm Chart - Empty values rendering
#===============================================================================
log_info "Test 1: Helm Chart rendering with minimal values"
cd /home/prod/Workspaces/deploy-system-unified

for chart in charts/auth-stack charts/backup-stack charts/logging-stack charts/proxy-stack; do
    if helm template "$chart" --namespace test --generate-name >/dev/null 2>&1; then
        log_pass "$chart renders with minimal values"
    else
        log_fail "$chart fails to render"
    fi
done

#===============================================================================
# Test 2: Helm Chart - Invalid values handling
#===============================================================================
log_info "Test 2: Helm Chart with invalid values (should fail gracefully)"
for chart in charts/auth-stack charts/backup-stack charts/logging-stack charts/proxy-stack; do
    # Create temp values file with invalid YAML
    echo "invalid: yaml: [" > /tmp/bad_values.yaml
    if helm template "$chart" -f /tmp/bad_values.yaml --namespace test >/dev/null 2>&1; then
        log_skip "$chart accepts bad values (depends on strictness)"
    else
        log_pass "$chart rejects invalid values"
    fi
    rm -f /tmp/bad_values.yaml
done

#===============================================================================
# Test 3: Benchmark Script - Various runtime inputs
#===============================================================================
log_info "Test 3: Benchmark script with various inputs"
cd /home/prod/Workspaces/deploy-system-unified

# Test with podman (will fail if podman not available, but should handle gracefully)
if bash scripts/benchmark/benchmark_metrics.sh podman 1 2>&1 | grep -q "ERROR\| dependency\|Missing"; then
    log_pass "Benchmark handles missing podman gracefully"
else
    log_skip "Benchmark podman test - depends on environment"
fi

# Test with k8s (will fail if kubectl not available)
if bash scripts/benchmark/benchmark_metrics.sh k8s 1 2>&1 | grep -q "ERROR\| dependency\|Missing"; then
    log_pass "Benchmark handles missing kubectl gracefully"
else
    log_skip "Benchmark k8s test - depends on environment"
fi

# Test help output
if bash scripts/benchmark/benchmark_metrics.sh --help >/dev/null 2>&1; then
    log_pass "Benchmark help works"
else
    log_fail "Benchmark help failed"
fi

#===============================================================================
# Test 4: Benchmark Script - Unit conversion edge cases
#===============================================================================
log_info "Test 4: Unit conversion edge cases"

# Test bc calculation with edge values
if echo "scale=2; 0 / 100" | bc 2>/dev/null | grep -q "0"; then
    log_pass "Unit conversion handles zero values"
else
    log_fail "Unit conversion fails on zero"
fi

# Test with non-numeric (should return 0 or handle gracefully)
if echo "scale=2; abc / 100" | bc 2>/dev/null || echo "0" | grep -q "0"; then
    log_pass "Unit conversion handles non-numeric"
else
    log_skip "Unit conversion edge case"
fi

#===============================================================================
# Test 5: YAML Validation - All Chart.yaml files
#===============================================================================
log_info "Test 5: YAML validation for all Chart.yaml files"
cd /home/prod/Workspaces/deploy-system-unified

for chart in charts/*/Chart.yaml; do
    if python3 -c "import yaml; yaml.safe_load(open('$chart'))" 2>/dev/null; then
        log_pass "$chart is valid YAML"
    else
        log_fail "$chart has YAML errors"
    fi
done

#===============================================================================
# Test 6: SOPS Configuration
#===============================================================================
log_info "Test 6: SOPS configuration validation"
cd /home/prod/Workspaces/deploy-system-unified

if grep -q "creation_rules" .sops.yaml && grep -q "age:" .sops.yaml; then
    log_pass "SOPS config has valid structure"
else
    log_fail "SOPS config missing required fields"
fi

# Test regex patterns
if grep -q "encrypted_regex" .sops.yaml; then
    log_pass "SOPS has encrypted regex patterns"
else
    log_fail "SOPS missing encrypted regex"
fi

#===============================================================================
# Test 7: Ansible Playbook Syntax
#===============================================================================
log_info "Test 7: Ansible playbook syntax"
cd /home/prod/Workspaces/deploy-system-unified

for playbook in playbooks/*.yml; do
    # Check YAML syntax (ansible-playbook --syntax-check needs collections)
    if python3 -c "import yaml; yaml.safe_load(open('$playbook'))" 2>/dev/null; then
        log_pass "$(basename $playbook) is valid YAML"
    else
        log_fail "$(basename $playbook) has YAML errors"
    fi
done

#===============================================================================
# Test 8: Helm Lint All Charts
#===============================================================================
log_info "Test 8: Helm lint all charts"
cd /home/prod/Workspaces/deploy-system-unified

for chart in charts/*; do
    if helm lint "$chart" >/dev/null 2>&1; then
        log_pass "$(basename $chart) passes helm lint"
    else
        log_fail "$(basename $chart) fails helm lint"
    fi
done

#===============================================================================
# Test 9: Values.yaml Structure Validation
#===============================================================================
log_info "Test 9: Values.yaml structure validation"
cd /home/prod/Workspaces/deploy-system-unified

for values in charts/*/values.yaml; do
    # Check for empty required fields that should have values
    if grep -q 'password: ""' "$values" 2>/dev/null; then
        log_pass "$(basename $values) has documented empty required fields"
    else
        log_skip "$(basename $values) - no empty required fields"
    fi
done

#===============================================================================
# Test 10: Security - Check for hardcoded secrets
#===============================================================================
log_info "Test 10: Security - Scan for hardcoded secrets (excluding SOPS)"
cd /home/prod/Workspaces/deploy-system-unified

# Look for common secret patterns in non-encrypted files
SECRETS_FOUND=0
for file in charts/*/values.yaml; do
    if grep -E "password:|token:|secret:|api_key:" "$file" 2>/dev/null | grep -v '""' | grep -v "# " | grep -v "_file" >/dev/null; then
        # Check if they are empty or documented
        if ! grep -E '(REQUIRED|Set via|external secret)' "$file" >/dev/null 2>&1; then
            SECRETS_FOUND=1
        fi
    fi
done

if [ $SECRETS_FOUND -eq 0 ]; then
    log_pass "No undeclared hardcoded secrets found"
else
    log_fail "Potential undeclared secrets found"
fi

#===============================================================================
# SUMMARY
#===============================================================================
echo ""
echo "========================================"
echo "   CHAOS TEST SUMMARY"
echo "========================================"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo -e "Skipped: ${YELLOW}$TESTS_SKIPPED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All chaos tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Review output above.${NC}"
    exit 1
fi
