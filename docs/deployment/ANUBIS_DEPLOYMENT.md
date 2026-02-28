# Anubis AI Firewall - Deployment Guide
# =============================================================================
# Anubis is a Proof-of-Work (PoW) web firewall that protects applications
# from scrapers, bots, and automated attacks.
# Last Updated: 2026-02-28
# =============================================================================

## Overview

**Anubis** is an AI Firewall that uses Proof-of-Work challenges to protect web applications from automated attacks while allowing legitimate users through seamlessly.

| Property | Value |
|----------|-------|
| **Type** | Container (Podman Quadlet) |
| **Image** | `ghcr.io/techarohq/anubis:v1.24.0` |
| **Port** | 8080 |
| **Runtime** | Podman (systemd-managed) |
| **Priority** | P0 (Critical Security) |
| **Dependencies** | proxy-stack (Caddy) |

---

## What Does Anubis Do?

Anubis sits in front of your web applications and:

1. **Challenges Bots**: Requires visitors to solve a PoW puzzle
2. **Allows Humans**: Legitimate browsers solve it automatically
3. **Blocks Scrapers**: Automated tools can't solve the challenge efficiently
4. **Protects Resources**: Reduces server load from bot traffic

**Use Cases:**
- Protect LLM/ML endpoints from scraping
- Shield APIs from rate limit abuse
- Prevent credential stuffing attacks
- Reduce DDoS impact

---

## Deployment Options

### Option 1: Ansible Role (Recommended)

```yaml
# In your playbook
- name: Deploy Anubis AI Firewall
  hosts: all
  become: true
  roles:
    - containers/anubis
```

**Configuration (group_vars/all.yml):**
```yaml
anubis_enabled: true
anubis_port: 8080
anubis_difficulty: 5  # 1-10, higher = harder challenge
anubis_target_url: "http://app:80"  # Backend to protect
anubis_image: "ghcr.io/techarohq/anubis:v1.24.0"
anubis_container_name: "anubis-gatekeeper"
```

### Option 2: Run Anubis Only Playbook

```bash
# Deploy only Anubis
ansible-playbook run_anubis_only.yml -i inventory/production.ini
```

### Option 3: Ephemeral Edge (Caddy + Anubis)

```bash
# Deploy Caddy proxy with Anubis protection
ansible-playbook ephemeral_edge.yml -i inventory/production.ini
```

---

## Architecture

```
Internet
    │
    ▼
┌─────────────────┐
│   Anubis:8080   │ ← Proof-of-Work Challenge
└─────────────────┘
    │
    ▼ (Verified Traffic)
┌─────────────────┐
│    Caddy:80/443 │ ← TLS Termination
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  Your App:8080  │ ← Protected Application
└─────────────────┘
```

---

## Configuration Options

### Difficulty Levels

| Level | Value | Use Case | Bot Protection | User Impact |
|-------|-------|----------|----------------|-------------|
| Low | 1-3 | Internal apps | Basic | None |
| Medium | 4-6 | Public websites | Good | Minimal |
| High | 7-8 | API endpoints | Strong | Slight delay |
| Maximum | 9-10 | Under attack | Maximum | Noticeable |

**Recommended:** `anubis_difficulty: 5`

### Target URL Configuration

```yaml
# Protect a local application
anubis_target_url: "http://localhost:8080"

# Protect a container on the same network
anubis_target_url: "http://app:80"

# Protect an external service
anubis_target_url: "http://backend.internal:3000"
```

---

## Integration with Other Stacks

### With proxy-stack (Caddy)

**Caddyfile configuration:**
```caddy
example.com {
    reverse_proxy http://localhost:8080  # Anubis
}

# Anubis forwards to:
# http://app:80 (your actual application)
```

**Deployment order:**
1. Deploy your application
2. Deploy proxy-stack (Caddy)
3. Deploy anubis (pointing to your app)
4. Update Caddy to reverse proxy through Anubis

### With ops-stack (Homarr/Vaultwarden)

```yaml
# Protect Homarr dashboard
anubis_target_url: "http://homarr:3000"
anubis_port: 8081

# Protect Vaultwarden
anubis_target_url: "http://vaultwarden:80"
anubis_port: 8082
```

### With monitoring-stack (Grafana)

```yaml
# Protect Grafana
anubis_target_url: "http://grafana:3000"
anubis_port: 8083
```

---

## Resource Requirements

| Component | CPU | Memory | Storage |
|-----------|-----|--------|---------|
| Anubis Container | 100m | 128Mi | None (ephemeral) |

**Minimal overhead** - Anubis is very lightweight.

---

## Security Considerations

### Network Isolation

```yaml
# Anubis runs on isolated network
quadlet_network: anubis_net
quadlet_subnet: 10.89.50.0/24
```

### Firewall Rules

```bash
# Allow only Caddy to reach Anubis
sudo firewall-cmd --permanent --add-rich-rule='
  rule family="ipv4"
  source address="10.89.50.0/24"
  port port="8080" protocol="tcp"
  accept'
```

### Difficulty Tuning

**Monitor and adjust:**
```bash
# Check challenge completion rate
curl -s http://localhost:8080/metrics | grep anubis_challenges

# If too many false positives:
anubis_difficulty: 4  # Lower

# If bots getting through:
anubis_difficulty: 6  # Higher
```

---

## Deployment in Profiles

### Profile A (MINIMAL)
```yaml
anubis_enabled: false  # Not needed for testing
```

### Profile B (STANDARD)
```yaml
anubis_enabled: true
anubis_difficulty: 5
anubis_target_url: "http://localhost:8080"
```

### Profile C (PRODUCTION)
```yaml
anubis_enabled: true
anubis_difficulty: 6
anubis_target_url: "http://app:80"
anubis_port: 8080
quadlet_enable_gpu_support: false
```

### Profile F (SECURITY)
```yaml
anubis_enabled: true
anubis_difficulty: 8  # Higher for security-focused deployment
anubis_target_url: "http://app:80"
# Deploy in front of all public-facing apps
```

---

## Monitoring Anubis

### Metrics Endpoint

```bash
# Access metrics
curl http://localhost:8080/metrics

# Key metrics:
# - anubis_challenges_total
# - anubis_challenges_passed
# - anubis_challenges_failed
# - anubis_average_solve_time
```

### Logs

```bash
# View Anubis logs
sudo journalctl -u anubis-gatekeeper -f

# Filter for challenges
sudo journalctl -u anubis-gatekeeper | grep challenge
```

### Health Check

```bash
# Check if Anubis is running
sudo systemctl status anubis-gatekeeper

# Test challenge endpoint
curl -I http://localhost:8080
```

---

## Troubleshooting

### Anubis Not Starting

```bash
# Check logs
sudo journalctl -u anubis-gatekeeper -n 50

# Verify target is reachable
curl -I http://app:80

# Check network
podman network ls | grep anubis
```

### Too Many False Positives

```yaml
# Lower difficulty
anubis_difficulty: 4

# Or increase solve time
anubis_solve_timeout: 30s  # Default: 5s
```

### Bots Still Getting Through

```yaml
# Increase difficulty
anubis_difficulty: 7

# Add rate limiting in front
# Use Caddy rate_limit plugin
```

---

## Compatibility

### ✅ Compatible With

- All Kubernetes stacks (runs as Podman container)
- Caddy/NGINX/Traefik reverse proxies
- Any HTTP/HTTPS application
- Other security tools (CrowdSec, Fail2Ban)

### ⚠️ Considerations

- **Not for WebSocket-heavy apps**: PoW challenge breaks persistent connections
- **API clients need tokens**: Automated clients need API keys to bypass
- **CDN integration**: May need to bypass Anubis for CDN IPs

---

## Quick Start

```bash
# 1. Set configuration
cat > /etc/anubis/config.yml <<EOF
anubis_enabled: true
anubis_port: 8080
anubis_difficulty: 5
anubis_target_url: "http://localhost:3000"
EOF

# 2. Deploy
ansible-playbook run_anubis_only.yml -i inventory/local.ini

# 3. Verify
curl http://localhost:8080

# 4. Point Caddy to Anubis
# Update Caddyfile: reverse_proxy http://localhost:8080

# 5. Reload Caddy
sudo systemctl reload caddy
```

---

## References

- **GitHub:** https://github.com/TecharoHQ/anubis
- **Documentation:** https://anubis.techaro.lol
- **Role Path:** `roles/containers/anubis`
- **Playbook:** `run_anubis_only.yml`
- **Ephemeral Deploy:** `ephemeral_edge.yml`

---

## Document Control

- **Version:** 1.0
- **Last Updated:** 2026-02-28
- **Maintained By:** Infrastructure Team
- **Related:** DEPLOYMENT_MATRIX.md, SECURITY_STANDARDS.md
