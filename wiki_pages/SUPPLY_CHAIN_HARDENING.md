# SUPPLY_CHAIN_HARDENING

## Overview
The Supply-Chain Hardening framework provides end-to-face cryptographic verification of all software components, from bare-metal repositories to containerized workloads.

**Status:** ✅ **Fully Integrated** (Feb 2026)

## 🛡 Capabilities

### 1. Repository & Binary Verification
| Component | Hardened Behavior | Mitigation |
| :--- | :--- | :--- |
| **GPU Repos** | Verifies GPG Key SHA256 + Fingerprint before import. | Prevents repository hijacking (MitM). |
| **RPMFusion** | Downloads -> Verifies SHA256 -> Installs. | Prevents tampered mirror packages. |
| **Intel OneAPI** | Mandatory GPG Fingerprint verification. | Prevents key substitution. |

### 2. Container Workload Verification (Cosign)
The system enforces **Sigstore/Cosign** signature verification for all container images before they are pulled or executed.
- **Enforcement**: Deployment hard-fails if an image lacks a valid signature (Action `700015`).
- **Standard**: Aligns with ISO 27001 §14.2.

### 3. Software Bill of Materials (SBOM Audit)
Automatically generates and signs a **CycloneDX (v1.5)** SBOM for the entire deployment.
- **Discovery**: Scans all roles for container images, Python libraries, and system binaries.
- **Immutability**: Every SBOM is signed (`sbom.json.sha256`) to prevent post-audit tampering.
- **Forensic Match**: The `security/scanning` role performs a real-time vulnerability match against the signed SBOM.

## 🚀 Activation

The framework is managed via `inventory/group_vars/all/os_settings.yml`.

### 1. Enable Global Supply Chain Guard
```yaml
system_container_cosign_verify: true
```

### 2. Run SBOM Audit
```bash
ansible-playbook production_deploy.yml --tags sbom
```
Report location: `ci-artifacts/sbom/sbom.json`

## ⚠️ Maintenance Note
**"Trust but Verify"**: The SBOM audit is a mandatory compliance gate in `hardened` and `production` profiles. If new, untrusted dependencies are introduced, the supply-chain watchdog will halt the deployment.
