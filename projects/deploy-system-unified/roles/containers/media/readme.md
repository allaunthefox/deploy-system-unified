# Media Container Role

This role deploys a comprehensive media stack using Podman Quadlets. It supports multi-tenancy, allowing multiple isolated instances of the stack to run on a single host.

## Storage Locations

The role enforces a strict directory structure for persistence. All paths are parametrized by `media_instance_name` (default: `default`) to ensure isolation between instances.

### Content Data (Large Storage)

Base Path: `{{ media_root_dir }}` (Default: `/srv/media/{{ media_instance_name }}`)

| Directory | Description | Container Mapping |
| :--- | :--- | :--- |
| `/movies` | Movie Library | Radarr, Plex, Jellyfin |
| `/tv` | TV Show Library | Sonarr, Plex, Jellyfin |
| `/music` | Music Library | Lidarr, Plex, Navidrome |
| `/books` | E-Book/Audiobook Library | Readarr, Audiobookshelf |
| `/downloads` | Transmission Downloads | Transmission (RW), Arrs (RW) |

### Configuration Data (Fast Storage/SSD)

Base Path: `{{ media_config_dir }}` (Default: `/srv/containers/media_config/{{ media_instance_name }}`)

| Directory | Service | Notes |
| :--- | :--- | :--- |
| `/jellyfin` | Jellyfin | Metadata and internal DB |
| `/plex` | Plex | Metadata and internal DB |
| `/radarr` | Radarr | SQLite DB & Config |
| `/sonarr` | Sonarr | SQLite DB & Config |
| `/lidarr` | Lidarr | SQLite DB & Config |
| `/readarr` | Readarr | SQLite DB & Config |
| `/prowlarr` | Prowlarr | SQLite DB & Config |
| `/jellyseerr`| Jellyseerr| SQLite DB & Config |
| `/navidrome` | Navidrome | SQLite DB & Config |
| `/transmission`| Transmission | Settings.json |

## Network And Exposure

- **Rootful mode** (Podman running as root) uses **host networking** (`Network=host`) for VPS compatibility; published ports are implicit and are not specified explicitly in quadlets.
- **Rootless mode** uses a user-defined pod network set by `media_pod_network` (default: `{{ media_network }}`).
- **Network creation**: The role will create a `.network` quadlet named `{{ media_network }}.network` (Driver=bridge). Override `media_network` to change the underlying bridge name; `media_pod_network` defaults to `{{ media_network }}` and controls what the pod attaches to in rootless mode.

In rootless mode:
  - If `media_gatekeeper_mode` is `false`, service ports are published to the host using `PublishPort` entries for direct access.
  - If `media_gatekeeper_mode` is `true`, service ports remain internal to the pod and Caddy snippets are generated for reverse-proxy-only access.
- Transmission peer port is always published on `51413 + {{ media_port_offset }}` (TCP/UDP).
- **Credentials note**: credentials such as `transmission_user` and `transmission_pass` default to placeholder values (e.g., `CHANGE_ME_IN_SOPS`) and MUST be overridden via SOPS/Vault for production use.

## Key Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `media_instance_name` | `default` | Unique identifier for this stack instance. |
| `media_port_offset` | `0` | Port offset for multi-tenant peer port mapping. |
| `media_pod_enable` | `true` | Enable the shared media pod. |
| `media_pod_name` | `media_pod_{{ media_instance_name }}` | Pod name for the stack. |
| `media_pod_network` | `media_net` | Network the media pod attaches to. |
| `media_hw_accel` | `false` | Pass `/dev/dri` to Jellyfin/Plex for Transcoding. |
| `media_gatekeeper_mode` | `false` | Enable reverse-proxy-only access and Caddy snippets. |
| `media_domain` | `media.example.com` | Base domain used for service subdomains. |
| `media_auth_provider` | `none` | Set to `authentik` to inject Forward Auth snippets into Caddy. |
