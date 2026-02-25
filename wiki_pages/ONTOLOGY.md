# ONTOLOGY

This document defines the formal relationship between **Deployment Profiles**, **Infrastructure Types**, and **Forensic Intelligence**. Adhering to this ontology prevents "distinction drift" and ensures that security policies and hardware optimizations are applied correctly.

## 🌌 The Four Dimensions

1.  **Deployment Profile (`deployment_profile`)**: Defines the *security posture* and *functional purpose* (e.g., `hardened`, `ephemeral`).
2.  **Infrastructure Type (`virt_type`)**: Defines the *hardware/virtualization layer* (e.g., `bare-metal`, `container`).
3.  **Architectural Profile**: Defines the *CPU architecture* and *GPU vendor* (e.g., `x86_64`, `nvidia`).
4.  **Forensic Dimension**: Defines the *auditable trace* left by actions, mapped to **350+ Action Codes**.

---

## 🗺️ Master Mapping

| Deployment Profile | Security Class | Forensic Grade | Primary Entrypoint |
| :--- | :--- | :--- | :--- |
| **`hardened`** (Default) | Strict | **Forensic** (Full Loki) | `base_hardened.yml` |
| **`production`** | Strict | **Compliance** (Signed Logs) | `production_deploy.yml` |
| **`ephemeral`** | Strict | **Minimal** (Basic Journal) | `base_ephemeral.yml` |
| **`vps`** | Strict | **Standard** (Rsyslog) | `vps_hardened.yml` |

---

## 🛠️ Action Code Suites

All actions in the framework are classified into one of the following suites for auditability:

| Suite | Action Code Range | ISO Standard | Purpose |
| :--- | :--- | :--- | :--- |
| **PQC Suite** | `400100 - 400110` | ISO 27001 §10.1 | Quantum-resistant crypto |
| **Forensic Suite** | `840030 - 840041` | ISO 27001 §12.4 | Loki/Grafana observability |
| **Threat Analysis Suite** | `480000 - 480010` | ISO 27001 Amd 1 | AI-Driven Log Auditing |
| **Autonomic Suite** | `900000 - 900031` | ISO 27040 | Verified recovery |
| **SBOM Suite** | `520040 - 520047` | ISO 27001 §14.2 | Supply chain verified |
| **Guard Suite** | `600030 - 600032` | ISO 9001 | Profile-based safety |
| **Integrity Response Suite** | `800510 - 800515` | NIST SI-7 | Hardware-Bound State Purge |

---

## 🏗️ Enforcement Rules

1.  **Hierarchy**: `inventory/group_vars/` MUST contain a file or directory matching each supported `deployment_profile`.
2.  **Validation**: The `ops/preflight` role validates that the selected `deployment_profile` matches the `virt_type` constraints.
3.  **Naming Consistency**: All tasks MUST follow the pattern `[Standard] | [Action Code] | [Name]`.
4.  **No Manual Override**: Security flags MUST be managed via the `deployment_profile` to ensure consistent forensic signatures.

## 🔄 Idempotency Contract

Every profile in this project adheres to a strict **Idempotency Contract**:
- **Baseline Assurance**: A second run of any playbook against a converged host MUST produce `changed=0`.
- **State-Aware Tasks**: Custom shell/command tasks MUST implement state checks (e.g., checking `/sys/` or `/proc/`) rather than blindly executing.
- **Action Verification**: Idempotence is verified via Action Code `600151` (Idempotency check pass).

## 🤖 LLM & RAG Usage

When assisting with this project, AI agents MUST refer to this ontology to determine the appropriate base role and security defaults. If a user requests a "secure" deployment, the agent should default to the `hardened` profile and ensure all tasks include the mandatory forensic metadata.
