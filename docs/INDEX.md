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
* **[Security Layers](./architecture/SECURITY_LAYERS.md)**: 5-layer Defense-in-Depth visual architecture.
* **[Boot Lifecycle](./architecture/BOOT_LIFECYCLE.md)**: Explicit boot sequence and forensic chain of trust.
* **[Network Topology](./architecture/NETWORK_TOPOLOGY.md)**: Data flow and network isolation map.
* **[Cross-Runtime Isolation](./architecture/CROSS_RUNTIME_ISOLATION.md)**: Securing stacks spanning LXC and Kubernetes.
* **[Combination Matrix](./architecture/DEPLOYMENT_COMBINATIONS.md)**: Visual guide to all supported and experimental deployment paths.
* **[Interaction Matrix](./architecture/CROSS_RUNTIME_MATRIX.md)**: Network interactions between Podman, K3s, LXC, and QEMU.
* **[Storage Interaction](./architecture/STORAGE_INTERACTION_MATRIX.md)**: Filesystem and directory access map for all runtimes.
* **[Forensic Flow](./architecture/FORENSIC_FLOW.md)**: Mermaid diagram of the auditable deployment pipeline.
* **[Layered Security](./architecture/LAYERED_SECURITY.md)**: How firewalls, access controls, and scanning work together.
* **[Ephemeral Design](./architecture/EPHEMERAL_DESIGN.md)**: Logic behind zero-footprint deployments.

### [2. Development](./development/CONTRIBUTING.md)

* **[Development Tooling](./development/TOOLING.md)**: Explaining switches (`--low-risk-repair`) and enforcement.
* **[Digest Maintenance](./development/DIGEST_MAINTENANCE.md)**: Automated image update and system support verification.
* **[Style Guide](./development/STYLE_GUIDE.md)**: Standards for YAML, Shell, and Ansible.
* **Testing**: Using Molecule for multi-platform idempotency verification.
* **CI**: Verify RHEL-compatible GPG keys (AlmaLinux) using `verify-rhel-compat-keys.yml`.
* **Verify RHEL-compatible GPG keys (AlmaLinux)**: CI test that validates NVIDIA & AMD ROCm repo GPG key checksum/fingerprint verification (workflow: `verify-rhel-compat-keys.yml`). Note: This workflow is manually runnable from the GitHub Actions UI (Actions → Verify RHEL-Compatible (AlmaLinux) GPG Keys → Run workflow).
* **Enforcement**: How `enforce_style_guide.sh` keeps the codebase clean.

### [3. Deployment](./deployment/EXAMPLES.md)

* **Solution Stacks**: How to use the Production, Development, and Ephemeral templates.
* **Production Deploy Template**: Use `PRODUCTION_DEPLOY.yml` as the canonical production deployment playbook. Treat `branch_templates/` as reference-only.
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
* **[SOPS Migration Guide](./deployment/SOPS_MIGRATION_GUIDE.md)**: Staged migration workflow from Vault to SOPS + Age with rollback gates.
* **[SOPS Key Rotation SOP](./deployment/SOPS_KEY_ROTATION_SOP.md)**: Operational key and secrets rotation cadence, emergency procedure, and audit checklist.
* **[Deployment Status](./deployment/DEPLOYMENT_STATUS.md)**: Current system readiness and implementation status.
* **[Architecture Migration](./deployment/ARCHITECTURE_MIGRATION_GUIDE.md)**: Guide for upgrading to the multi-arch standard.
* **Potential Problems**: [Issues to consider when deploying profile combinations](./deployment/POTENTIAL_PROBLEMS.md).

### [3a. Kubernetes & Helm](./deployment/KUBERNETES.md)

* **[Ingress Controller Setup](./deployment/INGRESS_CONTROLLER_SETUP.md)**: Caddy, Traefik, and Nginx ingress configuration.
* **[Helm Charts](./charts/index.md)**: Deployable Helm charts for:
  * **auth-stack**: Authentik (SSO)
  * **backup-stack**: Restic, Rclone (backups)
  * **database-stack**: PostgreSQL
  * **logging-stack**: Loki, Promtail (log aggregation)
  * **media-stack**: Jellyfin, Radarr, Sonarr
  * **monitoring-stack**: Prometheus, Grafana
  * **network-stack**: Pi-hole (DNS)
  * **ops-stack**: Homarr, Vaultwarden
  * **proxy-stack**: Caddy, Nginx (reverse proxy)
  * **security-stack**: Security tools
* **K8s Deployment**: Use `playbooks/deploy_kubernetes.yml` to deploy the full stack on K3s
* **Benchmark**: [K8s vs Podman methodology](./benchmarks/k8s_vs_podman_methodology.md) for resource comparison.

### [4. GPU Slicing](./deployment/GPU_SLICING.md)

* **GPU Support**: NVIDIA, AMD, and Intel GPU configuration
* **Slicing Strategies**: MIG, SR-IOV, time-slicing, and passthrough
* **Container Integration**: Kubernetes, LXC, and Podman with GPU acceleration
* **Branch Templates**: GPU-specific deployment configurations

### [5. Security & Forensics](./security/SECURITY_AUDIT_REPORT.md)

* **[Security Audit Report](./security/SECURITY_AUDIT_REPORT.md)**: Comprehensive security assessment and role analysis.
* **[Threat Model](./security/THREAT_MODEL.md)**: STRIDE analysis and residual risk assessment.
* **[Forensic Standards](./security/FORENSIC_STANDARDS.md)**: Mandatory task naming and Audit Event Identifier convention.
* **[Audit Event Identifier Catalog](../DSU_AUDIT_EVENT_IDENTIFIERS.md)**: 480+ forensic audit codes mapped to ISO standards.
* **[Forensic Restoration Runbook](./RESTORE_RUNBOOK.md)**: Step-by-step guide for ISO 27040 data restoration.

### [6. Planning](./planning/SUMMARY.md)

* **[Planning Summary](./planning/SUMMARY.md)**: Overview of all planning documents.
* **[Migration Strategy](./planning/MIGRATION_STRATEGY.md)**: Strategy for legacy data migration and credential rotation.
* **[Restructuring Plan 2026](./planning/RESTRUCTURING_PLAN_2026.md)**: Strategic plan for project restructuring including community enhancements.
* **[Community Enhancement Plan](./planning/COMMUNITY_ENHANCEMENT_PLAN.md)**: Plan to address community engagement deficits identified through analysis.
* **[Wiki Improvement Plan](./planning/WIKI_IMPROVEMENT_PLAN.md)**: Plan to address wiki content deficits, particularly overly long pages.
* **[GPU Plan](./planning/GPU_ENHANCED_PLAN.md)**: Planning document for GPU enhancements.
* **[Data Mapping](./planning/DATA_MAPPING.md)**: Detailed file lifecycle mapping for the migration process.

---

## 📚 Documentation Integration

For guidance on navigating between the main project documentation and the GitHub wiki, see the **[Documentation Bridge](DOCUMENTATION_BRIDGE.md)**.

## 🤖 LLM & RAG Support

For AI assistants and RAG systems, see the **[LLM Map](./development/LLM_MAP.md)** for high-density context loading.
Knowledge base research can be found in the sibling `LLM_RESEARCH` directory.
