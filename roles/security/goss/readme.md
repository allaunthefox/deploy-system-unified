# Goss Continuous Monitoring Role

This role provides Goss-based continuous security monitoring for the deploy-system-unified project.

## Features

- **Goss Installation**: Automated binary installation
- **Security Tests**: Pre-defined security validation tests
- **System Tests**: Basic system configuration tests
- **Drift Detection**: Automated configuration drift detection
- **Auto Remediation**: Automatic remediation for common issues
- **Cron Scheduling**: Scheduled validation runs

## Requirements

- Ansible 2.15+
- Supported OS: Ubuntu, Debian, Fedora, CentOS

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `goss_version` | `v0.4.4` | Goss version to install |
| `goss_output_format` | `json` | Output format (json, rspecish, etc.) |
| `goss_enable_drift_detection` | `true` | Enable drift detection |
| `goss_enable_auto_remediation` | `false` | Enable auto remediation |
| `goss_enable_cron` | `true` | Enable cron job |

## Example Playbook

```yaml
- hosts: monitoring
  roles:
    - role: security.goss
      vars:
        goss_version: "v0.4.4"
        goss_output_format: json
```

## Running Tests Manually

```bash
# Validate all tests
goss validate

# Validate with specific format
goss validate --format rspecish

# Validate and auto-remediate
goss validate --remediate
```

## Drift Detection

```bash
# Run drift detection
ansible-playbook /etc/goss/drift-detection.yml
```

## Remediation

```bash
# Run remediation playbook
ansible-playbook /etc/goss/remediation.yml
```

## Tags

- `security`
- `monitoring`
- `goss`
- `testing`
- `drift`

## Compliance

- ISO 27001 §12.2 (Configuration management)
- NIST 800-53 CM-3 (Configuration change control)
- NIST 800-53 CM-6 (Configuration settings)
