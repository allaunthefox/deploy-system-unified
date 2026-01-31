# LLM & RAG Semantic Map

**Project**: Deploy-System-Unified
**Focus**: Infrastructure-as-Code (Ansible), Security Hardening, Ephemeral Workloads.

## 🧠 Architectural Constraints
- **Anti-Comingling Rule**: No task should perform unrelated operations (e.g., firewalling and package installation must be separate).
- **Explicit Base**: All workloads must import a standard base layer (`base_hardened.yml` or `base_ephemeral.yml`).
- **Fail-Secure**: Firewall (default-deny) must be established before services are deployed.

## 🗺 Documentation Cross-Reference

| Entity | Primary Documentation | RAG Context (LLM_RESEARCH) |
| :--- | :--- | :--- |
| **Core Base** | `docs/architecture/README.md` | `ansible_documentation/overview.md` |
| **Firewall** | `roles/security/firewall/tasks/main.yml` | `ansible_documentation/modules.md` |
| **SSH Access** | `roles/security/access/tasks/main.yml` | `ansible_documentation/variables.md` |
| **Containers** | `roles/containers/tasks/main.yml` | `molecule_documentation/overview.md` |
| **Ephemeral** | `branch_templates/base_ephemeral.yml` | `research_guidelines.md` |
| **Style** | `docs/development/STYLE_GUIDE.md` | `Style_Guide.md` |

## 🛠 Key Role Definitions
- `core/repositories`: Trusted package source initialization.
- `core/time`: Chrony-based NTP sync (Essential for forensic logging).
- `security/firewall`: L3/L4 Perimeter lockdown.
- `security/access`: L7 Identity & SSH Match rule management.
- `ops/pre_connection`: Controller-side pre-flight/Port Knocking.
- `security/scanning`: Post-deployment integrity auditor.

## 📋 Operational Flags
- `--low-risk-repair`: Non-destructive formatting fixes (Safe for automation).
- `--fix`: Structural and architectural fixes (Requires review).
- `ssh_randomize_port`: Sticky random port assignment logic.
- `ephemeral_volatile_secrets`: RAM-disk (tmpfs) backing for secrets.
