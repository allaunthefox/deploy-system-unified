# Project Ontology: Deployment Profiles & Infrastructure

This document defines the formal relationship between **Deployment Profiles**, **Infrastructure Types**, and **Architectural Settings**. Adhering to this ontology prevents "distinction drift" and ensures that security policies and hardware optimizations are applied correctly.

## 🌌 The Three Dimensions

1.  **Deployment Profile (`deployment_profile`)**: Defines the *security posture* and *functional purpose* (e.g., `hardened`, `ephemeral`).
2.  **Infrastructure Type (`virt_type`)**: Defines the *hardware/virtualization layer* (e.g., `bare-metal`, `container`).
3.  **Architectural Profile**: Defines the *CPU architecture* and *GPU vendor* (e.g., `x86_64`, `nvidia`).

---

## 🗺️ Master Mapping

| Deployment Profile | Security Class | Primary Entrypoint | Expected `virt_type` |
| :--- | :--- | :--- | :--- |
| **`hardened`** (Default) | Strict | `base_hardened.yml` | `bare-metal`, `vps` |
| **`production`** | Strict | `production_deploy.yml` | `bare-metal`, `vps` |
| **`ephemeral`** | Strict | `base_ephemeral.yml` | `container`, `virtual` |
| **`vps`** | Strict | `vps_hardened.yml` | `virtual` |
| **`backup`** | Strict | `restore_data.yml` | `any` |
| **`workstation`** | Lenient | `gpu_workstations.yml` | `bare-metal` |
| **`dev`** | Lenient | `development_servers.yml` | `any` |

---

## 🛠️ Infrastructure Ontology (`virt_type`)

| `virt_type` | Description | Typical Constraints |
| :--- | :--- | :--- |
| **`bare-metal`** | Physical hardware | Requires full driver stack (GPU/CPU). |
| **`vps`** | Cloud VPS (e.g., Contabo) | Optimized for KVM with high-IO storage. |
| **`virtual`** | Generic VM / Guest | Uses passthrough or paravirtualized drivers. |
| **`container`** | Podman/LXC | Shared kernel; restricted sysctl/module access. |

---

## 🏗️ Enforcement Rules

1.  **Hierarchy**: `inventory/group_vars/` MUST contain a file or directory matching each supported `deployment_profile`.
2.  **Validation**: The `ops/preflight` role validates that the selected `deployment_profile` matches the `virt_type` constraints.
3.  **Naming Consistency**: All new branch templates MUST be named using the pattern `<profile>_<description>.yml`.
4.  **No Manual Override**: Avoid setting security-critical flags (like `firewall_enabled`) manually in tasks; rely on the `deployment_profile` to toggle these via group variables.

## 🛡️ Runtime Enforcement

The ontological contract is strictly enforced at runtime via `playbooks/preflight_validate.yml`. This playbook:
- **Ensures Uniqueness**: Asserts that every host belongs to exactly ONE ontological profile group.
- **Verifies State**: Checks that the host's actual variable state (e.g., `firewall_enabled`, `ssh_randomize_port`) matches the requirements of its declared profile.
- **Fail-Loudly**: Aborts the deployment immediately if a contract violation is detected, preventing inconsistent system states.

## 🔄 Idempotency Contract

Every profile in this project adheres to a strict **Idempotency Contract**:
- **Baseline Assurance**: A second run of any playbook against a converged host MUST produce `changed=0`.
- **State-Aware Tasks**: Custom shell/command tasks MUST implement state checks (e.g., checking `/sys/` or `/proc/`) rather than blindly executing.
- **No False Positives**: Deployment tools (like `verify_idempotence.sh`) are used to benchmark and ensure that re-runs do not trigger redundant changes.

## 🤖 LLM & RAG Usage

When assisting with this project, AI agents MUST refer to this ontology to determine the appropriate base role and security defaults. If a user requests a "secure" deployment, the agent should default to the `hardened` profile and `bare-metal` infrastructure unless otherwise specified.
