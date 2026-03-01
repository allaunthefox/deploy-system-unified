---
title: Network Security Posture
description: High-level visualization of the network security posture including microsegmentation, admission control fail-safes, and host-level isolation.
lastUpdated: 2026-02-28
auditEventIdentifier: DSU-MMD-160002
mermaidVersion: 1.2
rendererSupport:
  - github
  - gitlab
  - mermaid-live
---

# Network Security Posture

This diagram illustrates the atomic layers of network security, from the host firewall up through the Kubernetes zero-trust mesh.

```mermaid
graph TD
    %% Define styles
    classDef external fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef host fill:#e8f5e9,stroke:#2e7d32;
    classDef cluster fill:#e3f2fd,stroke:#1565c0;
    classDef mesh fill:#fff3e0,stroke:#ef6c00;
    classDef failsafe fill:#f3e5f5,stroke:#7b1fa2;

    %% External Entry
    Internet((Internet / External)):::external

    %% Host Level Isolation
    subgraph "Host Networking (Systemd-Networkd & Firewall)"
        UFW[UFW/Firewalld<br>Dynamic Port Allowlist]:::host
        IsoNet[Systemd Isolate=1<br>Backend Container Networks]:::host
    end

    %% Cluster Level Components
    subgraph "Kubernetes Boundary"
        ING[Ingress Controller<br>TLS Termination]:::cluster
        
        %% Mesh Level
        subgraph "Istio Service Mesh (Layer 7)"
            MTLS[Strict mTLS Enforcement<br>Zero-Trust Pod-to-Pod]:::mesh
            SWG[Istio Sidecar Proxies<br>Traffic Filtering]:::mesh
        end

        %% Workload Network Policies
        subgraph "Kubernetes NetworkPolicies (Layer 3/4)"
            NP_Media[Media-Stack NetworkPolicy<br>Explicit Allow]:::cluster
            NP_Log[Logging-Stack NetworkPolicy<br>Explicit Allow]:::cluster
        end

        %% Fail-Safe Layer
        subgraph "Admission Control (Kyverno)"
            GenPol[generate-default-deny<br>ClusterPolicy]:::failsafe
            DefDeny[Default-Deny All Ingress/Egress<br>Injected NetworkPolicy]:::failsafe
        end
    end

    %% Flow Dynamics
    Internet -- HTTPS --> UFW
    UFW -- Port 443 --> ING
    ING -- Routed --> SWG
    
    %% Traffic through Mesh
    SWG -- Encrypted Traffic --> MTLS
    MTLS -. Evaluates .-> NP_Media
    MTLS -. Evaluates .-> NP_Log
    
    %% Fail-safe Enforcement
    GenPol -- "Namespace Created" --> DefDeny
    DefDeny -. "Fallback if Custom NP Missing" .-> MTLS

    %% Host relationships
    IsoNet -. "Restricts Raw Container IFs" .-> UFW
```

---

## 🛡️ Key Security Postures Illustrated

| Component | Responsibility | Protection Level |
|-----------|----------------|------------------|
| **UFW / Firewalld** | Drops unlisted physical/TCP traffic before hitting the cluster. | Host / Node |
| **Systemd Networks** | `isolate=1` physical definitions ensure backend docker/raw containers can't natively route out. | Host / Docker |
| **Istio Strict mTLS** | Enforces zero-trust cryptographic identity and encryption for all intra-cluster pod communications. | Service Mesh (L7) |
| **App NetworkPolicies** | Atomic policies natively bound to Helm charts for tight L3/L4 control. | Kubernetes (L3/L4) |
| **Kyverno Fail-safe** | Mutating admission controller that guarantees a default-deny NetworkPolicy exists in every namespace. | Cluster Global |
