# Role_Reference

## Containers Roles

### `containers/anubis` — [Read details](roles/containers_anubis.md)
**anubis**



### `containers/authentik` — [Read details](roles/containers_authentik.md)
**authentik**



### `containers/caddy` — [Read details](roles/containers_caddy.md)
**caddy**



### `containers/common` — [Read details](roles/containers_common.md)
**common**



### `containers/config` — [Read details](roles/containers_config.md)
**config**



### `containers/lxc` — [Read details](roles/containers_lxc.md)
**lxc**



### `containers/media` — [Read details](roles/containers_media.md)
**Media Container Role**

This role deploys a comprehensive media stack using Podman Quadlets. It supports multi-tenancy, allowing multiple isolated instances of the stack to run on a single host.

### `containers/memcached` — [Read details](roles/containers_memcached.md)
**memcached**



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
**bootstrap**



### `core/entropy` — [Read details](roles/core_entropy.md)
**entropy**



### `core/hardware_support` — [Read details](roles/core_hardware_support.md)
**hardware_support**



### `core/identity` — [Read details](roles/core_identity.md)
**identity**



### `core/logging` — [Read details](roles/core_logging.md)
**logging**



### `core/memory` — [Read details](roles/core_memory.md)
**memory**



### `core/repositories` — [Read details](roles/core_repositories.md)
**repositories**



### `core/secrets` — [Read details](roles/core_secrets.md)
**secrets**



### `core/systemd` — [Read details](roles/core_systemd.md)
**systemd**



### `core/time` — [Read details](roles/core_time.md)
**time**



### `core/updates` — [Read details](roles/core_updates.md)
**updates**



## Hardware Roles

### `hardware/firmware` — [Read details](roles/hardware_firmware.md)
**firmware**



### `hardware/gpu` — [Read details](roles/hardware_gpu.md)
**gpu**



### `hardware/sas` — [Read details](roles/hardware_sas.md)
**Hardware SAS Role (`hardware/sas`)**

This role provides support for Serial Attached SCSI (SAS) infrastructure, spanning legacy SAS-2 (6G) to modern SAS-3 (12G) and SAS-4 (24G) storage fabrics. It handles driver loading, tooling, and performance tuning for queue depths.

### `hardware/storage_tuning` — [Read details](roles/hardware_storage_tuning.md)
**storage_tuning**



### `hardware/virtual_guest` — [Read details](roles/hardware_virtual_guest.md)
**virtual_guest**



## Networking Roles

### `networking/container_networks` — [Read details](roles/networking_container_networks.md)
**container_networks**



### `networking/desktop` — [Read details](roles/networking_desktop.md)
**desktop**



### `networking/firewall` — [Read details](roles/networking_firewall.md)
**firewall**



### `networking/physical` — [Read details](roles/networking_physical.md)
**Networking Physical Role (`networking/physical`)**

This role manages physical network interface optimizations, specifically identifying interface speeds (1G, 2.5G, 10G, 25G, 40G, 100G) and identifying physical media types (Twisted Pair vs Fiber/DAC).

### `networking/services` — [Read details](roles/networking_services.md)
**services**



### `networking/virtual` — [Read details](roles/networking_virtual.md)
**virtual**



### `networking/vpn_mesh` — [Read details](roles/networking_vpn_mesh.md)
**vpn_mesh**



## Ops Roles

### `ops/cloud_init` — [Read details](roles/ops_cloud_init.md)
**cloud_init**



### `ops/connection_info` — [Read details](roles/ops_connection_info.md)
**connection_info**



### `ops/guest_management` — [Read details](roles/ops_guest_management.md)
**guest_management**



### `ops/monitoring` — [Read details](roles/ops_monitoring.md)
**Monitoring Role (`ops/monitoring`)**

This role deploys standard system monitoring agents and tools. It focuses on OS-level observability, providing metrics and health checks.

### `ops/pre_connection` — [Read details](roles/ops_pre_connection.md)
**pre_connection**



### `ops/preflight` — [Read details](roles/ops_preflight.md)
**preflight**



### `ops/session` — [Read details](roles/ops_session.md)
**session**



## Orchestration Roles

### `orchestration/k8s_node` — [Read details](roles/orchestration_k8s_node.md)
**k8s_node**



## Security Roles

### `security/access` — [Read details](roles/security_access.md)
**access**



### `security/advanced` — [Read details](roles/security_advanced.md)
**Advanced Security Hardening Role**

This role provides optional advanced security hardening features that can be enabled in profile branches. These features are designed to be optional additions to the standard security configuration and should not affect the main branch functionality.

### `security/audit_integrity` — [Read details](roles/security_audit_integrity.md)
**audit_integrity**



### `security/file_integrity` — [Read details](roles/security_file_integrity.md)
**file_integrity**



### `security/firejail` — [Read details](roles/security_firejail.md)
**firejail**



### `security/hardening` — [Read details](roles/security_hardening.md)
**hardening**



### `security/hardware_isolation` — [Read details](roles/security_hardware_isolation.md)
**hardware_isolation**



### `security/ips` — [Read details](roles/security_ips.md)
**ips**



### `security/kernel` — [Read details](roles/security_kernel.md)
**kernel**



### `security/mac_apparmor` — [Read details](roles/security_mac_apparmor.md)
**mac_apparmor**



### `security/resource_protection` — [Read details](roles/security_resource_protection.md)
**resource_protection**



### `security/sandboxing` — [Read details](roles/security_sandboxing.md)
**sandboxing**



### `security/scanning` — [Read details](roles/security_scanning.md)
**security/scanning role**

This role provides a comprehensive security framework for the Deploy-System-Unified project, including system validation, secure time synchronization, security tool configuration (trivy, aide, lynis, etc.), and secure handling of temporary files and SSH information.

### `security/sshd` — [Read details](roles/security_sshd.md)
**sshd**



## Storage Roles

### `storage/backup` — [Read details](roles/storage_backup.md)
**backup**



### `storage/filesystems` — [Read details](roles/storage_filesystems.md)
**filesystems**



## Virtualization Roles

### `virtualization/kvm` — [Read details](roles/virtualization_kvm.md)
**kvm**



### `virtualization/storage` — [Read details](roles/virtualization_storage.md)
**storage**



