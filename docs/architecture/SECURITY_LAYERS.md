# Security Architecture: Defense-in-Depth

**Audit Event Identifier:** DSU-MMD-180001  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-02-28  

This document visualizes the 5-layer security model enforced by **Deploy-System-Unified**. Each layer must be successfully provisioned and verified before the next layer is applied.

```mermaid
graph TB
    subgraph "Layer 1: Pod Security"
        PSC["Pod Security Context<br/>runAsNonRoot: true<br/>runAsUser: <app-specific><br/>seccompProfile: RuntimeDefault"]
        CSC["Container Security Context<br/>allowPrivilegeEscalation: false<br/>capabilities.drop: ALL<br/>readOnlyRootFilesystem"]
    end

    subgraph "Layer 2: RBAC"
        SA["ServiceAccount<br/>Per-stack identity"]
        ROLE["Role/ClusterRole<br/>Minimal permissions"]
        ROLEBIND["RoleBinding<br/>SA to Role binding"]
    end

    subgraph "Layer 3: Network Security"
        NP["Network Policies<br/>Pod isolation"]
        TLS["TLS Termination<br/>HTTPS encryption"]
        ING["Ingress Class<br/>Traffic routing"]
    end

    subgraph "Layer 4: Secrets Management"
        SOPS["SOPS Encryption<br/>Secrets at rest"]
        K8S["Kubernetes Secrets<br/>Runtime access"]
    end

    subgraph "Layer 5: Monitoring & Audit"
        AUDIT["Audit Event Identifiers<br/>ISO 27001 mapped"]
        MON["Monitoring Stack<br/>Prometheus/Grafana"]
        LOG["Logging Stack<br/>Loki/Promtail"]
    end

    PSC --> CSC
    CSC --> SA
    SA --> ROLE
    ROLE --> ROLEBIND
    ROLEBIND --> NP
    NP --> TLS
    TLS --> ING
    ING --> SOPS
    SOPS --> K8S
    K8S --> AUDIT
    AUDIT --> MON
    MON --> LOG

    classDef layer1 fill:#e3f2fd,stroke:#1565c0
    classDef layer2 fill:#e8f5e9,stroke:#2e7d32
    classDef layer3 fill:#fff3e0,stroke:#ef6c00
    classDef layer4 fill:#f3e5f5,stroke:#7b1fa2
    classDef layer5 fill:#ffebee,stroke:#c62828

    class PSC,CSC layer1
    class SA,ROLE,ROLEBIND layer2
    class NP,TLS,ING layer3
    class SOPS,K8S layer4
    class AUDIT,MON,LOG layer5
```

---

## 🛡️ The 5-Layer Model

| Layer | Name | Roles Involved | Audit Event Identifier Range | Purpose |
|-------|------|----------------|-----------------------------|---------|
| **1** | Pod Security | `containers/runtime`, `containers/quadlets` | `70xxxx` | Container isolation via security contexts |
| **2** | RBAC | `kubernetes/rbac`, `core/identity` | `30xxxx` | Least-privilege access control |
| **3** | Network Security | `networking/firewall`, `containers/caddy` | `54xxxx` | Traffic isolation and encryption |
| **4** | Secrets Management | `core/secrets`, `security/tpm_guard` | `45xxxx` | Encrypted secrets at rest and in transit |
| **5** | Monitoring & Audit | `core/logging`, `security/audit_integrity` | `84xxxx` | Forensic traceability and alerting |

---

## 🔗 Related Documentation

- [Security Architecture Overview](../deployment/mermaid/07_security_architecture.md) - Detailed security diagram
- [Forensic Flow](./FORENSIC_FLOW.md) - How audit events flow to Loki
- [Boot Lifecycle](./BOOT_LIFECYCLE.md) - Security during system startup

---

*Standard: ISO 27001 §8.20 (Network Security)*
*Last Updated: 2026-02-28*
