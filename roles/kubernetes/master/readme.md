# K3s Master Role

**Audit Event Identifier:** DSU-PLY-100583  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role deploys and configures the K3s control plane, supporting both standalone and high-availability (HA) modes.

## Architecture (HA Mode)

```mermaid
graph TD
    subgraph "High Availability Control Plane"
        VIP[Virtual IP: Kube-VIP] --> M1[Master Node 1]
        VIP --> M2[Master Node 2]
        VIP --> M3[Master Node 3]
        
        M1 <--> ETCD[(Embedded Etcd)]
        M2 <--> ETCD
        M3 <--> ETCD
    end
    
    subgraph "Workload Nodes"
        W1[Worker Node 1] --> VIP
        W2[Worker Node 2] --> VIP
    end
    
    ADMIN[Cluster Admin] --> VIP
    
    classDef control fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef worker fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef storage fill:#fff3e0,stroke:#ff6f00,stroke-width:2px;
    class M1,M2,M3,VIP control;
    class W1,W2 worker;
    class ETCD storage;
```

## Features
- **HA Ready**: Automated etcd-backed control plane scaling.
- **Floating IP**: Integrated Kube-VIP for seamless master failover.
- **Declarative**: Fully managed via `/etc/rancher/k3s/config.yaml`.
- **Security**: Hardened TLS SANs and automated token orchestration.

## Usage

```yaml
- name: Deploy HA K3s Master
  hosts: masters
  roles:
    - kubernetes/master
```
