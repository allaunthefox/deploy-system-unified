# security/hardening

**Role Path**: `roles/security/hardening`

## Description
**Core Hardening**
Enhanced core security configurations, including shell hardening and system-wide security policies.

## Key Tasks
- Ensure security-related packages are installed (Debian/Ubuntu)
- Ensure security-related packages are installed (RedHat/CentOS)
- Ensure security-related packages are installed (Arch Linux)
- Configure auditd service
- Harden file system permissions
- Harden user accounts
- Harden PAM configuration (Debian)
- Set security hardening completion flag

## Default Variables
- `security_hardening_enabled`
- `security_enable_ufw`
- `security_enable_fail2ban`
- `security_enable_auto_updates`
- `security_kernel_hardening`

---
*This page was automatically generated from role source code.*