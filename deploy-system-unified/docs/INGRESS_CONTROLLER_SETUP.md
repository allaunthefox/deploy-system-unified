# Kubernetes Ingress Controller Setup

**Created:** February 13, 2026  
**Status:** In Progress  
**Purpose:** Guide for setting up Ingress controllers to expose K8s services

## Supported Ingress Controllers

This project supports multiple ingress controllers. The choice depends on your infrastructure:

| Controller | Pros | Cons | Best For |
|------------|------|------|----------|
| **Caddy** | Automatic HTTPS, simple config | Less flexible | Development, simple setups |
| **Traefik** | Rich features, middleware | More complex | Production, advanced routing |
| **Nginx** | Widely used, stable | Manual TLS config | Maximum compatibility |

## Configuration

### Via Helm Values

All charts use configurable ingress class:

```yaml
ingress:
  enabled: true
  className: caddy  # caddy, traefik, nginx
  host: local
```

### Caddy Setup

```bash
# Install Caddy ingress controller
helm repo add caddy https://caddyserver.github.io/k8s-ingress-controller
helm install caddy caddy/k8s-ingress-controller
```

### Traefik Setup

```bash
# Install Traefik
helm repo add traefik https://traefik.github.io/charts
helm install traefik traefik/traefik
```

### Nginx Setup

```bash
# Install Nginx Ingress Controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx
```

## Usage Examples

### Exposing Services

With ingress configured, services are available at:

- `jellyfin.local` (media-stack)
- `radarr.local` (media-stack)
- `sonarr.local` (media-stack)
- `homarr.local` (ops-stack)
- `vaultwarden.local` (ops-stack)
- `prometheus.local` (monitoring)
- `grafana.local` (monitoring)

### TLS/HTTPS

#### Caddy (Automatic)

Caddy automatically provisions Let's Encrypt certificates:

```yaml
ingress:
  annotations:
    caddy.ingress.kubernetes.io/tls: "auto"
```

#### Traefik

```yaml
ingress:
  annotations:
    traefik.ingress.kubernetes.io/router.tls: "true"
```

#### Nginx

```yaml
ingress:
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
```

## DNS Configuration

Add entries to `/etc/hosts` or your DNS server:

```
127.0.0.1 jellyfin.local
127.0.0.1 radarr.local
127.0.0.1 sonarr.local
127.0.0.1 homarr.local
127.0.0.1 vaultwarden.local
127.0.0.1 prometheus.local
127.0.0.1 grafana.local
```

For production, replace `127.0.0.1` with your ingress controller's external IP.

## Troubleshooting

### Ingress Not Working

1. Check ingress controller pods are running:
   ```bash
   kubectl get pods -n ingress-nginx
   ```

2. Check ingress resources:
   ```bash
   kubectl describe ingress
   ```

3. Check controller logs:
   ```bash
   kubectl logs -n ingress-nginx <ingress-pod>
   ```

### TLS Issues

1. Verify certificate status:
   ```bash
   kubectl get certificates
   ```

2. Check cert-manager pods:
   ```bash
   kubectl get pods -n cert-manager
   ```

## Resources

- [Caddy Ingress Controller](https://github.com/caddyserver/k8s-ingress-controller)
- [Traefik Kubernetes](https://doc.traefik.io/traefik/providers/kubernetes-ingress/)
- [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
