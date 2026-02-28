# Documentation Index

Welcome to the **Deploy-System-Unified (DSU)** Knowledge Base. This repository contains the complete technical specifications and operational guides for our high-resilience, security-first infrastructure.

---

## 🏛️ 1. Architecture & Philosophy
The core logic and design patterns governing the project.

*   **[Terminology](TERMINOLOGY)**: Formal definitions with ISO/NIST citations for every term.
*   **[Ontology & Profiles](ONTOLOGY)**: Formal mapping of security postures to hardware.
*   **[Modular Layers](MODULAR_LAYERS)**: The 7-layer defense-in-depth model.
*   **[Core Philosophy](SEPARATION_OF_CONCERNS)**: Separation of Concerns (SoC) — the foundational rule for task modularity.
*   **[High-Resilience Plan](PLAN_HIGH_RESILIENCE_PLAN_2026)**: The project's security roadmap and HRoT mandate.
*   **[Volatile Design](EPHEMERAL_DESIGN)**: Zero-footprint and RAM-disk secret infrastructure (Ephemeral Credentials).
*   **[Layered Security](LAYERED_SECURITY)**: Coordination between firewall, MAC, and kernel hardening.
*   **Architecture Guides**: [x86](ARCH_X86) | [ARM64](ARCH_ARM64) | [RISC-V](ARCH_RISCV64)

---

## 🚀 2. Operations & Deployment
How to deploy and maintain DSU environments.

*   **[Universal Deployment Guide](UNIVERSAL_DEPLOYMENT_GUIDE)**: The master SOP for all production runs.
*   **[Quick Reference](QUICK_REFERENCE)**: Common commands and "cheat sheet" for operators.
*   **[Deployment Status](DEPLOYMENT_STATUS)**: Current implementation readiness and compliance scores.
*   **[OS Configuration](OS_CONFIGURATION)**: Fleet-wide "Single Source of Truth" settings.
*   **[Restore Runbook](RESTORE_RUNBOOK)**: Disaster recovery and autonomic restore procedures.
*   **[SOPS Migration Guide](SOPS_MIGRATION_GUIDE)**: Transitioning from Vault to SOPS/Age encryption.

---

## 🛡️ 3. Security & Compliance
Formal standards and hardening specifications.

*   **[ISO Tagging Standard](ISO_TAGGING_STANDARD)**: Mapping tasks to ISO 27001, NIST, and CIS.
*   **[Compliance Gap Analysis](COMPLIANCE_GAP_ANALYSIS)**: Current status of control remediation.
*   **[Supply-Chain Hardening](SUPPLY_CHAIN_HARDENING)**: GPG, Checksums, and Cosign enforcement.
*   **[Hybrid Security Setup](SECURITY_CROWDSEC_HYBRID)**: Integrating container agents with host firewalls.
*   **[Standardized Auditing](ROLE_IMPLEMENTATION_STANDARDS_REVIEW)**: Detailed comparison vs. industry benchmarks.

---

## 🔌 4. Hardware & Acceleration
Optimizing for specific architectures and GPUs.

*   **[GPU Stack Setup](GPU_STACK_SETUP)**: Unified driver installation and compute readiness.
*   **[Intel GPU Guide](INTEL_GPU_GUIDE)**: Detailed Intel-specific configuration and Battlemage setup.
*   **[GPU Slicing Architecture](GPU_SLICING)**: Implementation of MIG, SR-IOV, and Time-Slicing.
*   **[Hardware Compatibility Matrix](HARDWARE_COMPATIBILITY_MATRIX)**: Validated CPU/GPU combinations.
*   **[Vendor Profiles](ARCH_VENDOR_PROFILES)**: Explicit hardware selection parameters.

---

## 💻 5. Development & Quality
Tools and standards for contributing to DSU.

*   **[Documentation Style Guide](DOCUMENTATION_STYLE_GUIDE)**: Standards for all project documentation.
*   **[Naming Convention Standard](NAMING_CONVENTION_STANDARD)**: SCREAMING_SNAKE_CASE file naming standard.
*   **[Ansible Style Guide](ANSIBLE_STYLE_GUIDE)**: Task naming, lint rules, and role structure.
*   **[Style Guide Overview](STYLE_GUIDE)**: Standards for [YAML](DEV_STYLE_YAML_STYLE_GUIDE), [Ansible](DEV_STYLE_ANSIBLE_STYLE_GUIDE), [Shell](DEV_STYLE_SHELL_STYLE_GUIDE), and [Docs](DEV_STYLE_DOCUMENTATION_STYLE_GUIDE).
*   **[Development Tooling](TOOLING)**: Usage guide for style enforcement and repair tools.
*   **[Pre-commit Hooks](PRE_COMMIT)**: Local linting and secret detection setup.
*   **[Testing Framework](TESTING_NEGATIVE_IMPLEMENTATION)**: Comprehensive guide to [Negative Testing](TESTING_NEGATIVE_IMPLEMENTATION) and [Idempotency Verification](QUALITY_IDEMPOTENCY_BLOCKERS).
*   **[LLM Context Map](LLM_MAP)**: Technical grounding for AI-assisted engineering.
*   **[Wiki Improvement Plan](../docs/planning/WIKI_IMPROVEMENT_PLAN.md)**: Plan to address wiki content deficits.

---

## 📊 6. Reference Library
Technical lookup for roles and variables.

*   **[Role Reference](ROLE_REFERENCE)**: Master list of all 81+ Ansible roles.
*   **[Variable Reference](VARIABLE_REFERENCE)**: Global and role-specific variable definitions.
*   **[Audit Event Identifier Catalog](DSU_AUDIT_EVENT_IDENTIFIERS)**: 480+ forensic audit codes mapped to ISO standards.

---

## 📅 7. Planning & Archive
Future directions and historical implementation phases.

*   **[Release Cycles](RELEASE_CYCLES)**: v1.x and v2.0 roadmap.
*   **[Stability Plan](PLAN_STABILITY_PLAN)**: Focus on 100% idempotence and reliability.
*   **Planning Archive**:
    *   [Stability Execution 2026](PLAN_STABILITY_EXECUTION_PLAN_2026)
    *   [Security Enhancement 2026](PLAN_SECURITY_ENHANCEMENT_PLAN_2026)
    *   [Role Enhancement 2026](PLAN_ROLE_ENHANCEMENT_EXECUTION_PLAN_2026)
    *   [Community Enhancement](PLAN_COMMUNITY_ENHANCEMENT_PLAN)
    *   [Compliance Framework Integration](PLAN_COMPLIANCE_FRAMEWORK_INTEGRATION_PLAN)
    *   [Architecture Migration Guide](ARCH_MIGRATION_GUIDE)
    *   [Determinism Roadmap](PLAN_DETERMINISM_ROADMAP)

---

### 📚 Documentation Integration

For guidance on navigating between the GitHub wiki and the main project documentation, see the **[Documentation Bridge](../docs/DOCUMENTATION_BRIDGE.md)**.
