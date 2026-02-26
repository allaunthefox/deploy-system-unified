# Cross-Runtime Isolation: LXC & Kubernetes

**Standard**: DSU-6767-X  
**Compliance**: ISO 27001 §8.22 (Segregation of Networks) / NIST SP 800-190

---

## 📖 Overview

In complex stacks where **LXC (LXD)** and **Kubernetes (K3s)** coexist on the same host, there is a risk of "Runtime Bleed" where isolation boundaries are bypassed via shared kernel resources or overlapping subnets.

---

## 🚨 Identified Risks

1.  **Subnet Overlap**: If LXC's `lxcbr0` and K3s's `cni0` use the same CIDR, routing becomes non-deterministic.
2.  **Unprotected Inter-Runtime Traffic**: Traffic moving directly between an LXC container and a K3s pod bypasses the **Layer 5 (Caddy)** ingress controls.
3.  **Privilege Escalation**: Privileged LXC containers can monitor K3s namespace traffic if not restricted by **Layer 2 (AppArmor)**.

---

## 🛡️ Mandatory Hardening Rules

### 1. Explicit Network Segregation
- **Rule**: LXC and K3s MUST use non-overlapping CIDRs.
- **Verification**: `ops/preflight` now checks for CIDR conflicts.

### 2. Forensic Tagging
- **Rule**: Every interaction between runtimes must be tagged with **Action Code 820205** (K8s Service Created) or **700030** (Network Create).

### 3. Ingress-Only Communication
- **Rule**: All traffic between an LXC application and a Kubernetes service MUST pass through the **Caddy Reverse Proxy**.
- **Implementation**:
    - App in LXC calls `service.example.com` (Caddy).
    - Caddy proxies to K3s internal IP.
    - *Direct IP-to-IP communication is forbidden.*

---

## 🛠️ Configuration Example

**Safe Cross-Runtime Link (Caddyfile):**
```caddy
# Bridge LXC to K3s securely
api.internal.host {
    reverse_proxy 10.43.0.10:8080 # K3s Service Cluster IP
}
```

---

*Verified by: DSU Security Architect*
*Last Updated: February 2026*
