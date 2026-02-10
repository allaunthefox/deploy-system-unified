# Documentation_Index

Welcome to the documentation for **Deploy-System-Unified**, a modular, security-first infrastructure deployment system built on Ansible.

## 📖 Philosophical Foundation

This project is built on a core architectural principle:
> **"Complexity is not a problem, but comingling tasks is."**

Every role, task, and playbook is designed to be granular, single-purpose, and explicit.

## 📂 Documentation Map

### 🏛️ Architecture

* **[Modular Layers](MODULAR_LAYERS)**: Understanding the split between "The Base" and "The Stack."
* **[Ontology & Profiles](ONTOLOGY)**: The formal relationship between profiles and infrastructure.
* **[Core Philosophy](NON_COMINGLING)**: Why we avoid comingled tasks.
* **[Layered Security](LAYERED_SECURITY)**: How firewalls, access controls, and scanning work together.
* **[Virtual Networking](VIRTUAL_NETWORKING)**: VLANs, VXLANs, and L2/L3 isolation.
* **[Backup Strategy](BACKUP_STRATEGY)**: rclone, restic, and system snapshots.
* **[GPU Slicing Architecture](GPU_SLICING)**: Architectural overview of GPU slicing implementation.
* **[Ephemeral Design](EPHEMERAL_DESIGN)**: Logic behind zero-footprint deployments.

### 💻 Development

* **[Development Tooling](TOOLING)**: Explaining switches (`--low-risk-repair`) and enforcement.
* **[Style Guide](STYLE_GUIDE)**: Standards for YAML, Shell, and Ansible.
* **[Pre-commit Hooks](PRE_COMMIT)**: Installing and using local enforcement.
* **[LLM Context Map](LLM_MAP)**: High-density context for AI assistants.
* **[Contributing](CONTRIBUTING)**: Guidelines for contributing to the project.

### 🚀 Deployment

* **[Universal Deployment Guide](UNIVERSAL_DEPLOYMENT_GUIDE)**: Master SOP for replicable system deployment.
* **[Deployment Status](DEPLOYMENT_STATUS)**: Current system readiness and implementation status.
* **[OS Configuration](OS_CONFIGURATION)**: The "Single Source of Truth" for fleet-wide OS settings.
* **[SSH Idempotence Guardrails](SSH_IDEMPOTENCE_GUARDRAILS)**: Deterministic SSH configuration and anti-drift rules.
* **[Hardware Compatibility Matrix](HARDWARE_COMPATIBILITY_MATRIX)**: Supported CPU/GPU combinations and platform tiers.
* **[GPU Interaction Matrix](GPU_INTERACTION_MATRIX)**: Behavior in VM, Container, and Hybrid environments.
* **[GPU Stack Setup](GPU_STACK_SETUP)**: Detailed guide for installing unified GPU drivers and compute stacks.
* **[Architecture & Vendor Profiles](ARCH_VENDOR_PROFILES)**: Explicit arch/vendor selection to avoid x86-only assumptions.
* **[Hybrid Security Setup](SECURITY_CROWDSEC_HYBRID)**: Implementation details for the Container+Host CrowdSec architecture.
* **[Supply-Chain Hardening](SUPPLY_CHAIN_HARDENING)**: Configuration guide for strict GPG/Checksum verification.
* **[EXAMPLES](EXAMPLES)**: Solution stack examples.

### 📅 Planning

* **[Stability Plan 2026](STABILITY_EXECUTION_PLAN_2026)**: Phase 1 accomplishments and Phase 2 objectives.
* **[Migration Plan](MIGRATION_PLAN)**: Legacy data migration and credential rotation.
* **[Restructuring Plan](RESTRUCTURING_PLAN_2026)**: Strategic plan for project restructuring.
* **[GPU Enhanced Plan](GPU_ENHANCED_PLAN)**: Detailed planning for GPU enhancements.

### 🔒 Security

* **[Security Audit Report](SECURITY_AUDIT_REPORT)**: Comprehensive security assessment and role analysis.