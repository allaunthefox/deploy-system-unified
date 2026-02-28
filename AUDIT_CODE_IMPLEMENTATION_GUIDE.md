# Audit Code Implementation Guide
# =============================================================================
# Bulk implementation guide for remaining files
# Generated: 2026-02-28
# =============================================================================

## Overview

This document provides templates and instructions for bulk audit code assignment across the remaining ~1,100+ files in the Deploy-System-Unified repository.

---

## 📝 Audit Code Templates by File Type

### 1. Jinja2 Templates (.j2 files)

**Location:** `roles/*/templates/*.j2`  
**Count:** 39 files  
**Code Range:** `DSU-TPL-900001` to `DSU-TPL-900099`

**Template Header:**
```jinja2
{# =============================================================================
# Audit Event Identifier: DSU-TPL-900XXX
# Template Type: <Service/Component> Configuration
# Description: <Brief description>
# Rendered To: <destination path pattern>
# Last Updated: 2026-02-28
# Version: 1.0
# ============================================================================= #}
```

**Example Assignment:**
- `roles/kubernetes/master/templates/k3s.service.j2` → `DSU-TPL-900001`
- `roles/containers/monitoring/templates/prometheus.container.j2` → `DSU-TPL-900002`
- `roles/security/falco/templates/falco.yaml.j2` → `DSU-TPL-900003`

---

### 2. Role Task Files (tasks/*.yml)

**Location:** `roles/*/tasks/*.yml`  
**Count:** 167 files  
**Code Range:** `DSU-PLY-110000` to `DSU-PLY-119999`

**Template Header:**
```yaml
# =============================================================================
# Audit Event Identifier: DSU-PLY-11XXXX
# File Type: Role Tasks
# Role: <role_name>
# Description: <Brief description>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

**Bulk Assignment Strategy:**
- `roles/*/tasks/main.yml` → `DSU-PLY-110001` to `DSU-PLY-110100` (by role alphabetically)
- `roles/*/tasks/*.yml` (subtasks) → `DSU-PLY-110101` to `DSU-PLY-110199`

---

### 3. Role Defaults (defaults/main.yml)

**Location:** `roles/*/defaults/main.yml`  
**Count:** 89 files  
**Code Range:** `DSU-PLY-120000` to `DSU-PLY-129999`

**Template Header:**
```yaml
# =============================================================================
# Audit Event Identifier: DSU-PLY-12XXXX
# File Type: Role Defaults
# Role: <role_name>
# Description: Default variables for <role_name>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

---

### 4. Role Handlers (handlers/main.yml)

**Location:** `roles/*/handlers/main.yml`  
**Count:** 90 files  
**Code Range:** `DSU-PLY-130000` to `DSU-PLY-139999`

**Template Header:**
```yaml
# =============================================================================
# Audit Event Identifier: DSU-PLY-13XXXX
# File Type: Role Handlers
# Role: <role_name>
# Description: Event handlers for <role_name>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

---

### 5. Molecule Test Files

**Location:** `molecule/*/` and `roles/*/molecule/`  
**Count:** 744+ files  
**Code Range:** `DSU-TST-1000001` to `DSU-TST-1099999`

**Bulk Assignment by Scenario:**
- `molecule/default/*` → `DSU-TST-1000001` to `DSU-TST-1000010`
- `molecule/production/*` → `DSU-TST-1000011` to `DSU-TST-1000020`
- `molecule/kubernetes-master/*` → `DSU-TST-1000021` to `DSU-TST-1000030`
- Continue pattern for each scenario

**Template for molecule.yml:**
```yaml
# =============================================================================
# Audit Event Identifier: DSU-TST-10XXXXX
# File Type: Molecule Scenario Configuration
# Scenario: <scenario_name>
# Role: <role_name>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

---

### 6. Test Files (tests/)

**Location:** `tests/*`  
**Count:** 9 files  
**Code Range:** `DSU-TST-1000100` to `DSU-TST-1000199`

**Python Test Template:**
```python
#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-TST-1001XX
# File Type: Python Test Script
# Test Type: <unit/integration/validation>
# Description: <Brief description>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

**YAML Test Template:**
```yaml
# =============================================================================
# Audit Event Identifier: DSU-TST-1001XX
# File Type: YAML Test Playbook
# Test Type: <validation/integration>
# Description: <Brief description>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

---

### 7. Remaining Shell Scripts

**Location:** `scripts/*.sh`, `dev_tools/scripts/*.sh`, `docker/*.sh`  
**Count:** 19 files  
**Code Range:** `DSU-SHS-400008` to `DSU-SHS-400099`

**Template Header:**
```bash
#!/bin/sh
# =============================================================================
# Audit Event Identifier: DSU-SHS-400XXX
# Script Type: <Automation/Validation/Benchmark/Setup>
# Description: <Brief description>
# Usage: <command usage>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

---

### 8. Remaining Python Scripts

**Location:** `scripts/*.py`, `tests/*.py`, `dev_tools/scripts/*.py`, `qwen_agents/*.py`  
**Count:** 14 files  
**Code Range:** `DSU-PYS-500004` to `DSU-PYS-599999`

**Template Header:**
```python
#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500XXX
# Script Type: <Automation/Validation/Reporting/Testing>
# Description: <Brief description>
# Usage: <command usage>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

---

### 9. Inventory Files

**Location:** `inventory/*.ini`, `inventory/group_vars/*.yml`, `inventory/host_vars/*.yml`  
**Count:** 21 files  
**Code Range:** `DSU-INV-700004` to `DSU-INV-799999`

**INI Template:**
```ini
# =============================================================================
# Audit Event Identifier: DSU-INV-700XXX
# Inventory Type: <Environment/Scenario>
# Description: <Brief description>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

**YAML Template:**
```yaml
# =============================================================================
# Audit Event Identifier: DSU-INV-700XXX
# Inventory Type: Group Variables
# Group: <group_name>
# Description: <Brief description>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
```

---

## 🚀 Bulk Implementation Script

For large-scale implementation, use this approach:

```bash
#!/bin/bash
# audit_code_bulk_assign.sh
# Bulk audit code assignment script

# Example for role task files
assign_task_codes() {
    local role_dir="$1"
    local base_code="$2"
    local counter=0
    
    for task_file in "$role_dir"/tasks/*.yml; do
        if [ -f "$task_file" ]; then
            code=$(printf "DSU-PLY-%06d" $((base_code + counter)))
            # Add header to file
            cat > "$task_file.tmp" << EOF
# =============================================================================
# Audit Event Identifier: $code
# File Type: Role Tasks
# Role: $(basename "$role_dir")
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
$(cat "$task_file")
EOF
            mv "$task_file.tmp" "$task_file"
            echo "Assigned $code to $task_file"
            ((counter++))
        fi
    done
}

# Usage example:
# assign_task_codes "roles/core/bootstrap" 110001
```

---

## 📊 Assignment Tracking Spreadsheet

| File Path | Assigned Code | Status | Date Assigned |
|-----------|---------------|--------|---------------|
| `roles/kubernetes/master/templates/k3s.service.j2` | `DSU-TPL-900001` | ⏳ Pending | - |
| `roles/containers/monitoring/templates/prometheus.container.j2` | `DSU-TPL-900002` | ⏳ Pending | - |
| ... | ... | ... | ... |

---

## ✅ Completed Implementations

See completed items in `CODE_CONFIG_AUDIT_REGISTRY.md`:
- ✅ Container files (8/8 - 100%)
- ✅ Playbooks (17/17 - 100%)
- ✅ Helm charts (10/10 - 100%)
- ✅ Shell scripts (8/27 - 30%)
- ✅ Python scripts (3/17 - 18%)
- ✅ CI/CD (5/5 - 100%)
- ✅ Inventory (3/23 - 13%)

---

## 📈 Next Steps

1. **Phase 1:** Complete remaining shell scripts and Python scripts (HIGH priority)
2. **Phase 2:** Complete inventory files (HIGH priority)
3. **Phase 3:** Jinja2 templates (HIGH priority)
4. **Phase 4:** Role task files main.yml (HIGH priority)
5. **Phase 5:** Role defaults and handlers (MEDIUM priority)
6. **Phase 6:** Molecule test files (bulk assignment - LOW priority)

---

**Generated:** 2026-02-28  
**Total Remaining:** ~1,100+ files  
**Estimated Time:** 2-3 weeks for complete coverage
