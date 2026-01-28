# Workspaces Directory

This directory contains all development projects organized by project.

## Structure

- `projects/` - Contains individual project directories
  - `deploy-system-unified/` - The Deploy-System-Unified project with Ansible playbooks and branch templates

## Projects

### Deploy-System-Unified
Located at `projects/deploy-system-unified/`

A system for setting up production-ready container infrastructure with one command. Features secure SSH configuration, Podman container management, and Caddy reverse proxy with automatic HTTPS.

Contains:
- `main.yml` - The main playbook with clean, stable configuration for the main branch
- `branch_templates/` - Specialized templates for different deployment scenarios
- Documentation files (README.md, CONTRIBUTING.md)