# =============================================================================
# Audit Event Identifier: DSU-HLM-300000
# Last Updated: 2026-02-28
# =============================================================================
# Monitoring and Media Stack Deployment Guide

**Last Updated:** 2026-02-28  
**Version:** 1.0  

---

## Overview

This guide covers the automated deployment of monitoring (Prometheus/Grafana) and media (Jellyfin/Radarr/Sonarr) stacks using the Deploy-System-Unified framework.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Kubernetes Cluster (K3s)                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐      ┌─────────────────────┐      │
│  │   monitoring NS     │      │     media NS        │      │
│  │                     │      │                     │      │
│  │  ┌───────────────┐  │      │  ┌───────────────┐  │      │
│  │  │   Grafana     │  │      │  │   Jellyfin    │  │      │
│  │  │   :3000       │  │      │  │   :8096       │  │      │
│  │  └───────────────┘  │      │  └───────────────┘  │      │
│  │                     │      │                     │      │
│  │  ┌───────────────┐  │      │  ┌───────────────┐  │      │
│  │  │  Prometheus   │  │      │  │    Radarr     │  │      │
│  │  │   :9090       │  │      │  │   :7878       │  │      │
│  │  └───────────────┘  │      │  └───────────────┘  │      │
│  │                     │      │                     │      │
│  │  ┌───────────────┐  │      │  ┌───────────────┐  │      │
│  │  │ Alertmanager  │  │      │  │    Sonarr     │  │      │
│  │  │   :9093       │  │      │  │   :8989       │  │      │
│  │  └───────────────┘  │      │  └───────────────┘  │      │
│  └─────────────────────┘      └─────────────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

1. **K3s cluster** (v1.31.4+ recommended)
2. **Helm** (v3.16+)
3. **Ansible** (v2.16+)
4. **kubernetes.core** Ansible collection

### Deploy with Ansible (Recommended)

```bash
cd /home/prod/Workspaces/repos/github/deploy-system-unified

# Deploy both stacks with default settings
ansible-playbook deploy_monitoring_media.yml -i inventory/your_inventory.ini

# Deploy with custom configuration
ansible-playbook deploy_monitoring_media.yml -i inventory/your_inventory.ini \
  -e monitoring_persistence_enabled=true \
  -e media_persistence_enabled=true \
  -e media_gpu_enabled=false

# Skip preflight checks (for testing)
ansible-playbook deploy_monitoring_media.yml -i inventory/your_inventory.ini \
  --skip-tags preflight
```

### Deploy with Helm (Manual)

```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Deploy monitoring stack
helm upgrade --install monitoring charts/monitoring-stack \
  -n monitoring \
  --create-namespace \
  --set prometheus.persistence.enabled=true \
  --set grafana.persistence.enabled=true

# Deploy media stack
helm upgrade --install media charts/media-stack \
  -n media \
  --create-namespace \
  --set jellyfin.persistence.config.enabled=true \
  --set jellyfin.persistence.media.enabled=true \
  --set hardware.gpu.enabled=false
```

---

## Configuration

### Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `monitoring_stack_enabled` | `true` | Enable/disable monitoring stack deployment |
| `media_stack_enabled` | `true` | Enable/disable media stack deployment |
| `monitoring_persistence_enabled` | `true` | Enable persistent storage for monitoring |
| `media_persistence_enabled` | `true` | Enable persistent storage for media apps |
| `media_gpu_enabled` | `false` | Enable GPU acceleration for Jellyfin |
| `timezone` | `UTC` | Timezone for media applications |

### Persistence Configuration

#### With Persistent Storage (Production)

```yaml
# inventory/group_vars/production.yml
monitoring_persistence_enabled: true
media_persistence_enabled: true

# Ensure storage provisioner is working
# kubectl get storageclass
```

#### Without Persistent Storage (Testing)

```yaml
# inventory/group_vars/development.yml
monitoring_persistence_enabled: false
media_persistence_enabled: false

# Uses emptyDir volumes - data lost on pod restart
```

### GPU Acceleration

For hardware transcoding in Jellyfin:

```yaml
# inventory/group_vars/production.yml
media_gpu_enabled: true

# Prerequisites:
# 1. Install GPU device plugin for Kubernetes
# 2. Ensure node has compatible GPU (Intel/AMD/NVIDIA)
```

---

## Accessing Services

### Port Forward (Local Access)

```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Grafana
kubectl port-forward -n monitoring svc/monitoring-monitoring-stack-grafana 3000:3000
# Access: http://localhost:3000 (admin/admin)

# Prometheus
kubectl port-forward -n monitoring svc/monitoring-monitoring-stack-prometheus 9090:9090
# Access: http://localhost:9090

# Jellyfin
kubectl port-forward -n media svc/media-media-stack-jellyfin 8096:8096
# Access: http://localhost:8096

# Radarr
kubectl port-forward -n media svc/media-media-stack-radarr 7878:7878
# Access: http://localhost:7878

# Sonarr
kubectl port-forward -n media svc/media-media-stack-sonarr 8989:8989
# Access: http://localhost:8989
```

### Ingress (Network Access)

Configure ingress controllers for external access:

```yaml
# charts/monitoring-stack/values.yaml
ingress:
  enabled: true
  className: caddy  # or traefik, nginx
  host: monitoring.example.com
```

---

## Validation

### Check Deployment Status

```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Check all pods
kubectl get pods -n monitoring,media

# Check all deployments
kubectl get deployments -n monitoring,media

# Check services
kubectl get services -n monitoring,media
```

### Expected Output

```
NAMESPACE    NAME                                                  READY   STATUS
monitoring   monitoring-monitoring-stack-grafana                   1/1     Running
monitoring   monitoring-monitoring-stack-prometheus                1/1     Running
media        media-media-stack-jellyfin                            1/1     Running
media        media-media-stack-radarr                              1/1     Running
media        media-media-stack-sonarr                              1/1     Running
```

### Run Validation Playbook

```bash
ansible-playbook deploy_monitoring_media.yml -i inventory/your_inventory.ini \
  --tags validate
```

---

## Troubleshooting

### Pods Stuck in Pending

**Cause:** PVC provisioning issues

```bash
# Check PVC status
kubectl get pvc -n monitoring,media

# Check storage class
kubectl get storageclass

# If using local-path, check provisioner
kubectl get pods -n kube-system -l app=local-path-provisioner
```

**Solution:** Deploy without persistence for testing:
```bash
ansible-playbook deploy_monitoring_media.yml -i inventory/your_inventory.ini \
  -e monitoring_persistence_enabled=false \
  -e media_persistence_enabled=false
```

### Prometheus CrashLoopBackOff

**Cause:** Missing configuration

**Solution:** The chart now includes a ConfigMap with default Prometheus configuration. If you still see issues:

```bash
kubectl get configmap -n monitoring
kubectl describe pod -n monitoring -l app=prometheus
```

### Jellyfin Pending (GPU)

**Cause:** GPU device plugin not installed

**Solution:** Disable GPU or install device plugin:
```bash
# Disable GPU
ansible-playbook deploy_monitoring_media.yml -i inventory/your_inventory.ini \
  -e media_gpu_enabled=false

# Or install Intel GPU device plugin
kubectl apply -f https://github.com/intel/intel-device-plugins-for-kubernetes/releases/download/v0.27.0/deployment-schemas/intel-device-plugin-operator.yaml
```

### Grafana Cannot Connect to Prometheus

**Cause:** Datasource URL incorrect

**Solution:** Verify datasource configuration:
```bash
kubectl get configmap -n monitoring monitoring-monitoring-stack-grafana-datasources -o yaml
```

---

## Production Considerations

### Security

1. **Change default credentials:**
   ```yaml
   # inventory/group_vars/production.yml
   grafana_admin_password: "{{ vault_grafana_password }}"
   ```

2. **Enable TLS:**
   Configure ingress with TLS certificates

3. **Network policies:**
   Restrict inter-namespace communication

### Backup

1. **Grafana dashboards:** Export and backup regularly
2. **Prometheus data:** Use persistent storage with backup
3. **Media configs:** Backup `/config` directories

### Monitoring

1. **Set up alerts:** Configure Alertmanager receivers
2. **Import dashboards:** Add Kubernetes monitoring dashboards to Grafana
3. **Configure retention:** Adjust Prometheus retention based on storage

---

## Chart Structure

### monitoring-stack

```
charts/monitoring-stack/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── prometheus-deployment.yaml
    ├── prometheus-configmap.yaml      # Prometheus configuration
    ├── grafana-deployment.yaml
    ├── ingress.yaml
    └── _helpers.tpl
```

### media-stack

```
charts/media-stack/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── jellyfin-deployment.yaml       # Conditional PVC support
    ├── radarr-deployment.yaml         # Conditional PVC support
    ├── sonarr-deployment.yaml         # Conditional PVC support
    ├── services.yaml
    ├── pvc.yaml                       # Conditional PVC creation
    ├── ingress.yaml
    └── _helpers.tpl
```

---

## Upgrade Path

### Upgrade Charts

```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Upgrade monitoring stack
helm upgrade monitoring charts/monitoring-stack -n monitoring

# Upgrade media stack
helm upgrade media charts/media-stack -n media
```

### Upgrade via Ansible

```bash
ansible-playbook deploy_monitoring_media.yml -i inventory/your_inventory.ini \
  --tags helm
```

---

## Related Documentation

- [Main README](../README.md)
- [Kubernetes Deployment](./KUBERNETES_DEPLOYMENT.md)
- [Chart Development](./CHART_DEVELOPMENT.md)
- [Production Deployment Guide](../docs/deployment/PRODUCTION.md)

---

## Support

For issues or questions:
1. Check [troubleshooting section](#troubleshooting)
2. Review logs: `kubectl logs -n <namespace> -l app=<app-name>`
3. Open an issue on GitHub
