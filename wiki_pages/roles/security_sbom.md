# Role: security/sbom (Supply Chain Audit)

**Classification:** POL-SEC (Security Policy Enforcement)  
**Standard:** ISO 27001 §14.2  
**Action Codes:** 520040 - 520047

## Overview
The `security/sbom` role implements Software Bill of Materials (SBOM) generation and supply-chain auditing. It ensures that every container image and software library used in the project is cataloged, signed, and auditable.

## Key Features
- **Automated Scanning**: Python-based discovery of all role dependencies.
- **CycloneDX Export**: Generates industry-standard SBOM JSON (v1.5).
- **Immutable Tracing**: Automatically signs audit records with SHA256.
- **Forensic Integration**: Linked to Action Codes for real-time audit visibility.

## Configuration
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `core_secrets_enabled` | bool | `true` | Enable/disable SBOM audit |

## Compliance Mapping
- **ISO 27001 §14.2**: Security in development and support processes.
- **NIST SP 800-161**: Supply Chain Risk Management.
- **Action 520041**: Supply Chain Verified.
