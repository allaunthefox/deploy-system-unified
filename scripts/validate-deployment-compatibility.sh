#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400005
# Script Type: Compatibility Validation
# Description: Checks for known incompatibilities before deployment
# Usage: ./scripts/validate-deployment-compatibility.sh [inventory-file]
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Deployment Compatibility Validator
# Checks for known incompatibilities before deployment
#
# Usage: ./scripts/validate-deployment-compatibility.sh [inventory-file]
# Example: ./scripts/validate-deployment-compatibility.sh inventory/production.ini

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Counters
PASS=0
WARN=0
FAIL=0

log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS++))
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARN++))
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL++))
}

echo "========================================"
echo "Deployment Compatibility Validator"
echo "========================================"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    log_warn "kubectl not found - skipping cluster checks"
    KUBECTL_AVAILABLE=false
else
    KUBECTL_AVAILABLE=true
fi

# Check 1: Multiple Ingress Controllers
echo "=== Checking: Ingress Controllers ==="
if [ "$KUBECTL_AVAILABLE" = true ]; then
    INGRESS_COUNT=$(kubectl get daemonsets,deployments -A -l app.kubernetes.io/component=ingress 2>/dev/null | wc -l || echo "0")
    if [ "$INGRESS_COUNT" -gt 1 ]; then
        log_fail "Multiple ingress controllers detected ($INGRESS_COUNT). Use only ONE."
    else
        log_pass "Single ingress controller configured"
    fi
else
    log_warn "Skipping ingress check (no kubectl)"
fi

# Check 2: DNS Conflicts
echo ""
echo "=== Checking: DNS Configuration ==="
if [ "$KUBECTL_AVAILABLE" = true ]; then
    COREDNS_PODS=$(kubectl get pods -n kube-system -l k8s-app=kube-dns 2>/dev/null | grep -c Running || echo "0")
    if [ "$COREDNS_PODS" -gt 0 ]; then
        log_pass "CoreDNS is running"
    else
        log_warn "CoreDNS not running - cluster DNS may be broken"
    fi
else
    log_warn "Skipping DNS check (no kubectl)"
fi

# Check 3: GPU Device Plugin
echo ""
echo "=== Checking: GPU Configuration ==="
GPU_IN_VALUES=$(grep -r "gpu.enabled: true" charts/*/values*.yaml 2>/dev/null | wc -l || echo "0")
if [ "$GPU_IN_VALUES" -gt 0 ]; then
    log_warn "GPU enabled in chart values - checking for device plugin..."
    if [ "$KUBECTL_AVAILABLE" = true ]; then
        GPU_PLUGIN=$(kubectl get daemonsets -n kube-system -l app=device-plugin 2>/dev/null | wc -l || echo "0")
        if [ "$GPU_PLUGIN" -eq 0 ]; then
            log_fail "GPU enabled but no device plugin found. Install plugin or disable GPU."
        else
            log_pass "GPU device plugin present"
        fi
    else
        log_warn "Cannot verify GPU plugin (no kubectl)"
    fi
else
    log_pass "GPU not enabled (no check needed)"
fi

# Check 4: Resource Validation
echo ""
echo "=== Checking: Cluster Resources ==="
if [ "$KUBECTL_AVAILABLE" = true ]; then
    TOTAL_CPU=$(kubectl top nodes 2>/dev/null | awk 'NR>1 {sum+=$2} END {print sum+0}' || echo "0")
    TOTAL_MEM=$(kubectl top nodes 2>/dev/null | awk 'NR>1 {sum+=$4} END {print sum+0}' || echo "0")
    
    echo "  Total CPU: ${TOTAL_CPU}m"
    echo "  Total Memory: ${TOTAL_MEM}Mi"
    
    # Check against production requirements
    if [ "$TOTAL_CPU" -lt 16000 ]; then
        log_warn "CPU < 16 cores - Production profile may fail"
    else
        log_pass "Sufficient CPU for production"
    fi
    
    if [ "$TOTAL_MEM" -lt 64000 ]; then
        log_warn "Memory < 64Gi - Production profile may fail"
    else
        log_pass "Sufficient memory for production"
    fi
else
    log_warn "Skipping resource check (no kubectl)"
fi

# Check 5: Storage Class
echo ""
echo "=== Checking: Storage Configuration ==="
if [ "$KUBECTL_AVAILABLE" = true ]; then
    STORAGE_CLASS_COUNT=$(kubectl get storageclass 2>/dev/null | grep -c "default\|(default)" || echo "0")
    if [ "$STORAGE_CLASS_COUNT" -gt 0 ]; then
        log_pass "Default storage class available"
    else
        log_warn "No default storage class - PVCs may not bind"
    fi
else
    log_warn "Skipping storage check (no kubectl)"
fi

# Check 6: Inventory File Validation
echo ""
echo "=== Checking: Inventory Configuration ==="
INVENTORY_FILE="${1:-inventory/production.ini}"
if [ -f "$INVENTORY_FILE" ]; then
    log_pass "Inventory file exists: $INVENTORY_FILE"
    
    # Check for production profile
    if grep -q "production" "$INVENTORY_FILE" 2>/dev/null; then
        log_warn "Production profile detected - verify hardware requirements"
    fi
else
    log_warn "Inventory file not found: $INVENTORY_FILE"
fi

# Check 7: Secrets Configuration
echo ""
echo "=== Checking: Secrets Configuration ==="
if [ -f "inventory/group_vars/all/secrets.sops.yml" ]; then
    log_pass "SOPS encrypted secrets found"
elif [ -f "inventory/group_vars/all/secrets.sops.template.yaml" ]; then
    log_warn "SOPS template found but not encrypted. Run: sops -e secrets.sops.template.yaml > secrets.sops.yml"
else
    log_warn "No secrets file found. Create secrets before production deployment."
fi

# Check 8: Preflight Validation
echo ""
echo "=== Checking: Preflight Requirements ==="
if command -v ansible-playbook &> /dev/null; then
    if [ -f "playbooks/preflight_validate.yml" ]; then
        log_pass "Preflight validation playbook available"
        echo "  Run: ansible-playbook playbooks/preflight_validate.yml -i $INVENTORY_FILE"
    else
        log_warn "Preflight validation playbook not found"
    fi
else
    log_warn "Ansible not found - cannot run preflight checks"
fi

# Summary
echo ""
echo "========================================"
echo "Validation Summary"
echo "========================================"
echo -e "Passed:   ${GREEN}$PASS${NC}"
echo -e "Warnings: ${YELLOW}$WARN${NC}"
echo -e "Failed:   ${RED}$FAIL${NC}"
echo ""

if [ $FAIL -gt 0 ]; then
    echo -e "${RED}❌ VALIDATION FAILED${NC}"
    echo "Fix the failed checks before deploying."
    echo ""
    echo "Recommended actions:"
    if grep -q "Multiple ingress" <<< "$FAIL"; then
        echo "  - Remove extra ingress controllers"
    fi
    if grep -q "GPU enabled but no device plugin" <<< "$FAIL"; then
        echo "  - Install GPU device plugin OR disable GPU in values"
    fi
    exit 1
elif [ "$WARN" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  VALIDATION PASSED WITH WARNINGS${NC}"
    echo "Review warnings before production deployment."
    exit 0
else
    echo -e "${GREEN}✅ VALIDATION PASSED${NC}"
    echo "All compatibility checks passed!"
    exit 0
fi
