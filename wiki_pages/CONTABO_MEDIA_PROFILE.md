# Contabo Media Profile Documentation

## 1. Overview

This profile represents the "Media Stack" configuration specifically tuned for the **Contabo Cloud VPS 30 SSD** instance. It is deployed using the `containers/media` Ansible role within the Unified Deployment System.

**Target Hardware**:

- **vCPU**: 8 Cores (AMD EPYC)
- **RAM**: 24 GB
- **Storage**: 800 GB NVMe SSD (Btrfs)
- **Networking**: 400 Mbit/s Port
- **OS**: Arch Linux (Hardened)

## 2. Architecture Decisions

### Networking Strategy: `Network=host`

Unlike standard container deployments that use bridged networks, this profile uses a **Host Network Pod** (`media_pod_default`). Note that the role implements two execution modes: rootful (host networking) and rootless (user-defined pod network via `media_pod_network`). By default this profile targets VPS deployments and uses host networking for simplicity and performance.

- **Reasoning**:
    - **Performance**: Eliminates NAT overhead for high-bandwidth streaming (Jellyfin) and peer-to-peer traffic (Transmission).
    - **Simplicity**: Resolves complex port mapping issues for BitTorrent DHT/PEX protocols.
    - **IPv6**: Native host IPv6 support without container CNI complexity.

**Defaults & Gatekeeper**: `media_gatekeeper_mode` is `false` by default (services are directly accessible). Enable `media_gatekeeper_mode: true` to restrict direct host exposure and generate Caddy reverse-proxy snippets instead. The role creates a `media_net` bridge quadlet by default and exposes `media_network` as an override for the bridge name; `media_pod_network` defaults to `media_network`. Also, service credentials such as `transmission_user`/`transmission_pass` default to placeholder values (e.g., `CHANGE_ME_IN_SOPS`) and should be set via SOPS/Vault for production.

### Storage Layout

The system uses **Btrfs** subvolumes for efficient storage management.

- **Media Root**: `/srv/media/default/`
    - `/srv/media/default/movies`
    - `/srv/media/default/tv`
    - `/srv/media/default/music`
    - `/srv/media/default/books`
    - `/srv/media/default/downloads`
- **Config Root**: `/srv/containers/media_config/default/` (Persistent app data)

### Security Defaults (Least Privilege)

This profile follows the project’s **explicit allow** posture:

- **SSH transfer**: OpenSSH + `piped` transfer (no SFTP/SCP dependency).
- **NFS**: Disabled unless explicitly enabled in a profile.
- **Rsync**: SSH-based only, and disabled unless explicitly enabled.

Reference: `docs/deployment/SSH_TRANSFER_PROFILE.md`

#### Example Overrides (Explicit Allow)

```yaml
# Enable NFS explicitly (example)
storage_nfs_enable: true
storage_nfs_allow_broad_exports: false
storage_nfs_exports:
  - path: /srv/media/default
    clients:
      - "10.0.0.0/24(rw,sync,no_subtree_check)"
storage_nfs_mounts:
  - src: "10.0.0.10:/srv/media/default"
    path: /mnt/media
    opts: "rw,noatime"

# Enable SSH-based rsync explicitly (example)
ops_rsync_enable: true
ops_rsync_allowlist:
  - src: /srv/containers
    dest: "backup@10.0.0.20:/backups/containers"
    ssh_key: "/home/prod/.ssh/backup_key"
```

#### Ephemeral Profiles (Extra Guard)

For `deployment_profile: "ephemeral"`, you must explicitly opt in:

```yaml
storage_nfs_ephemeral_allow: true
ops_rsync_ephemeral_allow: true
```

## 3. Service Inventory

The following services are **Enabled** in this profile:

### Core Media Serving

| Service | Image | Port | Description |
|:---|:---|:---|:---|
| **Jellyfin** | `jellyfin/jellyfin:10.11.6` | 8096 | Primary Media Server (Video/Music) |
| **Kavita** | `jvmilazz0/kavita:0.8.9` | 5000 | Manga & Comic Server |
| **Audiobookshelf** | `advplyr/audiobookshelf:2.32.1` | 13378 | Audiobooks & Podcast Server |

### Automatic Retrieval (The "Arr" Stack)

| Service | Image | Port | Description |
|:---|:---|:---|:---|
| **Radarr** | `linuxserver/radarr:6.0.4` | 7878 | Movie Management |
| **Sonarr** | `linuxserver/sonarr:4.0.16` | 8989 | TV Series Management |
| **Bazarr** | `linuxserver/bazarr:1.5.5` | 6767 | Subtitle Management |
| **Prowlarr** | `linuxserver/prowlarr:2.3.0` | 9696 | Indexer Manager (NZB/Torrent) |
| **Transmission** | `linuxserver/transmission:4.1.0` | 9091 | BitTorrent Client |

### Disabled Services

These services are present in the code but **disabled** for this specific profile to conserve resources or reduce scope:

- **Plex**: Disabled (Favoring Jellyfin FOSS).
- **Lidarr**: Disabled (Music automation not required).
- **Readarr**: Disabled (Book automation not required).
- **Jellyseerr**: Disabled (Request management not required for single-tenant).
- **Navidrome**: Disabled (Jellyfin handles music).

## 4. Integration Points

### Reverse Proxy (Caddy)

The stack integrates with Caddy (deployed via `containers/caddy`) for SSL termination.

- **Config Path**: `/srv/containers/caddy/conf.d/media_stack_default.caddy`
- **Domain**: `media_domain` var (Default: `media.example.com`)
- **Proxy Method**: Reverse Proxy to `localhost:<port>` (due to Host Networking).

### Security (CrowdSec)

- **Log Monitoring**: The `logs` volumes are mounted RO to the CrowdSec agent.
- **Bouncer**: Host Firewall Bouncer protects the ports.

## 5. Deployment command

To redeploy or update this stack:

```bash
ansible-playbook site.yml --tags "containers/media"
```
