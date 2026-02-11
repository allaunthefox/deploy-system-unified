# security_file_integrity

**Role Path**: `roles/security/file_integrity`

## Description
**File Integrity Monitoring**
Initializes and manages AIDE (Advanced Intrusion Detection Environment) for file integrity monitoring.

## Key Tasks
- Install AIDE
- Check if AIDE database already exists
- Initialize AIDE database (Baseline - Debian/Ubuntu)
- Initialize AIDE database (Baseline - RedHat/Arch)
- Ensure AIDE database is in place (Debian/Ubuntu)
- Ensure AIDE database is in place (RedHat/Arch)
- Skip AIDE database initialization in check mode
- Configure AIDE cron job for daily checks
- Create AIDE log directory
- Configure AIDE to check for changes on boot
- Enable AIDE boot check service
- Skip AIDE boot check service enablement in check mode
- Set file integrity monitoring completion flag

---
*This page was automatically generated from role source code.*