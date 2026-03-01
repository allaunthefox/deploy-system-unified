# SOPS_MIGRATION_GUIDE

**Status:** Phase 3 - Cutover Ready  
**Effective Date:** 2026-02-13  
**Last Updated:** 2026-02-24  
**Current Provider of Record:** Dual Mode (Vault + SOPS)  
**Target Provider:** SOPS + Age (`inventory/group_vars/all/secrets.sops.yml`)

## Purpose

This guide defines a safe migration path from Vault-only secrets handling to SOPS-based encrypted variables without weakening existing preflight safety checks.

---

## PHASE 3: CUTOVER CHECKLIST

The following checklist must be completed before switching from Vault to SOPS mode:

### Pre-Cutover Validation

- [ ] **Backup Vault Secrets**: Copy `secrets.generated.yml` to a secure backup location
- [ ] **Verify SOPS Decryption**: Run `sops -d secrets.sops.yml` and confirm all keys decrypt
- [ ] **Validate Age Keys**: Confirm all recipients in `.sops.yaml` have valid keys
- [ ] **Test Dry-Run**: Execute `ansible-playbook PRODUCTION_DEPLOY.yml --check` in SOPS mode
- [ ] **Operator Signoff**: Get signoff from at least one additional operator

### Cutover Execution

- [ ] **Set Provider Mode**: Set `secrets_provider_mode: 'sops'` in inventory
- [ ] **Update Preflight**: Modify `playbooks/PREFLIGHT_ASSERTIONS.YML` to allow SOPS-only mode
- [ ] **Run Preflight**: Execute `ansible-playbook playbooks/PREFLIGHT_ASSERTIONS.YML`
- [ ] **Run Production Deploy**: Execute `ansible-playbook PRODUCTION_DEPLOY.yml` with SOPS mode

### Post-Cutover Verification

- [ ] **Verify Secrets Loaded**: Confirm all expected secrets are available to roles
- [ ] **Test Application Health**: Verify deployed applications can access their secrets
- [ ] **Document Rollback Plan**: Keep Vault backup accessible for 30 days
- [ ] **Notify Team**: Send cutover completion notification to operators

---

## Current Enforcement Baseline

1. `playbooks/PREFLIGHT_ASSERTIONS.YML` requires `inventory/group_vars/all/secrets.generated.yml` to be Vault-encrypted.
2. `playbooks/PREFLIGHT_ASSERTIONS.YML` currently fails if a repository-root `.sops.yaml` exists.
3. `ansible.cfg` already enables the SOPS vars plugin (`community.sops.sops`) for future compatibility.

Because of this, migration must be staged. Do not remove Vault guardrails before SOPS policy and key custody are validated.

## Setting Provider Mode

The secret provider mode is controlled by the `secrets_provider_mode` variable:

| Mode | Description | Use Case |
|------|-------------|----------|
| `vault` | Use Ansible Vault only | Legacy mode |
| `sops` | Use SOPS only | Target production mode |
| `dual` | Validate both providers | Migration/testing |

Set in `inventory/group_vars/all/secrets_config.yml`:
```yaml
secrets_provider_mode: "sops"  # Change from 'dual' to 'sops' after cutover
```

---

## Scope for Initial Migration

Prioritized variables:

1. `authentik_secret_key`
2. `postgres_password` (mapped to active role variable names, see mapping below)
3. `transmission_pass`
4. `vaultwarden_admin_token`
5. `access_admin_password_hash`

### Variable Mapping Notes

| Conceptual Secret | Current Variable(s) in Roles | Notes |
| :--- | :--- | :--- |
| Authentik app secret | `authentik_secret_key` | Used by `roles/containers/authentik` |
| Postgres password (Authentik) | `authentik_pg_pass` | `postgres_password` should map to concrete service var |
| Transmission password | `transmission_pass` | Used by `roles/containers/media` |
| Vaultwarden admin token | `vaultwarden_admin_token` | Used by `roles/containers/ops` + preflight guard |
| Access admin password hash | `access_admin_password_hash` | Used by `roles/security/access` |

## Migration Preconditions

1. Approved key custodians and recovery contacts are assigned.
2. SOPS Age key recipients are generated and validated out-of-band.
3. Rollback owner is assigned for the migration window.
4. Existing Vault file is backed up and decryptable.
5. CI and preflight changes are prepared to support dual-provider validation.

---

## Phase Plan

### Phase 0: Preparation and Backups

1. Export a secure backup of current encrypted Vault secrets file.
2. Verify decrypt/read of `inventory/group_vars/all/secrets.generated.yml`.
3. Define migration window and rollback checkpoint.

Example:
```bash
ansible-vault view projects/deploy-system-unified/inventory/group_vars/all/secrets.generated.yml >/dev/null
cp projects/deploy-system-unified/inventory/group_vars/all/secrets.generated.yml /secure-backup/secrets.generated.yml.vault
```

### Phase 1: Age Key Provisioning

1. Generate Age keypairs on secured operator workstations.
2. Store private keys outside the repository (HSM, password manager, or secured secret store).
3. Share only recipients with authorized maintainers.

Example:
```bash
age-keygen -o ~/.config/sops/age/keys.txt
grep '^# public key:' ~/.config/sops/age/keys.txt
```

### Phase 2: SOPS Policy Authoring (Out-of-Repo Until Gate Update)

Do not commit repository-root `.sops.yaml` while current preflight assertions still block it.

Create a reviewed candidate policy file outside repo root first:

```yaml
creation_rules:
  - path_regex: inventory/group_vars/all/secrets\\.sops\\.yml$
    age:
      - age1exampleexampleexampleexampleexampleexampleexample
```

### Phase 3: Build `secrets.sops.yml` from Vault Source

1. Decrypt Vault source to a secure temporary path.
2. Build `inventory/group_vars/all/secrets.sops.yml` with mapped variable names.
3. Encrypt with SOPS.
4. Shred/remove temporary plaintext.

Example flow:
```bash
ansible-vault view projects/deploy-system-unified/inventory/group_vars/all/secrets.generated.yml > /tmp/secrets.migration.yml
cp /tmp/secrets.migration.yml projects/deploy-system-unified/inventory/group_vars/all/secrets.sops.yml
sops -e -i projects/deploy-system-unified/inventory/group_vars/all/secrets.sops.yml
shred -u /tmp/secrets.migration.yml
```

### Phase 4: Dual-Provider Validation

Until cutover is approved:

1. Keep Vault file valid and encrypted.
2. Keep SOPS file encrypted and readable by authorized operators.
3. Run preflight assertions and production dry-run checks.

Example:
```bash
ansible-playbook projects/deploy-system-unified/playbooks/PREFLIGHT_ASSERTIONS.YML -i projects/deploy-system-unified/inventory/local.ini
ansible-playbook projects/deploy-system-unified/PRODUCTION_DEPLOY.yml -i projects/deploy-system-unified/inventory/local.ini --check
```

### Phase 5: Cutover Gating Update

Update preflight policy so it enforces correctness instead of blanket-blocking `.sops.yaml`:

1. Allow `.sops.yaml` only when it contains valid non-placeholder recipients.
2. Support explicit secret-provider mode (`vault`, `sops`, `dual`).
3. Fail if selected provider artifacts are missing or unencrypted.

### Phase 6: Controlled Cutover

1. Set provider mode to `dual` first; validate deploy path.
2. Move to `sops` mode only after green CI + dry-run + operator signoff.
3. Keep tested Vault rollback path for one full rotation cycle.

---

## Rollback Procedure (Vault-Only)

If cutover fails:

1. Re-enable Vault-only mode in preflight/provider config:
   ```yaml
   # inventory/group_vars/all/secrets_config.yml
   secrets_provider_mode: "vault"
   ```

2. Remove SOPS file from active variable loading path (if needed):
   ```bash
   mv inventory/group_vars/all/secrets.sops.yml /secure-backup/
   ```

3. Confirm `secrets.generated.yml` decrypts and deploy succeeds:
   ```bash
   ansible-vault view inventory/group_vars/all/secrets.generated.yml
   ansible-playbook PRODUCTION_DEPLOY.yml --check
   ```

4. Open incident review before next cutover attempt.

---

## Cutover Exit Criteria

1. SOPS-encrypted file exists for prioritized variables and decrypts with approved keys.
2. Preflight assertions validate selected provider policy.
3. CI proves secrets consumption path in deployment workflow.
4. Rollback drill to Vault-only has been executed successfully.

---

## Secrets Template Reference

The `secrets.sops.yml.example` template is located at:
`inventory/group_vars/all/secrets.sops.yml.example`

This template includes:
- Access control credentials
- Database passwords
- Authentik secrets
- Wiki.js secrets
- Vaultwarden admin token
- Media stack credentials (Transmission)
- Monitoring stack credentials (Grafana)
- Backup/restic passwords
- External API tokens (Porkbun, CrowdSec)

To use the template:
```bash
# 1. Copy the template
cp inventory/group_vars/all/secrets.sops.yml.example inventory/group_vars/all/secrets.sops.yml

# 2. Edit with your values
vim inventory/group_vars/all/secrets.sops.yml

# 3. Encrypt with SOPS
sops -e -i inventory/group_vars/all/secrets.sops.yml

# 4. Verify encryption
sops -d inventory/group_vars/all/secrets.sops.yml
```

---

## Key Rotation

For key rotation instructions, see: `docs/deployment/SOPS_KEY_ROTATION_SOP.md`
