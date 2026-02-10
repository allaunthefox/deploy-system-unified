# README

This project follows a **Layered Infrastructure** approach, strictly adhering to the principle:
> "Complexity is not a problem, but comingling tasks is."

## 🏗 The Modular Layers

### 1. The Foundation (`main.yml`)

The absolute entry point. It handles physical system readiness (directory structures, preflight checks) but **never** contains roles. It ensures the target is "Ansible-ready."

### 2. The Infrastructure Bases

These are pure infrastructure playbooks that define the system's personality without assuming a workload.

* **[Base Hardened](../../../wiki_pages/base_hardened.md)**: Standard secure foundation (Firewall, SSH Hardening, Time Sync).
* **[Base Ephemeral](../../../wiki_pages/base_ephemeral.md)**: Volatile foundation (RAM-disks, secure shredding, immutable audit trails).

### 3. The Solution Stacks (Branches)

These templates import a Base Layer and add a specific application workload.

* **Production**: Base Hardened + Secure Container Runtime + Caddy + Scanning.
* **Development**: Base Hardened (Flexible) + Container Runtime + Caddy.
* **Ephemeral**: Base Ephemeral + Container Runtime + Caddy + Scanning.
* **Virtual Hypervisor**: Base Hardened + QEMU/KVM + **virt_networking** + **virt_storage** + **libguestfs** for robust recovery.
* **K8s Secure Node**: Base Hardened + Kubernetes readiness logic.
* **VPS Hardened**: Cloud Provider Sync + Base Hardened + VPS-specific kernel/IO tuning.
* **Bare Metal Hardened**: Base Hardened + Physical Hardware Support + Disk Tuning.

## 🔒 Security Architecture

### Layered Defense

1. **L3/L4 (Firewall)**: Established *first* with a default-deny policy via `networking/firewall`.
2. **L7 (Access)**: Identity-based restrictions using SSH Match blocks via `security/access`.
3. **Audit**: Immutable, chrony-verified logs for every deployment event.
4. **Verification**: Post-deployment integrity scanning via `security/scanning`.

## 🛠 Operational Utilities

Utilities like `ops/session` (Tmux) and `ops/connection_info` (Connection encryption) are kept in the `ops/` namespace to keep the security roles focused purely on the target's posture.
