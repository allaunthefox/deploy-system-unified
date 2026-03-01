# INDEX

Welcome to the documentation for **Deploy-System-Unified**, a modular, security-first infrastructure deployment system built on Ansible.

![Verify RHEL-compatible GPG keys](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/verify-rhel-compat-keys.yml/badge.svg)

## 📖 Philosophical Foundation

This project is built on a core architectural principle:
> **"Complexity is not a problem, but comingling tasks is."**

Every role, task, and playbook is designed to be granular, single-purpose, and explicit.

## 📂 Documentation Map

### [1. Architecture](Home)

* **[Core Philosophy](SEPARATION_OF_CONCERNS)**: Why we avoid comingled tasks.
* **[Virtual Networking](VIRTUAL_NETWORKING)**: VLANs, VXLANs, and L2/L3 isolation.
* **[Backup Strategy](BACKUP_STRATEGY)**: rclone, restic, and system snapshots.
* **[GPU Slicing Architecture](GPU_SLICING)**: Architectural overview of GPU slicing implementation.
* **[Modular Layers](MODULAR_LAYERS)**: Understanding the split between "The Base" and "The Stack."
* **[Security Layers](SECURITY_LAYERS)**: 5-layer Defense-in-Depth visual architecture.
* **[Boot Lifecycle](BOOT_LIFECYCLE)**: Explicit boot sequence and forensic chain of trust.
* **[Network Topology](NETWORK_TOPOLOGY)**: Data flow and network isolation map.
* **[Cross-Runtime Isolation](CROSS_RUNTIME_ISOLATION)**: Securing stacks spanning LXC and Kubernetes.
* **[Combination Matrix](DEPLOYMENT_COMBINATIONS)**: Visual guide to all supported and experimental deployment paths.
* **[Interaction Matrix](CROSS_RUNTIME_MATRIX)**: Network interactions between Podman, K3s, LXC, and QEMU.
* **[Storage Interaction](STORAGE_INTERACTION_MATRIX)**: Filesystem and directory access map for all runtimes.
* **[Forensic Flow](FORENSIC_FLOW)**: Mermaid diagram of the auditable deployment pipeline.
* **[Layered Security](LAYERED_SECURITY)**: How firewalls, access controls, and scanning work together.
* **[Ephemeral Design](EPHEMERAL_DESIGN)**: Logic behind zero-footprint deployments.

### [2. Development](CONTRIBUTING)

* **[Development Tooling](TOOLING)**: Explaining switches (`--low-risk-repair`) and enforcement.
* **[Digest Maintenance](DIGEST_MAINTENANCE)**: Automated image update and system support verification.
* **[Style Guide](STYLE_GUIDE)**: Standards for YAML, Shell, and Ansible.
* **Testing**: Using Molecule for multi-platform idempotency verification.
* **CI**: Verify RHEL-compatible GPG keys (AlmaLinux) using `verify-rhel-compat-keys.yml`.
* **Verify RHEL-compatible GPG keys (AlmaLinux)**: CI test that validates NVIDIA & AMD ROCm repo GPG key checksum/fingerprint verification (workflow: `verify-rhel-compat-keys.yml`). Note: This workflow is manually runnable from the GitHub Actions UI (Actions → Verify RHEL-Compatible (AlmaLinux) GPG Keys → Run workflow).
* **Enforcement**: How `enforce_style_guide.sh` keeps the codebase clean.

### [3. Deployment](EXAMPLES)

* **Solution Stacks**: How to use the Production, Development, and Ephemeral templates.
* **Production Deploy Template**: Use `PRODUCTION_DEPLOY.yml` as the canonical production deployment playbook. Treat `branch_templates/` as reference-only.
* **Variables**: Configuring randomized ports, IP restrictions, and secrets.
* **[Architecture & Vendor Profiles](ARCH_VENDOR_PROFILES)**: Explicit arch/vendor selection to avoid x86-only assumptions.
* **[Hardware Compatibility Matrix](HARDWARE_COMPATIBILITY_MATRIX)**: Supported CPU/GPU combinations and platform tiers.
* **[GPU Interaction Matrix](GPU_INTERACTION_MATRIX)**: Behavior in VM, Container, and Hybrid environments.
* **[OS Configuration](OS_CONFIGURATION)**: The "Single Source of Truth" for fleet-wide OS settings.
* **[GPU Stack Setup](GPU_STACK_SETUP)**: Detailed guide for installing unified GPU drivers and compute stacks.
* **[Container Runtime Guide](CONTAINER_RUNTIME)**: Default Podman capabilities and runtime security settings.
* **[Universal Deployment Guide](UNIVERSAL_DEPLOYMENT_GUIDE)**: Master SOP for replicable system deployment.
* **[Contabo Media Profile](CONTABO_MEDIA_PROFILE)**: Specifications for the VPS 30 SSD Media Stack.
* **[SSH Transfer Profile](SSH_TRANSFER_PROFILE)**: Standard SSH transfer method and fallbacks.
* **[SSH Incident Postmortem](SSH_INCIDENT_POSTMORTEM)**: Root cause analysis and resolution timeline.
* **[SSH Idempotence Guardrails](SSH_IDEMPOTENCE_GUARDRAILS)**: Deterministic SSH configuration and anti-drift rules.
* **[Hybrid Security Setup](SECURITY_CROWDSEC_HYBRID)**: Implementation details for the Container+Host CrowdSec architecture.
* **[Supply-Chain Hardening](SUPPLY_CHAIN_HARDENING)**: Configuration guide for strict GPG/Checksum verification of third-party repositories.
* **[SOPS Migration Guide](SOPS_MIGRATION_GUIDE)**: Staged migration workflow from Vault to SOPS + Age with rollback gates.
* **[SOPS Key Rotation SOP](SOPS_KEY_ROTATION_SOP)**: Operational key and secrets rotation cadence, emergency procedure, and audit checklist.
* **[Deployment Status](DEPLOYMENT_STATUS)**: Current system readiness and implementation status.
* **[Architecture Migration](ARCHITECTURE_MIGRATION_GUIDE)**: Guide for upgrading to the multi-arch standard.
* **Potential Problems**: [Issues to consider when deploying profile combinations](POTENTIAL_PROBLEMS).

### [3a. Kubernetes & Helm](KUBERNETES)

* **[Ingress Controller Setup](INGRESS_CONTROLLER_SETUP)**: Caddy, Traefik, and Nginx ingress configuration.
* **[Helm Charts](index)**: Deployable Helm charts for:
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
* **K8s Deployment**: Use `playbooks/DEPLOY_KUBERNETES.YML` to deploy the full stack on K3s
* **Benchmark**: [K8s vs Podman methodology](k8s_vs_podman_methodology) for resource comparison.

### [4. GPU Slicing](GPU_SLICING)

* **GPU Support**: NVIDIA, AMD, and Intel GPU configuration
* **Slicing Strategies**: MIG, SR-IOV, time-slicing, and passthrough
* **Container Integration**: Kubernetes, LXC, and Podman with GPU acceleration
* **Branch Templates**: GPU-specific deployment configurations

### [5. Security & Forensics](SECURITY_AUDIT_REPORT)

* **[Security Audit Report](SECURITY_AUDIT_REPORT)**: Comprehensive security assessment and role analysis.
* **[Threat Model](THREAT_MODEL)**: STRIDE analysis and residual risk assessment.
* **[Forensic Standards](FORENSIC_STANDARDS)**: Mandatory task naming and Audit Event Identifier convention.
* **[Audit Event Identifier Catalog](DSU_AUDIT_EVENT_IDENTIFIERS)**: 480+ forensic audit codes mapped to ISO standards.
* **[Forensic Restoration Runbook](RESTORE_RUNBOOK)**: Step-by-step guide for ISO 27040 data restoration.

### [6. Planning](SUMMARY)

* **[Planning Summary](SUMMARY)**: Overview of all planning documents.
* **[Migration Strategy](MIGRATION_STRATEGY)**: Strategy for legacy data migration and credential rotation.
* **[Restructuring Plan 2026](RESTRUCTURING_PLAN_2026)**: Strategic plan for project restructuring including community enhancements.
* **[Community Enhancement Plan](COMMUNITY_ENHANCEMENT_PLAN)**: Plan to address community engagement deficits identified through analysis.
* **[Wiki Improvement Plan](WIKI_IMPROVEMENT_PLAN)**: Plan to address wiki content deficits, particularly overly long pages.
* **[GPU Plan](GPU_ENHANCED_PLAN)**: Planning document for GPU enhancements.
* **[Data Mapping](DATA_MAPPING)**: Detailed file lifecycle mapping for the migration process.

---

## 📚 Documentation Integration

For guidance on navigating between the main project documentation and the GitHub wiki, see the **[Documentation Bridge](DOCUMENTATION_BRIDGE)**.

## 🤖 LLM & RAG Support

For AI assistants and RAG systems, see the **[LLM Map](LLM_MAP)** for high-density context loading.
Knowledge base research can be found in the sibling `LLM_RESEARCH` directory.
