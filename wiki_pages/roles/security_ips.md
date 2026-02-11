# security/ips

**Role Path**: `roles/security/ips`

## Description
**Intrusion Prevention (Fail2Ban)**
Deploys and configures Fail2Ban with custom filters for SSHD and Caddy to mitigate brute-force attacks.

## Key Tasks
- Install Fail2Ban
- Configure Fail2Ban for SSH protection
- Install Caddy Filter
- Configure Fail2Ban for Caddy (Web Protection)
- Enable and start Fail2Ban

## Default Variables
- `ips_fail2ban_sshd_maxretry`
- `ips_fail2ban_sshd_bantime`
- `ips_fail2ban_sshd_findtime`
- `ips_fail2ban_sshd_enabled`
- `ips_fail2ban_caddy_enabled`
- `ips_fail2ban_caddy_maxretry`
- `ips_fail2ban_caddy_bantime`

---
*This page was automatically generated from role source code.*