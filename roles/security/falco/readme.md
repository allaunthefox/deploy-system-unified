# Falco Runtime Security Role

This role provides Falco runtime security monitoring for the deploy-system-unified project.

## Features

- **Package Installation**: Native package installation for Debian/RHEL systems
- **Binary Installation**: Manual binary installation for unsupported systems
- **Rules Configuration**: Custom security rules for detecting threats
- **Kubernetes Support**: Kubernetes audit rules and detection
- **Alert Integration**: Webhook and syslog alert forwarding
- **JSON Output**: Structured logging for SIEM integration

## Requirements

- Ansible 2.15+
- Supported OS: Ubuntu, Debian, Fedora, CentOS

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `falco_version` | `0.36.2` | Falco version to install |
| `falco_install_method` | `package` | Installation method: package, binary |
| `falco_config.log_level` | `info` | Logging level |
| `falco_config.json_output` | `true` | Enable JSON output |

## Example Playbook

```yaml
- hosts: security_monitors
  roles:
    - role: security.falco
      vars:
        falco_version: "0.36.2"
        falco_install_method: package
```

## Custom Rules

Place custom rules in `/etc/falco/rules.d/falco-rules.yaml`:

```yaml
- rule: Detect sensitive file access
  desc: Detect access to sensitive files
  condition: open_read and fd.name in (/etc/shadow, /etc/passwd)
  priority: WARNING
```

## Tags

- `security`
- `runtime`
- `falco`
- `monitoring`
- `kubernetes`

## Compliance

- ISO 27001 §12.3 (Information backup)
- NIST 800-53 AU-2 (Event logging)
- NIST 800-53 SI-4 (System monitoring)
