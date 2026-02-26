# VERSIONING_POLICY

This document provides a snapshot of the core software and tool versions currently employed by the project and outlines the policy for future upgrades.

## 📦 Current Version Snapshot (February 2026)

| Component | Version | Role |
| :--- | :--- | :--- |
| **Project** | `v1.4.2-stable` | Current verified release |
| **Ansible Core** | `2.16.x` | Primary orchestration engine |
| **Python** | `3.11+` | Runtime for scripts and Ansible |
| **Molecule** | `v6.x` | Role testing framework |
| **Podman** | `v4.9+` | Primary container runtime (Quadlets) |
| **SOPS** | `v3.8+` | Secrets management |

## 📈 Continuous Evolution Policy

The Deploy-System-Unified project adheres to a **continuous upward migration** strategy. 

### 1. Upward Mobility
Versions listed above are not static. To ensure maximum security, performance, and compatibility with emerging hardware (like Intel Battlemage and RISC-V platforms), the project will continuously move its version requirements upward as time goes on.

### 2. Security-First Upgrades
Security patches for core components (Ansible, Python, Kernel) are prioritized. When a dependency reaches end-of-life (EOL) or a critical vulnerability is identified, the project will mandate a minimum version increase across the fleet.

### 3. Stability Gates
While we move upward, we do so through the stability gates defined in the **[Stability Plan 2026](PLAN_STABILITY_EXECUTION_PLAN_2026)**. Every version increase must pass:
- FQCN linting.
- Idempotence verification via Molecule.
- Style guide enforcement.

---
*Last Updated: Wednesday, February 11, 2026*
