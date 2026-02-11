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
* **[x86 Architecture Guide](ARCH_GUIDE_X86)**: Specific considerations for x86_64 deployments.
* **[ARM64 Architecture Guide](ARCH_GUIDE_ARM64)**: Optimizing for ARM64 (SBCs, Cloud, etc.).
* **[RISC-V Architecture Guide](ARCH_GUIDE_RISCV64)**: Emerging support for RISC-V platforms.

### 💻 Development

* **[Development Tooling](TOOLING)**: Explaining switches (`--low-risk-repair`) and enforcement.
* **[Style Guide](STYLE_GUIDE)**: Standards for YAML, Shell, and Ansible.
* **[Pre-commit Hooks](PRE_COMMIT)**: Installing and using local enforcement.
* **[LLM Context Map](LLM_MAP)**: High-density context for AI assistants.
* **[Contributing](CONTRIBUTING)**: Guidelines for contributing to the project.
* **[Research Guidelines](RESEARCH_GUIDELINES)**: Standards for technical research and documentation.

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
* **[Intel Battlemage Guide](INTEL_BATTLEMAGE_GUIDE)**: Specific setup for modern Intel GPUs.
* **[Intel Video Guide](INTEL_VIDEO_GUIDE)**: Hardware acceleration guide for Intel QuickSync.
* **[EXAMPLES](EXAMPLES)**: Solution stack examples.

#### 🛠 Auxiliary Playbooks
* **`bootstrap_ssh.yml`**: Initial SSH setup for fresh hosts.
* **`fix_ssh.yml`**: Emergency repair for broken SSH configurations.
* **`restore_data.yml`**: Orchestrates data restoration from Restic/Rclone backups.
* **`preflight_diagnose.yml`**: Deep diagnostic suite for system readiness issues.

### 🤖 CI/CD & Automation

* **[CI/CD Workflows](CI_CD_WORKFLOWS)**: Overview of GitHub Actions and automated enforcement.
* **[Negative Testing Implementation](NEGATIVE_TESTING_IMPLEMENTATION)**: How we verify security failure modes.

### 📋 Planning & Improvement

* **[Wiki Improvement Plan](../projects/deploy-system-unified/docs/planning/WIKI_IMPROVEMENT_PLAN)**: Plan to address wiki content deficits, particularly overly long pages.
* **[Community Enhancement Plan](../projects/deploy-system-unified/docs/planning/COMMUNITY_ENHANCEMENT_PLAN)**: Plan to address community engagement deficits identified through analysis.

### 📊 Variable References

* **[Variable Reference Overview](Variable_Reference)**: High-level overview of project variables
* **[Variable Reference: Containers](Variable_Reference_Containers)**: Variables for container-related roles
* **[Variable Reference: Core](Variable_Reference_Core)**: Variables for core system roles
* **[Variable Reference: Security](Variable_Reference_Security)**: Variables for security-related roles
* **[Variable Reference: Networking](Variable_Reference_Networking)**: Variables for networking roles
* **[Variable Reference: Storage](Variable_Reference_Storage)**: Variables for storage roles

### 📝 Style Guides

* **[Style Guide Overview](STYLE_GUIDE)**: High-level overview of project style requirements
* **[YAML Style Guide](YAML_Style_Guide)**: Standards for YAML files
* **[Ansible Style Guide](Ansible_Style_Guide)**: Best practices for Ansible content
* **[Shell Style Guide](Shell_Style_Guide)**: Requirements for shell scripts
* **[Documentation Style Guide](Documentation_Style_Guide)**: Guidelines for documentation

### 📚 Documentation Integration

For guidance on navigating between the GitHub wiki and the main project documentation, see the **[Documentation Bridge](../projects/deploy-system-unified/docs/DOCUMENTATION_BRIDGE.md)**.