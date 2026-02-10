# Home

Modular, security-first infrastructure deployment. This wiki serves as the comprehensive knowledge base for the project architecture, development standards, and deployment procedures.

## 📖 Navigation

- **[Documentation Index](Documentation_Index)**: The master map of all available guides.
- **[Role Reference](Role_Reference)**: Systematic breakdown of every Ansible role.
- **[Variable Reference](Variable_Reference)**: Definitive dictionary of all configuration variables.
- **[Ontology & Profiles](ONTOLOGY)**: Understanding the security and infrastructure framework.

## 🚀 Quick Start

To deploy the canonical production solution:
```bash
ansible-playbook production_deploy.yml -i inventory/your_inventory.ini
```

See the **[Universal SOP](UNIVERSAL_DEPLOYMENT_GUIDE)** for step-by-step instructions.

---

**Pre-commit & local checks:** See the **[Pre-commit Guide](PRE_COMMIT)** for instructions on installing local enforcement tools.