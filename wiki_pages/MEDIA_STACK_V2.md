# MEDIA_STACK_V2

## Overview

This document outlines the expanded container ecosystem for the `deploy-system-unified` project. It integrates the full suite of media and operational services into the multi-tenant `containers/media` role and the new `containers/ops` role.

## Service Inventory

### 1. Core Media Services (Role: `containers/media`)

These services share the `media_pod` and benefit from the `media_instance_name` isolation.

| Service | Image | Function | Internal Port | Ingress Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Jellyfin** | `jellyfin/jellyfin` | Media Server | `8096` | Caddy + Authentik |
| **Plex** | `plexinc/pms-docker` | Media Server (Alt) | `32400` | Host Network / Caddy |
| **Radarr** | `linuxserver/radarr` | Movies | `7878` | Caddy + Authentik |
| **Sonarr** | `linuxserver/sonarr` | TV | `8989` | Caddy + Authentik |
| **Lidarr** | `linuxserver/lidarr` | Music | `8686` | Caddy + Authentik |
| **Readarr** | `linuxserver/readarr` | Books | `8787` | Caddy + Authentik |
| **Prowlarr** | `linuxserver/prowlarr` | Indexer | `9696` | Caddy + Authentik |
| **Jellyseerr** | `fallenbagel/jellyseerr` | Requests | `5055` | Caddy + Authentik |
| **Navidrome** | `deluan/navidrome` | Music Stream | `4533` | Caddy + Authentik |
| **Audiobookshelf** | `advplyr/audiobookshelf` | AuB Stream | `13378` | Caddy + Authentik |
| **Kavita** | `kavitareader/kavita` | Manga/E-book | `5000` | Caddy + Authentik |
| **Transmission** | `linuxserver/transmission`| Downloader | `9091` | Caddy + Authentik |

#### Port Offset Strategy (Multi-Tenancy)

* **Web UIs**: No offset needed. Bound to `localhost` inside the Pod/Bridge and accessed via unique subdomains (`lidarr-family.domain.com` -> `lidarr-family:8686`).
* **P2P Ingress**: Requires Host Port mapping.
    * **Transmission Peer**: `51413 + {{ media_port_offset }}`.

#### Volume Layout

Root: `/srv/media/{{ media_instance_name }}`

* `/config/{service}`: Application data.
* `/data/media`: Shared content library.
* `/data/downloads`: Download extraction area.

### 2. Operations & Dashboard (Role: `containers/ops`)

These services run adjacent to the media stack but provide infrastructure utility.

| Service | Image | Function | Internal Port |
| :--- | :--- | :--- | :--- |
| **Homarr** | `ghcr.io/ajnart/homarr` | Dashboard | `7575` |
| **Vaultwarden** | `vaultwarden/server` | Passwords | `80` (Rocket) |
| **Wiki.js** | `requarks/wiki` | Documentation | `3000` |
| **Wastebin** | `matze/wastebin` | Pastebin | `8088` |

### 3. Identity Provider (Role: `containers/authentik`)

* **Status**: Implemented.
* **Integration**: Provides `authentik_protect` snippet for all Caddy ingress routes listed above.

## Kubernetes Helm Charts

As of February 2026, the media and ops stacks are also available as Helm charts for Kubernetes deployment:

### media-stack Chart

Located in `charts/media-stack/`, includes:

| Service | Template | Port |
|---------|----------|------|
| Jellyfin | `jellyfin-deployment.yaml` | 8096 |
| Radarr | `radarr-deployment.yaml` | 7878 |
| Sonarr | `sonarr-deployment.yaml` | 8989 |

**Features:**
- Liveness/readiness probes
- PVCs for config and media storage
- Configurable ingress (caddy/traefik/nginx)
- GPU support modeled

### ops-stack Chart

Located in `charts/ops-stack/`, includes:

| Service | Template | Port |
|---------|----------|------|
| Homarr | `homarr-deployment.yaml` | 7575 |
| Vaultwarden | `vaultwarden-deployment.yaml` | 8081, 3012 (ws) |

**Features:**
- K8s Secret for admin token
- PVCs for configs, icons, data
- Liveness/readiness probes
- Configurable ingress

### Ingress Configuration

Both charts support configurable ingress class via values.yaml:

```yaml
ingress:
  enabled: true
  className: caddy  # Options: caddy, traefik, nginx
  host: local
```

### Validation

```bash
helm lint charts/media-stack charts/ops-stack  # Passed
helm unittest charts/media-stack charts/ops-stack  # 13/13 tests passed
```

## Implementation Roadmap

1. **Refactor `containers/media`**:
    * Add tasks for: Lidarr, Readarr, Jellyseerr, Navidrome, Audiobookshelf, Kavita.
    * Ensure all distinct functionality (Listening, Reading, Watching) maps to the standardized `media_root_dir` structure.
2. **Create `containers/ops`**:
    * Scaffold new role.
    * Implement Vaultwarden (SQLite/MariaDB) and Homarr.
3. **Deploy**:
    * Update `media_streaming_server.yml` to enable specific feature flags (e.g., `enable_books: true`, `enable_music: true`).
4. **Kubernetes Deployment (Phase 3)**:
    * Helm charts now available for K3s/K8s deployment
    * Benchmark Podman vs K8s resource usage in progress
