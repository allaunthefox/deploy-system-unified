# index

This directory contains Helm charts for deploying various service stacks on Kubernetes (K3s).

## Available Charts

| Chart | Services | Port |
|-------|----------|------|
| auth-stack | Authentik (SSO) | 9000 |
| backup-stack | Restic, Rclone | 8080 |
| database-stack | PostgreSQL, Redis | 5432, 6379 |
| logging-stack | Loki, Promtail | 3100 |
| media-stack | Jellyfin, Radarr, Sonarr | 8096, 7878, 8989 |
| monitoring-stack | Prometheus, Grafana | 9090, 3000 |
| network-stack | Pi-hole | 53, 80 |
| ops-stack | Homarr, Vaultwarden | 7575, 8081 |
| proxy-stack | Caddy, Nginx | 80, 443 |
| security-stack | Security tools | - |

## Usage

```bash
# Add charts to your cluster
helm install media-stack ./charts/media-stack
helm install ops-stack ./charts/ops-stack
helm install monitoring-stack ./charts/monitoring-stack

# Upgrade existing installations
helm upgrade media-stack ./charts/media-stack
```

## Documentation

- [K8s Deployment Guide](../deployment/KUBERNETES.md)
- [Ingress Controller Setup](../deployment/INGRESS_CONTROLLER_SETUP.md)
