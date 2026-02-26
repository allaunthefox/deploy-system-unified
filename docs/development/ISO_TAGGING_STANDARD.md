# ISO_TAGGING_STANDARD

**Purpose:** This document defines the standardized Ansible tags for implementing ISO, NIST, and CIS compliance controls across the Deploy-System-Unified project.

**Reference:** `DSU_ACTION_CODES_COMPLETE.md`, NIST SP 800-53 Rev 5, ISO/IEC 27002:2022.

---

## 🏗️ Naming Standards (ISO 9001 Alignment)

To ensure global auditability, all project components follow strict naming schemas.

### 🏷️ Tag Standard (snake_case)
All tags MUST use **snake_case**. Kebab-case or spaces are strictly forbidden.
- ✅ `iso_27001_8_26`
- ✅ `restore_test`
- ❌ `iso-27001-8-26`
- ❌ `restore-test`

### 📂 Role Classification (ISO Document ID)
Roles are categorized in `meta/main.yml` using standard document-type prefixes:
- **`POL-SEC`**: Security Policy Enforcement (e.g., `security/sshd`)
- **`SOP-OPS`**: Standard Operating Procedures (e.g., `ops/monitoring`)
- **`WI-CONT`**: Work Instructions for Containers (e.g., `containers/runtime`)
- **`STD-CORE`**: Core Standards & Infrastructure (e.g., `core/logging`)

---

## 🏷️ ISO 27001:2022 / 27002:2022 (Security Controls)

These tags map to the ISO/IEC 27001:2022 framework. ISO 27002:2022 provides the implementation guidance for these controls.

| Tag | Domain | ISO 27002 Control | Applicable Roles |
|-----|--------|-------------------|------------------|
| `iso_27001_8_8` | Vulnerability Mgmt | 8.8 (Idempotency) | All |
| `iso_27001_8_9` | Config Mgmt | 8.9 (Configuration) | `core/bootstrap` |
| `iso_27001_8_17` | Clock Sync | 8.17 (Clock Sync) | `core/time` |
| `iso_27001_8_26` | App Security | 8.26 (Application) | `security/firejail` |
| `iso_27001_9_2` | Access Provision | 9.2 (User Access) | `security/sshd` |
| `iso_27001_10_1` | Cryptography | 10.1 (Crypto) | `security/sshd` |

---

## 🏷️ NIST SP 800-53 Rev 5 (Federal Standard)

Industry leaders like `ansible-lockdown` use NIST tags as a universal compliance language.

| Tag | Control Name | ISO 27001 Map | Role |
|-----|--------------|---------------|------|
| `nist_ac_2` | Access Control | §9.2 | `security/access` |
| `nist_ac_3` | Access Enforcement | §9.4 | `networking/firewall` |
| `nist_au_2` | Audit Events | §12.4 | `security/audit_integrity` |
| `nist_ia_2` | Identification/Auth | §9.2 | `security/sshd` |
| `nist_sc_8` | Transmission Security | §10.1 | `security/sshd` |

---

## 🏷️ Operational & Audit Tags

Use these tags to control *how* playbooks execute in compliance contexts.

| Tag | Purpose | Description |
|-----|---------|-------------|
| `audit` | **Audit Mode** | Only run verification/check tasks. |
| `remediate` | **Remediate Mode** | Apply changes to reach compliance. |
| `scored` | **Scored Control** | Directly impacts compliance score. |
| `level_1` | **CIS Level 1** | Base hardening (low impact). |
| `level_2` | **CIS Level 2** | Defense-in-depth (may impact perf). |

---

## 🏷️ Post-Quantum Cryptography (PQC)

As organizations transition to quantum-resistant infrastructure (CNSA 2.0), use these tags to mark PQC-capable or enforced tasks.

| Tag | Standard | Description | Action Code |
|-----|----------|-------------|-------------|
| `pqc` | **NIST PQC** | General Post-Quantum capability. | 400100 |
| `pqc_hybrid` | **Hybrid Mode** | Classical + Quantum-Resistant. | 400101 |
| `pqc_fips_203` | **ML-KEM** | Lattice key encapsulation. | 400101 |
| `pqc_fips_204` | **ML-DSA** | Lattice signatures. | 400102 |
| `cnsa_2_0` | **NSA CNSA 2.0** | National Security alignment. | 400101 |

---

## Automated Recovery Verification & Storage Security (ISO 27040)

These tags mark tasks that implement self-healing and integrity verification for storage systems.

| Tag | Standard | Description | Audit Event Identifier |
|-----|----------|-------------|-----------|
| `restore_test` | **ISO 27040** | Automated sample restore verification. | 900003 |
| `integrity_verify` | **ISO 27040** | Cryptographic hash verification. | 900004 |
| `dedupe` | **ISO 27040** | Offline storage deduplication (NoDupeLabs). | 500060 |
| `archival` | **ISO 27040** | High-compression archival optimization. | 500070 |
| `hardened_archival` | **ISO 27040 §13** | Archival with mandatory integrity verification. | 600032 |
| `profile_guard` | **ISO 9001** | Environment-specific safety restrictions. | 600030 |
| `secrets_archival` | **ISO 27001 §10.1** | Secret key management for archival. | 400015 |
| `boot_integrity` | **NIST SP 800-193** | Secure Boot and PCR attestation. | 800510 |
| `pqc_secrets` | **ISO 27001 §10.1** | Quantum-resistant secret storage. | 400103 |
| `supply_chain` | **ISO 27001 §14.2** | Image signature and provenance verification. | 700014 |
| `sbom` | **ISO 27001 §14.2** | Software Bill of Materials generation. | 520040 |

---

## Security Observability (ISO 27001 §8.15/§8.16)

These tags mark the enhanced observability stack that enables real-time forensic auditing.

| Tag | Component | Description | Audit Event Identifier |
|-----|-----------|-------------|-----------|
| `loki` | **Aggregator** | Centralized log aggregation engine. | 840040 |
| `promtail` | **Collector** | Audit Event Identifier aware log collector. | 840031 |
| `forensic` | **Visualization** | DSU Security Observability Dashboard. | 840041 |

---

### Role Implementation Roadmap (PQC & Advanced)

| Role | Status | Implementation |
|------|--------|----------------|
| `security/sshd` | ✅ Active | Hybrid ML-KEM / sntrup761 support. |
| `storage/backup/restic` | ✅ Active | ISO 27040 Automated Restore Testing. |
| `containers/monitoring` | ✅ Active | Security Observability Dashboards (Loki). |
| `networking/vpn_mesh` | ⏳ Roadmap | Waiting for WireGuard PQC standardization. |
| `core/secrets` | ⏳ Roadmap | Future integration with PQC-ready Age/SOPS. |

---

## 📝 Implementation Guide

### Example: NIST + ISO Combined Task

```yaml
- name: "CIS 5.2.11 | NIST SC-8 | ISO 27001 §10.1 | Configure strong ciphers"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    line: "Ciphers chacha20-poly1305@openssh.com..."
  tags:
    - cis_5_2_11
    - nist_sc_8
    - iso_27001_10_1
    - remediate
    - scored
```
