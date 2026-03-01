# KUBERNETES

This section covers Kubernetes cluster deployment and Helm chart usage.

## Overview

The project supports a hybrid deployment strategy:
- **Podman (Systemd Quadlets)**: Primary for edge/lightweight workloads
- **Kubernetes (K3s)**: For scalable production workloads

## Quick Start

### 1. Deploy K3s Cluster

```bash
ansible-playbook -i inventory/<your_inventory> deploy-k3s.yml
```

### 2. Install Helm Charts

```bash
# Add charts to your cluster
helm install media-stack ./charts/media-stack
helm install ops-stack ./charts/ops-stack
helm install monitoring-stack ./charts/monitoring-stack
```

## Available Charts

| Chart | Services | Port |
|-------|----------|------|
| media-stack | Jellyfin, Radarr, Sonarr | 8096, 7878, 8989 |
| ops-stack | Homarr, Vaultwarden | 7575, 8081 |
| monitoring-stack | Prometheus, Grafana | 9090, 3000 |
| network-stack | Pi-hole, WireGuard | 53, 80, 51820 |
| database-stack | PostgreSQL, Redis | 5432, 6379 |
| logging-stack | Loki, Promtail | 3100 |
| auth-stack | Authentik | 9000 |

## Ingress Configuration

Choose your ingress controller:

- [Ingress Controller Setup](INGRESS_CONTROLLER_SETUP)
- [Variable Reference: Ingress]()

## Benchmarking

Compare Podman vs Kubernetes resource usage:

- [K8s vs Podman Methodology](k8s_vs_podman_methodology)
- [Results Template](k8s_vs_podman_resource_usage)

## Helm Values Example

```yaml
# my-values.yaml
ingress:
  enabled: true
  className: caddy  # caddy, traefik, or nginx
  host: local

# For production TLS with Caddy:
# ingress:
#   annotations:
#     caddy.ingress.kubernetes.io/tls: "auto"
```

## Related Documentation

- [PHASE3_SECRETS_K8S_PLAN](PHASE3_SECRETS_K8S_PLAN)
- [Media Stack V2]()
