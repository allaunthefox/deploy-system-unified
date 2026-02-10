# Layered Security Architecture

Security in this project is not a single task but a multi-layered defense strategy. By strictly ordering the execution of security roles, we ensure a "Fail-Secure" posture.

## 🛡️ The Defense-in-Depth Model

### 1. Perimeter Defense (L3/L4)
**Role**: `networking/firewall`
- **Philosophy**: Default-Deny.
- **Action**: All incoming ports are closed *before* any service is installed. Only essential ports (e.g., SSH on a randomized port) are explicitly opened.

### 2. Identity & Access Control (L7)
**Role**: `security/access` & `security/sshd`
- **Philosophy**: Least Privilege.
- **Action**: SSH is hardened with strong ciphers and Ed25519 keys. Identity-based restrictions are applied using SSH Match blocks to control who can access specific subsystems.

### 3. Kernel & System Hardening
**Role**: `security/kernel` & `security/hardening`
- **Philosophy**: Attack Surface Reduction.
- **Action**: Sysctl tuning for network stack protection, IOMMU/DMA protection, and disabling of unused protocols (e.g., legacy filesystems).

### 4. Application Isolation
**Role**: `security/sandboxing` & `security/firejail`
- **Philosophy**: Process Containment.
- **Action**: High-risk applications are wrapped in sandboxes or Firejail profiles to prevent lateral movement in the event of a breach.

### 5. Integrity Verification
**Role**: `security/scanning`
- **Philosophy**: Trust but Verify.
- **Action**: Post-deployment audits verify that the system state matches the intended security posture. Scans identify weak permissions or unexpected changes.

## 🔄 Coordination

The layers work together via the **[Ontology](ONTOLOGY)**. Selecting a `hardened` profile automatically coordinates the settings across all five layers, ensuring that a change in the firewall policy is reflected in the access control and scanning logic.
