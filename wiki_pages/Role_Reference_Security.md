# Role Reference: Security

This document provides detailed information about security-related roles in Deploy-System-Unified.

## Security Roles Overview

| Role | Description | Key Features |
|------|-------------|---------------|
| `security/access` | SSH & User Access | Match rules, admin users, password policy |
| `security/advanced` | Advanced Hardening | Optional security features |
| `security/audit_integrity` | Cryptographic Log Immutability | Signed audit logs |
| `security/file_integrity` | File Integrity Monitoring | AIDE integration |
| `security/firejail` | Application Sandboxing | Firejail profiles |
| `security/hardening` | Core Hardening | Shell hardening, security policies |
| `security/hardware_isolation` | Hardware Level Protection | PCIe passthrough, IOMMU |
| `security/ips` | Intrusion Prevention | Fail2Ban integration |
| `security/kernel` | Sysctl Hardening | Network stack, ASLR settings |
| `security/mac_apparmor` | Mandatory Access Control | AppArmor profiles |
| `security/resource_protection` | DoS Mitigation | Resource limits |
| `security/sandboxing` | User-space Isolation | Additional sandboxing |
| `security/scanning` | Vulnerability Scanning | Lynis, Trivy, Checkov |
| `security/sbom` | Supply Chain Audit | CycloneDX SBOM |
| `security/sshd` | SSH Daemon Hardening | Strong ciphers, key exchange |

## Security Architecture

### Five-Layer Defense

The project implements a comprehensive five-layer security model:

1. **Network Security** - Firewall, VPN mesh, network segmentation
2. **Access Control** - SSH hardening, user management, MAC
3. **System Hardening** - Kernel parameters, sysctl, security policies
4. **Application Security** - Firejail, sandboxing, resource limits
5. **Monitoring & Response** - File integrity, audit logs, vulnerability scanning

### Compliance Mapping

Security roles map to major compliance frameworks:
- **ISO 27001** - Access control, cryptography, audit logging
- **NIST SP 800-193** - Platform firmware resiliency
- **CIS Benchmarks** - Level 1 & 2 hardening

## See Also

- [Variable Reference: Security](Variable_Reference_Security)
- [Security Audit Report](SECURITY_AUDIT_REPORT)
- [Layered Security](LAYERED_SECURITY)
