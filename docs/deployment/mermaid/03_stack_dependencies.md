---
title: Stack Dependencies & Relationships
description: Complete dependency graph showing which stacks depend on others
lastUpdated: 2026-02-28
auditEventIdentifier: DSU-MMD-120001
mermaidVersion: 1.2
rendererSupport:
  - github
  - gitlab
  - mermaid-live
---

```mermaid
graph TD
    subgraph "Tier 0 - No Dependencies (Can deploy first)"
        S01["📊 monitoring-stack"]
        S02["🎬 media-stack"]
        S03["📝 logging-stack"]
        S04["🗄️ database-stack"]
        S06["💾 backup-stack"]
        S07["🌐 network-stack"]
        S08["🔀 proxy-stack"]
        S10["🛡️ security-stack"]
    end

    subgraph "Tier 1 - Single Dependency"
        S05["🔐 auth-stack"]
        S11["🤖 anubis"]
    end

    subgraph "Tier 2 - Optional Dependencies"
        S09["⚙️ ops-stack"]
    end

    subgraph "Dependency Types"
        D1["🔴 Required"]
        D2["🟡 Optional"]
        D3["🔵 Integrates With"]
    end

    S05 ==>|Requires DB| S04
    S11 ==>|Protects| S08
    S09 -.->|Uses Auth| S05
    S10 -.->|Sends Logs| S03
    S06 -.->|Backs Up| S01
    S06 -.->|Backs Up| S04
    S06 -.->|Backs Up| S05

    classDef tier0 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef tier1 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef tier2 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef legend fill:#f5f5f5,stroke:#666,stroke-width:1px

    class S01,S02,S03,S04,S06,S07,S08,S10 tier0
    class S05,S11 tier1
    class S09 tier2
    class D1,D2,D3 legend

    linkStyle 0 stroke:#ff0000,stroke-width:3px
    linkStyle 1 stroke:#ff0000,stroke-width:3px
    linkStyle 2 stroke:#ffa500,stroke-width:2px,stroke-dasharray:5 5
    linkStyle 3,4,5,6 stroke:#0066cc,stroke-width:1px,stroke-dasharray:3 3
```

---

## 📋 Dependency Tiers

### Tier 0 - No Dependencies (Deploy First)
- monitoring-stack, media-stack, logging-stack, database-stack
- backup-stack, network-stack, proxy-stack, security-stack

### Tier 1 - Single Dependency
- **auth-stack** → requires database-stack
- **anubis** → protects proxy-stack

### Tier 2 - Optional Dependencies
- **ops-stack** → optionally uses auth-stack

---

## 🔗 See Also

- [Complete Stack Overview](./01_complete_stack_overview.md) - All stacks details
- [Deployment Workflow](./08_deployment_workflow.md) - Deployment order
- [Incompatibilities](./04_incompatibilities.md) - Combinations to avoid
