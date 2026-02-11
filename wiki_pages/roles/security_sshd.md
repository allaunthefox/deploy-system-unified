# security/sshd

**Role Path**: `roles/security/sshd`

## Description
**SSH Daemon Hardening**
Enhanced SSH daemon configuration focusing on strong ciphers, key exchange, and authentication policies.

## Key Tasks
- Check if sshd_config backup exists
- Backup original sshd_config (only if missing)
- Determine SSH service name
- Ensure SSH privilege separation directory exists (for validation in containers)
- Configure SSH port
- Configure SSH protocol and algorithms
- Disable weak SSH host keys
- Generate strong Ed25519 host key if missing
- Generate strong RSA host key if missing
- Set correct permissions on SSH host keys
- Comment out unmanaged SSH authentication settings
- Configure enhanced SSH security settings
- Verify sshd_config has single-instance directives
- Add trusted-group Match blocks for allowed forwarding (conditional)
- Set SSHD configuration completion flag

## Default Variables
- `sshd_backup_config`
- `sshd_disable_weak_keys`
- `sshd_use_strong_ciphers`
- `sshd_allow_tcp_forwarding`
- `sshd_allow_agent_forwarding`
- `sshd_allow_x11_forwarding`
- `sshd_permit_root_login`
- `sshd_password_authentication`
- `sshd_config_path`
- `sshd_enable_trusted_group_exceptions`
- `sshd_trusted_groups`

---
*This page was automatically generated from role source code.*