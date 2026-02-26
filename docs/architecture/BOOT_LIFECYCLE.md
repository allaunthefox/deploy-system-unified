# Explicit Boot Lifecycle & Forensic Chain of Trust

**Standard**: DSU-6767-B  
**Compliance**: NIST SP 800-193 (Platform Integrity) / ISO 27001 §12.4  
**Scope**: All Hardware & Virtualization Runtimes

---

## 🛰️ The Forensic Boot Sequence

This document defines the mandatory execution order during system startup. No layer may initialize until its forensic predecessor has verified the environment.

```mermaid
graph TD
    subgraph "Phase 1: Hardware Root of Trust"
        B1[UEFI / BIOS] -->|Secure Boot Verified| B2[GRUB Bootloader]
        B2 -->|Kernel Params Loaded| B3[Linux Kernel]
    end

    subgraph "Phase 2: Security Sentinel (Layer 2)"
        B3 -->|Enforce| MAC[AppArmor / SELinux]
        MAC -->|Action Code 440001| AUDIT[auditd Service]
    end

    subgraph "Phase 3: Network Gate (Layer 1)"
        AUDIT -->|Code 540000| FW[Firewall: Default-Deny]
        FW -->|Bridge Ready| NET[Container Bridges]
    end

    subgraph "Phase 4: Runtime Execution (Layer 4)"
        NET -->|Systemd User| P[Podman Quadlets]
        NET -->|Systemd System| L[LXC / LXD]
        NET -->|K3s Master| K[Kubernetes]
        
        P -->|Action Code 400020| ID[UUID Assigned]
        L -->|Action Code 400020| ID
        K -->|Action Code 400020| ID
    end

    subgraph "Phase 5: Forensic Aggregation"
        ID -->|Wait for Loki| LOG[Forensic Aggregator]
        LOG -->|Code 840040| DASH[Grafana Dashboard]
    end

    subgraph "Phase 6: Gateway Ingress (Layer 5)"
        LOG -->|Code 540000| CAD[Caddy Reverse Proxy]
        CAD -->|Forward Auth| AUTH[Authentik]
        CAD -->|Code 540001| READY((SYSTEM ONLINE))
    end

    style READY fill:#dfd,stroke:#333,stroke-width:4px
    style MAC fill:#fdd,stroke:#333
    style FW fill:#fdd,stroke:#333
```

---

## 🛡️ Forensic Dependency Rules

1.  **Rule [B-01] (The MAC Mandate)**: The Linux Kernel MUST load AppArmor/SELinux profiles before any user-space services are spawned.
2.  **Rule [B-02] (The Aggregator Wait)**: Runtimes (LXC/Podman) MUST perform a TCP handshake check with the Forensic Aggregator (Loki) before emitting their first `Container Start` event.
3.  **Rule [B-03] (The Ingress Lock)**: Caddy MUST NOT open Port 443 until the Authentik identity service reports a healthy state via its local API.

---

*Verified by: DSU Platform Architect*  
*Last Updated: February 2026*
