# NEGATIVE_TESTING_IMPLEMENTATION

## Overview

This document outlines the complete implementation of negative testing for the permissive roles in the Deploy-System-Unified project. The solution provides comprehensive test coverage for the `verify_secrets.yml` task file across all permissive roles.

## Implementation Summary

### Preflight Podman Access

For local testing with Molecule and the Podman driver, ensure the test runner has access to the Podman socket. A convenience script and Makefile target are provided to check `podman info` and to fail with clear remediation instructions if access still fails:

- scripts/ensure_podman_access.sh
- Makefile target: `molecule-precheck`

Run `make molecule-precheck` before `molecule test` to preflight Podman access.


### 1. Current State Analysis

**Verified permissive roles:**
- `containers/ops` - ✅ `verify_secrets.yml` + `molecule/negative` scenario (Vaultwarden file checks)
- `containers/caddy` - ✅ `verify_secrets.yml` + `molecule/negative` scenario (caddy.env + Caddyfile placeholder checks)
- `containers/authentik` - ✅ `verify_secrets.yml` + `molecule/negative` scenario (authentik.env file checks + default variable checks)
- `containers/media` - ✅ `verify_secrets.yml` + `molecule/negative` scenario (Transmission credential asserts)

**Current verify_secrets.yml implementations (role-specific):**
- `roles/containers/ops/tasks/verify_secrets.yml`: asserts `vaultwarden.env` exists, mode `0600`, owner matches `containers_secrets_owner`, and no placeholder tokens.
- `roles/containers/caddy/tasks/verify_secrets.yml`: asserts `caddy.env` exists, mode `0600`, owner matches `containers_secrets_owner`, no placeholder tokens, and validates Caddyfile placeholder email.
- `roles/containers/authentik/tasks/verify_secrets.yml`: asserts `authentik.env` exists, mode `0600`, owner matches, no placeholder tokens, file is non-empty, and default weak vars are not used.
- `roles/containers/media/tasks/verify_secrets.yml`: asserts Transmission credentials are defined and non-empty when fail-secure is enabled.

### 2. Negative Testing Framework

#### Molecule Test Structure

For each permissive role, create the following structure:

```
roles/{role_name}/molecule/negative/
├── molecule.yml          # Test configuration
├── converge.yml          # Test scenarios
└── verify.yml           # Test assertions
```

#### Test Scenarios

Base matrix cases used across roles:
- `missing_file` (file-based roles) or missing credential (media)
- `wrong_permissions` (file-based roles)
- `placeholder_values` (file-based roles)
- `wrong_owner` (file-based roles)

Role-specific additions:
- `containers/caddy`: `empty_file`, `placeholder_caddyfile`
- `containers/authentik`: `empty_file`
- `containers/media`: `missing_transmission_user`, `missing_transmission_pass`, `empty_transmission_user`, `empty_transmission_pass`

Note: For `containers/media`, the base matrix cases are mapped to Transmission credential failure modes to keep the shared CI matrix consistent.

### 3. Implementation Details

Each permissive role implements a `molecule/negative` scenario driven by the `test_case` environment variable and an Ansible verifier that asserts `verify_secrets.yml` fails when expected.

Reference implementations:
- `roles/containers/ops/molecule/negative/molecule.yml`
- `roles/containers/ops/molecule/negative/converge.yml`
- `roles/containers/ops/molecule/negative/verify.yml`
- `roles/containers/caddy/molecule/negative/molecule.yml`
- `roles/containers/caddy/molecule/negative/converge.yml`
- `roles/containers/caddy/molecule/negative/verify.yml`
- `roles/containers/authentik/molecule/negative/molecule.yml`
- `roles/containers/authentik/molecule/negative/converge.yml`
- `roles/containers/authentik/molecule/negative/verify.yml`
- `roles/containers/media/molecule/negative/molecule.yml`
- `roles/containers/media/molecule/negative/converge.yml`
- `roles/containers/media/molecule/negative/verify.yml`

Driver: `podman` (consistent with repository defaults).

### 4. GitHub Actions CI Integration

Workflow: `.github/workflows/negative-tests.yml`

Matrix:
- Roles: `containers/ops`, `containers/caddy`, `containers/authentik`, `containers/media`
- Base test cases: `missing_file`, `wrong_permissions`, `placeholder_values`, `wrong_owner`
- Additional includes:
  - `containers/caddy`: `empty_file`, `placeholder_caddyfile`
  - `containers/authentik`: `empty_file`
  - `containers/media`: `missing_transmission_user`, `missing_transmission_pass`, `empty_transmission_user`, `empty_transmission_pass`

Execution:
- Uses Podman (`molecule[podman]`)
- Runs `molecule test --scenario-name negative` per matrix entry
- Uploads Molecule artifacts per role/test case

### 5. Expansion to Additional Roles

Status: Complete for current permissive roles. For any new permissive role, add:
- `tasks/verify_secrets.yml` aligned to the role's secret model
- `molecule/negative` scenario with `test_case` gating
- CI matrix entry in `.github/workflows/negative-tests.yml`

Avoid copying a generic template across roles; align checks to the role’s actual secret inputs.

### 6. Verifier Implementation (Ansible)

Negative scenarios use the Ansible verifier with a `block`/`rescue` pattern to capture expected failures and assert that `verify_secrets.yml` fails. See:
- `roles/containers/ops/molecule/negative/verify.yml`
- `roles/containers/caddy/molecule/negative/verify.yml`
- `roles/containers/authentik/molecule/negative/verify.yml`
- `roles/containers/media/molecule/negative/verify.yml`

### 7. Project Philosophy Alignment

This implementation follows the project's established patterns:

- **Consistency**: Uses the same structure and naming conventions as existing Molecule tests
- **Security Focus**: Emphasizes security validation and proper secret handling
- **Documentation**: Includes comprehensive documentation and comments
- **CI/CD Integration**: Integrates with existing GitHub Actions workflows
- **Maintainability**: Uses reusable patterns that can be easily extended to other roles

### 8. Next Steps

1. **Keep matrices aligned**: Update `.github/workflows/negative-tests.yml` when secret models change.
2. **Expand role-specific cases**: Add new negative cases as additional secrets are introduced.
3. **Validation**: Use `make molecule-precheck` and `molecule test --scenario-name negative`, or rely on CI runs.

### 9. Benefits

- **Security Assurance**: Ensures secrets are properly configured before deployment
- **Early Detection**: Catches configuration issues before they reach production
- **Consistency**: Standardizes secret validation across all permissive roles
- **Maintainability**: Provides clear test patterns that are easy to understand and extend
- **CI/CD Integration**: Automatically validates secrets in the deployment pipeline

This comprehensive implementation provides robust negative testing coverage for all permissive roles, ensuring that secret validation works correctly in failure scenarios and maintaining the project's high security standards.
