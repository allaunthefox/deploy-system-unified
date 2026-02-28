#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400028
# Script Type: Bulk Audit Code Assignment
# Description: Adds audit code headers to all remaining files
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Bulk Audit Code Assignment Script
# Adds audit code headers to remaining files in the repository

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "=== Deploy-System-Unified Bulk Audit Code Assignment ==="
echo "Project directory: $PROJECT_DIR"
echo ""

# Counter for audit codes
INVENTORY_COUNTER=700004
TEMPLATE_COUNTER=900001
TASK_COUNTER=110000
DEFAULTS_COUNTER=120000
HANDLER_COUNTER=130000
MOLECULE_COUNTER=1000001

# ============================================================================
# 1. Inventory Files
# ============================================================================
echo "[1/7] Processing inventory files..."

for f in inventory/*.ini inventory/group_vars/*.yml inventory/host_vars/*.yml inventory/group_vars/all/*.yml; do
    if [ -f "$f" ] && ! grep -q "Audit Event Identifier" "$f" 2>/dev/null; then
        CODE="DSU-INV-$(printf '%06d' $INVENTORY_COUNTER)"
        if [[ "$f" == *.ini ]]; then
            TYPE="Inventory (INI)"
        else
            TYPE="Inventory (YAML)"
        fi
        cat > /tmp/inv_header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# Inventory Type: $TYPE
# File: $f
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/inv_header.txt "$f" > /tmp/inv_new.txt && mv /tmp/inv_new.txt "$f"
        echo "  ✓ $f -> $CODE"
        INVENTORY_COUNTER=$((INVENTORY_COUNTER + 1))
    fi
done

# ============================================================================
# 2. Jinja2 Templates
# ============================================================================
echo ""
echo "[2/7] Processing Jinja2 templates..."

for f in $(find roles -name "*.j2" -type f 2>/dev/null | head -50); do
    if ! grep -q "Audit Event Identifier" "$f" 2>/dev/null; then
        CODE="DSU-TPL-$(printf '%06d' $TEMPLATE_COUNTER)"
        ROLE_NAME=$(echo "$f" | sed 's|roles/||' | cut -d'/' -f2)
        cat > /tmp/tpl_header.txt << EOF
{# =============================================================================
# Audit Event Identifier: $CODE
# Template Type: $ROLE_NAME Configuration
# File: $f
# Last Updated: 2026-02-28
# Version: 1.0
# ============================================================================= #}
EOF
        cat /tmp/tpl_header.txt "$f" > /tmp/tpl_new.txt && mv /tmp/tpl_new.txt "$f"
        echo "  ✓ $f -> $CODE"
        TEMPLATE_COUNTER=$((TEMPLATE_COUNTER + 1))
    fi
done

# ============================================================================
# 3. Test YAML Files
# ============================================================================
echo ""
echo "[3/7] Processing test YAML files..."

for f in tests/*.yml; do
    if [ -f "$f" ] && ! grep -q "Audit Event Identifier" "$f" 2>/dev/null; then
        CODE="DSU-TST-1000110"
        cat > /tmp/test_header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Test Playbook
# File: $f
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/test_header.txt "$f" > /tmp/test_new.txt && mv /tmp/test_new.txt "$f"
        echo "  ✓ $f -> $CODE"
    fi
done

# ============================================================================
# 4. Role Task Files (main.yml only for now)
# ============================================================================
echo ""
echo "[4/7] Processing role task files (main.yml)..."

for f in $(find roles -path "*/tasks/main.yml" -type f 2>/dev/null | head -120); do
    if ! grep -q "Audit Event Identifier" "$f" 2>/dev/null; then
        CODE="DSU-PLY-$(printf '%06d' $TASK_COUNTER)"
        ROLE_NAME=$(echo "$f" | sed 's|roles/||' | cut -d'/' -f2)
        cat > /tmp/task_header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Role Tasks (main.yml)
# Role: $ROLE_NAME
# File: $f
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/task_header.txt "$f" > /tmp/task_new.txt && mv /tmp/task_new.txt "$f"
        echo "  ✓ $f -> $CODE"
        TASK_COUNTER=$((TASK_COUNTER + 1))
    fi
done

# ============================================================================
# 5. Role Defaults
# ============================================================================
echo ""
echo "[5/7] Processing role defaults..."

for f in $(find roles -path "*/defaults/main.yml" -type f 2>/dev/null | head -100); do
    if ! grep -q "Audit Event Identifier" "$f" 2>/dev/null; then
        CODE="DSU-PLY-$(printf '%06d' $DEFAULTS_COUNTER)"
        ROLE_NAME=$(echo "$f" | sed 's|roles/||' | cut -d'/' -f2)
        cat > /tmp/def_header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Role Defaults (main.yml)
# Role: $ROLE_NAME
# File: $f
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/def_header.txt "$f" > /tmp/def_new.txt && mv /tmp/def_new.txt "$f"
        echo "  ✓ $f -> $CODE"
        DEFAULTS_COUNTER=$((DEFAULTS_COUNTER + 1))
    fi
done

# ============================================================================
# 6. Role Handlers
# ============================================================================
echo ""
echo "[6/7] Processing role handlers..."

for f in $(find roles -path "*/handlers/main.yml" -type f 2>/dev/null | head -100); do
    if ! grep -q "Audit Event Identifier" "$f" 2>/dev/null; then
        CODE="DSU-PLY-$(printf '%06d' $HANDLER_COUNTER)"
        ROLE_NAME=$(echo "$f" | sed 's|roles/||' | cut -d'/' -f2)
        cat > /tmp/handler_header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Role Handlers (main.yml)
# Role: $ROLE_NAME
# File: $f
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/handler_header.txt "$f" > /tmp/handler_new.txt && mv /tmp/handler_new.txt "$f"
        echo "  ✓ $f -> $CODE"
        HANDLER_COUNTER=$((HANDLER_COUNTER + 1))
    fi
done

# ============================================================================
# 7. Molecule Test Files (bulk by scenario)
# ============================================================================
echo ""
echo "[7/7] Processing molecule test files (bulk assignment)..."

# Process molecule.yml files by scenario
for scenario_dir in $(find molecule -maxdepth 1 -type d 2>/dev/null | grep -v "^molecule$" | head -20); do
    SCENARIO_NAME=$(basename "$scenario_dir")
    MOLECULE_YML="$scenario_dir/molecule.yml"
    if [ -f "$MOLECULE_YML" ] && ! grep -q "Audit Event Identifier" "$MOLECULE_YML" 2>/dev/null; then
        CODE="DSU-TST-$(printf '%07d' $MOLECULE_COUNTER)"
        cat > /tmp/mol_header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Molecule Scenario Configuration
# Scenario: $SCENARIO_NAME
# File: $MOLECULE_YML
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/mol_header.txt "$MOLECULE_YML" > /tmp/mol_new.txt && mv /tmp/mol_new.txt "$MOLECULE_YML"
        echo "  ✓ $MOLECULE_YML -> $CODE"
        MOLECULE_COUNTER=$((MOLECULE_COUNTER + 10))
    fi
done

# Also process role-specific molecule files
for f in $(find roles -path "*/molecule/*/molecule.yml" -type f 2>/dev/null | head -50); do
    if ! grep -q "Audit Event Identifier" "$f" 2>/dev/null; then
        CODE="DSU-TST-$(printf '%07d' $MOLECULE_COUNTER)"
        cat > /tmp/mol_header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Molecule Scenario Configuration
# File: $f
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/mol_header.txt "$f" > /tmp/mol_new.txt && mv /tmp/mol_new.txt "$f"
        echo "  ✓ $f -> $CODE"
        MOLECULE_COUNTER=$((MOLECULE_COUNTER + 10))
    fi
done

echo ""
echo "=== Bulk Assignment Complete ==="
echo "Inventory files processed: $((INVENTORY_COUNTER - 700004))"
echo "Templates processed: $((TEMPLATE_COUNTER - 900001))"
echo "Task files processed: $((TASK_COUNTER - 110000))"
echo "Defaults processed: $((DEFAULTS_COUNTER - 120000))"
echo "Handlers processed: $((HANDLER_COUNTER - 130000))"
echo "Molecule files processed: $((MOLECULE_COUNTER - 1000001))"
echo ""
echo "Total files updated: $((INVENTORY_COUNTER - 700004 + TEMPLATE_COUNTER - 900001 + TASK_COUNTER - 110000 + DEFAULTS_COUNTER - 120000 + HANDLER_COUNTER - 130000 + (MOLECULE_COUNTER - 1000001) / 10))"
