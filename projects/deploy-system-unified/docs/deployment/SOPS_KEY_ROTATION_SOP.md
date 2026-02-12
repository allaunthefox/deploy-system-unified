# SOPS_KEY_ROTATION_SOP

**Status:** Draft complete, approval pending  
**Applies To:** SOPS Age keys and high-impact service/application secrets used by Deploy-System-Unified

## Purpose

This SOP defines routine and emergency key/secret rotation for the SOPS migration program while preserving fail-secure deployment behavior.

## Roles and Responsibilities

1. **Primary Custodian:** Executes rotation steps and evidence capture.
2. **Secondary Custodian:** Reviews and co-approves sensitive key actions (two-person control).
3. **On-Call Operator:** Executes emergency rollback if rotation causes service impact.

## Rotation Cadence

1. **Application secrets** (`authentik_secret_key`, `transmission_pass`, `vaultwarden_admin_token`): every 90 days.
2. **Database credentials** (for example `authentik_pg_pass`): every 90 days and after any restore/import event.
3. **SOPS Age recipients/private keys:** every 180 days, or immediately on custodian change.
4. **Emergency rotation:** immediate (within 1 hour) after key exposure, credential leak, or suspected compromise.

## Preconditions

1. Change window and rollback owner assigned.
2. Latest encrypted secret artifacts available (`secrets.generated.yml`, `secrets.sops.yml` if active).
3. Deployment health baseline is green before rotation starts.
4. Current key inventory and custodian roster is up to date.

## Routine Secret Rotation Procedure

1. Generate new secrets with approved generators.
2. Update encrypted secrets source (Vault or SOPS depending on active mode).
3. Apply targeted deployment for affected roles/services.
4. Validate service health and authentication paths.
5. Invalidate/revoke old credentials.

Examples:
```bash
openssl rand -base64 48
openssl passwd -6 'NewStrongPassword'
```

Provider-specific update examples:
```bash
# Vault source
ansible-vault edit projects/deploy-system-unified/inventory/group_vars/all/secrets.generated.yml

# SOPS source
sops projects/deploy-system-unified/inventory/group_vars/all/secrets.sops.yml
```

## SOPS Age Key Rotation Procedure

1. Generate replacement Age keypair(s).
2. Update recipients in approved SOPS policy.
3. Re-encrypt all SOPS-managed secret files with new recipients.
4. Verify decryption with new keys; verify old keys are removed per policy.
5. Revoke/archive superseded private keys after grace period.

Example:
```bash
age-keygen -o ~/.config/sops/age/keys-2026q2.txt
sops updatekeys projects/deploy-system-unified/inventory/group_vars/all/secrets.sops.yml
sops -d projects/deploy-system-unified/inventory/group_vars/all/secrets.sops.yml >/dev/null
```

## Emergency Rotation Procedure

Trigger conditions:

1. Private key material leaked or suspected exposed.
2. Credential appears in logs, tickets, chat, or unencrypted files.
3. Incident response requests immediate invalidation.

Emergency steps:

1. Freeze non-essential deploy activity.
2. Rotate exposed secret/key first, then dependent credentials.
3. Force service restarts/session invalidation where applicable.
4. Validate production path with preflight + smoke checks.
5. File incident summary with timeline and corrective actions.

## Validation Checklist

1. Preflight assertions pass.
2. Affected service authentication works with new credentials.
3. No placeholder/default values remain for rotated keys.
4. Prior credentials are disabled and cannot be reused.

## Rollback Procedure

If rotation introduces outage:

1. Restore last known-good encrypted secret artifact.
2. Re-deploy affected roles only.
3. Confirm service recovery.
4. Open corrective action ticket before next rotation attempt.

## Evidence and Audit Trail

Store per-rotation evidence in controlled artifacts:

1. Rotation timestamp (UTC) and scope.
2. Custodian + reviewer identity.
3. Files/variables rotated.
4. Validation command outputs (sanitized).
5. Rollback actions (if any).

Recommended artifact path:

`projects/deploy-system-unified/ci-artifacts/secrets-rotation/<rotation_id>/`

