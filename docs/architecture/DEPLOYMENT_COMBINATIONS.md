# Master Deployment Combination Matrix

This document provides a visual guide to the supported and experimental combinations within the **Deploy-System-Unified** ecosystem.

---

## 🛰️ Deployment Decision Tree

This diagram maps the path from selecting a security posture to the final application workload.

```mermaid
graph TD
    START((Start Deployment)) --> POSTURE{Select Posture}
    
    %% Posture Selection
    POSTURE -->|High Volatility| EPH[Ephemeral]
    POSTURE -->|Security Baseline| HRD[Hardened]
    POSTURE -->|Full Workload| PRD[Production]

    %% Platform Selection
    EPH --> PLAT_E{Platform}
    HRD --> PLAT_H{Platform}
    PRD --> PLAT_P{Platform}

    PLAT_E --> BM_E[Bare Metal]
    PLAT_E --> VM_E[KVM Guest]
    
    PLAT_H --> VPS_H[VPS / Cloud]
    PLAT_H --> BM_H[Bare Metal]
    
    PLAT_P --> BM_P[Bare Metal]
    PLAT_P --> CLD_P[AWS/Azure/GCP]

    %% Architecture Gates
    BM_E & VM_E & VPS_H & BM_H & BM_P & CLD_P --> ARCH{Architecture}
    
    ARCH -->|Verified| X86[x86_64]
    ARCH -->|Experimental| ARM[aarch64]
    ARCH -->|Experimental| RISC[riscv64]

    %% Workload Stacks
    X86 & ARM & RISC --> STACK{Workload Stack}

    subgraph "Core Solution Stacks"
        STACK --> EDGE[Edge: Caddy + Anubis + Authentik]
        STACK --> MEDIA[Media: Jellyfin + ARR + Immich]
        STACK --> LIFE[Life: Mealie + Paperless + Firefly]
        STACK --> AI[AI: Ollama + Open WebUI]
        STACK --> ARCHIVE[Archive: TubeArchivist + Kiwix]
        STACK --> OPS[Ops: Homarr + Vaultwarden + Syncthing]
        STACK --> K8S[K8s: K3s + Helm Charts]
    end

    %% Status Indicators
    style X86 fill:#dfd,stroke:#333
    style ARM fill:#fdf,stroke:#333,stroke-dasharray: 5 5
    style RISC fill:#fdf,stroke:#333,stroke-dasharray: 5 5
    style PRD fill:#bbf,stroke:#333,stroke-width:2px
```

---

## 📊 Compatibility & Support Matrix

| Dimension | Option | Audit Log Retention Class | Status |
| :--- | :--- | :--- | :--- |
| **Posture** | `ephemeral` | Minimal Footprint | Stable |
| | `hardened` | High Integrity | Stable |
| | `production` | Full Observability | Stable |
| **Platform** | Bare Metal | Full HW Access | Verified |
| | VPS / Cloud | Network Constrained | Verified |
| | KVM / LXC | Resource Isolated | Verified |
| **Arch** | `x86_64` | Native | Stable |
| | `aarch64` | Emulated/Exp | **Experimental** |
| | `riscv64` | Emulated/Exp | **Experimental** |

---

## 🛠️ Combined Profile Logic

The project prevents "Forbidden Combinations" via preflight assertions:
1.  **Strict Singularity**: A host cannot be both `ephemeral` and `production`.
2.  **Architecture Guard**: Non-x86 deployments trigger an `experimental` warning (Code 600030).
3.  **Storage Guard**: Ephemeral hosts are blocked from mounting persistent `/srv` data unless explicitly authorized.

*Verified by: DSU Orchestrator*  
*Compliance: ISO 9001 / ISO 27001 §17.1*
