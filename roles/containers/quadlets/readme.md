# Quadlets Role

**Audit Event Identifier:** DSU-PLY-100117  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role manages the deployment of Podman Quadlet files, which allow Systemd to natively manage containers as services.

## Architecture

```mermaid
graph TD
    subgraph Configuration
        YAML[Quadlet Definition] --> GEN(Systemd Generator)
        GEN --> UNIT[Service Unit]
    end
    
    subgraph Execution
        UNIT --> PODMAN[Podman]
        PODMAN --> CONTAINER[Container Process]
    end
    
    subgraph Security
        UNIT --> SECCOMP[Seccomp Profile]
        UNIT --> USER[User Namespace]
    end
    
    classDef config fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef exec fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef sec fill:#ffebee,stroke:#c62828,stroke-width:2px;
    
    class YAML,GEN,UNIT config;
    class PODMAN,CONTAINER exec;
    class SECCOMP,USER sec;
```

## Features
- **Native Integration**: Treat containers like standard system services.
- **Dependency Management**: Define startup order and dependencies using Systemd logic.
- **Rootless Support**: Seamless deployment of user-scoped Quadlets.
- **Auto-Updates**: Integration with Podman Auto-Update for image freshness.

## Usage

```yaml
- name: Deploy Quadlets
  hosts: container_nodes
  roles:
    - containers/quadlets
```
