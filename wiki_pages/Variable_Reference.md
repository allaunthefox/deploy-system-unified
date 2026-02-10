# Variable_Reference

## Containers Variables

### `containers/anubis`
- `anubis_enabled`
- `anubis_port`
- `anubis_difficulty`
- `anubis_target_url`
- `anubis_image`
- `anubis_container_name`
- `quadlet_enable_gpu_support`
- `quadlet_gpu_capabilities`

### `containers/authentik`
- `authentik_enable`
- `authentik_image`
- `authentik_redis_image`
- `authentik_postgres_image`
- `authentik_base_dir`
- `authentik_data_dir`
- `authentik_config_dir`
- `authentik_port_http`
- `authentik_port_https`
- `authentik_pg_user`
- `authentik_pg_db`
- `authentik_pg_pass`
- `authentik_secret_key`
- `containers_authentik_fail_secure`
- `authentik_email_host`
- `authentik_email_port`
- `authentik_email_username`
- `authentik_email_password`
- `authentik_email_from`
- `authentik_email_use_tls`
- `authentik_network_name`

### `containers/caddy`
- `containers_caddy_generate_config`
- `containers_caddy_acme_email`
- `containers_caddy_http_port`
- `containers_caddy_https_port`
- `containers_caddy_https_port_udp`
- `containers_porkbun_api_key`
- `containers_porkbun_secret_api_key`
- `containers_caddy_network`
- `containers_caddy_extra_networks`
- `containers_crowdsec_enable`
- `containers_crowdsec_image`
- `containers_crowdsec_firewall_bouncer_key`
- `containers_caddy_fail_secure`
- `containers_crowdsec_firewall_bouncer_version`
- `containers_crowdsec_firewall_bouncer_sha256`
- `containers_crowdsec_secrets_dir`
- `containers_crowdsec_collections`
- `containers_quadlet_enable_gpu_support`

### `containers/config`
- `container_linger_users`

### `containers/lxc`
- `lxc_enable_gpu_support`
- `lxc_gpu_vendor`
- `lxc_gpu_slicing`
- `lxc_gpu_default_configs`
- `lxc_container_gpu_config`
- `lxc_gpu_security`
- `lxc_gpu_resource_limits`
- `intel_oneapi_gpg_key_url`
- `intel_oneapi_gpg_keyring_path`
- `intel_oneapi_repo`
- `intel_oneapi_gpg_fingerprint`
- `intel_oneapi_gpg_fingerprint_verify`
- `lxc_gpu_network`

### `containers/media`
- `containers_media_instance_name`
- `containers_media_port_offset`
- `containers_media_network`
- `containers_media_hw_accel`
- `containers_media_require_avx`
- `containers_media_stack_enable`
- `containers_media_root_dir`
- `containers_media_config_dir`
- `containers_media_puid`
- `containers_media_pgid`
- `containers_media_timezone`
- `containers_jellyfin_enable`
- `containers_jellyfin_image`
- `containers_jellyfin_port_http`
- `containers_jellyfin_memory_max`
- `containers_plex_enable`
- `containers_plex_image`
- `containers_plex_port_http`
- `containers_plex_claim_token`
- `containers_radarr_enable`
- `containers_radarr_image`
- `containers_radarr_port`
- `containers_sonarr_enable`
- `containers_sonarr_image`
- `containers_sonarr_port`
- `containers_lidarr_enable`
- `containers_lidarr_image`
- `containers_lidarr_port`
- `containers_readarr_enable`
- `containers_readarr_image`
- `containers_readarr_port`
- `containers_prowlarr_enable`
- `containers_prowlarr_image`
- `containers_prowlarr_port`
- `containers_jellyseerr_enable`
- `containers_jellyseerr_image`
- `containers_jellyseerr_port`
- `containers_navidrome_enable`
- `containers_navidrome_image`
- `containers_navidrome_port`
- `containers_transmission_enable`
- `containers_transmission_image`
- `containers_transmission_port_web`
- `containers_transmission_port_peer`
- `containers_transmission_user`
- `containers_transmission_pass`
- `containers_media_pod_enable`
- `containers_media_pod_name`
- `containers_media_gatekeeper_mode`
- `containers_media_domain`
- `containers_media_pod_network`
- `containers_media_auth_provider`
- `containers_media_auth_url`
- `containers_media_fail_secure`
- `containers_bazarr_enable`
- `containers_bazarr_image`
- `containers_bazarr_port`
- `containers_kavita_enable`
- `containers_kavita_image`
- `containers_kavita_port`
- `containers_audiobookshelf_enable`
- `containers_audiobookshelf_image`
- `containers_audiobookshelf_port`

### `containers/memcached`
- `memcached_enable`
- `memcached_image`
- `memcached_port`
- `memcached_memory_mb`
- `memcached_status_check`

### `containers/monitoring`
- `monitoring_enable`
- `monitoring_instance`
- `monitoring_root_dir`
- `monitoring_config_dir`
- `monitoring_network`
- `monitoring_pod_name`
- `monitoring_prometheus_image`
- `monitoring_grafana_image`
- `monitoring_grafana_admin_user`
- `monitoring_grafana_admin_password`
- `containers_monitoring_fail_secure`

### `containers/ops`
- `containers_ops_enable`
- `containers_ops_pod_name`
- `containers_ops_pod_network`
- `containers_ops_root_dir`
- `containers_ops_config_dir`
- `ops_enable`
- `ops_pod_name`
- `ops_pod_network`
- `ops_root_dir`
- `ops_config_dir`
- `containers_homarr_enable`
- `containers_homarr_image`
- `containers_homarr_port`
- `homarr_enable`
- `homarr_image`
- `homarr_port`
- `containers_vaultwarden_enable`
- `containers_vaultwarden_image`
- `containers_vaultwarden_port`
- `containers_vaultwarden_signups_allowed`
- `containers_vaultwarden_admin_token`
- `containers_vaultwarden_fail_secure`
- `vaultwarden_fail_secure`
- `vaultwarden_enable`
- `vaultwarden_image`
- `vaultwarden_port`
- `vaultwarden_signups_allowed`
- `vaultwarden_admin_token`
- `containers_wiki_enable`
- `containers_wiki_image`
- `containers_wiki_port`
- `containers_wiki_db_secret`
- `wiki_enable`
- `wiki_image`
- `wiki_port`
- `wiki_db_secret`
- `containers_wastebin_enable`
- `containers_wastebin_image`
- `containers_wastebin_port`
- `wastebin_enable`
- `wastebin_image`
- `wastebin_port`
- `containers_ops_domain`
- `ops_domain`
- `containers_filebrowser_enable`
- `containers_filebrowser_image`
- `containers_filebrowser_port`
- `filebrowser_enable`
- `filebrowser_image`
- `filebrowser_port`

### `containers/quadlets`
- `containers_quadlet_network_name`
- `containers_quadlet_create_network`
- `containers_quadlet_network_subnet`
- `containers_quadlet_network_gateway`
- `containers_quadlet_network_iprange`
- `containers_quadlet_custom_files`
- `containers_quadlet_arch_override`
- `containers_quadlet_enable_gpu_support`
- `containers_quadlet_gpu_vendor`
- `containers_quadlet_gpu_devices`
- `containers_quadlet_gpu_capabilities`
- `containers_quadlet_gpu_slicing`
- `containers_quadlet_gpu_default_configs`
- `containers_quadlet_container_gpu_config`

### `containers/runtime`
- `containers_install_podman`
- `containers_enable_socket`
- `podman_rootless_enabled`
- `podman_rootless_user`
- `podman_rootless_user_home`
- `podman_rootless_network_mode`
- `podman_rootless_allow_privileged_ports`
- `podman_rootless_privileged_port_start`
- `containers_systemd_dir`
- `containers_systemd_scope`
- `containers_systemd_owner`
- `containers_systemd_group`
- `containers_secrets_dir`
- `containers_secrets_owner`
- `containers_secrets_group`
- `containers_systemd_env`
- `intel_oneapi_gpg_key_url`
- `intel_oneapi_gpg_keyring_path`
- `intel_oneapi_repo`
- `intel_oneapi_gpg_fingerprint`
- `intel_oneapi_gpg_fingerprint_verify`
- `containers_pull_retries`
- `containers_pull_delay`
- `containers_arch_override`
- `containers_enable_gpu_support`
- `containers_gpu_vendor`
- `containers_gpu_count`
- `containers_gpu_slicing`
- `containers_gpu_profiles`
- `containers_gpu_device_selectors`

## Core Variables

### `core/bootstrap`
- `core_install_base_packages`
- `system_base_packages`
- `system_standard_directories`

### `core/entropy`
- `entropy_service_mapping`

### `core/hardware_support`
- `enable_hardware_discovery`
- `require_avx`
- `require_aes_ni`
- `require_crypto_extensions`
- `warn_on_missing_avx`
- `warn_on_missing_crypto`

### `core/identity`
- `identity_set_hostname`
- `identity_domain`

### `core/logging`
- `logging_journal_remote_packages`

### `core/memory`
- `core_memory_compression_strategy`
- `core_memory_shared_vram`
- `core_memory_workload_profile`
- `core_memory_thp_state`
- `core_memory_zram_size_percent`
- `core_memory_zram_algorithm`
- `core_memory_zram_priority`
- `core_memory_zswap_compressor`
- `core_memory_zswap_zpool`
- `core_memory_zswap_max_pool_percent`
- `core_memory_swappiness`
- `core_memory_cache_pressure`
- `core_memory_dirty_bytes`
- `core_memory_dirty_background_bytes`

### `core/repositories`
- `rpmfusion_free_url`
- `rpmfusion_nonfree_url`
- `rpmfusion_free_sha256`
- `rpmfusion_nonfree_sha256`
- `rpmfusion_verify_checksum`

### `core/systemd`
- `systemd_configure_journald`
- `systemd_configure_resolved`
- `systemd_persistent_journal`

### `core/time`
- `time_service_mapping`

## Hardware Variables

### `hardware/firmware`
- `cpu_tier`
- `is_server_cpu`
- `hardware_monitor_temp`
- `hardware_enable_watchdog`

### `hardware/gpu`
- `gpu_stack_enable`
- `gpu_stack_vendor`
- `gpu_stack_mode`
- `gpu_stack_reservation`
- `gpu_stack_arch`
- `gpu_stack_enable_egpu`
- `gpu_stack_egpu_interface`
- `gpu_stack_enable_rdma`
- `gpu_stack_enable_dp_alt_mode`
- `gpu_stack_enable_oneapi`
- `gpu_stack_enable_cuda`
- `gpu_stack_enable_rocm`
- `intel_oneapi_gpg_key_url`
- `intel_oneapi_gpg_keyring_path`
- `intel_oneapi_repo`
- `intel_oneapi_gpg_fingerprint`
- `intel_oneapi_gpg_fingerprint_verify`
- `amd_rocm_gpg_key_url`
- `amd_rocm_gpg_keyring_path`
- `amd_rocm_gpg_key_sha256`
- `amd_rocm_gpg_fingerprint`
- `amd_rocm_gpg_key_verify`
- `nvidia_gpg_key_url`
- `nvidia_gpg_key_sha256`
- `nvidia_gpg_fingerprint`
- `nvidia_gpg_key_verify`
- `gpu_desktop_enable_audio`
- `gpu_desktop_power_profile`
- `gpu_desktop_enable_wayland_support`
- `gpu_desktop_enable_x11_support`
- `gpu_desktop_grant_user_access`

### `hardware/sas`
- `hardware_sas_install_tools`
- `hardware_sas_enable_monitoring`
- `hardware_sas_configure_smartd`
- `hardware_sas_load_drivers`
- `hardware_sas_drivers`
- `hardware_sas_packages`
- `hardware_sas_queue_depth`
- `hardware_sas_smartd_opts`

## Networking Variables

### `networking/container_networks`
- `container_networks_enable`
- `podman_rootless_enabled`
- `podman_rootless_user`
- `podman_rootless_user_home`
- `containers_systemd_dir`
- `containers_systemd_scope`
- `containers_systemd_owner`
- `containers_systemd_group`
- `containers_systemd_env`
- `container_networks_list`

### `networking/desktop`
- `networking_desktop_enable_wifi`
- `networking_desktop_wifi_backend`
- `networking_desktop_manager`
- `networking_desktop_install_gui_tools`

### `networking/firewall`
- `firewall_enabled`
- `firewall_allowed_tcp_ports`
- `firewall_allow_endlessh`
- `firewall_endlessh_port`
- `firewall_allowed_udp_ports`
- `firewall_additional_rules`
- `firewall_forward_policy`

### `networking/physical`
- `interface_capabilities`
- `networking_physical_install_tools`
- `networking_physical_manage_mtu`
- `networking_physical_jumbo_frames_enabled`
- `networking_physical_jumbo_mtu`
- `networking_physical_ring_tuning_enabled`
- `networking_physical_rx_ring_size`
- `networking_physical_tx_ring_size`
- `networking_physical_offload_tuning_enabled`
- `networking_physical_enable_tso`
- `networking_physical_enable_gso`
- `networking_physical_enable_lro`
- `networking_physical_profiles`
- `networking_physical_default_profile`

## Ops Variables

### `ops/connection_info`
- `encryption_method`
- `ssh_rsync_destination`
- `ops_rsync_enable`
- `ops_rsync_allowlist`
- `ops_rsync_ephemeral_allow`
- `ssh_randomize_port`
- `ssh_port_cache_dir`

### `ops/monitoring`
- `monitoring_enable_node_exporter`
- `monitoring_enable_smartmon`
- `monitoring_enable_nvme_cli`
- `monitoring_node_exporter_version`
- `monitoring_node_exporter_port`
- `monitoring_node_exporter_collectors`
- `monitoring_smartd_interval`

### `ops/preflight`
- `preflight_require_systemd`
- `preflight_check_memory`
- `preflight_min_memory_mb`
- `preflight_check_network`
- `preflight_connectivity_check_url`
- `preflight_required_binaries`

### `ops/session`
- `tmux_session_for_deployment`
- `tmux_session_name`

## Orchestration Variables

## Security Variables

### `security/access`
- `ssh_match_rules`
- `access_admin_user`
- `access_admin_password_hash`
- `access_admin_password_enforce`
- `access_admin_password_placeholders`

### `security/advanced`
- `advanced_security_hardening_enabled`
- `ssh_randomize_port`
- `ssh_random_port_range_start`
- `ssh_random_port_range_end`
- `ssh_random_port_file_dest`
- `ssh_rsync_destination`
- `ssh_key_rotation_enabled`
- `ssh_key_rotation_interval_days`
- `tmux_session_for_deployment`
- `tmux_session_name`
- `encryption_method`

### `security/firejail`
- `firejail_enable_gpu`

### `security/hardening`
- `security_hardening_enabled`
- `security_enable_ufw`
- `security_enable_fail2ban`
- `security_enable_auto_updates`
- `security_kernel_hardening`

### `security/ips`
- `ips_fail2ban_sshd_maxretry`
- `ips_fail2ban_sshd_bantime`
- `ips_fail2ban_sshd_findtime`
- `ips_fail2ban_sshd_enabled`
- `ips_fail2ban_caddy_enabled`
- `ips_fail2ban_caddy_maxretry`
- `ips_fail2ban_caddy_bantime`

### `security/kernel`
- `kernel_profile`
- `kernel_enable_iommu`
- `kernel_restrict_dma`
- `kernel_hugepages_enabled`

### `security/resource_protection`
- `resource_min_ram_mb`
- `resource_default_tasks_max`
- `resource_default_memory_max`

### `security/scanning`
- `security_scanning_enable`
- `security_scanning_install_tools`
- `security_package_mapping`
- `security_scanning_extra_packages`
- `security_scanning_optional_tools`
- `security_scanning_critical_tools`
- `security_scanning_rkhunter_warning_threshold`
- `security_scanning_aide_change_threshold`
- `security_scanning_lynis_issue_threshold`
- `security_scanning_checkov_issue_threshold`

### `security/sshd`
- `sshd_backup_config`
- `sshd_disable_weak_keys`
- `sshd_use_strong_ciphers`
- `sshd_allow_tcp_forwarding`
- `sshd_allow_agent_forwarding`
- `sshd_allow_x11_forwarding`
- `sshd_permit_root_login`
- `sshd_password_authentication`
- `sshd_config_path`
- `sshd_enable_trusted_group_exceptions`
- `sshd_trusted_groups`

## Storage Variables

## Virtualization Variables

