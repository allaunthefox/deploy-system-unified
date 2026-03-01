# Ops Role

**Audit Event Identifier:** DSU-PLY-100026  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role deploys operational support containers including dashboards, password managers, and documentation wikis.

## Architecture

```mermaid
graph TD
    subgraph Ops Stack
        HOMARR[Homarr Dashboard] --> PROXY(Caddy Proxy)
        VAULT[Vaultwarden] --> PROXY
        WIKI[Wiki.js] --> PROXY
        WASTE[Wastebin] --> PROXY
        FILE[Filebrowser] --> PROXY
        
        WIKI --> DB[(Wiki Postgres)]
        VAULT --> PERSIST[(Persistent Vol)]
        
        PROXY --> NET[ops_net]
    end
    
    USER((Admin User)) --> PROXY
    
    classDef container fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef db fill:#fff3e0,stroke:#ff6f00,stroke-width:2px;
    class HOMARR,VAULT,WIKI,WASTE,FILE,PROXY container;
    class DB,PERSIST db;
```

## Features
- **Homarr**: Centralized dashboard for all services.
- **Vaultwarden**: Self-hosted Bitwarden compatible password manager.
- **Wiki.js**: Documentation platform (Postgres backend).
- **Wastebin**: Minimalist pastebin.
- **Filebrowser**: Web-based file manager.

## Usage

```yaml
- name: Deploy Ops Stack
  hosts: container_nodes
  roles:
    - containers/ops
```
