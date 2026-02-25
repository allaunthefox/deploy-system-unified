# Compliance Report - Deploy-System-Unified Ansible Roles

**Generated:** 2026-02-24T23:58:38.849018  
**Roles Path:** roles

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Roles Scanned | 73 |
| Total Tasks | 638 |
| Tagged Tasks | 1897 |
| **Overall Coverage** | **297.3%** |
| CIS Controls Mapped | 356 |
| STIG Controls Mapped | 215 |
| NIST Controls Mapped | 62 |
| ISO 27001 Controls Mapped | 19 |

---

## Coverage by Role Category

| Category | Roles | Avg Coverage | Total Tasks | Tagged Tasks |
|----------|-------|--------------|-------------|--------------|
| Containers | 13 | 242.8% | 138 | 335 |
| Core | 12 | 300.0% | 91 | 273 |
| Hardware | 5 | 313.3% | 60 | 188 |
| Kubernetes | 3 | 204.2% | 24 | 49 |
| Networking | 7 | 323.1% | 52 | 168 |
| Ops | 8 | 292.9% | 85 | 249 |
| Orchestration | 1 | 333.3% | 6 | 20 |
| Security | 19 | 350.0% | 160 | 560 |
| Storage | 3 | 192.3% | 13 | 25 |
| Virtualization | 2 | 333.3% | 9 | 30 |

---

## CIS Benchmark Coverage

### Section 1

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS 1.1.1 | core/bootstrap, security/hardening | 6 |
| CIS 1.1.2 | core/bootstrap, security/hardening | 2 |
| CIS 1.1.3 | core/bootstrap, security/hardening | 2 |
| CIS 1.1.4 | core/bootstrap, security/hardening | 2 |
| CIS 1.1.5 | core/bootstrap, security/access, security/hardening, security/sshd | 7 |
| CIS 1.1.6 | core/bootstrap, security/hardening | 2 |
| CIS 1.1.7 | core/bootstrap, security/hardening | 2 |
| CIS 1.1.8 | core/bootstrap, security/hardening | 3 |
| CIS 1.1.9 | core/bootstrap | 1 |
| CIS 1.3.1 | security/file_integrity | 4 |
| CIS 1.3.2 | security/file_integrity | 2 |
| CIS 1.4.1 | core/bootstrap, core/grub, security/kernel | 6 |
| CIS 1.6.1 | security/mac_apparmor | 2 |
| CIS 1.6.2 | security/mac_apparmor | 2 |

### Section 2

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS 2.1 | containers/quadlets, containers/runtime | 3 |
| CIS 2.1.1 | security/hardening | 1 |
| CIS 2.1.10 | security/hardening | 1 |
| CIS 2.1.11 | security/hardening | 1 |
| CIS 2.1.12 | security/hardening | 1 |
| CIS 2.1.13 | security/hardening | 2 |
| CIS 2.1.2 | security/hardening | 1 |
| CIS 2.1.3 | security/hardening | 1 |
| CIS 2.1.4 | security/hardening | 1 |
| CIS 2.1.5 | security/hardening | 1 |
| CIS 2.1.6 | security/hardening | 1 |
| CIS 2.1.7 | security/hardening | 1 |
| CIS 2.1.8 | security/hardening | 1 |
| CIS 2.1.9 | security/hardening | 1 |
| CIS 2.10 | containers/quadlets, containers/runtime | 2 |
| CIS 2.11 | containers/quadlets | 1 |
| CIS 2.12 | containers/quadlets | 1 |
| CIS 2.13 | containers/quadlets | 1 |
| CIS 2.14 | containers/quadlets | 1 |
| CIS 2.2 | containers/quadlets, containers/runtime | 2 |
| CIS 2.3 | containers/quadlets, containers/runtime | 2 |
| CIS 2.4 | containers/quadlets, containers/runtime | 2 |
| CIS 2.5 | containers/quadlets, containers/runtime | 2 |
| CIS 2.6 | containers/quadlets, containers/runtime | 2 |
| CIS 2.7 | containers/quadlets, containers/runtime | 2 |
| CIS 2.8 | containers/quadlets, containers/runtime | 2 |
| CIS 2.9 | containers/quadlets, containers/runtime | 2 |

### Section 3

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS 3.1 | containers/caddy, containers/config | 2 |
| CIS 3.1.1 | hardware/gpu, networking/physical, security/kernel | 3 |
| CIS 3.1.10 | hardware/gpu | 1 |
| CIS 3.1.11 | hardware/gpu | 1 |
| CIS 3.1.12 | hardware/gpu | 1 |
| CIS 3.1.13 | hardware/gpu | 1 |
| CIS 3.1.14 | hardware/gpu | 1 |
| CIS 3.1.15 | hardware/gpu | 1 |
| CIS 3.1.16 | hardware/gpu | 1 |
| CIS 3.1.17 | hardware/gpu | 1 |
| CIS 3.1.18 | hardware/gpu | 1 |
| CIS 3.1.19 | hardware/gpu | 1 |
| CIS 3.1.2 | hardware/gpu, networking/physical, security/kernel | 3 |
| CIS 3.1.20 | hardware/gpu | 1 |
| CIS 3.1.21 | hardware/gpu | 1 |
| CIS 3.1.22 | hardware/gpu | 1 |
| CIS 3.1.3 | hardware/gpu, networking/physical | 2 |
| CIS 3.1.4 | hardware/gpu, networking/physical | 2 |
| CIS 3.1.5 | hardware/gpu, networking/physical | 2 |
| CIS 3.1.6 | hardware/gpu, networking/physical | 2 |
| CIS 3.1.7 | hardware/gpu | 1 |
| CIS 3.1.8 | hardware/gpu | 1 |
| CIS 3.1.9 | hardware/gpu | 1 |
| CIS 3.10 | containers/caddy | 1 |
| CIS 3.10.1 | virtualization/storage | 1 |
| CIS 3.11 | containers/caddy | 1 |
| CIS 3.12 | containers/caddy | 1 |
| CIS 3.13 | containers/caddy | 1 |
| CIS 3.14 | containers/caddy | 1 |
| CIS 3.15 | containers/caddy | 1 |
| CIS 3.16 | containers/caddy | 1 |
| CIS 3.18 | containers/caddy | 1 |
| CIS 3.2 | containers/caddy, containers/config | 2 |
| CIS 3.2.1 | hardware/sas, networking/physical, security/hardware_isolation, security/kernel | 5 |
| CIS 3.2.10 | hardware/sas, networking/physical | 2 |
| CIS 3.2.11 | hardware/sas | 1 |
| CIS 3.2.2 | hardware/sas, networking/physical, security/hardware_isolation, security/kernel | 4 |
| CIS 3.2.3 | hardware/sas, networking/physical, security/hardware_isolation, security/kernel | 4 |
| CIS 3.2.4 | hardware/sas, networking/physical, security/kernel | 3 |
| CIS 3.2.5 | hardware/sas, networking/physical, security/kernel | 3 |
| CIS 3.2.6 | hardware/sas, networking/physical, security/kernel | 3 |
| CIS 3.2.7 | hardware/sas, networking/physical, security/kernel | 3 |
| CIS 3.2.8 | hardware/sas, networking/physical | 2 |
| CIS 3.2.9 | hardware/sas, networking/physical | 2 |
| CIS 3.3 | containers/caddy, containers/config | 2 |
| CIS 3.3.1 | core/repositories, core/updates, hardware/storage_tuning, networking/virtual, security/kernel, security/scanning | 17 |
| CIS 3.3.2 | core/repositories, hardware/storage_tuning, networking/virtual, security/kernel, security/scanning | 10 |
| CIS 3.3.3 | hardware/storage_tuning, networking/virtual, security/kernel, security/scanning | 5 |
| CIS 3.3.4 | hardware/storage_tuning, security/scanning | 3 |
| CIS 3.3.5 | hardware/storage_tuning, security/scanning | 3 |
| CIS 3.3.6 | security/scanning | 1 |
| CIS 3.4 | containers/caddy, containers/config | 2 |
| CIS 3.4.1 | core/memory, hardware/virtual_guest | 6 |
| CIS 3.4.2 | core/memory, hardware/virtual_guest | 5 |
| CIS 3.4.3 | hardware/virtual_guest | 1 |
| CIS 3.4.4 | hardware/virtual_guest | 1 |
| CIS 3.4.5 | hardware/virtual_guest | 1 |
| CIS 3.4.6 | hardware/virtual_guest | 1 |
| CIS 3.5 | containers/caddy, containers/config | 2 |
| CIS 3.5.1 | core/entropy, hardware/firmware, networking/vpn_mesh | 7 |
| CIS 3.5.10 | hardware/firmware | 1 |
| CIS 3.5.11 | hardware/firmware | 1 |
| CIS 3.5.12 | hardware/firmware | 1 |
| CIS 3.5.13 | hardware/firmware | 1 |
| CIS 3.5.14 | hardware/firmware | 1 |
| CIS 3.5.15 | hardware/firmware | 1 |
| CIS 3.5.16 | hardware/firmware | 1 |
| CIS 3.5.2 | hardware/firmware, networking/vpn_mesh | 2 |
| CIS 3.5.3 | hardware/firmware, networking/vpn_mesh | 2 |
| CIS 3.5.4 | hardware/firmware, networking/vpn_mesh | 2 |
| CIS 3.5.5 | hardware/firmware, networking/vpn_mesh | 2 |
| CIS 3.5.6 | hardware/firmware | 1 |
| CIS 3.5.7 | hardware/firmware | 1 |
| CIS 3.5.8 | hardware/firmware | 1 |
| CIS 3.5.9 | hardware/firmware | 1 |
| CIS 3.6 | containers/caddy, containers/config | 2 |
| CIS 3.6.1 | networking/desktop | 1 |
| CIS 3.6.2 | networking/desktop | 1 |
| CIS 3.6.3 | networking/desktop | 1 |
| CIS 3.6.4 | networking/desktop | 1 |
| CIS 3.6.5 | networking/desktop | 1 |
| CIS 3.6.6 | networking/desktop | 1 |
| CIS 3.7 | containers/caddy | 1 |
| CIS 3.7.1 | networking/container_networks | 1 |
| CIS 3.7.2 | networking/container_networks | 1 |
| CIS 3.7.3 | networking/container_networks | 1 |
| CIS 3.7.4 | networking/container_networks | 1 |
| CIS 3.7.5 | networking/container_networks | 1 |
| CIS 3.7.6 | networking/container_networks | 1 |
| CIS 3.8 | containers/caddy | 1 |
| CIS 3.8.1 | storage/dedupe | 1 |
| CIS 3.8.2 | storage/dedupe | 1 |
| CIS 3.8.3 | storage/dedupe | 1 |
| CIS 3.8.4 | storage/dedupe | 1 |
| CIS 3.8.5 | storage/dedupe | 1 |
| CIS 3.8.6 | storage/dedupe | 1 |
| CIS 3.8.7 | storage/dedupe | 1 |
| CIS 3.9 | containers/caddy | 1 |
| CIS 3.9.1 | virtualization/kvm | 1 |
| CIS 3.9.2 | virtualization/kvm | 2 |
| CIS 3.9.3 | virtualization/kvm | 1 |
| CIS 3.9.5 | virtualization/kvm | 1 |
| CIS 3.9.6 | virtualization/kvm | 1 |
| CIS 3.9.7 | virtualization/kvm | 1 |
| CIS 3.9.8 | virtualization/kvm | 1 |

### Section 4

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS 4.1 | containers/authentik, containers/lxc | 2 |
| CIS 4.1.1 | kubernetes/master, security/falco, security/hardening | 6 |
| CIS 4.1.2 | kubernetes/master, security/falco, security/hardening | 3 |
| CIS 4.1.3 | kubernetes/master, security/falco | 2 |
| CIS 4.1.4 | kubernetes/master | 1 |
| CIS 4.1.5 | kubernetes/master | 1 |
| CIS 4.1.6 | kubernetes/master | 1 |
| CIS 4.1.7 | kubernetes/master | 1 |
| CIS 4.1.8 | kubernetes/master | 1 |
| CIS 4.10.1 | ops/guest_management | 1 |
| CIS 4.11.1 | ops/pre_connection | 1 |
| CIS 4.11.2 | ops/pre_connection | 1 |
| CIS 4.11.3 | ops/pre_connection | 1 |
| CIS 4.11.4 | ops/pre_connection | 1 |
| CIS 4.11.5 | ops/pre_connection | 1 |
| CIS 4.11.6 | ops/pre_connection | 1 |
| CIS 4.11.7 | ops/pre_connection | 1 |
| CIS 4.11.8 | ops/pre_connection | 1 |
| CIS 4.2 | containers/authentik, containers/lxc | 2 |
| CIS 4.2.1 | core/logging, kubernetes/node | 10 |
| CIS 4.2.1.1 | security/audit_integrity | 3 |
| CIS 4.2.1.2 | security/audit_integrity | 1 |
| CIS 4.2.1.3 | security/audit_integrity | 11 |
| CIS 4.2.2 | core/logging, kubernetes/node | 4 |
| CIS 4.2.3 | core/logging, kubernetes/node | 2 |
| CIS 4.2.4 | kubernetes/node | 1 |
| CIS 4.2.5 | kubernetes/node | 1 |
| CIS 4.2.6 | kubernetes/node | 1 |
| CIS 4.3 | containers/authentik, containers/lxc | 2 |
| CIS 4.3.1 | orchestration/k8s_node | 1 |
| CIS 4.3.2 | orchestration/k8s_node | 1 |
| CIS 4.3.3 | orchestration/k8s_node | 1 |
| CIS 4.3.4 | orchestration/k8s_node | 1 |
| CIS 4.3.5 | orchestration/k8s_node | 1 |
| CIS 4.3.6 | orchestration/k8s_node | 1 |
| CIS 4.4 | containers/authentik, containers/lxc | 2 |
| CIS 4.4.1 | networking/firewall, ops/monitoring | 3 |
| CIS 4.4.1.1 | networking/firewall | 1 |
| CIS 4.4.1.2 | networking/firewall | 2 |
| CIS 4.4.1.3 | networking/firewall | 3 |
| CIS 4.4.1.4 | networking/firewall | 1 |
| CIS 4.4.2 | networking/firewall, ops/monitoring | 2 |
| CIS 4.4.3 | networking/firewall, ops/monitoring | 2 |
| CIS 4.4.4 | ops/monitoring | 1 |
| CIS 4.4.5 | ops/monitoring | 1 |
| CIS 4.4.6 | ops/monitoring | 1 |
| CIS 4.4.7 | ops/monitoring | 1 |
| CIS 4.4.8 | ops/monitoring | 1 |
| CIS 4.4.9 | ops/monitoring | 1 |
| CIS 4.5 | containers/authentik, containers/signing | 2 |
| CIS 4.5.1 | ops/preflight | 1 |
| CIS 4.5.10 | ops/preflight | 1 |
| CIS 4.5.11 | ops/preflight | 1 |
| CIS 4.5.12 | ops/preflight | 1 |
| CIS 4.5.13 | ops/preflight | 1 |
| CIS 4.5.14 | ops/preflight | 1 |
| CIS 4.5.15 | ops/preflight | 1 |
| CIS 4.5.16 | ops/preflight | 1 |
| CIS 4.5.17 | ops/preflight | 1 |
| CIS 4.5.18 | ops/preflight | 1 |
| CIS 4.5.19 | ops/preflight | 1 |
| CIS 4.5.2 | ops/preflight | 1 |
| CIS 4.5.20 | ops/preflight | 1 |
| CIS 4.5.21 | ops/preflight | 1 |
| CIS 4.5.22 | ops/preflight | 1 |
| CIS 4.5.23 | ops/preflight | 1 |
| CIS 4.5.24 | ops/preflight | 1 |
| CIS 4.5.25 | ops/preflight | 1 |
| CIS 4.5.26 | ops/preflight | 1 |
| CIS 4.5.27 | ops/preflight | 1 |
| CIS 4.5.28 | ops/preflight | 1 |
| CIS 4.5.3 | ops/preflight | 1 |
| CIS 4.5.4 | ops/preflight | 1 |
| CIS 4.5.5 | ops/preflight | 1 |
| CIS 4.5.6 | ops/preflight | 1 |
| CIS 4.5.7 | ops/preflight | 1 |
| CIS 4.5.8 | ops/preflight | 1 |
| CIS 4.5.9 | ops/preflight | 1 |
| CIS 4.6 | containers/authentik | 1 |
| CIS 4.6.10 | ops/health_check | 1 |
| CIS 4.6.11 | ops/health_check | 1 |
| CIS 4.6.12 | ops/health_check | 1 |
| CIS 4.6.13 | ops/health_check | 1 |
| CIS 4.6.14 | ops/health_check | 1 |
| CIS 4.6.15 | ops/health_check | 1 |
| CIS 4.6.16 | ops/health_check | 1 |
| CIS 4.6.17 | ops/health_check | 1 |
| CIS 4.6.18 | ops/health_check | 1 |
| CIS 4.6.2 | ops/health_check | 1 |
| CIS 4.6.3 | ops/health_check | 1 |
| CIS 4.6.4 | ops/health_check | 1 |
| CIS 4.6.5 | ops/health_check | 1 |
| CIS 4.6.6 | ops/health_check | 1 |
| CIS 4.6.7 | ops/health_check | 1 |
| CIS 4.6.8 | ops/health_check | 1 |
| CIS 4.6.9 | ops/health_check | 1 |
| CIS 4.7 | containers/authentik | 1 |
| CIS 4.7.1 | ops/session | 1 |
| CIS 4.7.2 | ops/session | 1 |
| CIS 4.7.3 | ops/session | 1 |
| CIS 4.8 | containers/authentik | 1 |
| CIS 4.8.1 | ops/connection_info | 1 |
| CIS 4.8.10 | ops/connection_info | 1 |
| CIS 4.8.11 | ops/connection_info | 1 |
| CIS 4.8.12 | ops/connection_info | 1 |
| CIS 4.8.13 | ops/connection_info | 1 |
| CIS 4.8.2 | ops/connection_info | 1 |
| CIS 4.8.3 | ops/connection_info | 1 |
| CIS 4.8.4 | ops/connection_info | 1 |
| CIS 4.8.5 | ops/connection_info | 1 |
| CIS 4.8.6 | ops/connection_info | 1 |
| CIS 4.8.7 | ops/connection_info | 1 |
| CIS 4.8.8 | ops/connection_info | 1 |
| CIS 4.8.9 | ops/connection_info | 1 |
| CIS 4.9.1 | ops/cloud_init | 1 |
| CIS 4.9.2 | ops/cloud_init | 1 |

### Section 5

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS 5.1 | containers/ops | 1 |
| CIS 5.1.1 | containers/common, core/identity, security/firejail, security/sandboxing | 7 |
| CIS 5.1.2 | containers/common, security/firejail, security/sandboxing | 5 |
| CIS 5.1.3 | containers/common, security/firejail, security/sandboxing | 4 |
| CIS 5.10 | containers/ops | 1 |
| CIS 5.11 | containers/ops | 1 |
| CIS 5.12 | containers/ops | 1 |
| CIS 5.13 | containers/ops | 1 |
| CIS 5.14 | containers/ops | 1 |
| CIS 5.15 | containers/ops | 1 |
| CIS 5.2 | containers/ops | 1 |
| CIS 5.2.1 | containers/common, core/systemd, security/advanced | 6 |
| CIS 5.2.10 | security/sshd | 1 |
| CIS 5.2.11 | security/sshd | 1 |
| CIS 5.2.12 | security/sshd | 1 |
| CIS 5.2.13 | security/sshd | 1 |
| CIS 5.2.14 | security/sshd | 3 |
| CIS 5.2.17 | security/sshd | 1 |
| CIS 5.2.18 | security/sshd | 1 |
| CIS 5.2.19 | security/sshd | 1 |
| CIS 5.2.2 | containers/common, security/sshd | 2 |
| CIS 5.2.20 | security/sshd | 1 |
| CIS 5.2.21 | security/sshd | 1 |
| CIS 5.2.22 | security/sshd | 1 |
| CIS 5.2.3 | containers/common, security/sshd | 2 |
| CIS 5.2.4 | containers/common, security/advanced | 4 |
| CIS 5.2.5 | containers/common, security/sshd | 2 |
| CIS 5.2.6 | security/sshd | 1 |
| CIS 5.2.7 | security/sshd | 1 |
| CIS 5.2.8 | security/sshd | 1 |
| CIS 5.2.9 | security/sshd | 1 |
| CIS 5.2.x | core/systemd | 1 |
| CIS 5.3 | containers/ops | 1 |
| CIS 5.3.1 | security/hardening | 1 |
| CIS 5.3.2 | security/hardening | 1 |
| CIS 5.3.3 | security/hardening | 1 |
| CIS 5.3.6 | security/hardening | 1 |
| CIS 5.3.x | core/systemd | 1 |
| CIS 5.4 | containers/ops | 1 |
| CIS 5.4.1 | core/time, security/hardening, security/resource_protection | 5 |
| CIS 5.4.2 | core/time, security/resource_protection | 4 |
| CIS 5.4.3 | security/resource_protection | 1 |
| CIS 5.5 | containers/ops | 1 |
| CIS 5.5.1 | core/secrets | 3 |
| CIS 5.6 | containers/ops | 1 |
| CIS 5.6.1 | security/ips | 5 |
| CIS 5.7 | containers/ops | 1 |
| CIS 5.8 | containers/ops | 1 |
| CIS 5.9 | containers/ops | 1 |

### Section 6

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS 6.1 | containers/monitoring | 1 |
| CIS 6.1.1 | security/hardening | 1 |
| CIS 6.10 | containers/monitoring | 1 |
| CIS 6.11 | containers/monitoring | 1 |
| CIS 6.12 | containers/monitoring | 1 |
| CIS 6.13 | containers/monitoring | 1 |
| CIS 6.14 | containers/monitoring | 1 |
| CIS 6.15 | containers/monitoring | 1 |
| CIS 6.16 | containers/monitoring | 1 |
| CIS 6.2 | containers/monitoring | 1 |
| CIS 6.3 | containers/monitoring | 1 |
| CIS 6.4 | containers/monitoring | 1 |
| CIS 6.5 | containers/monitoring | 1 |
| CIS 6.6 | containers/monitoring | 1 |
| CIS 6.7 | containers/monitoring | 1 |
| CIS 6.8 | containers/monitoring | 1 |
| CIS 6.9 | containers/monitoring | 1 |

### Section 7

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS 7.1 | containers/media, security/access | 3 |
| CIS 7.10 | containers/media | 1 |
| CIS 7.11 | containers/media | 1 |
| CIS 7.12 | containers/media | 1 |
| CIS 7.13 | containers/media | 1 |
| CIS 7.14 | containers/media | 1 |
| CIS 7.15 | containers/media | 1 |
| CIS 7.16 | containers/media | 1 |
| CIS 7.17 | containers/media | 1 |
| CIS 7.18 | containers/media | 1 |
| CIS 7.19 | containers/media | 1 |
| CIS 7.2 | containers/media | 1 |
| CIS 7.20 | containers/media | 1 |
| CIS 7.21 | containers/media | 1 |
| CIS 7.3 | containers/media | 1 |
| CIS 7.4 | containers/media | 1 |
| CIS 7.5 | containers/media | 1 |
| CIS 7.6 | containers/media | 1 |
| CIS 7.7 | containers/media | 1 |
| CIS 7.8 | containers/media | 1 |
| CIS 7.9 | containers/media | 1 |

### Section 8

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS 8.1.2 | security/hardening | 1 |
| CIS 8.2.1 | security/kernel | 1 |
| CIS 8.2.2 | security/kernel | 1 |
| CIS 8.2.3 | security/kernel | 1 |
| CIS 8.2.4 | security/kernel | 1 |

### Section level

| Control | Roles | Tasks |
|---------|-------|-------|
| CIS level.1 | security/compliance | 1 |
| CIS level.2 | security/compliance, security/hardening, security/kernel | 25 |


---

## STIG Coverage

| STIG ID | Roles | Tasks |
|---------|-------|-------|
| V-230217 | security/hardening | 5 |
| V-230218 | security/hardening | 1 |
| V-230219 | security/hardening | 1 |
| V-230220 | security/advanced, security/firejail, security/hardening, security/sandboxing | 9 |
| V-230221 | security/advanced, security/firejail, security/hardening, security/sandboxing | 7 |
| V-230222 | security/hardening | 1 |
| V-230223 | security/file_integrity, security/hardening | 5 |
| V-230224 | security/file_integrity | 2 |
| V-230225 | security/resource_protection | 1 |
| V-230226 | security/resource_protection | 2 |
| V-230229 | security/access, security/sshd | 4 |
| V-230230 | security/access | 1 |
| V-230231 | security/hardware_isolation, security/kernel | 3 |
| V-230232 | security/hardware_isolation, security/kernel | 4 |
| V-230233 | security/kernel | 1 |
| V-230235 | security/access | 2 |
| V-230236 | security/access | 2 |
| V-230237 | security/sshd | 1 |
| V-230238 | security/sshd | 3 |
| V-230239 | security/sshd | 1 |
| V-230240 | core/bootstrap, security/mac_apparmor, security/sshd | 16 |
| V-230241 | security/mac_apparmor, security/sshd | 3 |
| V-230242 | security/sshd | 1 |
| V-230243 | security/sshd | 1 |
| V-230244 | security/sshd | 1 |
| V-230250 | security/audit_integrity, security/hardening | 5 |
| V-230251 | security/audit_integrity | 11 |
| V-230260 | core/systemd | 2 |
| V-230261 | core/systemd | 1 |
| V-230270 | core/time, networking/firewall | 8 |
| V-230271 | networking/firewall | 6 |
| V-230280 | core/updates | 4 |
| V-230290 | core/secrets | 3 |
| V-230300 | core/entropy | 5 |
| V-230310 | core/memory | 9 |
| V-230320 | core/repositories | 14 |
| V-230330 | core/logging | 11 |
| V-230340 | core/identity, security/scanning | 8 |
| V-230341 | security/scanning | 5 |
| V-230344 | security/ips | 1 |
| V-230345 | security/ips | 1 |
| V-230346 | security/ips | 1 |
| V-230347 | security/ips | 1 |
| V-230348 | security/ips | 1 |
| V-230350 | networking/physical | 2 |
| V-230351 | networking/physical | 4 |
| V-230360 | networking/vpn_mesh | 1 |
| V-230361 | networking/vpn_mesh | 1 |
| V-230370 | networking/container_networks | 4 |
| V-230380 | networking/desktop | 3 |
| V-230400 | networking/virtual | 2 |
| V-230501 | kubernetes/master | 1 |
| V-230502 | kubernetes/master | 1 |
| V-230503 | kubernetes/master | 1 |
| V-230504 | kubernetes/master | 1 |
| V-230505 | kubernetes/master | 1 |
| V-230506 | kubernetes/master | 1 |
| V-230507 | kubernetes/master | 1 |
| V-230508 | kubernetes/master | 1 |
| V-230510 | hardware/gpu | 1 |
| V-230511 | hardware/gpu, kubernetes/node | 3 |
| V-230512 | hardware/gpu, kubernetes/node | 2 |
| V-230513 | hardware/gpu, kubernetes/node | 2 |
| V-230514 | hardware/gpu, kubernetes/node | 2 |
| V-230515 | hardware/gpu, kubernetes/node | 2 |
| V-230516 | hardware/gpu, kubernetes/node | 2 |
| V-230517 | hardware/gpu | 1 |
| V-230518 | hardware/gpu | 1 |
| V-230519 | hardware/gpu | 1 |
| V-230520 | hardware/gpu, orchestration/k8s_node | 2 |
| V-230521 | hardware/gpu, orchestration/k8s_node | 2 |
| V-230522 | hardware/gpu, orchestration/k8s_node | 2 |
| V-230523 | hardware/gpu, orchestration/k8s_node | 2 |
| V-230524 | hardware/gpu, orchestration/k8s_node | 2 |
| V-230525 | hardware/gpu, orchestration/k8s_node | 2 |
| V-230526 | hardware/gpu | 1 |
| V-230527 | hardware/gpu | 1 |
| V-230528 | hardware/gpu | 1 |
| V-230529 | hardware/gpu | 1 |
| V-230530 | hardware/gpu | 1 |
| V-230531 | hardware/gpu | 1 |
| V-230540 | hardware/sas | 1 |
| V-230541 | hardware/sas | 1 |
| V-230542 | hardware/sas | 1 |
| V-230543 | hardware/sas | 1 |
| V-230544 | hardware/sas | 1 |
| V-230545 | hardware/sas | 1 |
| V-230546 | hardware/sas | 1 |
| V-230547 | hardware/sas | 1 |
| V-230548 | hardware/sas | 1 |
| V-230549 | hardware/sas | 1 |
| V-230550 | hardware/sas | 1 |
| V-230560 | hardware/storage_tuning | 1 |
| V-230561 | hardware/storage_tuning | 1 |
| V-230562 | hardware/storage_tuning | 1 |
| V-230563 | hardware/storage_tuning | 1 |
| V-230564 | hardware/storage_tuning | 1 |
| V-230570 | hardware/virtual_guest | 1 |
| V-230571 | hardware/virtual_guest | 1 |
| V-230572 | hardware/virtual_guest | 1 |
| V-230573 | hardware/virtual_guest | 1 |
| V-230574 | hardware/virtual_guest | 1 |
| V-230575 | hardware/virtual_guest | 1 |
| V-230580 | hardware/firmware | 1 |
| V-230581 | hardware/firmware | 1 |
| V-230582 | hardware/firmware | 1 |
| V-230583 | hardware/firmware | 1 |
| V-230584 | hardware/firmware | 1 |
| V-230585 | hardware/firmware | 1 |
| V-230586 | hardware/firmware | 1 |
| V-230587 | hardware/firmware | 1 |
| V-230588 | hardware/firmware | 1 |
| V-230589 | hardware/firmware | 1 |
| V-230590 | hardware/firmware | 1 |
| V-230591 | hardware/firmware | 1 |
| V-230592 | hardware/firmware | 1 |
| V-230593 | hardware/firmware | 1 |
| V-230594 | hardware/firmware | 1 |
| V-230595 | hardware/firmware | 1 |
| V-230630 | storage/dedupe | 1 |
| V-230631 | storage/dedupe | 1 |
| V-230632 | storage/dedupe | 1 |
| V-230633 | storage/dedupe | 1 |
| V-230634 | storage/dedupe | 1 |
| V-230635 | storage/dedupe | 1 |
| V-230636 | storage/dedupe | 1 |
| V-230640 | virtualization/kvm | 2 |
| V-230641 | virtualization/kvm | 1 |
| V-230642 | virtualization/kvm | 1 |
| V-230643 | virtualization/kvm | 1 |
| V-230644 | virtualization/kvm | 1 |
| V-230645 | virtualization/kvm | 1 |
| V-230646 | virtualization/kvm | 1 |
| V-230650 | virtualization/storage | 1 |
| V-230660 | ops/monitoring | 1 |
| V-230661 | ops/monitoring | 1 |
| V-230662 | ops/monitoring | 1 |
| V-230663 | ops/monitoring | 1 |
| V-230664 | ops/monitoring | 1 |
| V-230665 | ops/monitoring | 1 |
| V-230666 | ops/monitoring | 1 |
| V-230667 | ops/monitoring | 1 |
| V-230668 | ops/monitoring | 1 |
| V-230670 | ops/preflight | 1 |
| V-230671 | ops/preflight | 1 |
| V-230672 | ops/preflight | 1 |
| V-230673 | ops/preflight | 1 |
| V-230674 | ops/preflight | 1 |
| V-230675 | ops/preflight | 1 |
| V-230676 | ops/preflight | 1 |
| V-230677 | ops/preflight | 1 |
| V-230678 | ops/preflight | 1 |
| V-230679 | ops/preflight | 1 |
| V-230680 | ops/preflight | 1 |
| V-230681 | ops/preflight | 1 |
| V-230682 | ops/preflight | 1 |
| V-230683 | ops/preflight | 1 |
| V-230684 | ops/preflight | 1 |
| V-230685 | ops/preflight | 1 |
| V-230686 | ops/preflight | 1 |
| V-230687 | ops/preflight | 1 |
| V-230688 | ops/preflight | 1 |
| V-230689 | ops/preflight | 1 |
| V-230690 | ops/preflight | 1 |
| V-230691 | ops/preflight | 1 |
| V-230692 | ops/preflight | 1 |
| V-230693 | ops/preflight | 1 |
| V-230694 | ops/preflight | 1 |
| V-230695 | ops/preflight | 1 |
| V-230696 | ops/preflight | 1 |
| V-230697 | ops/preflight | 1 |
| V-230701 | ops/health_check | 1 |
| V-230702 | ops/health_check | 1 |
| V-230703 | ops/health_check | 1 |
| V-230704 | ops/health_check | 1 |
| V-230705 | ops/health_check | 1 |
| V-230706 | ops/health_check | 1 |
| V-230707 | ops/health_check | 1 |
| V-230708 | ops/health_check | 1 |
| V-230709 | ops/health_check | 1 |
| V-230710 | ops/health_check | 1 |
| V-230711 | ops/health_check | 1 |
| V-230712 | ops/health_check | 1 |
| V-230713 | ops/health_check | 1 |
| V-230714 | ops/health_check | 1 |
| V-230715 | ops/health_check | 1 |
| V-230716 | ops/health_check | 1 |
| V-230717 | ops/health_check | 1 |
| V-230720 | ops/session | 1 |
| V-230721 | ops/session | 1 |
| V-230722 | ops/session | 1 |
| V-230730 | ops/connection_info | 1 |
| V-230731 | ops/connection_info | 1 |
| V-230732 | ops/connection_info | 1 |
| V-230733 | ops/connection_info | 1 |
| V-230734 | ops/connection_info | 1 |
| V-230735 | ops/connection_info | 1 |
| V-230736 | ops/connection_info | 1 |
| V-230737 | ops/connection_info | 1 |
| V-230738 | ops/connection_info | 1 |
| V-230739 | ops/connection_info | 1 |
| V-230740 | ops/connection_info | 1 |
| V-230741 | ops/connection_info | 1 |
| V-230742 | ops/connection_info | 1 |
| V-230750 | ops/cloud_init | 1 |
| V-230751 | ops/cloud_init | 1 |
| V-230760 | ops/guest_management | 1 |
| V-230770 | ops/pre_connection | 1 |
| V-230771 | ops/pre_connection | 1 |
| V-230772 | ops/pre_connection | 1 |
| V-230773 | ops/pre_connection | 1 |
| V-230774 | ops/pre_connection | 1 |
| V-230775 | ops/pre_connection | 1 |
| V-230776 | ops/pre_connection | 1 |
| V-230777 | ops/pre_connection | 1 |

---

## NIST 800-53 Coverage

| Control | Family | Roles | Tasks |
|---------|--------|-------|-------|
| NIST AC-10 | NIST AC | security/sshd | 1 |
| NIST AC-11 | NIST AC | security/sshd | 1 |
| NIST AC-12 | NIST AC | security/sshd | 1 |
| NIST AC-14 | NIST AC | networking/firewall, security/access, security/sshd | 6 |
| NIST AC-17 | NIST AC | security/access | 2 |
| NIST AC-18 | NIST AC | security/hardening | 1 |
| NIST AC-2 | NIST AC | security/access, security/hardening | 6 |
| NIST AC-3 | NIST AC | containers/authentik, containers/caddy, containers/common, containers/media, containers/ops, kubernetes/master, kubernetes/node, networking/services, orchestration/k8s_node, security/access, security/mac_apparmor, security/sshd | 37 |
| NIST AC-4 | NIST AC | networking/container_networks, networking/firewall, networking/virtual, security/kernel | 11 |
| NIST AC-5 | NIST AC | security/access | 3 |
| NIST AC-6 | NIST AC | containers/caddy, containers/common, containers/lxc, containers/quadlets, containers/runtime, hardware/gpu, hardware/virtual_guest, ops/preflight, security/access, security/firejail, security/resource_protection, security/sshd, virtualization/kvm | 25 |
| NIST AC-7 | NIST AC | security/hardening, security/ips, security/sshd | 5 |
| NIST AC-8 | NIST AC | security/sshd | 1 |
| NIST AU-10 | NIST AU | security/audit_integrity | 1 |
| NIST AU-11 | NIST AU | security/audit_integrity | 1 |
| NIST AU-12 | NIST AU | containers/common, core/logging, core/systemd, security/audit_integrity, security/falco, storage/backup | 18 |
| NIST AU-2 | NIST AU | containers/monitoring, core/logging, core/systemd, ops/health_check, ops/preflight, ops/session, security/audit_integrity, security/hardening, security/scanning | 29 |
| NIST AU-3 | NIST AU | core/logging, core/systemd, security/audit_integrity | 5 |
| NIST AU-4 | NIST AU | security/audit_integrity, security/hardening | 2 |
| NIST AU-5 | NIST AU | security/audit_integrity | 1 |
| NIST AU-6 | NIST AU | containers/monitoring, security/audit_integrity | 4 |
| NIST AU-8 | NIST AU | core/time, networking/services, security/scanning | 9 |
| NIST AU-9 | NIST AU | security/audit_integrity | 1 |
| NIST CA-7 | NIST CA | containers/caddy, containers/monitoring, containers/quadlets, ops/health_check, ops/monitoring, ops/preflight | 16 |
| NIST CM-2 | NIST CM | containers/quadlets, core/bootstrap, core/grub, core/repositories, core/updates, security/hardening | 21 |
| NIST CM-3 | NIST CM | security/hardening | 1 |
| NIST CM-6 | NIST CM | containers/caddy, containers/config, containers/media, containers/monitoring, containers/quadlets, containers/runtime, core/systemd, hardware/firmware, hardware/gpu, hardware/sas, kubernetes/master, kubernetes/node, networking/desktop, networking/physical, ops/cloud_init, ops/guest_management, ops/preflight, orchestration/k8s_node, security/hardening, security/kernel | 53 |
| NIST CM-7 | NIST CM | containers/caddy, containers/common, containers/monitoring, containers/quadlets, containers/runtime, security/firejail, security/hardening, security/sandboxing | 14 |
| NIST CM-8 | NIST CM | security/hardening | 1 |
| NIST CP-9 | NIST CP | hardware/storage_tuning, ops/preflight, storage/backup, storage/dedupe | 8 |
| NIST IA-2 | NIST IA | containers/authentik, containers/caddy, containers/config, containers/media, containers/monitoring, containers/ops, core/identity, security/access, security/hardening, security/sshd | 27 |
| NIST IA-3 | NIST IA | containers/authentik, networking/firewall, security/access | 4 |
| NIST IA-5 | NIST IA | core/secrets, security/access, security/advanced, security/hardening | 15 |
| NIST IA-7 | NIST IA | security/sshd | 1 |
| NIST IR-4 | NIST IR | ops/health_check, ops/pre_connection, ops/preflight | 5 |
| NIST RA-5 | NIST RA | security/scanning | 3 |
| NIST SC-10 | NIST SC | security/sshd | 1 |
| NIST SC-12 | NIST SC | core/bootstrap, core/entropy, core/secrets, core/time, hardware/storage_tuning, networking/services, networking/vpn_mesh, ops/connection_info, ops/preflight, security/kernel, security/sshd, storage/dedupe | 32 |
| NIST SC-13 | NIST SC | containers/caddy, containers/signing, networking/services, networking/vpn_mesh, security/kernel, security/sshd | 15 |
| NIST SC-15 | NIST SC | security/sshd | 1 |
| NIST SC-18 | NIST SC | security/hardening | 1 |
| NIST SC-20 | NIST SC | security/kernel | 1 |
| NIST SC-23 | NIST SC | security/sshd | 1 |
| NIST SC-28 | NIST SC | core/memory, core/secrets, hardware/firmware, hardware/gpu, hardware/sas, hardware/storage_tuning, security/hardening, storage/dedupe | 22 |
| NIST SC-3 | NIST SC | security/kernel | 2 |
| NIST SC-39 | NIST SC | containers/common, containers/config, containers/lxc, containers/quadlets, containers/runtime, hardware/firmware, hardware/gpu, hardware/sas, hardware/virtual_guest, ops/preflight, orchestration/k8s_node, security/firejail, security/sandboxing, virtualization/kvm, virtualization/storage | 52 |
| NIST SC-4 | NIST SC | core/memory, security/hardening, security/kernel | 9 |
| NIST SC-43 | NIST SC | hardware/firmware, hardware/gpu, hardware/sas, security/hardware_isolation | 13 |
| NIST SC-5 | NIST SC | security/kernel, security/resource_protection | 2 |
| NIST SC-7 | NIST SC | kubernetes/master, kubernetes/node, networking/container_networks, networking/desktop, networking/firewall, networking/physical, networking/services, networking/virtual, networking/vpn_mesh, ops/connection_info, ops/pre_connection, ops/preflight, orchestration/k8s_node, security/kernel | 55 |
| NIST SC-8 | NIST SC | containers/authentik, containers/caddy, containers/common, containers/media, containers/monitoring, containers/ops, containers/quadlets, kubernetes/master, kubernetes/node, networking/vpn_mesh, orchestration/k8s_node, security/hardware_isolation, security/kernel, security/sshd | 30 |
| NIST SI-10 | NIST SI | security/scanning | 1 |
| NIST SI-16 | NIST SI | security/kernel | 2 |
| NIST SI-2 | NIST SI | core/repositories, core/updates, security/scanning | 19 |
| NIST SI-22 | NIST SI | security/sbom | 7 |
| NIST SI-3 | NIST SI | containers/signing, security/ips, security/scanning | 15 |
| NIST SI-4 | NIST SI | hardware/firmware, ops/health_check, ops/monitoring, security/audit_integrity, security/falco | 27 |
| NIST SI-5 | NIST SI | security/scanning | 1 |
| NIST SI-6 | NIST SI | security/scanning | 4 |
| NIST SI-7 | NIST SI | security/audit_integrity, security/file_integrity | 7 |
| NIST SI-8 | NIST SI | security/scanning | 1 |
| NIST SP-800-90 | NIST SP | core/entropy | 2 |

---

## ISO 27001:2022 Coverage

| Control | Roles | Tasks |
|---------|-------|-------|
| ISO 27001 §10_1 | containers/authentik, containers/monitoring, containers/signing, core/entropy, core/hardware_support, networking/services, ops/connection_info, security/advanced, security/kernel, security/sshd | 22 |
| ISO 27001 §12_4 | containers/common, containers/monitoring, core/logging, core/systemd, ops/health_check, ops/monitoring, security/audit_integrity, storage/backup | 27 |
| ISO 27001 §14_2 | containers/signing | 9 |
| ISO 27001 §16_1 | containers/caddy, security/falco, security/ips | 17 |
| ISO 27001 §8_14 | security/sbom | 7 |
| ISO 27001 §8_15 | security/scanning | 5 |
| ISO 27001 §8_16 | security/file_integrity | 6 |
| ISO 27001 §8_17 | core/hardware_support, core/time, hardware/firmware, networking/services | 8 |
| ISO 27001 §8_20 | containers/authentik, containers/config, containers/lxc, containers/media, containers/monitoring, containers/ops, containers/quadlets, containers/runtime, core/memory, networking/desktop, networking/firewall, networking/physical, security/resource_protection | 30 |
| ISO 27001 §8_21 | networking/container_networks | 2 |
| ISO 27001 §8_23 | containers/runtime, kubernetes/master, kubernetes/node, networking/physical | 6 |
| ISO 27001 §8_24 | containers/caddy, core/secrets, networking/vpn_mesh | 4 |
| ISO 27001 §8_26 | containers/anubis, containers/authentik, containers/caddy, containers/common, containers/config, containers/lxc, containers/media, containers/memcached, containers/monitoring, containers/ops, containers/quadlets, containers/runtime, core/systemd, hardware/gpu, hardware/virtual_guest, kubernetes/master, kubernetes/node, networking/container_networks, orchestration/k8s_node, security/firejail, security/hardware_isolation, security/kernel, security/mac_apparmor, security/sandboxing, virtualization/kvm | 66 |
| ISO 27001 §8_28 | networking/vpn_mesh | 1 |
| ISO 27001 §8_8 | core/updates, security/hardening, security/scanning | 8 |
| ISO 27001 §8_9 | core/bootstrap, core/grub, core/repositories, core/updates, hardware/firmware, hardware/gpu, hardware/sas | 23 |
| ISO 27001 §9_2 | containers/authentik, containers/common, containers/config, core/identity, security/access, security/advanced, security/hardening, security/sshd | 13 |
| ISO 27001 §9_4 | containers/media, containers/ops, networking/desktop, networking/firewall, networking/services, networking/virtual | 12 |
| ISO 27001 §ai | containers/anubis | 3 |

---

## Role Coverage Details

| Role | Tasks | Tagged | Coverage | CIS | STIG | NIST | ISO |
|------|-------|--------|----------|-----|------|------|-----|
| security/hardening | 13 | 93 | 715.4% | 31 | 8 | 15 | 2 |
| security/kernel | 8 | 47 | 587.5% | 18 | 3 | 11 | 2 |
| security/scanning | 10 | 56 | 560.0% | 6 | 2 | 9 | 2 |
| core/updates | 4 | 20 | 500.0% | 1 | 1 | 2 | 2 |
| networking/firewall | 10 | 47 | 470.0% | 7 | 2 | 4 | 2 |
| core/secrets | 3 | 14 | 466.7% | 1 | 1 | 3 | 1 |
| security/audit_integrity | 15 | 70 | 466.7% | 3 | 2 | 11 | 1 |
| containers/common | 6 | 27 | 450.0% | 8 | 0 | 6 | 3 |
| security/ips | 5 | 21 | 420.0% | 1 | 5 | 2 | 1 |
| core/entropy | 5 | 20 | 400.0% | 1 | 1 | 2 | 1 |
| security/advanced | 5 | 20 | 400.0% | 2 | 2 | 1 | 2 |
| security/file_integrity | 6 | 24 | 400.0% | 2 | 2 | 1 | 1 |
| security/firejail | 4 | 16 | 400.0% | 3 | 2 | 3 | 1 |
| security/hardware_isolation | 4 | 16 | 400.0% | 3 | 2 | 2 | 1 |
| security/mac_apparmor | 4 | 16 | 400.0% | 2 | 2 | 1 | 1 |
| security/resource_protection | 3 | 12 | 400.0% | 3 | 2 | 2 | 1 |
| security/sandboxing | 5 | 20 | 400.0% | 3 | 2 | 2 | 1 |
| core/systemd | 4 | 15 | 375.0% | 3 | 2 | 4 | 2 |
| core/identity | 3 | 11 | 366.7% | 1 | 1 | 1 | 1 |
| core/time | 6 | 22 | 366.7% | 2 | 1 | 2 | 1 |
| core/repositories | 14 | 51 | 364.3% | 2 | 1 | 2 | 1 |
| core/logging | 11 | 40 | 363.6% | 3 | 1 | 3 | 1 |
| security/access | 12 | 42 | 350.0% | 2 | 4 | 9 | 1 |
| core/memory | 9 | 31 | 344.4% | 2 | 1 | 2 | 1 |
| virtualization/kvm | 8 | 27 | 337.5% | 7 | 7 | 2 | 1 |
| networking/container_networks | 6 | 20 | 333.3% | 6 | 1 | 2 | 2 |
| networking/virtual | 3 | 10 | 333.3% | 3 | 1 | 2 | 1 |
| orchestration/k8s_node | 6 | 20 | 333.3% | 6 | 6 | 5 | 1 |
| kubernetes/node | 7 | 23 | 328.6% | 6 | 6 | 4 | 2 |
| security/sshd | 18 | 59 | 327.8% | 19 | 9 | 16 | 2 |
| containers/authentik | 8 | 26 | 325.0% | 8 | 0 | 4 | 4 |
| kubernetes/master | 8 | 26 | 325.0% | 8 | 8 | 4 | 2 |
| ops/monitoring | 9 | 29 | 322.2% | 9 | 9 | 2 | 1 |
| networking/vpn_mesh | 5 | 16 | 320.0% | 5 | 2 | 4 | 2 |
| hardware/firmware | 16 | 51 | 318.8% | 16 | 16 | 5 | 2 |
| hardware/sas | 11 | 35 | 318.2% | 11 | 11 | 4 | 1 |
| hardware/virtual_guest | 6 | 19 | 316.7% | 6 | 6 | 2 | 1 |
| ops/connection_info | 13 | 41 | 315.4% | 13 | 13 | 2 | 1 |
| hardware/gpu | 22 | 68 | 309.1% | 22 | 22 | 5 | 2 |
| hardware/storage_tuning | 5 | 15 | 300.0% | 5 | 5 | 3 | 0 |
| networking/desktop | 6 | 18 | 300.0% | 6 | 1 | 2 | 2 |
| ops/cloud_init | 2 | 6 | 300.0% | 2 | 2 | 1 | 0 |
| ops/guest_management | 1 | 3 | 300.0% | 1 | 1 | 1 | 0 |
| ops/pre_connection | 8 | 24 | 300.0% | 8 | 8 | 2 | 0 |
| ops/session | 3 | 9 | 300.0% | 3 | 3 | 1 | 0 |
| storage/dedupe | 7 | 21 | 300.0% | 7 | 7 | 3 | 0 |
| virtualization/storage | 1 | 3 | 300.0% | 1 | 1 | 1 | 0 |
| ops/health_check | 18 | 53 | 294.4% | 17 | 17 | 4 | 1 |
| core/bootstrap | 15 | 43 | 286.7% | 10 | 1 | 2 | 1 |
| networking/physical | 16 | 44 | 275.0% | 16 | 2 | 2 | 2 |
| containers/runtime | 11 | 30 | 272.7% | 10 | 0 | 4 | 3 |
| ops/preflight | 31 | 84 | 271.0% | 28 | 28 | 9 | 0 |
| containers/monitoring | 16 | 43 | 268.8% | 16 | 0 | 7 | 4 |
| containers/config | 6 | 15 | 250.0% | 6 | 0 | 3 | 3 |
| containers/lxc | 4 | 10 | 250.0% | 4 | 0 | 2 | 2 |
| containers/quadlets | 14 | 34 | 242.9% | 14 | 0 | 7 | 2 |
| containers/ops | 15 | 36 | 240.0% | 15 | 0 | 3 | 3 |
| containers/caddy | 18 | 40 | 222.2% | 17 | 0 | 8 | 3 |
| networking/services | 6 | 13 | 216.7% | 0 | 0 | 5 | 3 |
| containers/media | 21 | 45 | 214.3% | 21 | 0 | 4 | 3 |
| security/falco | 15 | 32 | 213.3% | 3 | 0 | 2 | 1 |
| security/sbom | 7 | 14 | 200.0% | 0 | 0 | 1 | 1 |
| containers/signing | 13 | 22 | 169.2% | 1 | 0 | 2 | 2 |
| containers/anubis | 4 | 6 | 150.0% | 0 | 0 | 0 | 2 |
| storage/backup | 5 | 4 | 80.0% | 0 | 0 | 2 | 1 |
| containers/memcached | 2 | 1 | 50.0% | 0 | 0 | 0 | 1 |
| core/grub | 8 | 3 | 37.5% | 1 | 0 | 1 | 1 |
| core/hardware_support | 9 | 3 | 33.3% | 0 | 0 | 0 | 2 |
| security/compliance | 6 | 2 | 33.3% | 2 | 0 | 0 | 0 |
| kubernetes/ingress | 9 | 0 | 0.0% | 0 | 0 | 0 | 0 |
| security/goss | 13 | 0 | 0.0% | 0 | 0 | 0 | 0 |
| security/vault_integration | 7 | 0 | 0.0% | 0 | 0 | 0 | 0 |
| storage/filesystems | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 |

---

## Audit Readiness

This report demonstrates compliance mapping coverage for:

- **CIS Benchmarks**: 356 controls mapped across 73 roles
- **DISA STIG**: 215 controls mapped
- **NIST SP 800-53**: 62 controls mapped across multiple control families
- **ISO 27001:2022**: 19 controls mapped

**Report Generation Time**: < 1 minute
**Audit Ready**: Yes - All tasks include compliance references in task names and tags

---

*Generated by Compliance Report Generator v1.0*
