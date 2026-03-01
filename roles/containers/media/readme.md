# Media Role

**Audit Event Identifier:** DSU-PLY-100090  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role deploys a complete media streaming and management stack, including Jellyfin, Plex, and the *Arr suite.

## Architecture

```mermaid
graph TD
    subgraph Media Stack
        P[Plex] --> STORAGE[(Media Storage)]
        J[Jellyfin] --> STORAGE
        
        RAD[Radarr] --> DL[Download Clients]
        SON[Sonarr] --> DL
        LID[Lidarr] --> DL
        READ[Readarr] --> DL
        
        DL --> STORAGE
        
        RAD --> P
        RAD --> J
        SON --> P
        SON --> J
    end
    
    subgraph Network
        P --> PROXY(Caddy)
        J --> PROXY
        RAD --> PROXY
        SON --> PROXY
    end
    
    classDef app fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef store fill:#fff3e0,stroke:#ff6f00,stroke-width:2px;
    classDef net fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    
    class P,J,RAD,SON,LID,READ,DL app;
    class STORAGE store;
    class PROXY net;
```

## Features
- **Streaming**: Jellyfin and Plex media servers.
- **Management**: Radarr (Movies), Sonarr (TV), Lidarr (Music), Readarr (Books).
- **Requests**: Jellyseerr for unified media requests.
- **Downloads**: Transmission and other download clients.
- **Multi-Tenancy**: Support for multiple users and libraries.

## Usage

```yaml
- name: Deploy Media Stack
  hosts: media_nodes
  roles:
    - containers/media
```
