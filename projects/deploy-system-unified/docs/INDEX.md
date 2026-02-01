# Deploy-System-Unified Documentation
Welcome to the documentation for **Deploy-System-Unified**, a modular, security-first infrastructure deployment system built on Ansible.

## 📖 Philosophical Foundation
This project is built on a core architectural principle:
> **"Complexity is not a problem, but comingling tasks is."**

Every role, task, and playbook is designed to be granular, single-purpose, and explicit.
## 📂 Documentation Map

### [1. Architecture](./architecture/README.md)
*   **[Core Philosophy](./architecture/NON_COMINGLING.md)**: Why we avoid comingled tasks.
*   **[Virtual Networking](./architecture/VIRTUAL_NETWORKING.md)**: VLANs, VXLANs, and L2/L3 isolation.
*   **[Backup Strategy](./architecture/BACKUP_STRATEGY.md)**: rclone, restic, and system snapshots.
*   **Modular Layers**: Understanding the split between "The Base" and "The Stack."
*   **Layered Security**: How firewalls, access controls, and scanning work together.
*   **Ephemeral Design**: Logic behind zero-footprint deployments.
### [2. Development](./development/CONTRIBUTING.md)
*   **[Development Tooling](./development/TOOLING.md)**: Explaining switches (`--low-risk-repair`) and enforcement.
*   **[Style Guide](./development/STYLE_GUIDE.md)**: Standards for YAML, Shell, and Ansible.
*   **Testing**: Using Molecule for multi-platform idempotency verification.
*   **Enforcement**: How `enforce_style_guide.sh` keeps the codebase clean.

### [3. Deployment](./deployment/EXAMPLES.md)
*   **Solution Stacks**: How to use the Production, Development, and Ephemeral templates.
*   **Variables**: Configuring randomized ports, IP restrictions, and secrets.

### [4. GPU Slicing](./gpu_slicing_setup.md)
*   **GPU Support**: NVIDIA, AMD, and Intel GPU configuration
*   **Slicing Strategies**: MIG, SR-IOV, time-slicing, and passthrough
*   **Container Integration**: Kubernetes, LXC, and Podman with GPU acceleration
*   **Branch Templates**: GPU-specific deployment configurations

---

## 🤖 LLM & RAG Support
For AI assistants and RAG systems, see the **[LLM Map](./LLM_MAP.md)** for high-density context loading.
Knowledge base research can be found in the sibling `LLM_RESEARCH` directory.

