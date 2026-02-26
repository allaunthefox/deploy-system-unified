# Negative Testing Implementation

## Overview

This document outlines the complete implementation of negative testing for the permissive roles in the Deploy-System-Unified project. The solution provides comprehensive test coverage for the `verify_secrets.yml` task file across all permissive roles.

---

## Implementation Summary

### Preflight Podman Access

For local testing with Molecule and the Podman driver, ensure the test runner has access to the Podman socket. A convenience script and Makefile target are provided to check `podman info` and to fail with clear remediation instructions if access still fails:

- `scripts/ensure_podman_access.sh`
- Makefile target: `molecule-precheck`

Run `make molecule-precheck` before `molecule test` to preflight Podman access.

---

## Current State Analysis

### Permissive Roles Verification {#current-state-roles}

**Status:** Complete for all permissive roles.

**Coverage:**
- `containers/caddy` — verify_secrets.yml tested
- `containers/monitoring` — verify_secrets.yml tested
- `containers/authentik` — verify_secrets.yml tested
- All roles with `containers_*_fail_secure` variables

**Test Method:** Molecule scenarios with both valid and invalid secret configurations.

---

### Secret Verification Implementation {#current-state-secrets}

**Pattern:** All permissive roles use the same verification pattern:

```yaml
- name: Verify secrets exist
  ansible.builtin.assert:
    that:
      - my_secret is defined
      - my_secret | length > 0
    fail_msg: "Secret my_secret is required when fail_secure is enabled"
  when:
    - role_fail_secure | default(true) | bool
    - containers_fail_secure | default(true) | bool
```

**Test Coverage:** Tests verify both pass (valid secrets) and fail (missing secrets) scenarios.

---

## Implementation Plan

### Phase 1 — Foundation {#plan-phase1}

**Status:** Complete

**Deliverables:**
1. Molecule test scenarios for all permissive roles
2. Test fixtures with valid/invalid secret configurations
3. CI integration for automated testing

---

### Phase 2 — Expansion {#plan-phase2}

**Status:** Complete

**Deliverables:**
1. Extended test coverage to all container roles
2. Integration with preflight validation
3. Documentation of test patterns

---

### Phase 3 — Automation {#plan-phase3}

**Status:** Complete

**Deliverables:**
1. Automated test execution in CI pipeline
2. Test result reporting and artifacts
3. Integration with compliance reporting

---

## Verification Process

### Automated Tests {#verification-automated}

**Execution:** `make molecule-test` or `molecule test`

**Test Scenarios:**
1. **default** — Valid configuration, expects success
2. **fail_secure_enabled** — Missing secrets with fail_secure=true, expects failure
3. **fail_secure_disabled** — Missing secrets with fail_secure=false, expects success

**Coverage Report:** Generated in `.molecule/` after test execution.

---

### Manual Tests {#verification-manual}

**Procedure:**
1. Set up test inventory with placeholder secrets
2. Run playbook with `--check` flag
3. Verify expected failures occur
4. Replace placeholders with valid secrets
5. Re-run and verify success

**Documentation:** Record test results in test log.

---

## Remediation Steps

### Failed Tests {#remediation-failed}

**Common Causes:**
1. Missing secret in inventory
2. Incorrect variable name in role
3. fail_secure flag misconfigured

**Fix Procedure:**
1. Review test output for specific failure
2. Check secret exists in inventory
3. Verify variable naming matches role defaults
4. Re-run test after fix

---

### Security Issues {#remediation-security}

**Critical Failures:**
1. Secret exposed in logs (check `no_log: true`)
2. Placeholder not replaced in production
3. Fail_secure bypassed incorrectly

**Fix Procedure:**
1. Immediately rotate any exposed secrets
2. Update inventory with correct values
3. Re-enable fail_secure if bypassed
4. Document incident and resolution

---

## Related Documents

- **[TERMINOLOGY](TERMINOLOGY)** — Formal definitions including "Configuration Drift"
- **[QUALITY_IDEMPOTENCY_BLOCKERS](QUALITY_IDEMPOTENCY_BLOCKERS)** — Idempotency contract
<<<<<<< HEAD
- **[DSU_AUDIT_EVENT_IDENTIFIERS](DSU_AUDIT_EVENT_IDENTIFIERS)** — Audit Event Identifier 600151 (Idempotency check)
=======
- **[DSU_ACTION_CODES_COMPLETE](DSU_ACTION_CODES_COMPLETE)** — Audit Event Identifier 600151 (Idempotency check)
>>>>>>> c42ffcf4 (Rename wiki pages to SCREAMING_SNAKE_CASE convention)
