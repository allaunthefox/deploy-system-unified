#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400028
# Script Type: Bulk Audit Code Assignment (Fixed)
# Description: Adds audit codes to all remaining role files
# Usage: ./bulk_assign_role_codes.sh
# Last Updated: 2026-02-28
# Version: 1.1 (Fixed)
# =============================================================================

set -eu

PROJECT_DIR="/home/prod/Workspaces/repos/github/deploy-system-unified"
cd "$PROJECT_DIR"

echo "=== Bulk Role File Audit Code Assignment ==="
echo "Project: $PROJECT_DIR"
echo ""

# Counters
TASK_COUNTER=110000
DEFAULTS_COUNTER=120000
HANDLER_COUNTER=130000
TEMPLATE_COUNTER=900000
MOLECULE_COUNTER=1000000

# ============================================================================
# 1. Role Task Files (main.yml)
# ============================================================================
echo "[1/5] Processing role task files (main.yml)..."

for role_dir in roles/*/; do
    ROLE_NAME=$(basename "$role_dir")
    TASK_FILE="$role_dir/tasks/main.yml"
    
    if [ -f "$TASK_FILE" ] && ! grep -q "Audit Event Identifier" "$TASK_FILE" 2>/dev/null; then
        TASK_COUNTER=$((TASK_COUNTER + 1))
        CODE="DSU-PLY-$(printf '%06d' $TASK_COUNTER)"
        
        cat > /tmp/header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Role Tasks (main.yml)
# Role: $ROLE_NAME
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/header.txt "$TASK_FILE" > /tmp/new.txt && mv /tmp/new.txt "$TASK_FILE"
        echo "  ✓ $TASK_FILE -> $CODE"
    fi
done

# ============================================================================
# 2. Role Defaults (main.yml)
# ============================================================================
echo ""
echo "[2/5] Processing role defaults (main.yml)..."

for role_dir in roles/*/; do
    ROLE_NAME=$(basename "$role_dir")
    DEFAULTS_FILE="$role_dir/defaults/main.yml"
    
    if [ -f "$DEFAULTS_FILE" ] && ! grep -q "Audit Event Identifier" "$DEFAULTS_FILE" 2>/dev/null; then
        DEFAULTS_COUNTER=$((DEFAULTS_COUNTER + 1))
        CODE="DSU-PLY-$(printf '%06d' $DEFAULTS_COUNTER)"
        
        cat > /tmp/header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Role Defaults (main.yml)
# Role: $ROLE_NAME
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/header.txt "$DEFAULTS_FILE" > /tmp/new.txt && mv /tmp/new.txt "$DEFAULTS_FILE"
        echo "  ✓ $DEFAULTS_FILE -> $CODE"
    fi
done

# ============================================================================
# 3. Role Handlers (main.yml)
# ============================================================================
echo ""
echo "[3/5] Processing role handlers (main.yml)..."

for role_dir in roles/*/; do
    ROLE_NAME=$(basename "$role_dir")
    HANDLER_FILE="$role_dir/handlers/main.yml"
    
    if [ -f "$HANDLER_FILE" ] && ! grep -q "Audit Event Identifier" "$HANDLER_FILE" 2>/dev/null; then
        HANDLER_COUNTER=$((HANDLER_COUNTER + 1))
        CODE="DSU-PLY-$(printf '%06d' $HANDLER_COUNTER)"
        
        cat > /tmp/header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Role Handlers (main.yml)
# Role: $ROLE_NAME
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
        cat /tmp/header.txt "$HANDLER_FILE" > /tmp/new.txt && mv /tmp/new.txt "$HANDLER_FILE"
        echo "  ✓ $HANDLER_FILE -> $CODE"
    fi
done

# ============================================================================
# 4. Jinja2 Templates
# ============================================================================
echo ""
echo "[4/5] Processing Jinja2 templates..."

# Use process substitution to avoid subshell counter issue
while read -r template_file; do
    if ! grep -q "Audit Event Identifier" "$template_file" 2>/dev/null; then
        TEMPLATE_COUNTER=$((TEMPLATE_COUNTER + 1))
        CODE="DSU-TPL-$(printf '%06d' $TEMPLATE_COUNTER)"
        ROLE_NAME=$(echo "$template_file" | sed 's|roles/||' | cut -d'/' -f2)
        
        cat > /tmp/header.txt << EOF
{# =============================================================================
# Audit Event Identifier: $CODE
# Template Type: $ROLE_NAME Configuration
# Last Updated: 2026-02-28
# Version: 1.0
# ============================================================================= #}
EOF
        cat /tmp/header.txt "$template_file" > /tmp/new.txt && mv /tmp/new.txt "$template_file"
        echo "  ✓ $template_file -> $CODE"
    fi
done < <(find roles -name "*.j2" -type f 2>/dev/null)

# ============================================================================
# 5. Molecule Files (by scenario)
# ============================================================================
echo ""
echo "[5/5] Processing molecule files..."

# Root molecule scenarios
for scenario_dir in molecule/*/; do
    if [ -d "$scenario_dir" ]; then
        SCENARIO_NAME=$(basename "$scenario_dir")
        MOLECULE_YML="$scenario_dir/molecule.yml"
        
        if [ -f "$MOLECULE_YML" ] && ! grep -q "Audit Event Identifier" "$MOLECULE_YML" 2>/dev/null; then
            MOLECULE_COUNTER=$((MOLECULE_COUNTER + 1))
            CODE="DSU-TST-$(printf '%07d' $MOLECULE_COUNTER)"
            
            cat > /tmp/header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Molecule Scenario Configuration
# Scenario: $SCENARIO_NAME
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
            cat /tmp/header.txt "$MOLECULE_YML" > /tmp/new.txt && mv /tmp/new.txt "$MOLECULE_YML"
            echo "  ✓ $MOLECULE_YML -> $CODE"
        fi
    fi
done

# Role-specific molecule files
for role_dir in roles/*/; do
    ROLE_NAME=$(basename "$role_dir")
    for scenario_dir in "$role_dir"molecule/*/; do
        if [ -d "$scenario_dir" ]; then
            SCENARIO_NAME=$(basename "$scenario_dir")
            MOLECULE_YML="$scenario_dir/molecule.yml"
            
            if [ -f "$MOLECULE_YML" ] && ! grep -q "Audit Event Identifier" "$MOLECULE_YML" 2>/dev/null; then
                MOLECULE_COUNTER=$((MOLECULE_COUNTER + 1))
                CODE="DSU-TST-$(printf '%07d' $MOLECULE_COUNTER)"
                
                cat > /tmp/header.txt << EOF
# =============================================================================
# Audit Event Identifier: $CODE
# File Type: Molecule Scenario Configuration
# Role: $ROLE_NAME
# Scenario: $SCENARIO_NAME
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
EOF
                cat /tmp/header.txt "$MOLECULE_YML" > /tmp/new.txt && mv /tmp/new.txt "$MOLECULE_YML"
                echo "  ✓ $MOLECULE_YML -> $CODE"
            fi
        fi
    done
done

# ============================================================================
# Summary
# ============================================================================
echo ""
echo "=== Bulk Assignment Complete ==="
echo "Task files processed: $((TASK_COUNTER - 110000))"
echo "Defaults processed: $((DEFAULTS_COUNTER - 120000))"
echo "Handlers processed: $((HANDLER_COUNTER - 130000))"
echo "Templates processed: $((TEMPLATE_COUNTER - 900000))"
echo "Molecule files processed: $((MOLECULE_COUNTER - 1000000))"
echo ""
echo "Total files updated: $((TASK_COUNTER - 110000 + DEFAULTS_COUNTER - 120000 + HANDLER_COUNTER - 130000 + TEMPLATE_COUNTER - 900000 + MOLECULE_COUNTER - 1000000))"
