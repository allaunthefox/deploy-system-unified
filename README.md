# Workspaces Directory 📁

This workspace contains active development projects organized under `projects/`.

## Structure 🔧

- `projects/` — Individual project directories
  - `projects/deploy-system-unified/` — Deploy-System-Unified project (Ansible playbooks, roles, templates)

## Projects ✨

### Deploy-System-Unified
**Path:** `projects/deploy-system-unified/`

A production-oriented base for creating container-focused infrastructure deployments with opinionated, secure defaults. Key highlights:

- Secure SSH configuration and hardened defaults
- Podman container management with `quadlets`
- Caddy reverse proxy with automatic HTTPS
- Branch templates for different deployment scenarios (dev, prod, ephemeral)

Files of interest:
- `main.yml` — pristine base playbook (kept minimal; CI enforces main branch invariants)
- `branch_templates/` — copy a template (e.g., `production_servers.yml`) into your deployment and customize
- `roles/` — reusable Ansible roles used by the templates
- `dev_tools/` — helper scripts and CI tooling (style enforcement, secret checks)
- Documentation: `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`

## Quick start ▶️

1. Choose a branch template from `branch_templates/` (for example, `production_servers.yml`).
2. Copy it into your deployment directory as `site.yml` and customize inventory and variables.
3. Run the playbook:

```bash
ansible-playbook -i inventory/your-server.ini site.yml
```

> Tip: The repository includes CI checks for style and secret scanning. See `dev_tools/tools/style-guide-enforcement` and `.github/workflows`.

---

If you want me to expand any project section or add command examples, tell me which part to detail and I’ll update it.