# Handler duplication audit

Generated: 2026-02-14T20:30:00Z UTC

This file lists role handler files that contain multiple handler name variants that normalize to the same canonical (snake_case) identifier.

| File | Canonical (normalized) | Variants found |
|---|---:|---|
roles/containers/anubis/handlers/main.yml | restart_anubis_if_systemd_is_available | `restart anubis (if systemd is available)`, `restart_anubis_if_systemd_is_available`
roles/containers/anubis/handlers/main.yml | reload_systemd_if_systemd_is_available | `reload systemd (if systemd is available)`, `reload_systemd_if_systemd_is_available`
roles/containers/authentik/handlers/main.yml | reload_systemd | `reload systemd`, `reload_systemd`
roles/containers/authentik/handlers/main.yml | restart_caddy | `restart caddy`, `restart_caddy`
roles/containers/caddy/handlers/main.yml | reload_systemd | `Reload systemd`, `reload systemd`, `reload_systemd`
roles/containers/caddy/handlers/main.yml | restart_caddy | `Restart Caddy`, `restart caddy`, `restart_caddy`
roles/containers/common/handlers/main.yml | reload_systemd | `reload systemd`, `reload_systemd`
roles/containers/common/handlers/main.yml | restart_caddy | `restart caddy`, `restart_caddy`
roles/containers/common/handlers/main.yml | check_if_caddy_unit_exists | `Check if caddy unit exists`, `check_if_caddy_unit_exists`
roles/containers/common/handlers/main.yml | restart_caddy_service | `Restart caddy service`, `restart_caddy_service`
roles/containers/media/handlers/main.yml | reload_systemd | `Reload systemd`, `reload systemd`, `reload_systemd`
roles/containers/media/handlers/main.yml | restart_caddy | `Restart Caddy`, `restart caddy`, `restart_caddy`
roles/containers/media/handlers/main.yml | restart_media_stack | `Restart Media Stack`, `restart_media_stack`
roles/containers/memcached/handlers/main.yml | reload_systemd | `reload systemd`, `reload_systemd`
roles/containers/memcached/handlers/main.yml | restart_memcached | `restart memcached`, `restart_memcached`
roles/containers/monitoring/handlers/main.yml | reload_systemd | `Reload systemd`, `reload systemd`, `reload_systemd`
roles/containers/monitoring/handlers/main.yml | restart_monitoring_pod | `Restart Monitoring Pod`, `restart_monitoring_pod`
roles/containers/ops/handlers/main.yml | reload_systemd | `Reload systemd`, `reload systemd`, `reload_systemd`
roles/containers/ops/handlers/main.yml | restart_caddy | `Restart Caddy`, `restart caddy`, `restart_caddy`
roles/containers/quadlets/handlers/main.yml | reload_systemd | `Reload systemd`, `reload systemd`, `reload_systemd`
roles/core/logging/handlers/main.yml | restart_journald | `restart journald`, `restart_journald`
roles/core/logging/handlers/main.yml | restart_rsyslog | `restart rsyslog`, `restart_rsyslog`
roles/core/memory/handlers/main.yml | restart_systemd_zram_setup | `restart systemd-zram-setup`, `restart_systemd_zram_setup`
roles/core/systemd/handlers/main.yml | restart_journald | `restart journald`, `restart_journald`
roles/core/systemd/handlers/main.yml | restart_resolved | `restart resolved`, `restart_resolved`
roles/core/time/handlers/main.yml | restart_chrony | `restart chrony`, `restart_chrony`
roles/hardware/firmware/handlers/main.yml | restart_watchdog | `Restart watchdog`, `restart_watchdog`
roles/hardware/gpu/handlers/main.yml | update_initramfs_placeholder | `Update initramfs (placeholder)`, `update_initramfs_placeholder`
roles/hardware/gpu/handlers/main.yml | restart_display_manager_placeholder | `Restart Display Manager (Placeholder)`, `restart_display_manager_placeholder`
roles/hardware/gpu/handlers/main.yml | update_initramfs_debian | `Update Initramfs Debian`, `update_initramfs_debian`
roles/hardware/gpu/handlers/main.yml | update_initramfs_redhat | `Update Initramfs RedHat`, `update_initramfs_redhat`
roles/hardware/gpu/handlers/main.yml | update_initramfs_alpine | `Update Initramfs Alpine`, `update_initramfs_alpine`
roles/hardware/gpu/handlers/main.yml | reload_udev | `Reload udev`, `reload_udev`
roles/hardware/gpu/handlers/main.yml | update_initramfs_archlinux | `Update Initramfs Archlinux`, `update_initramfs_archlinux`
roles/hardware/sas/handlers/main.yml | update_initramfs | `update initramfs`, `update_initramfs`
roles/hardware/sas/handlers/main.yml | update_initramfs_rhel | `update initramfs (rhel)`, `update_initramfs_rhel`
roles/hardware/sas/handlers/main.yml | update_initramfs_arch | `update initramfs (arch)`, `update_initramfs_arch`
roles/hardware/storage_tuning/handlers/main.yml | reload_udev | `reload udev`, `reload_udev`
roles/hardware/virtual_guest/handlers/main.yml | reload_udev | `reload udev`, `reload_udev`
roles/hardware/virtual_guest/handlers/main.yml | reload_sysctl | `reload sysctl`, `reload_sysctl`
roles/kubernetes/master/handlers/main.yml | reload_systemd | `reload systemd`, `reload_systemd`
roles/kubernetes/master/handlers/main.yml | restart_k3s | `restart k3s`, `restart_k3s`
roles/networking/container_networks/handlers/main.yml | reload_systemd | `Reload systemd`, `reload_systemd`
roles/networking/desktop/handlers/main.yml | restart_networkmanager | `restart networkmanager`, `restart_networkmanager`
roles/networking/firewall/handlers/main.yml | reload_ufw | `Reload UFW`, `reload_ufw`
roles/networking/firewall/handlers/main.yml | reload_firewalld | `Reload Firewalld`, `reload_firewalld`
roles/networking/firewall/handlers/main.yml | reload_nftables | `Reload nftables`, `reload_nftables`
roles/networking/physical/handlers/main.yml | apply_netplan | `apply netplan`, `apply_netplan`
roles/networking/physical/handlers/main.yml | restart_networkmanager | `restart networkmanager`, `restart_networkmanager`
roles/networking/services/endlessh/handlers/main.yml | restart_endlessh | `restart endlessh`, `restart_endlessh`
roles/networking/services/endlessh/handlers/main.yml | reload_systemd | `reload systemd`, `reload_systemd`
roles/ops/monitoring/handlers/main.yml | restart_node_exporter | `restart node_exporter`, `restart_node_exporter`
roles/ops/monitoring/handlers/main.yml | restart_smartd | `restart smartd`, `restart_smartd`
roles/security/access/handlers/main.yml | restart_sshd | `restart sshd`, `restart_sshd`
roles/security/advanced/handlers/main.yml | restart_sshd | `Restart sshd`, `restart_sshd`
roles/security/audit_integrity/handlers/main.yml | restart_journald | `restart journald`, `restart_journald`
roles/security/ips/handlers/main.yml | restart_fail2ban | `restart fail2ban`, `restart_fail2ban`
roles/security/resource_protection/handlers/main.yml | reload_systemd | `reload systemd`, `reload_systemd`
roles/security/scanning/handlers/main.yml | restart_sshd | `restart sshd`, `restart_sshd`
roles/storage/backup/restic/handlers/main.yml | reload_systemd | `Reload systemd`, `reload_systemd`
roles/virtualization/kvm/handlers/main.yml | restart_libvirtd | `restart libvirtd`, `restart_libvirtd`
roles/virtualization/kvm/handlers/main.yml | reload_systemd | `reload systemd`, `reload_systemd`


Summary: found duplicates in 76 handler files.