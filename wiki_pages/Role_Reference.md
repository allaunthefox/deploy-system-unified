# Role_Reference

## Containers Roles

### `containers/anubis`
**anubis**



### `containers/authentik`
**authentik**



### `containers/caddy`
**caddy**



### `containers/common`
**common**



### `containers/config`
**config**



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

### `containers/ops`
**Ops Container Role**

This role deploys operational dashboard and utility tools alongside the media stack.

### `containers/quadlets`
**Quadlets Role**

This role manages **Podman Quadlets**, which are Systemd generator files for containers. It ensures that container networks and services are managed natively by Systemd, providing robustness and auto-start capabilities.

### `containers/runtime`
**Container Runtime Role**

This role handles the installation and configuration of the container runtime environment (Podman/Docker) and associated hardware support (GPU).

## Core Roles

### `core/bootstrap`
**bootstrap**



### `core/entropy`
**entropy**



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



## Networking Roles

### `networking/container_networks`
**container_networks**



### `networking/desktop`
**desktop**



### `networking/firewall`
**firewall**



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



### `ops/guest_management`
**guest_management**



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
**audit_integrity**



### `security/file_integrity`
**file_integrity**



### `security/firejail`
**firejail**



### `security/hardening`
**hardening**



### `security/hardware_isolation`
**hardware_isolation**



### `security/ips`
**ips**



### `security/kernel`
**kernel**



### `security/mac_apparmor`
**mac_apparmor**



### `security/resource_protection`
**resource_protection**



### `security/sandboxing`
**sandboxing**



### `security/scanning`
**security/scanning role**

This role provides a comprehensive security framework for the Deploy-System-Unified project, including system validation, secure time synchronization, security tool configuration (trivy, aide, lynis, etc.), and secure handling of temporary files and SSH information.

### `security/sshd`
**sshd**



## Storage Roles

### `storage/backup`
**backup**



### `storage/filesystems`
**filesystems**



## Virtualization Roles

### `virtualization/kvm`
**kvm**



### `virtualization/storage`
**storage**



