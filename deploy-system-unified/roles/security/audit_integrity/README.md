# security/audit_integrity

Implements Forward Secure Sealing (FSS) for systemd journal logs, ensuring tamper-evident audit trails with cryptographic verification.

## Overview

This role configures systemd's Forward Secure Sealing (FSS) feature, which provides cryptographic proof that journal logs have not been tampered with. It generates sealing keys, initializes FSS on the target system, and optionally stores encrypted verification keys on the Ansible controller for disaster recovery.

## Requirements

- **systemd** with journal support
- **Ansible Vault** for encrypting verification keys (controller-side)
- **Python 3** on controller (for FSS key extraction)

## Role Variables

### Required Variables

None - all variables have sensible defaults.

### Optional Variables

#### `audit_integrity_enabled`
- **Type:** Boolean
- **Default:** `true`
- **Description:** Master switch to enable/disable the entire audit integrity role.

#### `audit_integrity_verify_sealing`
- **Type:** Boolean
- **Default:** `false`
- **Description:** Whether to verify sealing key functionality after initialization. Set to `true` for validation runs.

#### `audit_integrity_store_keys`
- **Type:** Boolean
- **Default:** `true`
- **Description:** Whether to extract and store the FSS verification key on the controller.

#### `audit_integrity_output_dir`
- **Type:** String
- **Default:** `"/tmp/deploy-system-audit-integrity"`
- **Description:** Controller-side directory where encrypted FSS verification keys are stored. 
- **Important:** Changed from `/tmp` to avoid permission conflicts when Ansible tries to manage directory permissions on the controller's system `/tmp`.

#### `audit_integrity_vault_encrypt_id`
- **Type:** String
- **Default:** `"default"`
- **Description:** Vault ID to use when encrypting the FSS verification key with `ansible-vault encrypt`.
- **Added:** February 2026 - Required for compatibility with Ansible 2.20+ which mandates explicit vault ID specification.
- **Usage:** Specify which vault ID from your vault password file should be used to encrypt the FSS keys. Use `"default"` for single-vault setups.

## Dependencies

None.

## Example Playbook

### Basic Usage

```yaml
- hosts: all
  become: true
  roles:
    - role: security/audit_integrity
```

### Custom Configuration

```yaml
- hosts: all
  become: true
  roles:
    - role: security/audit_integrity
      vars:
        audit_integrity_verify_sealing: true
        audit_integrity_output_dir: "/secure/audit-keys"
        audit_integrity_vault_encrypt_id: "production"
```

### Disable FSS Key Storage

```yaml
- hosts: all
  become: true
  roles:
    - role: security/audit_integrity
      vars:
        audit_integrity_store_keys: false
```

## How It Works

1. **Persistent Journal Setup:** Ensures `/var/log/journal` exists for persistent logging
2. **FSS Initialization:** Generates sealing keys using `journalctl --setup-keys`
3. **Key Extraction (Optional):** Extracts the verification key from journal metadata
4. **Key Encryption (Optional):** Encrypts the verification key with Ansible Vault
5. **Controller Storage (Optional):** Stores encrypted key on the Ansible controller

## Verification

After running the role, verify FSS is active:

```bash
# Check journal sealing status
journalctl --verify

# Check for FSS keys
ls -la /var/log/journal/*/fss
```

## Security Notes

- **Verification Keys:** The FSS verification key is stored encrypted on the controller. Keep your vault password secure.
- **Sealing Keys:** The sealing key remains on the target system only and is never extracted.
- **Key Rotation:** FSS keys should be rotated periodically. Re-run the role to generate new keys.

## Troubleshooting

### Vault Encryption Fails

**Error:** `ERROR! Did not find any vault ID to use for encryption`

**Solution:** Ensure `audit_integrity_vault_encrypt_id` is set correctly. For Ansible 2.20+, this variable is required.

```yaml
audit_integrity_vault_encrypt_id: "default"  # or your specific vault ID
```

### Controller Directory Permission Errors

**Error:** Permission denied when creating `/tmp` subdirectories

**Solution:** Already resolved - the role uses `/tmp/deploy-system-audit-integrity` by default instead of `/tmp`.

### FSS Not Initializing

**Symptom:** `journalctl --verify` shows "No sealing yet"

**Solution:** Ensure the journal is persistent:
```bash
mkdir -p /var/log/journal
systemd-tmpfiles --create --prefix /var/log/journal
systemctl restart systemd-journald
```

## License

MIT

## Author Information

deploy-system-unified project
