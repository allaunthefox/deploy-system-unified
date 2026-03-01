# Role Reference

## Containers Roles

### `containers/ai`
**ai**



### `containers/anubis`
**anubis**



### `containers/archive`
**archive**



### `containers/authentik`
**authentik**



### `containers/caddy`
**caddy**



### `containers/common`
**common**



### `containers/config`
**config**



### `containers/home_assistant`
**home_assistant**



### `containers/immich`
**immich**



### `containers/life`
**life**



### `containers/lxc`
**lxc**



### `containers/media`
**Media Container Role**

This role deploys a comprehensive media stack using Podman Quadlets. It supports multi-tenancy, allowing multiple isolated instances of the stack to run on a single host.

### `containers/memcached`
**memcached**



### `containers/monitoring`
**Container Monitoring Role**

This role uses Podman Quadlets to deploy a monitoring stack consisting of Prometheus and Grafana.

### `containers/networking`
**networking**



### `containers/ops`
**Ops Container Role**

This role deploys operational dashboard and utility tools alongside the media stack.

### `containers/quadlets`
**Quadlets Role**

This role manages **Podman Quadlets**, which are Systemd generator files for containers. It ensures that container networks and services are managed natively by Systemd, providing robustness and auto-start capabilities.

### `containers/runtime`
**Container Runtime Role**

This role handles the installation and configuration of the container runtime environment (Podman/Docker) and associated hardware support (GPU).

### `containers/security`
**security**



### `containers/signing`
**Cosign Container Image Signing Role**

This role provides Cosign container image signing and verification for the deploy-system-unified project.

## Core Roles

### `core/bootstrap`
**bootstrap**



### `core/entropy`
**entropy**



### `core/grub`
**grub**



### `core/hardware_support`
**hardware_support**



### `core/identity`
**identity**



### `core/logging`
**logging**



### `core/memory`
**memory**



### `core/repositories`
**repositories**



### `core/secrets`
**secrets**



### `core/systemd`
**systemd**



### `core/time`
**time**



### `core/updates`
**updates**



## Hardware Roles

### `hardware/firmware`
**firmware**



### `hardware/gpu`
**gpu**



### `hardware/sas`
**Hardware SAS Role (`hardware/sas`)**

This role provides support for Serial Attached SCSI (SAS) infrastructure, spanning legacy SAS-2 (6G) to modern SAS-3 (12G) and SAS-4 (24G) storage fabrics. It handles driver loading, tooling, and performance tuning for queue depths.

### `hardware/storage_tuning`
**storage_tuning**



### `hardware/virtual_guest`
**virtual_guest**



## Kubernetes Roles

### `kubernetes/ingress`
**ingress**



### `kubernetes/master`
**master**



### `kubernetes/node`
**node**



## Networking Roles

### `networking/container_networks`
**container_networks**



### `networking/desktop`
**desktop**



### `networking/firewall`
**firewall**



### `networking/istio`
**istio**



### `networking/physical`
**Networking Physical Role (`networking/physical`)**

This role manages physical network interface optimizations, specifically identifying interface speeds (1G, 2.5G, 10G, 25G, 40G, 100G) and identifying physical media types (Twisted Pair vs Fiber/DAC).

### `networking/services`
**services**



### `networking/virtual`
**virtual**



### `networking/vpn_mesh`
**vpn_mesh**



## Ops Roles

### `ops/cloud_init`
**cloud_init**



### `ops/connection_info`
**connection_info**



### `ops/forensics`
**forensics**



### `ops/guest_management`
**guest_management**



### `ops/health_check`
**health_check**



### `ops/monitoring`
**Monitoring Role (`ops/monitoring`)**

This role deploys standard system monitoring agents and tools. It focuses on OS-level observability, providing metrics and health checks.

### `ops/pre_connection`
**pre_connection**



### `ops/preflight`
**preflight**



### `ops/session`
**session**



## Orchestration Roles

### `orchestration/k8s_node`
**k8s_node**



## Security Roles

### `security/access`
**access**



### `security/advanced`
**Advanced Security Hardening Role**

This role provides optional advanced security hardening features that can be enabled in profile branches. These features are designed to be optional additions to the standard security configuration and should not affect the main branch functionality.

### `security/audit_integrity`
**security/audit_integrity**

Implements Forward Secure Sealing (FSS) for systemd journal logs, ensuring tamper-evident audit trails with cryptographic verification.

### `security/automated_threat_analysis`
**automated_threat_analysis**



### `security/compliance`
**compliance**



### `security/database_hardening`
**database_hardening**



### `security/falco`
**Falco Runtime Security Role**

This role provides Falco runtime security monitoring for the deploy-system-unified project.

### `security/file_integrity`
**file_integrity**



### `security/firejail`
**firejail**



### `security/goss`
**Goss Continuous Monitoring Role**

This role provides Goss-based continuous security monitoring for the deploy-system-unified project.

### `security/hardening`
**hardening**



### `security/hardware_isolation`
**hardware_isolation**



### `security/ima_enforcement`
**ima_enforcement**



### `security/ips`
**ips**



### `security/kernel`
**kernel**



### `security/kyverno`
**kyverno**



### `security/mac_apparmor`
**mac_apparmor**



### `security/openscap`
**openscap**



### `security/resource_protection`
**resource_protection**



### `security/sandboxing`
**sandboxing**



### `security/sbom`
**Role: security/sbom**

POL-SEC | Software Bill of Materials (SBOM) generation and supply-chain auditing.

### `security/scanning`
**security/scanning role**

This role provides a comprehensive security framework for the Deploy-System-Unified project, including system validation, secure time synchronization, security tool configuration (trivy, aide, lynis, etc.), and secure handling of temporary files and SSH information.

### `security/sshd`
**sshd**



### `security/tpm_guard`
**tpm_guard**



### `security/vault_integration`
**HashiCorp Vault Integration Role**

This role provides HashiCorp Vault integration for the deploy-system-unified project.

## Shared Roles

## Sshd Roles

## Storage Roles

### `storage/backup`
**backup**



### `storage/dedupe`
**Role: storage/dedupe**

WI-CONT | NoDupeLabs archival standards for Btrfs deduplication.

### `storage/filesystems`
**filesystems**



## Virtualization Roles

### `virtualization/kvm`
**kvm**



### `virtualization/storage`
**storage**



