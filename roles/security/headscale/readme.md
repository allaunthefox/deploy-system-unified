# Headscale Role

**Audit Event Identifier:** DSU-PLY-100800  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role deploys and configures the Headscale controller, an open-source, self-hosted implementation of the Tailscale control server.

## Architecture

```mermaid
graph TD
    subgraph "Zero Trust Control Plane"
        HS[Headscale Controller] --> DB[(SQLite/Postgres)]
        HS --> API[GRPC/REST API]
    end
    
    subgraph "Overlay Network (100.64.0.0/10)"
        NODE_A[Linux Node A] <--> HS
        NODE_B[Linux Node B] <--> HS
        NODE_A <-->|Wireguard P2P| NODE_B
    end
    
    ADMIN[Admin CLI] --> API
    
    classDef controller fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef node fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    class HS,DB,API controller;
    class NODE_A,NODE_B node;
```

## Features
- **Self-Hosted**: Full control over your coordination server.
- **MagicDNS**: Internal DNS resolution for the tailnet.
- **Namespace Isolation**: Segment nodes into logical namespaces.
- **Hardened**: Runs as a dedicated system user with strict directory permissions.

## Usage

```yaml
- name: Deploy Headscale Controller
  hosts: management_nodes
  roles:
    - security/headscale
```
