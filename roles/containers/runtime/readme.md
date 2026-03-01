# Runtime Role

**Audit Event Identifier:** DSU-PLY-100130  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role installs and configures the core container runtime environment, including Podman, Netavark, and GPU support.

## Architecture

```mermaid
graph TD
    subgraph Runtime Core
        PODMAN[Podman] --> NET(Netavark)
        PODMAN --> DNS(Aardvark DNS)
        PODMAN --> RUNC(crun/runc)
        
        PODMAN --> QUAD[Quadlets]
        QUAD --> SYSTEMD[Systemd Units]
    end
    
    subgraph Hardware Support
        PODMAN --> GPU_DISP[GPU Dispatcher]
        GPU_DISP --> NVIDIA[NVIDIA CDI]
        GPU_DISP --> AMD[AMD ROCm]
        GPU_DISP --> INTEL[Intel Compute]
    end
    
    subgraph Security
        PODMAN --> SECCOMP[Seccomp Profiles]
        PODMAN --> APP_ARMOR[AppArmor/SELinux]
        PODMAN --> ROOTLESS[Rootless User NS]
    end
    
    classDef core fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef hw fill:#fff3e0,stroke:#ff6f00,stroke-width:2px;
    classDef sec fill:#ffebee,stroke:#c62828,stroke-width:2px;
    
    class PODMAN,NET,DNS,RUNC,QUAD,SYSTEMD core;
    class GPU_DISP,NVIDIA,AMD,INTEL hw;
    class SECCOMP,APP_ARMOR,ROOTLESS sec;
```

## Features
- **Podman**: Daemonless container engine.
- **Rootless**: Full rootless container support via user namespaces.
- **Quadlets**: Native Systemd integration for containers.
- **GPU Support**: Auto-detection and configuration for NVIDIA, AMD, and Intel.
- **Security**: Hardened defaults, Seccomp profiles, and AppArmor/SELinux integration.

## Usage

```yaml
- name: Setup Container Runtime
  hosts: all
  roles:
    - containers/runtime
```
