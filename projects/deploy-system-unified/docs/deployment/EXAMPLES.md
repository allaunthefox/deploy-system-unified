# Deployment Examples

This document provides practical examples for deploying various Solution Stacks using the modular architecture.

## 🚀 1. Production Container Host

Best for stable, long-running servers where security and log integrity are paramount.

### Configuration (`host_vars/prod-server.yml`)

```yaml
system_ssh_port: 2222
ssh_key_rotation_enabled: true

# Granular Firewall Rules
firewall_additional_rules:
  - { port: 2222, src: "10.0.50.0/24", comment: "Admin Subnet Only" }
```

### Execution

```bash
ansible-playbook -i inventory.ini branch_templates/production_servers.yml
```

---

## ⚡ 2. Ephemeral Security Sandbox

Best for CI/CD runners or temporary testing environments. Secrets vanish on reboot.

### Key Features

- **Volatile Secrets**: Stored in a 64MB RAM-disk.
- **Audit Trail**: Every deployment creates a hashed `DEPLOY_ID` in system logs.
- **Zero Footprint**: Controller shreds connection artifacts after the run.

### Execution

```bash
ansible-playbook -i inventory.ini branch_templates/ephemeral_containers.yml
```

---

## 🛠 3. Custom User Restrictions

Example of using the L7 Access layer to restrict specific users.

### Configuration

```yaml
ssh_match_rules:
  - type: User
    name: "deploy-bot"
    address: "192.168.1.50"
    options:
      - "AllowTcpForwarding no"
      - "X11Forwarding no"
```

## 📋 Common Operational Flags

When maintaining the codebase, use the optimized enforcement tool:

```bash
# Safely fix formatting (trailing spaces, newlines)
bash dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --low-risk-repair
# Perform structural fixes (file renaming)
bash dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --fix
```
