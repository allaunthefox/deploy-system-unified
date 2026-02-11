# containers/media

**Role Path**: `roles/containers/media`

## Description
**Media Container Role**
This role deploys a comprehensive media stack using Podman Quadlets with multi-tenancy support.

## Key Tasks
- Pull Media Images
- Create Media Network Quadlet
- Create Media Directories
- Create Media Pod Quadlet
- Deploy Media Caddy Configuration
- Create Jellyfin Container Quadlet
- Create Radarr Container Quadlet
- Create Sonarr Container Quadlet
- Create Prowlarr Container Quadlet
- Verify media secrets when fail-secure is enabled
- Enforce CHANGE_ME policy for media stack
- Create Transmission Secrets File
- Create Transmission Container Quadlet
- Create Lidarr Container Quadlet
- Create Readarr Container Quadlet
- Create Jellyseerr Container Quadlet
- Create Navidrome Container Quadlet
- Create Plex Container Quadlet
- Create Bazarr Container Quadlet
- Create Kavita Container Quadlet
- Create Audiobookshelf Container Quadlet

## Default Variables
- `containers_media_instance_name`
- `containers_media_port_offset`
- `containers_media_network`
- `containers_media_hw_accel`
- `containers_media_require_avx`
- `containers_media_stack_enable`
- `containers_media_root_dir`
- `containers_media_config_dir`
- `containers_media_puid`
- `containers_media_pgid`
- `containers_media_timezone`
- `containers_jellyfin_enable`
- `containers_jellyfin_image`
- `containers_jellyfin_port_http`
- `containers_jellyfin_memory_max`
- `containers_plex_enable`
- `containers_plex_image`
- `containers_plex_port_http`
- `containers_plex_claim_token`
- `containers_radarr_enable`
- `containers_radarr_image`
- `containers_radarr_port`
- `containers_sonarr_enable`
- `containers_sonarr_image`
- `containers_sonarr_port`
- `containers_lidarr_enable`
- `containers_lidarr_image`
- `containers_lidarr_port`
- `containers_readarr_enable`
- `containers_readarr_image`
- `containers_readarr_port`
- `containers_prowlarr_enable`
- `containers_prowlarr_image`
- `containers_prowlarr_port`
- `containers_jellyseerr_enable`
- `containers_jellyseerr_image`
- `containers_jellyseerr_port`
- `containers_navidrome_enable`
- `containers_navidrome_image`
- `containers_navidrome_port`
- `containers_transmission_enable`
- `containers_transmission_image`
- `containers_transmission_port_web`
- `containers_transmission_port_peer`
- `containers_transmission_user`
- `containers_transmission_pass`
- `containers_media_pod_enable`
- `containers_media_pod_name`
- `containers_media_gatekeeper_mode`
- `containers_media_domain`
- `containers_media_pod_network`
- `containers_media_auth_provider`
- `containers_media_auth_url`
- `containers_media_fail_secure`
- `containers_bazarr_enable`
- `containers_bazarr_image`
- `containers_bazarr_port`
- `containers_kavita_enable`
- `containers_kavita_image`
- `containers_kavita_port`
- `containers_audiobookshelf_enable`
- `containers_audiobookshelf_image`
- `containers_audiobookshelf_port`

---
*This page was automatically generated from role source code.*