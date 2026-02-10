# INDEX

Welcome to the documentation for **Deploy-System-Unified**, a modular, security-first infrastructure deployment system built on Ansible.

![Verify RHEL-compatible GPG keys](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/verify-rhel-compat-keys.yml/badge.svg)

## 📖 Philosophical Foundation

This project is built on a core architectural principle:
> **"Complexity is not a problem, but comingling tasks is."**

Every role, task, and playbook is designed to be granular, single-purpose, and explicit.

## 📂 Documentation Map

### [1. Architecture](./architecture/README.md)

* **[Core Philosophy](./architecture/NON_COMINGLING.md)**: Why we avoid comingled tasks.
* **[Virtual Networking](./architecture/VIRTUAL_NETWORKING.md)**: VLANs, VXLANs, and L2/L3 isolation.
* **[Backup Strategy](./architecture/BACKUP_STRATEGY.md)**: rclone, restic, and system snapshots.
* **[GPU Slicing Architecture](./architecture/GPU_SLICING.md)**: Architectural overview of GPU slicing implementation.
* **[Modular Layers](./architecture/MODULAR_LAYERS.md)**: Understanding the split between "The Base" and "The Stack."
* **[Layered Security](./architecture/LAYERED_SECURITY.md)**: How firewalls, access controls, and scanning work together.
* **[Ephemeral Design](./architecture/EPHEMERAL_DESIGN.md)**: Logic behind zero-footprint deployments.

### [2. Development](./development/CONTRIBUTING.md)

* **[Development Tooling](./development/TOOLING.md)**: Explaining switches (`--low-risk-repair`) and enforcement.
* **[Style Guide](./development/STYLE_GUIDE.md)**: Standards for YAML, Shell, and Ansible.
* **Testing**: Using Molecule for multi-platform idempotency verification.
* **CI**: Verify RHEL-compatible GPG keys (AlmaLinux) using `verify-rhel-compat-keys.yml`.
* **Verify RHEL-compatible GPG keys (AlmaLinux)**: CI test that validates NVIDIA & AMD ROCm repo GPG key checksum/fingerprint verification (workflow: `verify-rhel-compat-keys.yml`). Note: This workflow is manually runnable from the GitHub Actions UI (Actions → Verify RHEL-Compatible (AlmaLinux) GPG Keys → Run workflow).
* **Enforcement**: How `enforce_style_guide.sh` keeps the codebase clean.

### [3. Deployment](./deployment/EXAMPLES.md)

* **Solution Stacks**: How to use the Production, Development, and Ephemeral templates.
* **Production Deploy Template**: Use `production_deploy.yml` as the canonical production deployment playbook. Treat `branch_templates/` as reference-only.
* **Variables**: Configuring randomized ports, IP restrictions, and secrets.
* **[Architecture & Vendor Profiles](./deployment/ARCH_VENDOR_PROFILES.md)**: Explicit arch/vendor selection to avoid x86-only assumptions.
* **[Hardware Compatibility Matrix](./deployment/HARDWARE_COMPATIBILITY_MATRIX.md)**: Supported CPU/GPU combinations and platform tiers.
* **[GPU Interaction Matrix](./deployment/GPU_INTERACTION_MATRIX.md)**: Behavior in VM, Container, and Hybrid environments.
* **[OS Configuration](./deployment/OS_CONFIGURATION.md)**: The "Single Source of Truth" for fleet-wide OS settings.
* **[GPU Stack Setup](./deployment/GPU_STACK_SETUP.md)**: Detailed guide for installing unified GPU drivers and compute stacks.
* **[Container Runtime Guide](./deployment/CONTAINER_RUNTIME.md)**: Default Podman capabilities and runtime security settings.
* **[Universal Deployment Guide](./deployment/UNIVERSAL_DEPLOYMENT_GUIDE.md)**: Master SOP for replicable system deployment.
* **[Contabo Media Profile](./deployment/CONTABO_MEDIA_PROFILE.md)**: Specifications for the VPS 30 SSD Media Stack.
* **[SSH Transfer Profile](./deployment/SSH_TRANSFER_PROFILE.md)**: Standard SSH transfer method and fallbacks.
* **[SSH Incident Postmortem](./deployment/SSH_INCIDENT_POSTMORTEM.md)**: Root cause analysis and resolution timeline.
* **[SSH Idempotence Guardrails](./deployment/SSH_IDEMPOTENCE_GUARDRAILS.md)**: Deterministic SSH configuration and anti-drift rules.
* **[Hybrid Security Setup](./deployment/SECURITY_CROWDSEC_HYBRID.md)**: Implementation details for the Container+Host CrowdSec architecture.
* **[Supply-Chain Hardening](./deployment/SUPPLY_CHAIN_HARDENING.md)**: Configuration guide for strict GPG/Checksum verification of third-party repositories.
* **[Deployment Status](./deployment/DEPLOYMENT_STATUS.md)**: Current system readiness and implementation status.
* **[Architecture Migration](./deployment/ARCHITECTURE_MIGRATION_GUIDE.md)**: Guide for upgrading to the multi-arch standard.
* **Potential Problems**: [Issues to consider when deploying profile combinations](./deployment/POTENTIAL_PROBLEMS.md).

### [4. GPU Slicing](./deployment/GPU_SLICING.md)

* **GPU Support**: NVIDIA, AMD, and Intel GPU configuration
* **Slicing Strategies**: MIG, SR-IOV, time-slicing, and passthrough
* **Container Integration**: Kubernetes, LXC, and Podman with GPU acceleration
* **Branch Templates**: GPU-specific deployment configurations

### [5. Security](./security/SECURITY_AUDIT_REPORT.md)

* **[Security Audit Report](./security/SECURITY_AUDIT_REPORT.md)**: Comprehensive security assessment and role analysis.

### [6. Planning](./planning/MIGRATION_STRATEGY.md)

* **[Migration Strategy](./planning/MIGRATION_STRATEGY.md)**: Strategy for legacy data migration and credential rotation.
* **[Restructuring Plan 2026](./planning/RESTRUCTURING_PLAN_2026.md)**: Strategic plan for project restructuring.
* **[GPU Plan](./planning/GPU_ENHANCED_PLAN.md)**: Planning document for GPU enhancements.
* **[Data Mapping](./planning/DATA_MAPPING.md)**: Detailed file lifecycle mapping for the migration process.

---

## 🤖 LLM & RAG Support

For AI assistants and RAG systems, see the **[LLM Map](./development/LLM_MAP.md)** for high-density context loading.
Knowledge base research can be found in the sibling `LLM_RESEARCH` directory.
