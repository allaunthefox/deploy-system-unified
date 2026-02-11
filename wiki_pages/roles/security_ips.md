# security_ips

**role**: `security/ips`

**Intrusion Prevention (Fail2Ban)**
Deploys and configures Fail2Ban with custom filters for SSHD and Caddy to mitigate brute-force attacks.

## Variables

### ips_fail2ban_sshd_maxretry
- `ips_fail2ban_sshd_maxretry`

### ips_fail2ban_sshd_bantime
- `ips_fail2ban_sshd_bantime` — Increased from 1h for persistent offenders

### ips_fail2ban_sshd_findtime
- `ips_fail2ban_sshd_findtime` — Shortened from 10m to catch rapid bursts faster

### ips_fail2ban_sshd_enabled
- `ips_fail2ban_sshd_enabled`

### ips_fail2ban_caddy_enabled
- `ips_fail2ban_caddy_enabled`

### ips_fail2ban_caddy_maxretry
- `ips_fail2ban_caddy_maxretry`

### ips_fail2ban_caddy_bantime
- `ips_fail2ban_caddy_bantime`


