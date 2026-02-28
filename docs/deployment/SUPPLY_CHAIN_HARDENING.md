# SUPPLY_CHAIN_HARDENING

## Overview
The Supply-Chain Hardening Profile is an optional, high-security configuration layer designed to protect against **Repository Hijacking** and **Compromised Mirrors**. It enforces strict cryptographic verification (SHA256 Checksums and GPG Fingerprints) for third-party software sources.

**Target Audience:** High-security production environments, air-gapped systems, and regulatory-compliant deployments.

## 🛡 Capabilities

| Component | Standard Behavior (Default) | Hardened Behavior | Mitigation |
| :--- | :--- | :--- | :--- |
| **GPU Repos** | Trusts GPG Key URL implicitly. | Verifies GPG Key SHA256 + Fingerprint before import. | Prevents Man-in-the-Middle (MitM) replacement of GPG keys. |
| **RPMFusion** | Installs via direct URL (trusts mirror). | Downloads to temp file -> Verifies SHA256 -> Installs. | Prevents installation of tampered release RPMs from compromised mirrors. |
| **Intel OneAPI** | Trusts GPG Key URL. | Verifies GPG Fingerprint. | Prevents key substitution. |

## 🚀 Activation

The profile is managed via a single configuration file: `inventory/group_vars/all/hardened_supply_chain.yml`.

### 1. Enable Verification
Toggle the verification flags to `true`.

```yaml
nvidia_gpg_key_verify: true
amd_rocm_gpg_key_verify: true
intel_oneapi_gpg_fingerprint_verify: true
rpmfusion_verify_checksum: true
```

### 2. Pin Checksums
You must populate the checksum variables with the **current official hashes** from the vendor. These are left empty by default to prevent "stale pin" breakage during standard deployments.

**Example (Hypothetical Values):**
```yaml
# NVIDIA CUDA (RHEL 9)
nvidia_gpg_key_sha256: "d42d06850... (full hash)"
nvidia_gpg_fingerprint: "AE09 FE4B ..."

# RPMFusion (Fedora 40)
rpmfusion_free_sha256: "a1b2c3d4..."
rpmfusion_nonfree_sha256: "e5f6g7h8..."
```

### 3. Deployment
Run your standard playbook. The `hardware/gpu` and `core/repositories` roles will automatically detect the hardened variables and switch to "Verified Mode".

```bash
ansible-playbook -i inventory/prod.ini SITE.YML
```

## ⚠️ Maintenance Note
**"Pinned means Manual"**: When vendors rotate their signing keys or release new repository versions (e.g., Fedora 40 -> 41), deployments **will fail** until you update the hashes in `hardened_supply_chain.yml`. This is a feature, not a bug—it forces human review of the supply chain change.
