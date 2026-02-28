# Roles Architecture

**Audit Event Identifier:** DSU-MMD-190005  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-02-28  

This directory contains all the Ansible roles used in the Deploy-System-Unified project, organized logically by domain.

## Organization Map

```mermaid
graph TD
    ROLES[roles/] --> CORE[core/]
    ROLES --> SEC[security/]
    ROLES --> CONT[containers/]
    ROLES --> K8S[kubernetes/]
    ROLES --> NET[networking/]
    ROLES --> OPS[ops/]
    ROLES --> HW[hardware/]
    ROLES --> STOR[storage/]
    ROLES --> VIRT[virtualization/]
    
    CORE -->|System Baseline| CORE_SUB(Bootstrap, Identity, Logging...)
    SEC -->|Hardening| SEC_SUB(SSHD, Sandbox, Audit...)
    CONT -->|Workloads| CONT_SUB(Runtime, Media, AI...)
    K8S -->|Orchestration| K8S_SUB(Master, Worker)
    
    classDef main fill:#bbf,stroke:#333,stroke-width:2px;
    class ROLES main;
```
