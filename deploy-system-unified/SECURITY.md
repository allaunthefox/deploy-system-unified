# Security Policy

## Supported Versions

| Version | Supported          |
| :------ | :----------------- |
| Master  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

1.  **Do NOT open a public issue.**
2.  Email the maintainers directly (contact info in `AUTHORS` or via private repository message).
3.  Provide a detailed description of the vulnerability and steps to reproduce.

We will acknowledge your report within 48 hours and provide a timeline for a fix.

## Security Features

This project implements several security features by default:
- **SOPS/Age**: For secret encryption at rest.
- **Ansible Vault**: For legacy secret support.
- **Hardening Roles**: System hardening via `roles/security/hardening`.
- **Best Practices**: Least privilege SSH, firewall configuration, and audit logging.

Please ensure your contributions do not downgrade these security standards.
