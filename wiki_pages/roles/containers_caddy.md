# containers/caddy

**Role Path**: `roles/containers/caddy`

## Description
**Reverse Proxy (Caddy)**
Handles Caddy reverse proxy configuration with Red Team hardening for secrets.

## Key Tasks
- Validate Caddy Secrets (Red Team Hardening)
- Verify Caddy secret files when fail-secure is enabled
- Validate Porkbun API keys are set
- Create Caddy secrets file
- Create Proxy Network Quadlet
- Create Caddy directories
- Create Caddyfile
- Validate Quadlet GPU capabilities (Linux CAP_* only)
- Create Caddy container quadlet
- Set containers caddy completion flag
- Create Crowdsec Directories
- Create Crowdsec Container Quadlet
- Install Crowdsec Bouncer Dependencies
- Create Crowdsec Bouncer Directory (Host)
- Create Firewall Bouncer Config (Host)
- Check if Bouncer is installed
- Install Firewall Bouncer (Host)
- Enable and Start Firewall Bouncer

## Default Variables
- `containers_caddy_generate_config`
- `containers_caddy_acme_email`
- `containers_caddy_http_port`
- `containers_caddy_https_port`
- `containers_caddy_https_port_udp`
- `containers_porkbun_api_key`
- `containers_porkbun_secret_api_key`
- `containers_caddy_network`
- `containers_caddy_extra_networks`
- `containers_crowdsec_enable`
- `containers_crowdsec_image`
- `containers_crowdsec_firewall_bouncer_key`
- `containers_caddy_fail_secure`
- `containers_crowdsec_firewall_bouncer_version`
- `containers_crowdsec_firewall_bouncer_sha256`
- `containers_crowdsec_secrets_dir`
- `containers_crowdsec_collections`
- `containers_quadlet_enable_gpu_support`

---
*This page was automatically generated from role source code.*