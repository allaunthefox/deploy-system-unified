# Role_Reference_Containers

This document provides detailed information about container-related roles in Deploy-System-Unified.

## Container Roles Overview

| Role | Description | Key Features |
|------|-------------|---------------|
| `containers/anubis` | Web AI Firewall | Ingress traffic protection |
| `containers/authentik` | Identity Provider | Secret validation, negative testing |
| `containers/caddy` | Reverse Proxy | TLS, Red Team hardening |
| `containers/common` | Shared Logic | Common tasks across roles |
| `containers/config` | General Config | Storage directories, environment |
| `containers/lxc` | LXC GPU Passthrough | GPU slicing for LXC |
| `containers/media` | Media Stack | Podman Quadlets, multi-tenancy |
| `containers/memcached` | Caching | Distributed memory cache |
| `containers/monitoring` | Monitoring | Prometheus + Grafana |
| `containers/ops` | Ops Dashboard | Utility tools |
| `containers/quadlets` | Quadlets | Systemd generator files |
| `containers/runtime` | Container Runtime | Podman/Docker, GPU support |

## Container Architecture

### Podman Quadlets

The project uses Podman Quadlets for container management:
- Systemd generator files for native auto-start
- Container networks managed by Systemd
- Robust and reliable startup ordering

### Multi-Tenancy Support

Container roles support multi-tenant deployments:
- Network isolation via container networks
- Separate storage directories per service
- User-based access controls

## See Also

- [Variable Reference: Containers](Ref_Vars_Containers)
- [Container Runtime](CONTAINER_RUNTIME)
- [Media Stack](MEDIA_STACK_V2)
