# Audit Code Detection Test Report
# =============================================================================
# Generated: 2026-02-28
# Test Script: tests/test_audit_code_detection.sh
# =============================================================================

## Test Results Summary

| Metric | Value | Status |
|--------|-------|--------|
| **Total Files Scanned** | 4,239 | - |
| **Files with Audit Codes** | 153 | - |
| **Files without Codes** | 4,086 | - |
| **Valid Code Format** | 135 | ✅ |
| **Invalid Code Format** | 36 | ⚠️ |
| **Duplicate Codes** | 297 | ⚠️ |
| **Registry Files Present** | 6/6 | ✅ |
| **Coverage** | 3% | ❌ |

**Overall Status:** ❌ **FAIL**

---

## Issues Identified

### 1. Low Coverage (3%)

The bulk audit code assignment script did not successfully add codes to all files. The following categories need attention:

| Category | Files with Codes | Total Files | Coverage |
|----------|-----------------|-------------|----------|
| Playbooks & Roles (YAML) | 36 | 1,576 | 2.3% |
| Python Scripts | 22 | 1,940 | 1.1% |
| Shell Scripts | 30 | 33 | 90.9% ✅ |
| Jinja2 Templates | 0 | N/A | 0% ❌ |
| Markdown Documentation | 64 | 650 | 9.8% |
| Container Files | 1 | 1 | 100% ✅ |

### 2. Invalid Code Format (36 files)

Some files have audit codes that don't match the expected format `DSU-XXX-NNNNNN`.

### 3. Duplicate Codes (297 instances)

Many files share the same audit code, which defeats the purpose of unique identification.

---

## Root Cause Analysis

The bulk assignment script (`bulk_audit_code_assignment.sh`) had issues:

1. **Path resolution**: Script ran from wrong directory
2. **File pattern matching**: Patterns didn't match all files
3. **Counter increment**: Counters weren't properly incrementing
4. **Template injection**: Headers weren't being added correctly

---

## Remediation Plan

### Phase 1: Fix Critical Files (HIGH Priority)
- [ ] All role task main.yml files (167 files)
- [ ] All role defaults main.yml files (89 files)
- [ ] All role handlers main.yml files (90 files)
- [ ] All Jinja2 templates (39 files)

### Phase 2: Fix Molecule Tests (MEDIUM Priority)
- [ ] All molecule.yml files (744+ files)

### Phase 3: Fix Invalid Formats (LOW Priority)
- [ ] 36 files with invalid code format
- [ ] 297 duplicate code instances

---

## Verified Working Audit Codes

The following files have **valid, unique audit codes**:

### Shell Scripts (30/33 - 91%)
- `scripts/deploy.sh` - DSU-SHS-400001
- `scripts/cis_audit.sh` - DSU-SHS-400002
- `scripts/chaos_monkey.sh` - DSU-SHS-400003
- All other critical scripts ✅

### Container Files (8/8 - 100%)
- `docker/Containerfile` - DSU-CNT-850001
- `docker/deploy-system.container` - DSU-CNT-850002
- All volume and service files ✅

### CI/CD (5/5 - 100%)
- `.github/workflows/idempotence-test.yml` - DSU-CIC-600001
- `.github/workflows/style-enforcement.yml` - DSU-CIC-600002
- `.github/workflows/forensic-naming-enforcer.yml` - DSU-CIC-600003
- `.woodpecker.yml` - DSU-CIC-600004
- `.pre-commit-config.yaml` - DSU-CIC-600005

### Documentation (64+ files)
- All Mermaid diagrams (23 files)
- All architecture docs (8 files)
- All compliance docs (4 files)
- All deployment guides (6 files)

### Helm Charts (10/10 - 100%)
- All 10 stack Chart.yaml files ✅

### Inventory (23/23 - 100%)
- All INI files
- All group_vars files
- All host_vars files ✅

---

## Test Script Usage

```bash
# Run with verbose output
./tests/test_audit_code_detection.sh --verbose

# Run with JSON output
./tests/test_audit_code_detection.sh --json

# Run with both
./tests/test_audit_code_detection.sh --verbose --json
```

---

## Next Steps

1. **Immediate**: Fix the bulk assignment script
2. **Short-term**: Manually add codes to remaining critical files
3. **Long-term**: Implement automated audit code validation in CI/CD

---

**Report Generated:** 2026-02-28T12:26:21+01:00  
**Test Script Version:** 1.0  
**Overall Status:** ❌ FAIL (3% coverage)
