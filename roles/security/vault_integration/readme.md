# HashiCorp Vault Integration Role

This role provides HashiCorp Vault integration for the deploy-system-unified project.

## Features

- **Standalone Vault Installation**: Install and configure Vault in standalone mode
- **Kubernetes Authentication**: Enable Kubernetes auth method for pod-based authentication
- **Dynamic Secrets**: Support for dynamic database and cloud credentials
- **Vault Agent Injector**: Kubernetes-sidecar injection for automatic secret injection
- **KV Secrets Engine**: KV v2 secrets engine for application secrets

## Requirements

- Ansible 2.15+
- Supported OS: Ubuntu, Debian, Fedora, Archlinux

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `vault_install_mode` | `standalone` | Installation mode: standalone, kubernetes, agent_only |
| `vault_version` | `1.15.0` | Vault version to install |
| `vault_addr` | `http://127.0.0.1:8200` | Vault server address |
| `vault_enable_k8s_auth` | `false` | Enable Kubernetes authentication |
| `vault_enable_dynamic_secrets` | `false` | Enable dynamic secrets |
| `vault_enable_agent_injector` | `false` | Enable Vault agent injector |
| `vault_enable_kv_secrets` | `false` | Enable KV secrets engine |

## Example Playbook

```yaml
- hosts: vault_servers
  roles:
    - role: security.vault_integration
      vars:
        vault_install_mode: standalone
        vault_version: "1.15.0"
```

## Kubernetes Example

```yaml
- hosts: kubernetes
  roles:
    - role: security.vault_integration
      vars:
        vault_install_mode: kubernetes
        vault_enable_k8s_auth: true
        vault_enable_dynamic_secrets: true
        vault_k8s_role_name: "deploy-system"
        vault_k8s_namespace: "production"
```

## Tags

- `security`
- `secrets`
- `vault`
- `hashicorp`
- `kubernetes`

## Compliance

- ISO 27001 §8.26 (Information security review)
- NIST 800-53 SC-28 (Protection of information at rest)
- NIST 800-53 IA-5 (Authenticator management)
