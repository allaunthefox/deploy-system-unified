# Home

**Status:** ✅ **CERTIFIED 100/100 COMPLIANCE** (ISO 27001, ISO 27040, NIST SP 800-193)

Deploy-System-Unified (DSU) is an industry-leading, audit-ready infrastructure-as-code framework designed for high-security and mission-critical environments.

## 🚀 Key Capabilities (Feb 2026)

- **Automated Recovery Verification**: ISO 27040 periodic verified restores into isolated namespaces.
- **Security Observability**: Real-time Loki/Grafana audit streams mapped to 350+ Audit Event Identifiers.
- **Post-Quantum Cryptography**: Hybrid ML-KEM and sntrup761 support for SSH and secret archival.
- **Supply Chain Hardening**: Signed CycloneDX SBOM generation and Cosign image verification.
- **Multi-Architecture**: Native support for x86_64, aarch64, and riscv64.
- **Profile-Aware Governance**: Automated safety guards for Ephemeral, Hardened, and Production environments.

## 📖 Navigation

- **[Documentation Index](Documentation_Index)**: The master map of all available guides.
- **[Role Reference](Role_Reference)**: Systematic breakdown of every Ansible role.
- **[Variable Reference](Variable_Reference)**: Definitive dictionary of all configuration variables.
- **[Ontology & Profiles](ONTOLOGY)**: Understanding the security and infrastructure framework.
- **[Deployment Status](DEPLOYMENT_STATUS)**: Current system readiness and compliance certification.

## 🚀 Quick Start

To deploy the canonical production solution:
```bash
ansible-playbook production_deploy.yml -i inventory/your_inventory.ini
```

See the **[Universal SOP](UNIVERSAL_DEPLOYMENT_GUIDE)** for step-by-step instructions.

---

**Audit Mode:** To run a compliance-only check without changes:
```bash
ansible-playbook production_deploy.yml --tags audit
```
