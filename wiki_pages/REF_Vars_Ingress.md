# VARIABLE_REFERENCE_Ingress

## Ingress Controller Variables

### Global Ingress Settings

These variables apply to all Helm charts with ingress support.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ingress.enabled` | boolean | `true` | Enable ingress resources |
| `ingress.className` | string | `"caddy"` | Ingress controller class |
| `ingress.host` | string | `"local"` | DNS domain suffix |

### Ingress Controller Options

#### Caddy (Default)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ingress.className` | string | `"caddy"` | Set to `caddy` |

**Annotations:**
```yaml
annotations:
  caddy.ingress.kubernetes.io/tls: "auto"
```

#### Traefik

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ingress.className` | string | `"traefik"` | Set to `traefik` |

**Annotations:**
```yaml
annotations:
  traefik.ingress.kubernetes.io/router.tls: "true"
```

#### Nginx

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ingress.className` | string | `"nginx"` | Set to `nginx` |

**Annotations:**
```yaml
annotations:
  nginx.ingress.kubernetes.io/ssl-redirect: "true"
  cert-manager.io/cluster-issuer: "letsencrypt-prod"
```

## Helm Chart Ingress Examples

### media-stack

```yaml
# values.yaml
ingress:
  enabled: true
  className: caddy  # caddy, traefik, or nginx
  host: local
```

### ops-stack

```yaml
# values.yaml
ingress:
  enabled: true
  className: caddy
  host: local
```

### monitoring-stack

```yaml
# values.yaml
ingress:
  enabled: true
  className: caddy
  host: local
```

## DNS Configuration

After setting up ingress, configure DNS:

| Service | Default Host |
|---------|--------------|
| Jellyfin | `jellyfin.{{ ingress.host }}` |
| Radarr | `radarr.{{ ingress.host }}` |
| Sonarr | `sonarr.{{ ingress.host }}` |
| Homarr | `homarr.{{ ingress.host }}` |
| Vaultwarden | `vaultwarden.{{ ingress.host }}` |
| Prometheus | `prometheus.{{ ingress.host }}` |
| Grafana | `grafana.{{ ingress.host }}` |

## Related Documentation

- [INGRESS_CONTROLLER_SETUP](../docs/deployment/INGRESS_CONTROLLER_SETUP.md)
- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
