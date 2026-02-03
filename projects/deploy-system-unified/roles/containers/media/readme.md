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

## Network

* **Internal Network**: `deploy-net` (default). All containers communicate over this bridge.
* **Ingress**: Handled by Caddy Reverse Proxy (except Transmission Peer Port).
* **Ports**:
    * Transmission Peer (TCP/UDP): `51413 + {{ media_port_offset }}` (Host Bound)

## Key Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `media_instance_name` | `default` | Unique identifier for this stack instance. |
| `media_hw_accel` | `false` | Pass `/dev/dri` to Jellyfin/Plex for Transcoding. |
| `media_auth_provider` | `none` | Set to `authentik` to inject Forward Auth snippets into Caddy. |
