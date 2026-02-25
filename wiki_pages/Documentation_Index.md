# Documentation Index

Welcome to the **Deploy-System-Unified (DSU)** Knowledge Base. This repository contains the complete technical specifications and operational guides for our high-resilience, security-first infrastructure.

---

## 🏛️ 1. Architecture & Philosophy
The core logic and design patterns governing the project.

*   **[Modular Layers](MODULAR_LAYERS)**: The 7-layer defense-in-depth model.
*   **[Ontology & Profiles](ONTOLOGY)**: Formal mapping of security postures to hardware.
*   **[Core Philosophy](NON_COMINGLING)**: The "Anti-Comingling" rule for task modularity.
*   **[High-Resilience Plan](Plan_HIGH_RESILIENCE_PLAN_2026)**: The project's security roadmap and HRoT mandate.
*   **[Volatile Design](EPHEMERAL_DESIGN)**: Zero-footprint and RAM-disk secret infrastructure.
*   **[Layered Security](LAYERED_SECURITY)**: Coordination between firewall, MAC, and kernel hardening.
*   **Architecture Guides**: [x86](Arch_X86) | [ARM64](Arch_ARM64) | [RISC-V](Arch_RISCV64)

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
*   **[Vendor Profiles](Arch_Vendor_Profiles)**: Explicit hardware selection parameters.

---

## 💻 5. Development & Quality
Tools and standards for contributing to DSU.

*   **[Development Tooling](TOOLING)**: Usage guide for style enforcement and repair tools.
*   **[Style Guide Overview](STYLE_GUIDE)**: Standards for [YAML](Dev_Style_YAML_Style_Guide), [Ansible](Dev_Style_Ansible_Style_Guide), [Shell](Dev_Style_Shell_Style_Guide), and [Docs](Dev_Style_Documentation_Style_Guide).
*   **[Pre-commit Hooks](PRE_COMMIT)**: Local linting and secret detection setup.
*   **[Testing Framework](Testing_Negative_IMPLEMENTATION)**: Comprehensive guide to [Negative Testing](Testing_Negative_IMPLEMENTATION) and [Idempotency Verification](Quality_Idempotency_BLOCKERS).
*   **[LLM Context Map](LLM_MAP)**: Technical grounding for AI-assisted engineering.
*   **[Wiki Improvement Plan](../docs/planning/WIKI_IMPROVEMENT_PLAN.md)**: Plan to address wiki content deficits.

---

## 📊 6. Reference Library
Technical lookup for roles and variables.

*   **[Role Reference](Role_Reference)**: Master list of all 81+ Ansible roles.
*   **[Variable Reference](Variable_Reference)**: Global and role-specific variable definitions.
*   **[Action Code Catalog](DSU_ACTION_CODES_COMPLETE)**: 480+ forensic audit codes mapped to ISO standards.

---

## 📅 7. Planning & Archive
Future directions and historical implementation phases.

*   **[Release Cycles](RELEASE_CYCLES)**: v1.x and v2.0 roadmap.
*   **[Stability Plan](Plan_STABILITY_PLAN)**: Focus on 100% idempotence and reliability.
*   **Planning Archive**:
    *   [Stability Execution 2026](Plan_STABILITY_EXECUTION_PLAN_2026)
    *   [Security Enhancement 2026](Plan_SECURITY_ENHANCEMENT_PLAN_2026)
    *   [Role Enhancement 2026](Plan_ROLE_ENHANCEMENT_EXECUTION_PLAN_2026)
    *   [Community Enhancement](Plan_COMMUNITY_ENHANCEMENT_PLAN)
    *   [Compliance Framework Integration](Plan_COMPLIANCE_FRAMEWORK_INTEGRATION_PLAN)
    *   [Architecture Migration Guide](Arch_Migration_Guide)
    *   [Determinism Roadmap](Plan_DETERMINISM_ROADMAP)

---

### 📚 Documentation Integration

For guidance on navigating between the GitHub wiki and the main project documentation, see the **[Documentation Bridge](../docs/DOCUMENTATION_BRIDGE.md)**.
