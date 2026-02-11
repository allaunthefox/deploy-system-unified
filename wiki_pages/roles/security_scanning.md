# security/scanning

**Role Path**: `roles/security/scanning`

## Description
**Vulnerability Scanning**
Comprehensive system validation and vulnerability scanning (Lyinis, Trivy, Checkov).

## Key Tasks
- Validate preflight requirements (idempotent)
- Checkpoint preflight completion (only when no changes)
- Verify directory structure (idempotent)
- Checkpoint directory verification completion (only when no changes)
- Configure security tools (idempotent)
- Mark security tools configured
- Checkpoint security tools configuration (only when no changes)
- Verify Forensic Clock Synchronization (Chrony)
- Validate clock precision
- Checkpoint chrony validation (only when no changes)
- Run enhanced security scanning (idempotent)
- Mark security scanning configured
- Checkpoint enhanced scanning completion (only when no changes)
- Set security framework applied flag
- Validate final security state (idempotent)
- Checkpoint final validation (only when no changes)

## Default Variables
- `security_scanning_enable`
- `security_scanning_install_tools`
- `security_package_mapping`
- `security_scanning_extra_packages`
- `security_scanning_optional_tools`
- `security_scanning_critical_tools`
- `security_scanning_rkhunter_warning_threshold`
- `security_scanning_aide_change_threshold`
- `security_scanning_lynis_issue_threshold`
- `security_scanning_checkov_issue_threshold`

---
*This page was automatically generated from role source code.*