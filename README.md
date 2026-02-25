# Deploy-System-Unified

[![Style Enforcement](https://img.shields.io/github/actions/workflow/status/allaunthefox/deploy-system-unified/style-enforcement.yml?branch=main)](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/style-enforcement.yml)
[![Detect Secrets](https://img.shields.io/github/actions/workflow/status/allaunthefox/deploy-system-unified/detect-secrets.yml?branch=main)](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/detect-secrets.yml)
[![License](https://img.shields.io/github/license/allaunthefox/deploy-system-unified)](https://github.com/allaunthefox/deploy-system-unified/blob/main/LICENSE)
[![Wiki Lint](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/wiki-lint.yml/badge.svg)](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/wiki-lint.yml)

**Modular, security-first infrastructure deployment built on Ansible.**

---

## 🟢 Project Status

> **Base Layer: 100% Complete (Production Ready) ✅**

The core infrastructure and security hardening layers are fully implemented, verified, and production-ready.

- **Core Roles:** 12/12 Complete (100% Idempotence)
- **Security Roles:** 18/18 Complete (5-Layer Defense)
- **Kubernetes Roles:** 4/4 Complete
- **Networking:** 7/7 Complete
- **Containers:** 13/13 Complete
- **Hardware:** 5/5 Complete
- **Virtualization:** 2/2 Complete
- **Ops:** 8/8 Complete
- **Storage:** 3/3 Complete
- **Validation:** Tested on Contabo VPS (Feb 2026)
- **Compliance:** 100/100 (ISO 27001, ISO 27040, NIST SP 800-193, CIS)

👉 **[View Detailed Implementation Status](https://github.com/allaunthefox/deploy-system-unified/wiki/DEPLOYMENT_STATUS)**

---

## 🚀 Quick Start

### 🗺️ Deployment Pathfinder
Choose the path that matches your goal:

| I want to... | Use this Playbook | Recommended Profile |
|:---|:---|:---|
| **Harden a new server** | `base_hardened.yml` | `hardened` |
| **Deploy a Media Stack** | `production_deploy.yml` | `production` (Contabo) |
| **Test in a sandbox** | `site.yml` | `development` |
| **Run a one-off task** | `site.yml --tags <tag>` | `ephemeral` |

### Standard Execution
Use the canonical entrypoint for production deployments:

```bash
ansible-playbook production_deploy.yml -i inventory/your_inventory.ini
```

### Architecture Support

This project is architecture-aware and supports:
- **x86_64** (Intel/AMD)
- **aarch64** (ARM64)
- **riscv64** (RISC-V)

Core roles and GPU drivers adapt automatically to the target architecture.

### Reference Templates

Standard architecture patterns are available in `branch_templates/` for reference. Copy and customize for your deployment variant (production, development, ephemeral).

---

## 📖 Documentation

**Primary documentation hub:** [GitHub Wiki](https://github.com/allaunthefox/deploy-system-unified/wiki)

**Local documentation:** [Documentation Index](./docs/INDEX.md)

### Key Documentation Sections

| Section | Description |
|---------|-------------|
| [Architecture](./docs/architecture/README.md) | Core philosophy, virtual networking, backup strategy |
| [Development](./docs/development/CONTRIBUTING.md) | Contributing guide, style guide, tooling |
| [Deployment](./docs/deployment/EXAMPLES.md) | Solution stacks, vendor profiles, hardware matrix |
| [Planning](./docs/planning/) | Roadmaps, migration plans, stability execution |

---

## 📁 Project Structure

```
Deploy-System-Unified/
├── site.yml                    # Main playbook
├── production_deploy.yml       # Production entrypoint
├── base_hardened.yml           # Base hardening playbook
├── branch_templates/           # Architecture-specific templates
├── roles/                      # Ansible roles (categorized)
│   ├── core/                   # Core system roles
│   ├── containers/             # Container runtime & services
│   ├── hardware/               # Hardware-specific roles
│   ├── networking/             # Network configuration
│   ├── security/               # Security hardening
│   └── ...
├── playbooks/                  # Supporting playbooks
├── inventory/                  # Inventory files
├── docs/                       # Documentation
├── dev_tools/                  # Development tooling
└── molecule/                   # Test scenarios
```

---

## 🔧 Quick Commands

### Style Compliance Report

```bash
bash dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --report
```

### Detect Secrets Scan

```bash
pip install detect-secrets
detect-secrets scan --all-files
```

### Pre-commit Setup

See [docs/development/PRE_COMMIT.md](./docs/development/PRE_COMMIT.md) for local enforcement setup.

---

## 🤝 Contributing & Support

- **Contribution rules:** See [CONTRIBUTING.md](./CONTRIBUTING.md)
- **Security concerns:** See [SECURITY.md](./SECURITY.md) - we run `detect-secrets` in CI
- **Roadmap:** See [docs/planning/ROADMAP.md](./docs/planning/ROADMAP.md)

---

## 🛡️ Compliance & Standards

This project implements a rigorous **forensic traceability** framework linking code execution to compliance requirements.

| Standard | Coverage | Implementation |
|----------|----------|----------------|
| **CIS Benchmark** | Level 1 & 2 (Ubuntu 22.04) | Automated via `cis_level_1` tags |
| **ISO/IEC 27001:2022** | Full Coverage | Mapped via `iso_27001` tags |
| **ISO/IEC 27040:2024** | Storage Security | Automated `restore_test` enabled |
| **NIST SP 800-193** | Platform Firmware | Full compliance |
| **Autonomic Recovery**| **ISO 27040** (Storage) | Automated restore verification |
| **Forensic Intelligence**| **ISO 27001** (§12.4) | Loki-backed `Action Code` dashboards |
| **Forensic Audit** | Full Execution Trace | **350+ Action Codes** linked to specific controls |

**Forensic Traceability:**
Every security-critical task is tagged with its compliance requirement (e.g., `iso_27001_10_1`), enabling bidirectional tracing between:
- **Requirement:** "Implement strong cryptography" (ISO 27001 §10.1)
- **Execution:** Task `Configure SSH protocol` (Action Code `400011`)

---

## 📋 Key Features

- **Security-first**: Default-deny firewall, SOPS/Age secrets, audit integrity
- **Idempotent**: All roles pass idempotence benchmarks (12/12 core roles)
- **Multi-arch**: x86_64, aarch64, riscv64 support
- **Container-native**: Podman quadlets, Caddy reverse proxy
- **Disaster recovery**: Restic/rclone backups, restore runbooks
- **CI/CD**: Style enforcement, secret scanning, wiki linting, license compliance
- **Post-Quantum Security**: Hybrid ML-KEM/Ed25519 SSH, lattice-based secret archival
- **Runtime Security**: Falco-based threat detection
- **Supply Chain**: Cosign image verification, CycloneDX SBOM generation

---

## 📄 License

GPL-3.0 License - see [LICENSE](./LICENSE)

See [LICENSE-COMPLIANCE.md](./LICENSE-COMPLIANCE.md) for dependency license policy.

---

## 👥 Maintainers

- Repo owner: `@allaunthefox`
- For questions: Open an issue in the relevant category
