# Service Mesh Role

**Audit Event Identifier:** DSU-PLY-100900  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role deploys and configures a lightweight service mesh (Linkerd) for the K3s cluster, enabling automatic mTLS and service observability.

## Architecture

```mermaid
graph LR
    subgraph "Service Mesh Control Plane"
        CP[Linkerd Controller] --> ID[Identity Service]
        ID --> CA[Trust Anchor]
    end
    
    subgraph "Data Plane (Pod A)"
        A_APP[Application] <--> A_PROXY[Linkerd Proxy]
    end
    
    subgraph "Data Plane (Pod B)"
        B_PROXY[Linkerd Proxy] <--> B_APP[Application]
    end
    
    A_PROXY <== "mTLS Encrypted Tunnel" ==> B_PROXY
    
    classDef control fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef proxy fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef app fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    class CP,ID,CA control;
    class A_PROXY,B_PROXY proxy;
    class A_APP,B_APP app;
```

## Features
- **Automatic mTLS**: Transparent service-to-service encryption.
- **Ultra-Lightweight**: Rust-based proxies optimized for K3s edge nodes.
- **Observability**: Real-time golden metrics (Success rate, Latency, Throughput).
- **Security**: Automated certificate rotation and strict identity verification.

## Usage

```yaml
- name: Deploy Service Mesh
  hosts: master
  roles:
    - kubernetes/service_mesh
```
