#!/usr/bin/env bash
# Stability 2026 - Idempotence Verification Tool
# This script runs a playbook and ensures that a subsequent run produces zero changes.

set -euo pipefail

PLAYBOOK=$1
INVENTORY=${2:-inventory/local.ini}

if [ -z "$PLAYBOOK" ]; then
    echo "Usage: $0 <playbook> [inventory]"
    exit 1
fi

echo "--- STABILITY GATE: IDEMPOTENCE VERIFICATION ---"
echo "Target Playbook: $PLAYBOOK"
echo "Inventory: $INVENTORY"

# Step 1: Initial Converge (In a real CI, the system might already be converged)
echo "Step 1: Running initial convergence..."
ansible-playbook "$PLAYBOOK" -i "$INVENTORY"

# Step 2: Idempotence Check
echo "Step 2: Verifying idempotence (repeat run)..."
ansible-playbook "$PLAYBOOK" -i "$INVENTORY" > /tmp/idempotence_run.log 2>&1

# Check for changes in the log
# Ansible output for idempotence is usually 'changed=0'
if grep -q "changed=0" /tmp/idempotence_run.log && ! grep -q "changed=[1-9]" /tmp/idempotence_run.log; then
    echo "SUCCESS: Idempotence confirmed. Zero changes on second run."
    exit 0
else
    echo "FAILURE: Changes detected on second run. System is not idempotent."
    grep "changed=" /tmp/idempotence_run.log
    exit 1
fi
