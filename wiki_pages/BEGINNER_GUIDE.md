# BEGINNER_GUIDE

Welcome to Deploy-System-Unified! This guide will help you get started with the project.

## What is This Project?

Deploy-System-Unified is an **Ansible-based deployment system** that helps you set up and manage:
- Container runtimes (Podman, Docker)
- Kubernetes clusters (K3s)
- GPU acceleration (NVIDIA, AMD, Intel)
- Security hardening
- Media servers
- Networking services

## Quick Start

### 1. Prerequisites

```bash
# Install Ansible
pip install ansible

# Clone the repository
git clone https://github.com/your-repo/deploy-system-unified.git
cd deploy-system-unified

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Your Inventory

Edit `inventory/` files to define your servers:

```yaml
# inventory/hosts.yml
all:
  children:
    production:
      hosts:
        server1:
          ansible_host: 192.168.1.10
```

### 3. Run a Simple Deployment

```bash
# Test connection
ansible all -i inventory/ -m ping

# Run deployment
ansible-playbook -i inventory/production production_deploy.yml
```

## Understanding the Structure

```
deploy-system-unified/
├── playbooks/          # Main deployment playbooks
├── roles/              # Reusable Ansible roles
├── inventory/          # Server configurations
├── branch_templates/   # Pre-configured deployment templates
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## Key Concepts

### Roles

Roles are reusable sets of tasks. Main categories:
- **core** - Bootloader, system setup
- **containers** - Podman/Docker management
- **security** - Firewall, hardening
- **hardware** - GPU drivers
- **networking** - VPNs, proxies

### Profiles

The system uses deployment profiles:
- `bare_metal` - Physical servers
- `virtual_host` - VM hosts
- `virtual_guest` - Virtual machines
- `ephemeral` - Temporary containers

### Variables

Configuration is done through variables:
- `group_vars/` - Group-wide settings
- `host_vars/` - Per-server settings
- `defaults/main.yml` - Role defaults

## Common Tasks

### Enable GPU Support

```yaml
# group_vars/all.yml
gpu_stack_enable: true
gpu_stack_vendor: nvidia  # or amd, intel
```

### Enable Containers

```yaml
# group_vars/all.yml
containers_enable: true
containers_podman_enable: true
```

### Configure Networking

```yaml
# group_vars/all.yml
networking_firewall_enable: true
networking_vpn_enable: false
```

## Troubleshooting

### Check What's Running

```bash
ansible-playbook -i inventory/production --list-tasks
```

### Verbose Output

```bash
ansible-playbook -i inventory/production production_deploy.yml -v
```

### Skip Specific Tasks

```bash
ansible-playbook -i inventory/production production_deploy.yml --skip-tags=firewall
```

## Next Steps

- Read [Universal Deployment Guide](UNIVERSAL_DEPLOYMENT_GUIDE)
- Check [Variable Reference](Variable_Reference)
- Review [Role Reference](Role_Reference)
- See [Quick Reference](QUICK_REFERENCE) for common commands

## Getting Help

- Check [Troubleshooting](POTENTIAL_PROBLEMS)
- Review [Idempotency Blockers](Quality_Idempotency_BLOCKERS)
- Ask in community channels
