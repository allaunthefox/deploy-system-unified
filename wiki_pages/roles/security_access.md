# security/access

**Role Path**: `roles/security/access`

## Description
Security access role - SSH and user access configuration

## Key Tasks
- Ensure OpenSSH Server is installed
- Determine SSH service name
- Ensure SSH privilege separation directory exists
- Check for systemctl presence
- Ensure SSH service is running
- Create wheel group if not exists
- Configure sudo for wheel group
- Validate admin password hash (if enforcement enabled)
- Set admin account password hash (idempotent)
- Configure SSH Match blocks (User-level IP restrictions)
- Set access configuration completion flag

## Default Variables
- `ssh_match_rules`
- `access_admin_user`
- `access_admin_password_hash`
- `access_admin_password_enforce`
- `access_admin_password_placeholders`

---
*This page was automatically generated from role source code.*