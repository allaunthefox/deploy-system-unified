# security_ips

**role**: `security/ips`

**Intrusion Prevention (Fail2Ban)**
Deploys and configures Fail2Ban with custom filters for SSHD and Caddy to mitigate brute-force attacks.

## Variables

<a id="ips-fail2ban-sshd-maxretry"></a>### `ips_fail2ban_sshd_maxretry`
- `ips_fail2ban_sshd_maxretry`

<a id="ips-fail2ban-sshd-bantime"></a>### `ips_fail2ban_sshd_bantime`
- `ips_fail2ban_sshd_bantime` — Increased from 1h for persistent offenders

<a id="ips-fail2ban-sshd-findtime"></a>### `ips_fail2ban_sshd_findtime`
- `ips_fail2ban_sshd_findtime` — Shortened from 10m to catch rapid bursts faster

<a id="ips-fail2ban-sshd-enabled"></a>### `ips_fail2ban_sshd_enabled`
- `ips_fail2ban_sshd_enabled`

<a id="ips-ephemeral-skip"></a>### `ips_ephemeral_skip`
- `ips_ephemeral_skip`

<a id="ips-fail2ban-caddy-enabled"></a>### `ips_fail2ban_caddy_enabled`
- `ips_fail2ban_caddy_enabled`

<a id="ips-fail2ban-caddy-maxretry"></a>### `ips_fail2ban_caddy_maxretry`
- `ips_fail2ban_caddy_maxretry`

<a id="ips-fail2ban-caddy-bantime"></a>### `ips_fail2ban_caddy_bantime`
- `ips_fail2ban_caddy_bantime`


