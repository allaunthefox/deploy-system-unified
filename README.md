# Workspaces — Quick Overview & Guide 📁

[![Style Enforcement](https://img.shields.io/github/actions/workflow/status/allaunthefox/deploy-system-unified/style-enforcement.yml?branch=main)](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/style-enforcement.yml) [![Detect Secrets](https://img.shields.io/github/actions/workflow/status/allaunthefox/deploy-system-unified/detect-secrets.yml?branch=main)](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/detect-secrets.yml) [![License](https://img.shields.io/github/license/allaunthefox/deploy-system-unified)](https://github.com/allaunthefox/deploy-system-unified/blob/main/LICENSE) [![Wiki Lint](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/wiki-lint.yml/badge.svg)](https://github.com/allaunthefox/deploy-system-unified/actions/workflows/wiki-lint.yml)

This workspace holds multiple active projects, research, and tooling used across development. The README is organized for quick scanning with deeper links for details.

---

## At a glance ✨

- Root purpose: central repository of projects, tooling, and LLM research notes.  
- Key project: `projects/deploy-system-unified/` — production-focused Ansible base for container infrastructure.  
- CI & tooling: style enforcement, secret scanning, and helper scripts live under `projects/*/dev_tools` and `.github/workflows`.

---

## Top-level structure 🔍

- `projects/` — Project folders
  - `projects/deploy-system-unified/` — Deploy-System-Unified project (Ansible playbooks, roles, templates)
- `Offline_Research/` — Offline research and documentation
  - `Offline_Research/LLM_RESEARCH/` — Style guides, research notes, and documentation for LLM-driven docs and processes
- `ansiblelint/` — Custom Ansible Lint rules and tests (now inside deploy-system-unified)
- `dev_tools/` — Shared helper scripts, enforcement tools, and utilities used across projects (now inside deploy-system-unified)

---

## Notable project: Deploy-System-Unified 🚀
Path: `projects/deploy-system-unified/`

Short summary:
- Production-ready base for container infrastructure (Podman + quadlets, Caddy, secure SSH).  
- Provides `branch_templates/` for deployment variants (production, development, ephemeral).  
- Main playbook: `main.yml` (kept pristine; CI enforces no top-level `roles:` in main).  

Quick files to check:
- `main.yml` — pristine base playbook
- `branch_templates/` — templates to copy and customize for a deployment
- `roles/` — reusable Ansible roles
- `dev_tools/tools/style-guide-enforcement/` — enforcement script and reporting
- `.github/workflows/` — CI checks (style, detect-secrets)

---

## Quick start (2 commands) ▶️

1) Generate a style compliance report (no changes):

```bash
bash projects/deploy-system-unified/dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --report
```

2) Run detect-secrets locally:

```bash
pip install detect-secrets
detect-secrets scan projects/deploy-system-unified --all-files
```

---

## Contributing & support 🤝

- See `projects/deploy-system-unified/CONTRIBUTING.md` for contribution rules and branch template guidance.
- For security concerns (potential secrets), open an issue and tag `security`. We already run `detect-secrets` in CI.

---

## Contacts / Maintainers
- Repo owner: `@allaunthefox`
- For quick questions: open an issue in the relevant project folder

---

If you'd like, I can add CI badges to this README, include a minimal example inventory + `site.yml` quick-start, or extract a one-line TL;DR summary for console output. Which would you prefer? (badges / example / tl;dr / none)