#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400004
# Script Type: Security Validation (Helm Charts)
# Description: Validates Helm charts against security standards
# Usage: ./scripts/validate-chart-security.sh <chart-directory>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Chart Security Validation Script
# Validates Helm charts against Deploy-System-Unified security standards
#
# Usage: ./scripts/validate-chart-security.sh <chart-directory>
# Example: ./scripts/validate-chart-security.sh charts/monitoring-stack

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0

log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    PASS=$((PASS + 1))
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    FAIL=$((FAIL + 1))
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARN=$((WARN + 1))
}

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <chart-directory>"
    echo "Example: $0 charts/monitoring-stack"
    exit 1
fi

CHART_DIR="$1"

if [ ! -d "$CHART_DIR" ]; then
    echo -e "${RED}Error: Chart directory not found: $CHART_DIR${NC}"
    exit 1
fi

echo "========================================"
echo "Security Validation: $CHART_DIR"
echo "========================================"
echo ""

# Check for required files
echo "=== File Structure ==="
if [ -f "$CHART_DIR/Chart.yaml" ]; then
    log_pass "Chart.yaml exists"
else
    log_fail "Chart.yaml missing"
fi

if [ -f "$CHART_DIR/values.yaml" ]; then
    log_pass "values.yaml exists"
else
    log_fail "values.yaml missing"
fi

if [ -d "$CHART_DIR/templates" ]; then
    log_pass "templates/ directory exists"
else
    log_fail "templates/ directory missing"
fi

echo ""
echo "=== RBAC Configuration ==="

# Check for ServiceAccount
if grep -r "kind: ServiceAccount" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "ServiceAccount template found"
else
    log_warn "ServiceAccount template not found (may use default)"
fi

# Check for Role/ClusterRole
if grep -r "kind: Role\|kind: ClusterRole" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "Role/ClusterRole template found"
else
    log_warn "Role/ClusterRole template not found"
fi

# Check for RoleBinding
if grep -r "kind: RoleBinding\|kind: ClusterRoleBinding" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "RoleBinding template found"
else
    log_warn "RoleBinding template not found"
fi

# Check serviceAccountName reference in deployments
if grep -r "serviceAccountName:" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "Deployments reference ServiceAccount"
else
    log_warn "Deployments may use default ServiceAccount"
fi

echo ""
echo "=== Pod Security ==="

# Check for pod securityContext
if grep -r "runAsNonRoot: true" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "runAsNonRoot: true found"
else
    log_fail "runAsNonRoot: true NOT found"
fi

if grep -r "runAsUser:" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "runAsUser defined"
else
    log_fail "runAsUser NOT defined"
fi

if grep -r "seccompProfile:" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "seccompProfile defined"
else
    log_warn "seccompProfile NOT defined"
fi

echo ""
echo "=== Container Security ==="

# Check for container securityContext
if grep -r "allowPrivilegeEscalation: false" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "allowPrivilegeEscalation: false found"
else
    log_fail "allowPrivilegeEscalation: false NOT found"
fi

if grep -r "capabilities:" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    if grep -r "drop:" "$CHART_DIR/templates/" >/dev/null 2>&1; then
        log_pass "capabilities.drop defined"
        # Check for ALL in drop (handle multiline YAML with "- ALL")
        if grep -r "drop:" "$CHART_DIR/templates/" >/dev/null 2>&1 && \
           grep -r "\- ALL" "$CHART_DIR/templates/" >/dev/null 2>&1; then
            log_pass "capabilities.drop: ALL found"
        else
            log_warn "capabilities.drop: ALL NOT found"
        fi
    else
        log_warn "capabilities defined but no drop"
    fi
else
    log_fail "capabilities NOT defined"
fi

echo ""
echo "=== Resource Management ==="

# Check for resource requests/limits
if grep -r "resources:" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    # Check if resources are defined inline or via values
    if grep -r "requests:" "$CHART_DIR/templates/" >/dev/null 2>&1 || \
       grep -r "toYaml .Values.*.resources" "$CHART_DIR/templates/" >/dev/null 2>&1; then
        log_pass "Resource requests defined"
    else
        log_warn "Resource requests NOT defined"
    fi
    
    if grep -r "limits:" "$CHART_DIR/templates/" >/dev/null 2>&1 || \
       grep -r "toYaml .Values.*.resources" "$CHART_DIR/templates/" >/dev/null 2>&1; then
        log_pass "Resource limits defined"
    else
        log_warn "Resource limits NOT defined"
    fi
else
    log_fail "Resources NOT defined"
fi

echo ""
echo "=== Health Checks ==="

# Check for probes
if grep -r "livenessProbe:" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "livenessProbe defined"
else
    log_fail "livenessProbe NOT defined"
fi

if grep -r "readinessProbe:" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "readinessProbe defined"
else
    log_fail "readinessProbe NOT defined"
fi

echo ""
echo "=== Image Security ==="

# Check for image tag (not :latest)
if grep -r "image:" "$CHART_DIR/templates/" | grep -v ":latest" >/dev/null 2>&1; then
    log_pass "Images use specific tags (not :latest)"
else
    if grep -r "image:" "$CHART_DIR/templates/" | grep ":latest" >/dev/null 2>&1; then
        log_warn "Images use :latest tag"
    else
        log_pass "Image tags appear configurable"
    fi
fi

echo ""
echo "=== Secrets Management ==="

# Check for hardcoded secrets
if grep -rE "password:.*['\"][^'\"]{8,}['\"]" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_warn "Potential hardcoded password detected"
else
    log_pass "No obvious hardcoded passwords"
fi

# Check for secretKeyRef or secret creation
if grep -r "secretKeyRef:" "$CHART_DIR/templates/" >/dev/null 2>&1 || \
   grep -r "kind: Secret" "$CHART_DIR/templates/" >/dev/null 2>&1; then
    log_pass "Uses secretKeyRef or creates Secrets"
else
    log_warn "May not use secretKeyRef"
fi

echo ""
echo "========================================"
echo "Validation Summary"
echo "========================================"
echo -e "Passed:   ${GREEN}$PASS${NC}"
echo -e "Failed:   ${RED}$FAIL${NC}"
echo -e "Warnings: ${YELLOW}$WARN${NC}"
echo ""

if [ $FAIL -gt 0 ]; then
    echo -e "${RED}VALIDATION FAILED${NC}"
    echo "Please fix the failed checks before deploying."
    exit 1
elif [ $WARN -gt 0 ]; then
    echo -e "${YELLOW}VALIDATION PASSED WITH WARNINGS${NC}"
    echo "Review warnings before production deployment."
    exit 0
else
    echo -e "${GREEN}VALIDATION PASSED${NC}"
    echo "All security checks passed!"
    exit 0
fi
