# LLM_MAP

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
| **Firewall** | `roles/networking/firewall/tasks/main.yml` | `ansible_documentation/modules.md` |
| **SSH Access** | `roles/security/access/tasks/main.yml` | `ansible_documentation/variables.md` |
| **Containers** | `roles/containers/tasks/main.yml` | `molecule_documentation/overview.md` |
| **Ephemeral** | `branch_templates/base_ephemeral.yml` | `research_guidelines.md` |
| **Style** | `docs/development/STYLE_GUIDE.md` | `Style_Guide.md` (see also: YAML_Style_Guide, Ansible_Style_Guide, Shell_Style_Guide, Documentation_Style_Guide) |
| **GPU Slicing** | `docs/gpu_slicing_setup.md` | `planning/GPU_Slicing_Planning_Document.md` |

## 🛠 Key Role Definitions

- `core/repositories`: Trusted package source initialization.
- `core/time`: Chrony-based NTP sync (Essential for forensic logging).
- `networking/firewall`: L3/L4 Perimeter lockdown.
- `security/access`: L7 Identity & SSH Match rule management.
- `ops/pre_connection`: Controller-side pre-flight/Port Knocking.
- `security/scanning`: Post-deployment integrity auditor.
- `containers/runtime`: Container runtime configuration (Podman) with GPU support.
- `containers/lxc`: LXC container management with GPU passthrough.
- `containers/quadlets`: Systemd quadlet container orchestration.
- `orchestration/k8s_node`: Kubernetes node configuration with GPU device plugins.

## 📋 Operational Flags

- `--low-risk-repair`: Non-destructive formatting fixes (Safe for automation).
- `--fix`: Structural and architectural fixes (Requires review).
- `ssh_randomize_port`: Sticky random port assignment logic.
- `ephemeral_volatile_secrets`: RAM-disk (tmpfs) backing for secrets.
- `containers_enable_gpu_support`: Enable GPU acceleration for containers.
- `containers_gpu_vendor`: Specify GPU vendor (nvidia, amd, intel).
- `containers_gpu_slicing.strategy`: GPU slicing strategy (mig, sriov, time-slicing, passthrough).
