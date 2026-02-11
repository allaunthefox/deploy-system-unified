# core_bootstrap

**Role Path**: `roles/core/bootstrap`

## Description
**Core bootstrap role**
System initialization and base configuration.

## Key Tasks
- Gather system facts
- Set distribution-specific variables
- Construct Base Package List
- Ensure base packages are installed (Debian/Ubuntu)
- Ensure base packages are installed (RedHat/CentOS)
- Ensure base packages are installed (Arch)
- Ensure base packages are installed (Alpine)
- Create standard system directories
- Detect Virtualization Environment
- Report Virtualization Profile
- Generate high-entropy Deployment ID (Forensic Primary Key)
- Set bootstrap completion flag

## Default Variables
- `core_install_base_packages`
- `system_base_packages`
- `system_standard_directories`

---
*This page was automatically generated from role source code.*