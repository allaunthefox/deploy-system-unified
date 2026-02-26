# Threat Model: Deploy-System-Unified

**Standard**: NIST SP 800-154 / ISO 27001 §16.1  
**Methodology**: STRIDE  
**Status**: Active Audit

---

## 📈 System Overview

This project implements a 5-layer Defense-in-Depth model. This threat model analyzes potential vectors at each layer.

---

## 🔍 STRIDE Analysis

| Threat | Description | Mitigation | Status |
|--------|-------------|------------|--------|
| **Spoofing** | Unauthorized user or host impersonation. | `security/sshd` (PQC/Keys), `core/identity` (Unique UUIDs). | ✅ Hardened |
| **Tampering**| Malicious modification of roles or container images. | `security/sbom`, `security/file_integrity`, `cosign` verification. | ✅ Hardened |
| **Repudiation**| Actions taken without an auditable trail. | Mandatory **Forensic Action Codes** (Loki/Grafana). | ✅ Hardened |
| **Information Disclosure** | Leakage of secrets or sensitive logs. | **SOPS/Age** encryption, `detect-secrets` CI scan. | ✅ Hardened |
| **Denial of Service** | Resource exhaustion attacking host or services. | `security/resource_protection` (ulimits), `security/ips`. | ✅ Hardened |
| **Elevation of Privilege** | Container breakout or sudo escalation. | **Rootless Podman**, `security/sandboxing` (Firejail/Bubblewrap). | ✅ Hardened |

---

## ⚠️ Identified Gaps & Residual Risk

### 1. Internal Traffic Cleartext (Medium)
- **Vector**: Caddy proxies traffic to backend containers (Jellyfin, etc.) over HTTP via bridge networks.
- **Risk**: A compromised Layer 4 container could sniff internal L3 bridge traffic.
- **Remediation**: Transition to mTLS or `Internal=true` isolated Podman networks for all backends.

### 2. Variable Visibility Drift (Low)
- **Vector**: Compliance settings (e.g., `PASS_MAX_DAYS`) are defined in role `vars/` but not exposed in `group_vars/all`.
- **Risk**: Hard to verify exact policy values without reading deep role code.
- **Remediation**: Enact a `policy_overrides.yml` in `group_vars/all`.

---

## 🛠️ Operational Safeguards

1.  **Fail-Secure**: All security roles default to `fail_secure: true`.
2.  **Audit Pulse**: Weekly `security/goss` checks verify state consistency.

*Verified by: DSU Security Architect*
*Last Updated: February 2026*
