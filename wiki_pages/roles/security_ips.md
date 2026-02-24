# security_ips

**role**: `security/ips`

**Intrusion Prevention (Fail2Ban)**
Deploys and configures Fail2Ban with custom filters for SSHD and Caddy to mitigate brute-force attacks.

## Variables

### `ips_fail2ban_sshd_maxretry` {#ips-fail2ban-sshd-maxretry}
- `ips_fail2ban_sshd_maxretry`

### `ips_fail2ban_sshd_bantime` {#ips-fail2ban-sshd-bantime}
- `ips_fail2ban_sshd_bantime` — Increased from 1h for persistent offenders

### `ips_fail2ban_sshd_findtime` {#ips-fail2ban-sshd-findtime}
- `ips_fail2ban_sshd_findtime` — Shortened from 10m to catch rapid bursts faster

### `ips_fail2ban_sshd_enabled` {#ips-fail2ban-sshd-enabled}
- `ips_fail2ban_sshd_enabled`

### `ips_ephemeral_skip` {#ips-ephemeral-skip}
- `ips_ephemeral_skip`

### `ips_fail2ban_caddy_enabled` {#ips-fail2ban-caddy-enabled}
- `ips_fail2ban_caddy_enabled`

### `ips_fail2ban_caddy_maxretry` {#ips-fail2ban-caddy-maxretry}
- `ips_fail2ban_caddy_maxretry`

### `ips_fail2ban_caddy_bantime` {#ips-fail2ban-caddy-bantime}
- `ips_fail2ban_caddy_bantime`


