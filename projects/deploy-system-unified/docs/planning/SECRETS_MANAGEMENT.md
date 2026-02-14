# SECRETS_MANAGEMENT

**Status:** Transition planned, not active cutover.  
**Current Provider of Record:** Ansible Vault (`secrets.generated.yml`)  
**Target Provider:** SOPS + Age (after cutover criteria are met)

## Current State

1. Vault is actively enforced by preflight assertions.
2. SOPS vars plugin is enabled in `ansible.cfg` for future compatibility.
3. Placeholder `.sops.yaml` is currently blocked by preflight safety checks.

## Why This Matters

We want SOPS benefits (diffable encrypted values and key-based access) without breaking existing deployment safety guarantees.

## Cutover Prerequisites

1. Operator-ready migration guide exists and is approved.
2. Key rotation SOP exists and is approved.
3. Real project Age recipient keys are provisioned and tested.
4. Preflight assertions are updated to enforce valid SOPS config (instead of blocking all `.sops.yaml`).
5. CI verifies decryption/read path for encrypted SOPS variables.

## Migration Scope (Initial)

Move these variables first:

1. `authentik_secret_key`
2. `postgres_password` (role-specific mappings in migration guide)
3. `transmission_pass`
4. `vaultwarden_admin_token`
5. `access_admin_password_hash`

## Execution Phases

### Phase 1: Documentation and Policy (Current Window)

- Draft SOPS migration guide.
- Draft key rotation SOP.
- Define rollback to Vault-only operation.

### Phase 2: Tooling and Gate Update

- Add validated `.sops.yaml` template with real recipients.
- Update preflight assertions to validate SOPS config correctness.
- Add CI checks for SOPS-encrypted var consumption.

### Phase 3: Secret Migration

- Migrate prioritized variables to `secrets.sops.yml`.
- Remove hardcoded placeholders/default secrets in role defaults.
- Verify production deploy path with migrated secrets.

## Working Notes

- Do not add a placeholder `.sops.yaml` until preflight logic is updated.
- Keep Vault path fully operational until SOPS cutover checks are green.

## Completion Criteria

1. SOPS-managed secrets are active in CI and production deploy path.
2. Vault fallback is documented and tested.
3. No default secret placeholders remain in production-critical role defaults.
