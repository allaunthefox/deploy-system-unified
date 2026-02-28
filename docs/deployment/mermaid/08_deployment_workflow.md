---
title: Deployment Workflow & Validation
description: Complete deployment workflow from planning to validation
lastUpdated: 2026-02-28
auditEventIdentifier: DSU-MMD-170001
mermaidVersion: 1.2
rendererSupport:
  - github
  - gitlab
  - mermaid-live
diagramType: sequenceDiagram
---

```mermaid
sequenceDiagram
    participant User
    participant Preflight
    participant Ansible
    participant K8s
    participant Helm
    participant Validation

    User->>Preflight: 1. Run preflight checks
    Preflight->>Preflight: Validate secrets
    Preflight->>Preflight: Check resources
    Preflight->>Preflight: Verify inventory
    Preflight-->>User: ✅ Preflight passed

    User->>Ansible: 2. Deploy base hardening
    Ansible->>K8s: Install K3s
    K8s-->>Ansible: ✅ K3s ready

    User->>Ansible: 3. Deploy Helm charts
    loop For each stack
        Ansible->>Helm: helm install <stack>
        Helm->>K8s: Create namespace
        Helm->>K8s: Apply manifests
        K8s-->>Helm: ✅ Stack deployed
    end

    User->>Validation: 4. Validate deployment
    Validation->>K8s: Check pods running
    Validation->>K8s: Check services
    Validation->>K8s: Check PVCs
    Validation->>Validation: Run security checks
    Validation-->>User: ✅ Validation passed

    User->>User: 5. Post-deployment tasks
    Note over User: Configure DNS<br/>Import dashboards<br/>Test backups<br/>Configure alerts

    classDef user fill:#e3f2fd,stroke:#1565c0
    classDef check fill:#e8f5e9,stroke:#2e7d32
    classDef deploy fill:#fff3e0,stroke:#ef6c00
    classDef validate fill:#f3e5f5,stroke:#7b1fa2

    class User user
    class Preflight,Validation check
    class Ansible,K8s,Helm deploy
```

---

## 📋 Deployment Phases

| Phase | Description | Validation |
|-------|-------------|------------|
| **1: Preflight** | Validate secrets, resources, inventory | Secrets exist, resources available |
| **2: Base Hardening** | Install K3s, apply security baseline | K3s cluster ready |
| **3: Helm Charts** | Deploy stacks in dependency order | All pods running |
| **4: Validation** | Check pods, services, PVCs, security | All checks pass |
| **5: Post-Deployment** | DNS, dashboards, backups, alerts | System operational |

---

## 🔗 See Also

- [Stack Dependencies](./03_stack_dependencies.md) - Deployment order reference
- [Security Architecture](./07_security_architecture.md) - Security controls applied
- [Boot Lifecycle](../../architecture/BOOT_LIFECYCLE.md) - System boot sequence
- [Forensic Flow](../../architecture/FORENSIC_FLOW.md) - Audit event flow
