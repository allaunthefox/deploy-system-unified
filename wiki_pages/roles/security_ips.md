# security_ips

**role**: `security/ips`

**Intrusion Prevention (Fail2Ban)**
Deploys and configures Fail2Ban with custom filters for SSHD and Caddy to mitigate brute-force attacks.

## Variables

- <a id="ips_fail2ban_sshd_maxretry"></a>`ips_fail2ban_sshd_maxretry`
- <a id="ips_fail2ban_sshd_bantime"></a>`ips_fail2ban_sshd_bantime` — Increased from 1h for persistent offenders
- <a id="ips_fail2ban_sshd_findtime"></a>`ips_fail2ban_sshd_findtime` — Shortened from 10m to catch rapid bursts faster
- <a id="ips_fail2ban_sshd_enabled"></a>`ips_fail2ban_sshd_enabled`
- <a id="ips_fail2ban_caddy_enabled"></a>`ips_fail2ban_caddy_enabled`
- <a id="ips_fail2ban_caddy_maxretry"></a>`ips_fail2ban_caddy_maxretry`
- <a id="ips_fail2ban_caddy_bantime"></a>`ips_fail2ban_caddy_bantime`

