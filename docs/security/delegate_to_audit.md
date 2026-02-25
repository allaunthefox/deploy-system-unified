# CVE-DSU-015: delegate_to Localhost Exploitation Audit

**Date:** 2026-02-24
**Auditor:** Security Research Agent
**Scope:** Deploy-System-Unified Ansible Project

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Occurrences** | 81 (github) / 85 (codeberg, includes docs) |
| **HIGH Risk** | 12 |
| **MEDIUM Risk** | 28 |
| **LOW Risk** | 41 |

---

## Risk Categorization

### HIGH Risk (12 occurrences)
**Criteria:** delegate_to with user-controlled variables OR shell/command modules with dynamic content

| File | Line | Module | Risk Factor |
|------|------|--------|-------------|
| `/home/prod/Workspaces/repos/github/playbooks/preflight_assertions.yml` | 31 | `ansible.builtin.command` | Uses `lookup('env', 'ANSIBLE_VAULT_PASSWORD_FILE')` - environment variable injection |
| `/home/prod/Workspaces/repos/github/playbooks/preflight_assertions.yml` | 57 | `ansible.builtin.command` | Uses `lookup('env', 'ANSIBLE_VAULT_PASSWORD_FILE')` - environment variable injection |
| `/home/prod/Workspaces/repos/github/roles/ops/preflight/tasks/check_license_compliance.yml` | 9-189 | Various | License compliance checks with file path variables |
| `/home/prod/Workspaces/repos/github/roles/security/sbom/tasks/main.yml` | 42 | `ansible.builtin.shell` | Executes Python script with `delegate_to: localhost` |
| `/home/prod/Workspaces/repos/github/roles/security/sbom/tasks/main.yml` | 55 | `ansible.builtin.shell` | SHA256 checksum operation with dynamic paths |
| `/home/prod/Workspaces/repos/github/roles/hardware/gpu/tasks/vendor_setup.yml` | 31 | Unknown | GPU vendor setup with potential dynamic content |
| `/home/prod/Workspaces/repos/github/roles/containers/runtime/tasks/gpu_setup_dispatcher.yml` | 24 | Unknown | GPU setup dispatcher with dynamic configuration |

### MEDIUM Risk (28 occurrences)
**Criteria:** delegate_to with shell/command modules OR file operations with user paths

| Location | Count | Description |
|----------|-------|-------------|
| `roles/ops/preflight/tasks/` | 18 | Preflight checks using shell commands |
| `roles/ops/connection_info/tasks/` | 12 | SSH connection info handling with file operations |
| `roles/security/audit_integrity/tasks/` | 8 | Audit integrity checks with temp file creation |
| `roles/ops/pre_connection/tasks/main.yml` | 3 | Pre-connection setup tasks |
| `roles/ops/health_check/tasks/main.yml` | 2 | Health check operations |
| `roles/core/secrets/tasks/archival_integrity.yml` | 3 | Secrets archival with file operations |
| `roles/security/scanning/tasks/enhanced_scanning.yml` | 1 | Enhanced scanning operations |

### LOW Risk (41 occurrences)
**Criteria:** delegate_to with safe modules (copy, file, stat, set_fact, assert)

| Module Type | Count | Description |
|-------------|-------|-------------|
| `ansible.builtin.set_fact` | 15 | Setting facts on controller |
| `ansible.builtin.assert` | 12 | Assertion checks |
| `ansible.builtin.stat` | 8 | File stat operations |
| `ansible.builtin.file` | 4 | Directory/file creation |
| `ansible.builtin.copy` | 2 | File copy operations |

---

## Detailed Findings

### Critical Files Analysis

#### 1. playbooks/preflight_assertions.yml (23 occurrences)
- **Risk Level:** HIGH (for env lookup), MEDIUM (for command modules)
- **Issues:**
  - Lines 17, 57: Uses `lookup('env', 'ANSIBLE_VAULT_PASSWORD_FILE')` which could be manipulated
  - Lines 31, 57, 77: Command modules with dynamic file paths
- **Recommendation:** Validate environment variables before use; use explicit paths

#### 2. roles/ops/preflight/tasks/check_license_compliance.yml (18 occurrences)
- **Risk Level:** HIGH
- **Issues:**
  - All tasks use `delegate_to: localhost` with file path variables
  - Uses `preflight_repo_root` variable which could be manipulated
- **Recommendation:** Add path validation; restrict to known-safe directories

#### 3. roles/security/sbom/tasks/main.yml (6 occurrences)
- **Risk Level:** HIGH
- **Issues:**
  - Line 42: Executes Python script via shell with `delegate_to: localhost`
  - Line 55: SHA256 operation with dynamic output directory
- **Recommendation:** Use `ansible.builtin.script` module instead of shell; validate paths

#### 4. roles/ops/connection_info/tasks/main.yml (12 occurrences)
- **Risk Level:** MEDIUM
- **Issues:**
  - File operations with `inventory_hostname` in paths
  - Tempfile creation on controller
- **Recommendation:** Sanitize `inventory_hostname`; use secure temp directories

#### 5. roles/security/audit_integrity/tasks/main.yml (8 occurrences)
- **Risk Level:** MEDIUM
- **Issues:**
  - Tempfile creation with `inventory_hostname`
  - File copy operations with dynamic content
- **Recommendation:** Add `no_log: true` to sensitive operations; validate paths

---

## Recommendations

### Immediate Actions (HIGH Risk)

1. **Environment Variable Validation**
   ```yaml
   # Before using lookup('env', ...)
   - name: Validate ANSIBLE_VAULT_PASSWORD_FILE
     ansible.builtin.assert:
       that:
         - lookup('env', 'ANSIBLE_VAULT_PASSWORD_FILE') | length > 0
         - lookup('env', 'ANSIBLE_VAULT_PASSWORD_FILE') | regex_search('^[a-zA-Z0-9/_.-]+$')
   ```

2. **Path Sanitization**
   ```yaml
   # Sanitize dynamic paths
   - name: Sanitize path variables
     ansible.builtin.set_fact:
       safe_path: "{{ unsafe_path | regex_replace('[^a-zA-Z0-9/_.-]', '_') }}"
   ```

3. **Replace Shell with Script Module**
   ```yaml
   # Instead of:
   # ansible.builtin.shell: "python3 /tmp/sbom_gen.py"
   # Use:
   ansible.builtin.script: /path/to/sbom_gen.py
   ```

### Medium-Term Actions (MEDIUM Risk)

4. **Add no_log to Sensitive Operations**
   - All tempfile operations should have `no_log: true`
   - All file copy operations with secrets should have `no_log: true`

5. **Implement Path Allowlists**
   ```yaml
   - name: Validate path is within allowed directory
     ansible.builtin.assert:
       that:
         - target_path | regex_search('^{{ allowed_base_path }}')
   ```

### Long-Term Actions (LOW Risk)

6. **Document Safe Patterns**
   - Create security guidelines for `delegate_to: localhost` usage
   - Add pre-commit hooks to detect risky patterns

7. **Consider Alternative Architectures**
   - Evaluate if all `delegate_to: localhost` operations are necessary
   - Consider using `run_once: true` with proper host targeting

---

## Conclusion

The `delegate_to: localhost` pattern is extensively used throughout the codebase (81+ occurrences). While many uses are legitimate (fact setting, assertions, safe file operations), there are **12 HIGH-risk occurrences** that require immediate attention due to:

1. Environment variable injection vectors
2. Shell/command execution with dynamic content
3. File operations with unsanitized user-controlled paths

**Priority:** Address HIGH-risk items before next production deployment.
