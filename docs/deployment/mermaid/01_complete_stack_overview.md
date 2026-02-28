---
title: Deploy-System-Unified - Complete Stack Overview
description: All 11 deployable stacks with their components and relationships
lastUpdated: 2026-02-28
auditEventIdentifier: DSU-MMD-100001
mermaidVersion: 1.2
rendererSupport:
  - github
  - gitlab
  - mermaid-live
---

```mermaid
graph TB
    subgraph "Kubernetes Helm Charts (10 stacks)"
        S01["📊 monitoring-stack<br/>Namespace: monitoring<br/>Components: Prometheus, Grafana, Alertmanager<br/>Priority: P0"]
        S02["🎬 media-stack<br/>Namespace: media<br/>Components: Jellyfin, Radarr, Sonarr<br/>Priority: P1"]
        S03["📝 logging-stack<br/>Namespace: logging<br/>Components: Loki, Promtail<br/>Priority: P0"]
        S04["🗄️ database-stack<br/>Namespace: database<br/>Components: PostgreSQL, Redis<br/>Priority: P0"]
        S05["🔐 auth-stack<br/>Namespace: auth<br/>Components: Authentik<br/>Priority: P1<br/>Depends: database-stack"]
        S06["💾 backup-stack<br/>Namespace: backup<br/>Components: Restic, Rclone<br/>Priority: P2"]
        S07["🌐 network-stack<br/>Namespace: network<br/>Components: Pi-hole, WireGuard<br/>Priority: P1"]
        S08["🔀 proxy-stack<br/>Namespace: proxy<br/>Components: Caddy<br/>Priority: P0"]
        S09["⚙️ ops-stack<br/>Namespace: ops<br/>Components: Homarr, Vaultwarden<br/>Priority: P2"]
        S10["🛡️ security-stack<br/>Namespace: security<br/>Components: CrowdSec, Trivy<br/>Priority: P1"]
    end

    subgraph "Podman Containers (1 stack)"
        S11["🤖 anubis<br/>Type: Container (Podman)<br/>Components: Anubis AI Firewall<br/>Priority: P0<br/>Port: 8080<br/>Depends: proxy-stack"]
    end

    subgraph "Dependencies"
        S05 -.->|Requires| S04
        S11 -.->|Protects| S08
        S09 -.->|Optional Auth| S05
        S10 -.->|Logs to| S03
        S06 -.->|Backs up| S01
        S06 -.->|Backs up| S04
    end

    classDef k8s fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    classDef podman fill:#ffe1e1,stroke:#cc0000,stroke-width:2px
    classDef dependency fill:#f5f5f5,stroke:#666,stroke-width:1px,stroke-dasharray:5 5

    class S01,S02,S03,S04,S05,S06,S07,S08,S09,S10 k8s
    class S11 podman
    class S05,S09,S10,S06 dependency
```

---

## 📋 Stack Details

| Stack | Namespace | Priority | Components |
|-------|-----------|----------|------------|
| monitoring-stack | monitoring | P0 | Prometheus, Grafana, Alertmanager |
| media-stack | media | P1 | Jellyfin, Radarr, Sonarr |
| logging-stack | logging | P0 | Loki, Promtail |
| database-stack | database | P0 | PostgreSQL, Redis |
| auth-stack | auth | P1 | Authentik |
| backup-stack | backup | P2 | Restic, Rclone |
| network-stack | network | P1 | Pi-hole, WireGuard |
| proxy-stack | proxy | P0 | Caddy |
| ops-stack | ops | P2 | Homarr, Vaultwarden |
| security-stack | security | P1 | CrowdSec, Trivy |
| anubis | N/A (Podman) | P0 | Anubis AI Firewall |

---

## 🔗 See Also

- [Deployment Profiles](./02_deployment_profiles.md) - Which stacks are in each profile
- [Stack Dependencies](./03_stack_dependencies.md) - Detailed dependency graph
- [Incompatibilities](./04_incompatibilities.md) - Combinations to avoid
