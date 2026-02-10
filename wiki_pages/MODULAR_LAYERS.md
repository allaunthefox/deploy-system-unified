# MODULAR_LAYERS

Deploy-System-Unified utilizes a layered architecture to maintain a clear separation of concerns. This design ensures that infrastructure hardening is decoupled from application workloads.

## 🏗️ Layer 1: The Infrastructure Base

"The Base" defines the system's security personality and foundational environment. It is intended to be workload-agnostic.

### [Base Hardened](base_hardened)
The standard foundation for persistent systems (Bare Metal, VPS, VMs).
- **Security**: Firewall (L3/L4), SSH hardening (L7), Kernel hardening.
- **Consistency**: Time synchronization (Chrony), Repository initialization.
- **Audit**: Log integrity and system auditing (auditd).

### [Base Ephemeral](base_ephemeral)
A specialized foundation for high-security, zero-footprint environments.
- **Volatility**: RAM-disk backed structures.
- **Security**: Aggressive shredding on cleanup, immutable audit trails.

---

## 🚀 Layer 2: The Solution Stack

"The Stack" is the application layer that sits on top of a Base. Stacks are typically represented by branch templates or specific solution playbooks.

### [Production Deploy](production_deploy)
The canonical production stack.
- **Foundation**: Imports `base_hardened.yml`.
- **Workload**: Container runtimes (Podman), Orchestration (Quadlets), Reverse Proxy (Caddy).
- **Integrity**: Integrated security scanning.

### Specialized Stacks
- **GPU Workstations**: Base Hardened + Universal GPU Drivers + Compute Stacks.
- **K8s Secure Node**: Base Hardened + Kubernetes runtime readiness.
- **Media Stack**: Base Hardened + Containerized media services (Jellyfin, *Arr suite).

## 💡 Why This Split?

1. **Reusability**: One "Hardened Base" can power ten different "Solution Stacks."
2. **Auditability**: Security teams can audit the Base layer independently of the applications.
3. **Idempotence**: Changes to the application stack do not require a complete re-run of the infrastructure base.
