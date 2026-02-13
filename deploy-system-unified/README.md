# Deploy-System-Unified

Modular, security-first infrastructure deployment.

## 📖 Documentation

**The primary documentation hub is our [GitHub Wiki](https://github.com/allaunthefox/deploy-system-unified/wiki).**

For local file-based access, see the [**Documentation Index**](./docs/INDEX.md).

## 🚀 Quick Start

1. **Production Deployment**: Use the canonical entrypoint:
   ```bash
   ansible-playbook production_deploy.yml -i inventory/your_inventory.ini
   ```
2. **Architecture Support**: This project is now architecture-aware (x86_64, aarch64, riscv64). Core roles and GPU drivers adapt automatically to the target architecture.
3. **Reference Templates**: Standard architecture patterns are available in `branch_templates/` (categorized by architecture) for reference only.

**Pre-commit & local checks:** See [docs/development/PRE_COMMIT.md](./docs/development/PRE_COMMIT.md) for instructions on installing `pre-commit` and running the repository enforcement locally.
