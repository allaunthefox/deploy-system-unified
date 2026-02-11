# Role_Reference

## Containers Roles

### `containers/anubis` — [Read details](roles/containers_anubis.md)
**Web AI Firewall**
Deploys the Anubis Web AI Firewall to protect ingress traffic.

### `containers/authentik` — [Read details](roles/containers_authentik.md)
**Identity Provider (Authentik)**
Deploys Authentik for identity management, featuring comprehensive secret validation and negative testing.

### `containers/caddy` — [Read details](roles/containers_caddy.md)
**Reverse Proxy (Caddy)**
Handles Caddy reverse proxy configuration with Red Team hardening for secrets.

### `containers/common` — [Read details](roles/containers_common.md)
**Shared Container Logic**
Common tasks and placeholders shared across container roles.

### `containers/config` — [Read details](roles/containers_config.md)
**General Container Config**
Manages storage directories and general environment configuration for container workloads.

### `containers/lxc` — [Read details](roles/containers_lxc.md)
**LXC GPU Passthrough**
Handles GPU slicing and passthrough configuration specifically for LXC containers.

### `containers/media` — [Read details](roles/containers_media.md)
**Media Container Role**
This role deploys a comprehensive media stack using Podman Quadlets with multi-tenancy support.

### `containers/memcached` — [Read details](roles/containers_memcached.md)
**Caching (Memcached)**
Deploys Memcached using Podman Quadlets for distributed memory caching.

### `containers/monitoring` — [Read details](roles/containers_monitoring.md)
**Container Monitoring Role**

This role uses Podman Quadlets to deploy a monitoring stack consisting of Prometheus and Grafana.

### `containers/ops` — [Read details](roles/containers_ops.md)
**Ops Container Role**

This role deploys operational dashboard and utility tools alongside the media stack.

### `containers/quadlets` — [Read details](roles/containers_quadlets.md)
**Quadlets Role**

This role manages **Podman Quadlets**, which are Systemd generator files for containers. It ensures that container networks and services are managed natively by Systemd, providing robustness and auto-start capabilities.

### `containers/runtime` — [Read details](roles/containers_runtime.md)
**Container Runtime Role**

This role handles the installation and configuration of the container runtime environment (Podman/Docker) and associated hardware support (GPU).

## Core Roles

### `core/bootstrap` — [Read details](roles/core_bootstrap.md)
**Core bootstrap role**
System initialization and base configuration.

### `core/entropy` — [Read details](roles/core_entropy.md)
**Entropy Enhancement**
Ensures high-quality random number generation by installing and configuring entropy enhancement services.

### `core/hardware_support` — [Read details](roles/core_hardware_support.md)
**Hardware Discovery & Requirements**
Discovers CPU features (AVX, AES-NI) and handles hardware acceleration requirements.



### `core/identity` — [Read details](roles/core_identity.md)
**Identity & UUID Generation**
Handles system identity, hostname configuration, and entropy-backed UUID generation for virtualization objects.

### `core/logging` — [Read details](roles/core_logging.md)
**Forensic Logging Readiness**
Ensures mandatory forensic readiness by configuring systemd-journal-remote and log aggregation tools.

### `core/memory` — [Read details](roles/core_memory.md)
**Memory Compression & Swap Optimization**
Handles intelligent memory compression (zRAM/zswap) and swap management based on workload profiles.

### `core/repositories` — [Read details](roles/core_repositories.md)
**Repository Management**
Ensures secure repository configuration and management of third-party sources (RPMFusion, etc.).



### `core/secrets` — [Read details](roles/core_secrets.md)
**Secrets Management & Integrity**
Handles secure secret deployment with built-in integrity verification and validation tasks.

### `core/systemd` — [Read details](roles/core_systemd.md)
**Systemd Configuration & Hardening**
Ensures systemd components (journald, resolved) are configured and hardened according to project standards.

### `core/time` — [Read details](roles/core_time.md)
**Time Synchronization**
Ensures accurate system time via idempotent installation and configuration of time synchronization services (Chrony).

### `core/updates` — [Read details](roles/core_updates.md)
**Automated Security Patching**
Configures automated security updates and unattended patching to maintain a secure fleet.



## Hardware Roles

### `hardware/firmware` — [Read details](roles/hardware_firmware.md)
**Bare Metal Foundation**
Manages microcode, firmware updates, and low-level system attributes for physical hardware.

### `hardware/gpu` — [Read details](roles/hardware_gpu.md)
**Unified GPU Stack**
Automatic discovery and driver installation for AMD, Intel, and NVIDIA GPUs across architectures.

### `hardware/sas` — [Read details](roles/hardware_sas.md)
**Hardware SAS Role (`hardware/sas`)**
This role provides support for Serial Attached SCSI (SAS) infrastructure, spanning legacy SAS-2 (6G) to modern SAS-3 (12G) and SAS-4 (24G) storage fabrics. It handles driver loading, tooling, and performance tuning for queue depths.

### `hardware/storage_tuning` — [Read details](roles/hardware_storage_tuning.md)
**Physical Storage Optimization**
Optimizes I/O schedulers, disk parameters, and filesystem-specific mount options.

### `hardware/virtual_guest` — [Read details](roles/hardware_virtual_guest.md)
**Cloud Instance Tuning**
Optimizes the operating system when running inside a virtualized environment (Contabo, Hetzner, Generic Cloud).

## Networking Roles

### `networking/container_networks` — [Read details](roles/networking_container_networks.md)
**Container Isolation**
Configures kernel prerequisites and network definitions for isolated container traffic.

### `networking/desktop` — [Read details](roles/networking_desktop.md)
**Desktop Networking**
Configures Wi-Fi backends and NetworkManager settings for workstation profiles.

### `networking/firewall` — [Read details](roles/networking_firewall.md)
**Multi-Distro Firewall**
Unified interface for managing rules via UFW (Debian/Arch) or Firewalld (RHEL/Fedora).

### `networking/physical` — [Read details](roles/networking_physical.md)
**Networking Physical Role (`networking/physical`)**
This role manages physical network interface optimizations, specifically identifying interface speeds (1G, 2.5G, 10G, 25G, 40G, 100G) and identifying physical media types (Twisted Pair vs Fiber/DAC).

### `networking/services` — [Read details](roles/networking_services.md)
**Network Services**
Deploys specialized network services such as Endlessh tarpits.

### `networking/virtual` — [Read details](roles/networking_virtual.md)
**Virtual Networking**
Manages VLANs, VXLANs, and software-defined network overlays.

### `networking/vpn_mesh` — [Read details](roles/networking_vpn_mesh.md)
**Encrypted VPN Mesh**
Ensures kernel readiness and configuration for encrypted traffic mesh (Wireguard/Tailscale).

## Ops Roles

### `ops/cloud_init` — [Read details](roles/ops_cloud_init.md)
**Cloud Provider Sync**
Handles cloud-init configuration and synchronization for cloud-based deployments.

### `ops/connection_info` — [Read details](roles/ops_connection_info.md)
**Connection Management**
Manages SSH/Rsync connection metadata, randomization of ports, and ephemeral access.

### `ops/guest_management` — [Read details](roles/ops_guest_management.md)
**Guest Lifecycle**
Tools and tasks for managing the lifecycle of virtualized guests.

### `ops/monitoring` — [Read details](roles/ops_monitoring.md)
**Monitoring Role (`ops/monitoring`)**
This role deploys standard system monitoring agents and tools. It focuses on OS-level observability, providing metrics and health checks.

### `ops/pre_connection` — [Read details](roles/ops_pre_connection.md)
**Pre-connection Verification**
Initial connectivity and environment checks before the main deployment run.

### `ops/preflight` — [Read details](roles/ops_preflight.md)
**System Preflight**
Mandatory system validation (memory, network, binaries) to ensure environment readiness.

### `ops/session` — [Read details](roles/ops_session.md)
**Deployment Session**
Ensures deployments run within persistent sessions (Tmux) to prevent interruption.

## Orchestration Roles

### `orchestration/k8s_node` — [Read details](roles/orchestration_k8s_node.md)
**Kubernetes Node Setup**
Configures host requirements and plugins (GPU) for Kubernetes worker nodes.

## Security Roles

### `security/access` — [Read details](roles/security_access.md)
**SSH & User Access**
Manages SSH match rules, administrative users, and password policy enforcement.

### `security/advanced` — [Read details](roles/security_advanced.md)
**Advanced Security Hardening Role**
This role provides optional advanced security hardening features that can be enabled in profile branches. These features are designed to be optional additions to the standard security configuration and should not affect the main branch functionality.

### `security/audit_integrity` — [Read details](roles/security_audit_integrity.md)
**Cryptographic Log Immutability**
Ensures the integrity and immutability of system audit logs using cryptographic signatures.

### `security/file_integrity` — [Read details](roles/security_file_integrity.md)
**File Integrity Monitoring**
Initializes and manages AIDE (Advanced Intrusion Detection Environment) for file integrity monitoring.

### `security/firejail` — [Read details](roles/security_firejail.md)
**Application Sandboxing**
Configures Firejail profiles for isolating vulnerable applications in restricted environments.

### `security/hardening` — [Read details](roles/security_hardening.md)
**Core Hardening**
Enhanced core security configurations, including shell hardening and system-wide security policies.

### `security/hardware_isolation` — [Read details](roles/security_hardware_isolation.md)
**Hardware Level Protection**
Manages PCIe passthrough isolation and DMA protection (IOMMU) to prevent side-channel attacks.

### `security/ips` — [Read details](roles/security_ips.md)
**Intrusion Prevention (Fail2Ban)**
Deploys and configures Fail2Ban with custom filters for SSHD and Caddy to mitigate brute-force attacks.

### `security/kernel` — [Read details](roles/security_kernel.md)
**Sysctl Hardening**
Mandatory sysctl-based kernel hardening (network stack, process memory, and ASLR settings).

### `security/mac_apparmor` — [Read details](roles/security_mac_apparmor.md)
**Mandatory Access Control**
Configures and enforces AppArmor profiles for critical system services and containers.

### `security/resource_protection` — [Read details](roles/security_resource_protection.md)
**DoS Mitigation**
Implements resource limits (tasks, memory, descriptors) to mitigate denial-of-service and resource exhaustion.

### `security/sandboxing` — [Read details](roles/security_sandboxing.md)
**User-space Isolation**
Provides user-space isolation and additional sandboxing layers for untrusted workloads.

### `security/scanning` — [Read details](roles/security_scanning.md)
**Vulnerability Scanning**
Comprehensive system validation and vulnerability scanning (Lyinis, Trivy, Checkov).

### `security/sshd` — [Read details](roles/security_sshd.md)
**SSH Daemon Hardening**
Enhanced SSH daemon configuration focusing on strong ciphers, key exchange, and authentication policies.

## Storage Roles

### `storage/backup` — [Read details](roles/storage_backup.md)
**System Backup (restic/rclone)**
Comprehensive system backup strategy using restic for encrypted snapshots and rclone for cloud synchronization.

### `storage/filesystems` — [Read details](roles/storage_filesystems.md)
**Filesystem Management**
Handles BTRFS subvolumes, maintenance (scrubbing), and physical storage optimizations.

## Virtualization Roles

### `virtualization/kvm` — [Read details](roles/virtualization_kvm.md)
**Virtualization Layer**
Configures the KVM hypervisor layer, including CPU features and kernel modules for virtualization.

### `virtualization/storage` — [Read details](roles/virtualization_storage.md)
**Virtual Storage Management**
Manages storage backends (images, pools, volumes) specifically for virtualized guests.



