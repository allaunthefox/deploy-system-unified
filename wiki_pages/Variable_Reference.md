# Variable_Reference

## Containers Variables

### `containers/anubis`
- `[anubis_enabled](roles/containers_anubis.md#anubis_enabled)`
- `[anubis_port](roles/containers_anubis.md#anubis_port)`
- `[anubis_difficulty](roles/containers_anubis.md#anubis_difficulty)`
- `[anubis_target_url](roles/containers_anubis.md#anubis_target_url)`
- `[anubis_image](roles/containers_anubis.md#anubis_image)`
- `[anubis_container_name](roles/containers_anubis.md#anubis_container_name)`
- `[quadlet_enable_gpu_support](roles/containers_anubis.md#quadlet_enable_gpu_support)`
- `[quadlet_gpu_capabilities](roles/containers_anubis.md#quadlet_gpu_capabilities)`

### `containers/authentik`
- `[authentik_enable](roles/containers_authentik.md#authentik_enable)`
- `[authentik_image](roles/containers_authentik.md#authentik_image)`
- `[authentik_redis_image](roles/containers_authentik.md#authentik_redis_image)`
- `[authentik_postgres_image](roles/containers_authentik.md#authentik_postgres_image)`
- `[authentik_base_dir](roles/containers_authentik.md#authentik_base_dir)`
- `[authentik_data_dir](roles/containers_authentik.md#authentik_data_dir)`
- `[authentik_config_dir](roles/containers_authentik.md#authentik_config_dir)`
- `[authentik_port_http](roles/containers_authentik.md#authentik_port_http)`
- `[authentik_port_https](roles/containers_authentik.md#authentik_port_https)`
- `[authentik_pg_user](roles/containers_authentik.md#authentik_pg_user)`
- `[authentik_pg_db](roles/containers_authentik.md#authentik_pg_db)`
- `[authentik_pg_pass](roles/containers_authentik.md#authentik_pg_pass)`
- `[authentik_secret_key](roles/containers_authentik.md#authentik_secret_key)`
- `[containers_authentik_fail_secure](roles/containers_authentik.md#containers_authentik_fail_secure)`
- `[authentik_email_host](roles/containers_authentik.md#authentik_email_host)`
- `[authentik_email_port](roles/containers_authentik.md#authentik_email_port)`
- `[authentik_email_username](roles/containers_authentik.md#authentik_email_username)`
- `[authentik_email_password](roles/containers_authentik.md#authentik_email_password)`
- `[authentik_email_from](roles/containers_authentik.md#authentik_email_from)`
- `[authentik_email_use_tls](roles/containers_authentik.md#authentik_email_use_tls)`
- `[authentik_network_name](roles/containers_authentik.md#authentik_network_name)`

### `containers/caddy`
- `[containers_caddy_generate_config](roles/containers_caddy.md#containers_caddy_generate_config)`
- `[containers_caddy_acme_email](roles/containers_caddy.md#containers_caddy_acme_email)`
- `[containers_caddy_http_port](roles/containers_caddy.md#containers_caddy_http_port)`
- `[containers_caddy_https_port](roles/containers_caddy.md#containers_caddy_https_port)`
- `[containers_caddy_https_port_udp](roles/containers_caddy.md#containers_caddy_https_port_udp)`
- `[containers_porkbun_api_key](roles/containers_caddy.md#containers_porkbun_api_key)`
- `[containers_porkbun_secret_api_key](roles/containers_caddy.md#containers_porkbun_secret_api_key)`
- `[containers_caddy_network](roles/containers_caddy.md#containers_caddy_network)`
- `[containers_caddy_extra_networks](roles/containers_caddy.md#containers_caddy_extra_networks)`
- `[containers_crowdsec_enable](roles/containers_caddy.md#containers_crowdsec_enable)`
- `[containers_crowdsec_image](roles/containers_caddy.md#containers_crowdsec_image)`
- `[containers_crowdsec_firewall_bouncer_key](roles/containers_caddy.md#containers_crowdsec_firewall_bouncer_key)`
- `[containers_caddy_fail_secure](roles/containers_caddy.md#containers_caddy_fail_secure)`
- `[containers_crowdsec_firewall_bouncer_version](roles/containers_caddy.md#containers_crowdsec_firewall_bouncer_version)`
- `[containers_crowdsec_firewall_bouncer_sha256](roles/containers_caddy.md#containers_crowdsec_firewall_bouncer_sha256)`
- `[containers_crowdsec_secrets_dir](roles/containers_caddy.md#containers_crowdsec_secrets_dir)`
- `[containers_crowdsec_collections](roles/containers_caddy.md#containers_crowdsec_collections)`
- `[containers_quadlet_enable_gpu_support](roles/containers_caddy.md#containers_quadlet_enable_gpu_support)`

### `containers/config`
- `[container_linger_users](roles/containers_config.md#container_linger_users)`

### `containers/lxc`
- `[lxc_enable_gpu_support](roles/containers_lxc.md#lxc_enable_gpu_support)`
- `[lxc_gpu_vendor](roles/containers_lxc.md#lxc_gpu_vendor)`
- `[lxc_gpu_slicing](roles/containers_lxc.md#lxc_gpu_slicing)`
- `[lxc_gpu_default_configs](roles/containers_lxc.md#lxc_gpu_default_configs)`
- `[lxc_container_gpu_config](roles/containers_lxc.md#lxc_container_gpu_config)`
- `[lxc_gpu_security](roles/containers_lxc.md#lxc_gpu_security)`
- `[lxc_gpu_resource_limits](roles/containers_lxc.md#lxc_gpu_resource_limits)`
- `[intel_oneapi_gpg_key_url](roles/containers_lxc.md#intel_oneapi_gpg_key_url)`
- `[intel_oneapi_gpg_keyring_path](roles/containers_lxc.md#intel_oneapi_gpg_keyring_path)`
- `[intel_oneapi_repo](roles/containers_lxc.md#intel_oneapi_repo)`
- `[intel_oneapi_gpg_fingerprint](roles/containers_lxc.md#intel_oneapi_gpg_fingerprint)`
- `[intel_oneapi_gpg_fingerprint_verify](roles/containers_lxc.md#intel_oneapi_gpg_fingerprint_verify)`
- `[lxc_gpu_network](roles/containers_lxc.md#lxc_gpu_network)`

### `containers/media`
- `[containers_media_instance_name](roles/containers_media.md#containers_media_instance_name)`
- `[containers_media_port_offset](roles/containers_media.md#containers_media_port_offset)`
- `[containers_media_network](roles/containers_media.md#containers_media_network)`
- `[containers_media_hw_accel](roles/containers_media.md#containers_media_hw_accel)`
- `[containers_media_require_avx](roles/containers_media.md#containers_media_require_avx)`
- `[containers_media_stack_enable](roles/containers_media.md#containers_media_stack_enable)`
- `[containers_media_root_dir](roles/containers_media.md#containers_media_root_dir)`
- `[containers_media_config_dir](roles/containers_media.md#containers_media_config_dir)`
- `[containers_media_puid](roles/containers_media.md#containers_media_puid)`
- `[containers_media_pgid](roles/containers_media.md#containers_media_pgid)`
- `[containers_media_timezone](roles/containers_media.md#containers_media_timezone)`
- `[containers_jellyfin_enable](roles/containers_media.md#containers_jellyfin_enable)`
- `[containers_jellyfin_image](roles/containers_media.md#containers_jellyfin_image)`
- `[containers_jellyfin_port_http](roles/containers_media.md#containers_jellyfin_port_http)`
- `[containers_jellyfin_memory_max](roles/containers_media.md#containers_jellyfin_memory_max)`
- `[containers_plex_enable](roles/containers_media.md#containers_plex_enable)`
- `[containers_plex_image](roles/containers_media.md#containers_plex_image)`
- `[containers_plex_port_http](roles/containers_media.md#containers_plex_port_http)`
- `[containers_plex_claim_token](roles/containers_media.md#containers_plex_claim_token)`
- `[containers_radarr_enable](roles/containers_media.md#containers_radarr_enable)`
- `[containers_radarr_image](roles/containers_media.md#containers_radarr_image)`
- `[containers_radarr_port](roles/containers_media.md#containers_radarr_port)`
- `[containers_sonarr_enable](roles/containers_media.md#containers_sonarr_enable)`
- `[containers_sonarr_image](roles/containers_media.md#containers_sonarr_image)`
- `[containers_sonarr_port](roles/containers_media.md#containers_sonarr_port)`
- `[containers_lidarr_enable](roles/containers_media.md#containers_lidarr_enable)`
- `[containers_lidarr_image](roles/containers_media.md#containers_lidarr_image)`
- `[containers_lidarr_port](roles/containers_media.md#containers_lidarr_port)`
- `[containers_readarr_enable](roles/containers_media.md#containers_readarr_enable)`
- `[containers_readarr_image](roles/containers_media.md#containers_readarr_image)`
- `[containers_readarr_port](roles/containers_media.md#containers_readarr_port)`
- `[containers_prowlarr_enable](roles/containers_media.md#containers_prowlarr_enable)`
- `[containers_prowlarr_image](roles/containers_media.md#containers_prowlarr_image)`
- `[containers_prowlarr_port](roles/containers_media.md#containers_prowlarr_port)`
- `[containers_jellyseerr_enable](roles/containers_media.md#containers_jellyseerr_enable)`
- `[containers_jellyseerr_image](roles/containers_media.md#containers_jellyseerr_image)`
- `[containers_jellyseerr_port](roles/containers_media.md#containers_jellyseerr_port)`
- `[containers_navidrome_enable](roles/containers_media.md#containers_navidrome_enable)`
- `[containers_navidrome_image](roles/containers_media.md#containers_navidrome_image)`
- `[containers_navidrome_port](roles/containers_media.md#containers_navidrome_port)`
- `[containers_transmission_enable](roles/containers_media.md#containers_transmission_enable)`
- `[containers_transmission_image](roles/containers_media.md#containers_transmission_image)`
- `[containers_transmission_port_web](roles/containers_media.md#containers_transmission_port_web)`
- `[containers_transmission_port_peer](roles/containers_media.md#containers_transmission_port_peer)`
- `[containers_transmission_user](roles/containers_media.md#containers_transmission_user)`
- `[containers_transmission_pass](roles/containers_media.md#containers_transmission_pass)`
- `[containers_media_pod_enable](roles/containers_media.md#containers_media_pod_enable)`
- `[containers_media_pod_name](roles/containers_media.md#containers_media_pod_name)`
- `[containers_media_gatekeeper_mode](roles/containers_media.md#containers_media_gatekeeper_mode)`
- `[containers_media_domain](roles/containers_media.md#containers_media_domain)`
- `[containers_media_pod_network](roles/containers_media.md#containers_media_pod_network)`
- `[containers_media_auth_provider](roles/containers_media.md#containers_media_auth_provider)`
- `[containers_media_auth_url](roles/containers_media.md#containers_media_auth_url)`
- `[containers_media_fail_secure](roles/containers_media.md#containers_media_fail_secure)`
- `[containers_bazarr_enable](roles/containers_media.md#containers_bazarr_enable)`
- `[containers_bazarr_image](roles/containers_media.md#containers_bazarr_image)`
- `[containers_bazarr_port](roles/containers_media.md#containers_bazarr_port)`
- `[containers_kavita_enable](roles/containers_media.md#containers_kavita_enable)`
- `[containers_kavita_image](roles/containers_media.md#containers_kavita_image)`
- `[containers_kavita_port](roles/containers_media.md#containers_kavita_port)`
- `[containers_audiobookshelf_enable](roles/containers_media.md#containers_audiobookshelf_enable)`
- `[containers_audiobookshelf_image](roles/containers_media.md#containers_audiobookshelf_image)`
- `[containers_audiobookshelf_port](roles/containers_media.md#containers_audiobookshelf_port)`

### `containers/memcached`
- `[memcached_enable](roles/containers_memcached.md#memcached_enable)`
- `[memcached_image](roles/containers_memcached.md#memcached_image)`
- `[memcached_port](roles/containers_memcached.md#memcached_port)`
- `[memcached_memory_mb](roles/containers_memcached.md#memcached_memory_mb)`
- `[memcached_status_check](roles/containers_memcached.md#memcached_status_check)`

### `containers/monitoring`
- `[monitoring_enable](roles/containers_monitoring.md#monitoring_enable)`
- `[monitoring_instance](roles/containers_monitoring.md#monitoring_instance)`
- `[monitoring_root_dir](roles/containers_monitoring.md#monitoring_root_dir)`
- `[monitoring_config_dir](roles/containers_monitoring.md#monitoring_config_dir)`
- `[monitoring_network](roles/containers_monitoring.md#monitoring_network)`
- `[monitoring_pod_name](roles/containers_monitoring.md#monitoring_pod_name)`
- `[monitoring_prometheus_image](roles/containers_monitoring.md#monitoring_prometheus_image)`
- `[monitoring_grafana_image](roles/containers_monitoring.md#monitoring_grafana_image)`
- `[monitoring_grafana_admin_user](roles/containers_monitoring.md#monitoring_grafana_admin_user)`
- `[monitoring_grafana_admin_password](roles/containers_monitoring.md#monitoring_grafana_admin_password)`
- `[containers_monitoring_fail_secure](roles/containers_monitoring.md#containers_monitoring_fail_secure)`

### `containers/ops`
- `[containers_ops_enable](roles/containers_ops.md#containers_ops_enable)`
- `[containers_ops_pod_name](roles/containers_ops.md#containers_ops_pod_name)`
- `[containers_ops_pod_network](roles/containers_ops.md#containers_ops_pod_network)`
- `[containers_ops_root_dir](roles/containers_ops.md#containers_ops_root_dir)`
- `[containers_ops_config_dir](roles/containers_ops.md#containers_ops_config_dir)`
- `[ops_enable](roles/containers_ops.md#ops_enable)`
- `[ops_pod_name](roles/containers_ops.md#ops_pod_name)`
- `[ops_pod_network](roles/containers_ops.md#ops_pod_network)`
- `[ops_root_dir](roles/containers_ops.md#ops_root_dir)`
- `[ops_config_dir](roles/containers_ops.md#ops_config_dir)`
- `[containers_homarr_enable](roles/containers_ops.md#containers_homarr_enable)`
- `[containers_homarr_image](roles/containers_ops.md#containers_homarr_image)`
- `[containers_homarr_port](roles/containers_ops.md#containers_homarr_port)`
- `[homarr_enable](roles/containers_ops.md#homarr_enable)`
- `[homarr_image](roles/containers_ops.md#homarr_image)`
- `[homarr_port](roles/containers_ops.md#homarr_port)`
- `[containers_vaultwarden_enable](roles/containers_ops.md#containers_vaultwarden_enable)`
- `[containers_vaultwarden_image](roles/containers_ops.md#containers_vaultwarden_image)`
- `[containers_vaultwarden_port](roles/containers_ops.md#containers_vaultwarden_port)`
- `[containers_vaultwarden_signups_allowed](roles/containers_ops.md#containers_vaultwarden_signups_allowed)`
- `[containers_vaultwarden_admin_token](roles/containers_ops.md#containers_vaultwarden_admin_token)`
- `[containers_vaultwarden_fail_secure](roles/containers_ops.md#containers_vaultwarden_fail_secure)`
- `[vaultwarden_fail_secure](roles/containers_ops.md#vaultwarden_fail_secure)`
- `[vaultwarden_enable](roles/containers_ops.md#vaultwarden_enable)`
- `[vaultwarden_image](roles/containers_ops.md#vaultwarden_image)`
- `[vaultwarden_port](roles/containers_ops.md#vaultwarden_port)`
- `[vaultwarden_signups_allowed](roles/containers_ops.md#vaultwarden_signups_allowed)`
- `[vaultwarden_admin_token](roles/containers_ops.md#vaultwarden_admin_token)`
- `[containers_wiki_enable](roles/containers_ops.md#containers_wiki_enable)`
- `[containers_wiki_image](roles/containers_ops.md#containers_wiki_image)`
- `[containers_wiki_port](roles/containers_ops.md#containers_wiki_port)`
- `[containers_wiki_db_secret](roles/containers_ops.md#containers_wiki_db_secret)`
- `[wiki_enable](roles/containers_ops.md#wiki_enable)`
- `[wiki_image](roles/containers_ops.md#wiki_image)`
- `[wiki_port](roles/containers_ops.md#wiki_port)`
- `[wiki_db_secret](roles/containers_ops.md#wiki_db_secret)`
- `[containers_wastebin_enable](roles/containers_ops.md#containers_wastebin_enable)`
- `[containers_wastebin_image](roles/containers_ops.md#containers_wastebin_image)`
- `[containers_wastebin_port](roles/containers_ops.md#containers_wastebin_port)`
- `[wastebin_enable](roles/containers_ops.md#wastebin_enable)`
- `[wastebin_image](roles/containers_ops.md#wastebin_image)`
- `[wastebin_port](roles/containers_ops.md#wastebin_port)`
- `[containers_ops_domain](roles/containers_ops.md#containers_ops_domain)`
- `[ops_domain](roles/containers_ops.md#ops_domain)`
- `[containers_filebrowser_enable](roles/containers_ops.md#containers_filebrowser_enable)`
- `[containers_filebrowser_image](roles/containers_ops.md#containers_filebrowser_image)`
- `[containers_filebrowser_port](roles/containers_ops.md#containers_filebrowser_port)`
- `[filebrowser_enable](roles/containers_ops.md#filebrowser_enable)`
- `[filebrowser_image](roles/containers_ops.md#filebrowser_image)`
- `[filebrowser_port](roles/containers_ops.md#filebrowser_port)`

### `containers/quadlets`
- `[containers_quadlet_network_name](roles/containers_quadlets.md#containers_quadlet_network_name)`
- `[containers_quadlet_create_network](roles/containers_quadlets.md#containers_quadlet_create_network)`
- `[containers_quadlet_network_subnet](roles/containers_quadlets.md#containers_quadlet_network_subnet)`
- `[containers_quadlet_network_gateway](roles/containers_quadlets.md#containers_quadlet_network_gateway)`
- `[containers_quadlet_network_iprange](roles/containers_quadlets.md#containers_quadlet_network_iprange)`
- `[containers_quadlet_custom_files](roles/containers_quadlets.md#containers_quadlet_custom_files)`
- `[containers_quadlet_arch_override](roles/containers_quadlets.md#containers_quadlet_arch_override)`
- `[containers_quadlet_enable_gpu_support](roles/containers_quadlets.md#containers_quadlet_enable_gpu_support)`
- `[containers_quadlet_gpu_vendor](roles/containers_quadlets.md#containers_quadlet_gpu_vendor)`
- `[containers_quadlet_gpu_devices](roles/containers_quadlets.md#containers_quadlet_gpu_devices)`
- `[containers_quadlet_gpu_capabilities](roles/containers_quadlets.md#containers_quadlet_gpu_capabilities)`
- `[containers_quadlet_gpu_slicing](roles/containers_quadlets.md#containers_quadlet_gpu_slicing)`
- `[containers_quadlet_gpu_default_configs](roles/containers_quadlets.md#containers_quadlet_gpu_default_configs)`
- `[containers_quadlet_container_gpu_config](roles/containers_quadlets.md#containers_quadlet_container_gpu_config)`

### `containers/runtime`
- `[containers_install_podman](roles/containers_runtime.md#containers_install_podman)`
- `[containers_enable_socket](roles/containers_runtime.md#containers_enable_socket)`
- `[podman_rootless_enabled](roles/containers_runtime.md#podman_rootless_enabled)`
- `[podman_rootless_user](roles/containers_runtime.md#podman_rootless_user)`
- `[podman_rootless_user_home](roles/containers_runtime.md#podman_rootless_user_home)`
- `[podman_rootless_network_mode](roles/containers_runtime.md#podman_rootless_network_mode)`
- `[podman_rootless_allow_privileged_ports](roles/containers_runtime.md#podman_rootless_allow_privileged_ports)`
- `[podman_rootless_privileged_port_start](roles/containers_runtime.md#podman_rootless_privileged_port_start)`
- `[containers_systemd_dir](roles/containers_runtime.md#containers_systemd_dir)`
- `[containers_systemd_scope](roles/containers_runtime.md#containers_systemd_scope)`
- `[containers_systemd_owner](roles/containers_runtime.md#containers_systemd_owner)`
- `[containers_systemd_group](roles/containers_runtime.md#containers_systemd_group)`
- `[containers_secrets_dir](roles/containers_runtime.md#containers_secrets_dir)`
- `[containers_secrets_owner](roles/containers_runtime.md#containers_secrets_owner)`
- `[containers_secrets_group](roles/containers_runtime.md#containers_secrets_group)`
- `[containers_systemd_env](roles/containers_runtime.md#containers_systemd_env)`
- `[intel_oneapi_gpg_key_url](roles/containers_runtime.md#intel_oneapi_gpg_key_url)`
- `[intel_oneapi_gpg_keyring_path](roles/containers_runtime.md#intel_oneapi_gpg_keyring_path)`
- `[intel_oneapi_repo](roles/containers_runtime.md#intel_oneapi_repo)`
- `[intel_oneapi_gpg_fingerprint](roles/containers_runtime.md#intel_oneapi_gpg_fingerprint)`
- `[intel_oneapi_gpg_fingerprint_verify](roles/containers_runtime.md#intel_oneapi_gpg_fingerprint_verify)`
- `[containers_pull_retries](roles/containers_runtime.md#containers_pull_retries)`
- `[containers_pull_delay](roles/containers_runtime.md#containers_pull_delay)`
- `[containers_arch_override](roles/containers_runtime.md#containers_arch_override)`
- `[containers_enable_gpu_support](roles/containers_runtime.md#containers_enable_gpu_support)`
- `[containers_gpu_vendor](roles/containers_runtime.md#containers_gpu_vendor)`
- `[containers_gpu_count](roles/containers_runtime.md#containers_gpu_count)`
- `[containers_gpu_slicing](roles/containers_runtime.md#containers_gpu_slicing)`
- `[containers_gpu_profiles](roles/containers_runtime.md#containers_gpu_profiles)`
- `[containers_gpu_device_selectors](roles/containers_runtime.md#containers_gpu_device_selectors)`

## Core Variables

### `core/bootstrap`
- `[core_install_base_packages](roles/core_bootstrap.md#core_install_base_packages)`
- `[system_base_packages](roles/core_bootstrap.md#system_base_packages)`
- `[system_standard_directories](roles/core_bootstrap.md#system_standard_directories)`

### `core/entropy`
- `[entropy_service_mapping](roles/core_entropy.md#entropy_service_mapping)`

### `core/hardware_support`
- `[enable_hardware_discovery](roles/core_hardware_support.md#enable_hardware_discovery)`
- `[require_avx](roles/core_hardware_support.md#require_avx)`
- `[require_aes_ni](roles/core_hardware_support.md#require_aes_ni)`
- `[require_crypto_extensions](roles/core_hardware_support.md#require_crypto_extensions)`
- `[warn_on_missing_avx](roles/core_hardware_support.md#warn_on_missing_avx)`
- `[warn_on_missing_crypto](roles/core_hardware_support.md#warn_on_missing_crypto)`

### `core/identity`
- `[identity_set_hostname](roles/core_identity.md#identity_set_hostname)`
- `[identity_domain](roles/core_identity.md#identity_domain)`

### `core/logging`
- `[logging_journal_remote_packages](roles/core_logging.md#logging_journal_remote_packages)`

### `core/memory`
- `[core_memory_compression_strategy](roles/core_memory.md#core_memory_compression_strategy)`
- `[core_memory_shared_vram](roles/core_memory.md#core_memory_shared_vram)`
- `[core_memory_workload_profile](roles/core_memory.md#core_memory_workload_profile)`
- `[core_memory_thp_state](roles/core_memory.md#core_memory_thp_state)`
- `[core_memory_zram_size_percent](roles/core_memory.md#core_memory_zram_size_percent)`
- `[core_memory_zram_algorithm](roles/core_memory.md#core_memory_zram_algorithm)`
- `[core_memory_zram_priority](roles/core_memory.md#core_memory_zram_priority)`
- `[core_memory_zswap_compressor](roles/core_memory.md#core_memory_zswap_compressor)`
- `[core_memory_zswap_zpool](roles/core_memory.md#core_memory_zswap_zpool)`
- `[core_memory_zswap_max_pool_percent](roles/core_memory.md#core_memory_zswap_max_pool_percent)`
- `[core_memory_swappiness](roles/core_memory.md#core_memory_swappiness)`
- `[core_memory_cache_pressure](roles/core_memory.md#core_memory_cache_pressure)`
- `[core_memory_dirty_bytes](roles/core_memory.md#core_memory_dirty_bytes)`
- `[core_memory_dirty_background_bytes](roles/core_memory.md#core_memory_dirty_background_bytes)`

### `core/repositories`
- `[rpmfusion_free_url](roles/core_repositories.md#rpmfusion_free_url)`
- `[rpmfusion_nonfree_url](roles/core_repositories.md#rpmfusion_nonfree_url)`
- `[rpmfusion_free_sha256](roles/core_repositories.md#rpmfusion_free_sha256)`
- `[rpmfusion_nonfree_sha256](roles/core_repositories.md#rpmfusion_nonfree_sha256)`
- `[rpmfusion_verify_checksum](roles/core_repositories.md#rpmfusion_verify_checksum)`

### `core/systemd`
- `[systemd_configure_journald](roles/core_systemd.md#systemd_configure_journald)`
- `[systemd_configure_resolved](roles/core_systemd.md#systemd_configure_resolved)`
- `[systemd_persistent_journal](roles/core_systemd.md#systemd_persistent_journal)`

### `core/time`
- `[time_service_mapping](roles/core_time.md#time_service_mapping)`

## Hardware Variables

### `hardware/firmware`
- `[cpu_tier](roles/hardware_firmware.md#cpu_tier)`
- `[is_server_cpu](roles/hardware_firmware.md#is_server_cpu)`
- `[hardware_monitor_temp](roles/hardware_firmware.md#hardware_monitor_temp)`
- `[hardware_enable_watchdog](roles/hardware_firmware.md#hardware_enable_watchdog)`

### `hardware/gpu`
- `[gpu_stack_enable](roles/hardware_gpu.md#gpu_stack_enable)`
- `[gpu_stack_vendor](roles/hardware_gpu.md#gpu_stack_vendor)`
- `[gpu_stack_mode](roles/hardware_gpu.md#gpu_stack_mode)`
- `[gpu_stack_reservation](roles/hardware_gpu.md#gpu_stack_reservation)`
- `[gpu_stack_arch](roles/hardware_gpu.md#gpu_stack_arch)`
- `[gpu_stack_enable_egpu](roles/hardware_gpu.md#gpu_stack_enable_egpu)`
- `[gpu_stack_egpu_interface](roles/hardware_gpu.md#gpu_stack_egpu_interface)`
- `[gpu_stack_enable_rdma](roles/hardware_gpu.md#gpu_stack_enable_rdma)`
- `[gpu_stack_enable_dp_alt_mode](roles/hardware_gpu.md#gpu_stack_enable_dp_alt_mode)`
- `[gpu_stack_enable_oneapi](roles/hardware_gpu.md#gpu_stack_enable_oneapi)`
- `[gpu_stack_enable_cuda](roles/hardware_gpu.md#gpu_stack_enable_cuda)`
- `[gpu_stack_enable_rocm](roles/hardware_gpu.md#gpu_stack_enable_rocm)`
- `[intel_oneapi_gpg_key_url](roles/hardware_gpu.md#intel_oneapi_gpg_key_url)`
- `[intel_oneapi_gpg_keyring_path](roles/hardware_gpu.md#intel_oneapi_gpg_keyring_path)`
- `[intel_oneapi_repo](roles/hardware_gpu.md#intel_oneapi_repo)`
- `[intel_oneapi_gpg_fingerprint](roles/hardware_gpu.md#intel_oneapi_gpg_fingerprint)`
- `[intel_oneapi_gpg_fingerprint_verify](roles/hardware_gpu.md#intel_oneapi_gpg_fingerprint_verify)`
- `[amd_rocm_gpg_key_url](roles/hardware_gpu.md#amd_rocm_gpg_key_url)`
- `[amd_rocm_gpg_keyring_path](roles/hardware_gpu.md#amd_rocm_gpg_keyring_path)`
- `[amd_rocm_gpg_key_sha256](roles/hardware_gpu.md#amd_rocm_gpg_key_sha256)`
- `[amd_rocm_gpg_fingerprint](roles/hardware_gpu.md#amd_rocm_gpg_fingerprint)`
- `[amd_rocm_gpg_key_verify](roles/hardware_gpu.md#amd_rocm_gpg_key_verify)`
- `[nvidia_gpg_key_url](roles/hardware_gpu.md#nvidia_gpg_key_url)`
- `[nvidia_gpg_key_sha256](roles/hardware_gpu.md#nvidia_gpg_key_sha256)`
- `[nvidia_gpg_fingerprint](roles/hardware_gpu.md#nvidia_gpg_fingerprint)`
- `[nvidia_gpg_key_verify](roles/hardware_gpu.md#nvidia_gpg_key_verify)`
- `[gpu_desktop_enable_audio](roles/hardware_gpu.md#gpu_desktop_enable_audio)`
- `[gpu_desktop_power_profile](roles/hardware_gpu.md#gpu_desktop_power_profile)`
- `[gpu_desktop_enable_wayland_support](roles/hardware_gpu.md#gpu_desktop_enable_wayland_support)`
- `[gpu_desktop_enable_x11_support](roles/hardware_gpu.md#gpu_desktop_enable_x11_support)`
- `[gpu_desktop_grant_user_access](roles/hardware_gpu.md#gpu_desktop_grant_user_access)`

### `hardware/sas`
- `[hardware_sas_install_tools](roles/hardware_sas.md#hardware_sas_install_tools)`
- `[hardware_sas_enable_monitoring](roles/hardware_sas.md#hardware_sas_enable_monitoring)`
- `[hardware_sas_configure_smartd](roles/hardware_sas.md#hardware_sas_configure_smartd)`
- `[hardware_sas_load_drivers](roles/hardware_sas.md#hardware_sas_load_drivers)`
- `[hardware_sas_drivers](roles/hardware_sas.md#hardware_sas_drivers)`
- `[hardware_sas_packages](roles/hardware_sas.md#hardware_sas_packages)`
- `[hardware_sas_queue_depth](roles/hardware_sas.md#hardware_sas_queue_depth)`
- `[hardware_sas_smartd_opts](roles/hardware_sas.md#hardware_sas_smartd_opts)`

## Networking Variables

### `networking/container_networks`
- `[container_networks_enable](roles/networking_container_networks.md#container_networks_enable)`
- `[podman_rootless_enabled](roles/networking_container_networks.md#podman_rootless_enabled)`
- `[podman_rootless_user](roles/networking_container_networks.md#podman_rootless_user)`
- `[podman_rootless_user_home](roles/networking_container_networks.md#podman_rootless_user_home)`
- `[containers_systemd_dir](roles/networking_container_networks.md#containers_systemd_dir)`
- `[containers_systemd_scope](roles/networking_container_networks.md#containers_systemd_scope)`
- `[containers_systemd_owner](roles/networking_container_networks.md#containers_systemd_owner)`
- `[containers_systemd_group](roles/networking_container_networks.md#containers_systemd_group)`
- `[containers_systemd_env](roles/networking_container_networks.md#containers_systemd_env)`
- `[container_networks_list](roles/networking_container_networks.md#container_networks_list)`

### `networking/desktop`
- `[networking_desktop_enable_wifi](roles/networking_desktop.md#networking_desktop_enable_wifi)`
- `[networking_desktop_wifi_backend](roles/networking_desktop.md#networking_desktop_wifi_backend)`
- `[networking_desktop_manager](roles/networking_desktop.md#networking_desktop_manager)`
- `[networking_desktop_install_gui_tools](roles/networking_desktop.md#networking_desktop_install_gui_tools)`

### `networking/firewall`
- `[firewall_enabled](roles/networking_firewall.md#firewall_enabled)`
- `[firewall_allowed_tcp_ports](roles/networking_firewall.md#firewall_allowed_tcp_ports)`
- `[firewall_allow_endlessh](roles/networking_firewall.md#firewall_allow_endlessh)`
- `[firewall_endlessh_port](roles/networking_firewall.md#firewall_endlessh_port)`
- `[firewall_allowed_udp_ports](roles/networking_firewall.md#firewall_allowed_udp_ports)`
- `[firewall_additional_rules](roles/networking_firewall.md#firewall_additional_rules)`
- `[firewall_forward_policy](roles/networking_firewall.md#firewall_forward_policy)`

### `networking/physical`
- `[interface_capabilities](roles/networking_physical.md#interface_capabilities)`
- `[networking_physical_install_tools](roles/networking_physical.md#networking_physical_install_tools)`
- `[networking_physical_manage_mtu](roles/networking_physical.md#networking_physical_manage_mtu)`
- `[networking_physical_jumbo_frames_enabled](roles/networking_physical.md#networking_physical_jumbo_frames_enabled)`
- `[networking_physical_jumbo_mtu](roles/networking_physical.md#networking_physical_jumbo_mtu)`
- `[networking_physical_ring_tuning_enabled](roles/networking_physical.md#networking_physical_ring_tuning_enabled)`
- `[networking_physical_rx_ring_size](roles/networking_physical.md#networking_physical_rx_ring_size)`
- `[networking_physical_tx_ring_size](roles/networking_physical.md#networking_physical_tx_ring_size)`
- `[networking_physical_offload_tuning_enabled](roles/networking_physical.md#networking_physical_offload_tuning_enabled)`
- `[networking_physical_enable_tso](roles/networking_physical.md#networking_physical_enable_tso)`
- `[networking_physical_enable_gso](roles/networking_physical.md#networking_physical_enable_gso)`
- `[networking_physical_enable_lro](roles/networking_physical.md#networking_physical_enable_lro)`
- `[networking_physical_profiles](roles/networking_physical.md#networking_physical_profiles)`
- `[networking_physical_default_profile](roles/networking_physical.md#networking_physical_default_profile)`

## Ops Variables

### `ops/connection_info`
- `[encryption_method](roles/ops_connection_info.md#encryption_method)`
- `[ssh_rsync_destination](roles/ops_connection_info.md#ssh_rsync_destination)`
- `[ops_rsync_enable](roles/ops_connection_info.md#ops_rsync_enable)`
- `[ops_rsync_allowlist](roles/ops_connection_info.md#ops_rsync_allowlist)`
- `[ops_rsync_ephemeral_allow](roles/ops_connection_info.md#ops_rsync_ephemeral_allow)`
- `[ssh_randomize_port](roles/ops_connection_info.md#ssh_randomize_port)`
- `[ssh_port_cache_dir](roles/ops_connection_info.md#ssh_port_cache_dir)`

### `ops/monitoring`
- `[monitoring_enable_node_exporter](roles/ops_monitoring.md#monitoring_enable_node_exporter)`
- `[monitoring_enable_smartmon](roles/ops_monitoring.md#monitoring_enable_smartmon)`
- `[monitoring_enable_nvme_cli](roles/ops_monitoring.md#monitoring_enable_nvme_cli)`
- `[monitoring_node_exporter_version](roles/ops_monitoring.md#monitoring_node_exporter_version)`
- `[monitoring_node_exporter_port](roles/ops_monitoring.md#monitoring_node_exporter_port)`
- `[monitoring_node_exporter_collectors](roles/ops_monitoring.md#monitoring_node_exporter_collectors)`
- `[monitoring_smartd_interval](roles/ops_monitoring.md#monitoring_smartd_interval)`

### `ops/preflight`
- `[preflight_require_systemd](roles/ops_preflight.md#preflight_require_systemd)`
- `[preflight_check_memory](roles/ops_preflight.md#preflight_check_memory)`
- `[preflight_min_memory_mb](roles/ops_preflight.md#preflight_min_memory_mb)`
- `[preflight_check_network](roles/ops_preflight.md#preflight_check_network)`
- `[preflight_connectivity_check_url](roles/ops_preflight.md#preflight_connectivity_check_url)`
- `[preflight_required_binaries](roles/ops_preflight.md#preflight_required_binaries)`

### `ops/session`
- `[tmux_session_for_deployment](roles/ops_session.md#tmux_session_for_deployment)`
- `[tmux_session_name](roles/ops_session.md#tmux_session_name)`

## Orchestration Variables

## Security Variables

### `security/access`
- `[ssh_match_rules](roles/security_access.md#ssh_match_rules)`
- `[access_admin_user](roles/security_access.md#access_admin_user)`
- `[access_admin_password_hash](roles/security_access.md#access_admin_password_hash)`
- `[access_admin_password_enforce](roles/security_access.md#access_admin_password_enforce)`
- `[access_admin_password_placeholders](roles/security_access.md#access_admin_password_placeholders)`

### `security/advanced`
- `[advanced_security_hardening_enabled](roles/security_advanced.md#advanced_security_hardening_enabled)`
- `[ssh_randomize_port](roles/security_advanced.md#ssh_randomize_port)`
- `[ssh_random_port_range_start](roles/security_advanced.md#ssh_random_port_range_start)`
- `[ssh_random_port_range_end](roles/security_advanced.md#ssh_random_port_range_end)`
- `[ssh_random_port_file_dest](roles/security_advanced.md#ssh_random_port_file_dest)`
- `[ssh_rsync_destination](roles/security_advanced.md#ssh_rsync_destination)`
- `[ssh_key_rotation_enabled](roles/security_advanced.md#ssh_key_rotation_enabled)`
- `[ssh_key_rotation_interval_days](roles/security_advanced.md#ssh_key_rotation_interval_days)`
- `[tmux_session_for_deployment](roles/security_advanced.md#tmux_session_for_deployment)`
- `[tmux_session_name](roles/security_advanced.md#tmux_session_name)`
- `[encryption_method](roles/security_advanced.md#encryption_method)`

### `security/firejail`
- `[firejail_enable_gpu](roles/security_firejail.md#firejail_enable_gpu)`

### `security/hardening`
- `[security_hardening_enabled](roles/security_hardening.md#security_hardening_enabled)`
- `[security_enable_ufw](roles/security_hardening.md#security_enable_ufw)`
- `[security_enable_fail2ban](roles/security_hardening.md#security_enable_fail2ban)`
- `[security_enable_auto_updates](roles/security_hardening.md#security_enable_auto_updates)`
- `[security_kernel_hardening](roles/security_hardening.md#security_kernel_hardening)`

### `security/ips`
- `[ips_fail2ban_sshd_maxretry](roles/security_ips.md#ips_fail2ban_sshd_maxretry)`
- `[ips_fail2ban_sshd_bantime](roles/security_ips.md#ips_fail2ban_sshd_bantime)`
- `[ips_fail2ban_sshd_findtime](roles/security_ips.md#ips_fail2ban_sshd_findtime)`
- `[ips_fail2ban_sshd_enabled](roles/security_ips.md#ips_fail2ban_sshd_enabled)`
- `[ips_fail2ban_caddy_enabled](roles/security_ips.md#ips_fail2ban_caddy_enabled)`
- `[ips_fail2ban_caddy_maxretry](roles/security_ips.md#ips_fail2ban_caddy_maxretry)`
- `[ips_fail2ban_caddy_bantime](roles/security_ips.md#ips_fail2ban_caddy_bantime)`

### `security/kernel`
- `[kernel_profile](roles/security_kernel.md#kernel_profile)`
- `[kernel_enable_iommu](roles/security_kernel.md#kernel_enable_iommu)`
- `[kernel_restrict_dma](roles/security_kernel.md#kernel_restrict_dma)`
- `[kernel_hugepages_enabled](roles/security_kernel.md#kernel_hugepages_enabled)`

### `security/resource_protection`
- `[resource_min_ram_mb](roles/security_resource_protection.md#resource_min_ram_mb)`
- `[resource_default_tasks_max](roles/security_resource_protection.md#resource_default_tasks_max)`
- `[resource_default_memory_max](roles/security_resource_protection.md#resource_default_memory_max)`

### `security/scanning`
- `[security_scanning_enable](roles/security_scanning.md#security_scanning_enable)`
- `[security_scanning_install_tools](roles/security_scanning.md#security_scanning_install_tools)`
- `[security_package_mapping](roles/security_scanning.md#security_package_mapping)`
- `[security_scanning_extra_packages](roles/security_scanning.md#security_scanning_extra_packages)`
- `[security_scanning_optional_tools](roles/security_scanning.md#security_scanning_optional_tools)`
- `[security_scanning_critical_tools](roles/security_scanning.md#security_scanning_critical_tools)`
- `[security_scanning_rkhunter_warning_threshold](roles/security_scanning.md#security_scanning_rkhunter_warning_threshold)`
- `[security_scanning_aide_change_threshold](roles/security_scanning.md#security_scanning_aide_change_threshold)`
- `[security_scanning_lynis_issue_threshold](roles/security_scanning.md#security_scanning_lynis_issue_threshold)`
- `[security_scanning_checkov_issue_threshold](roles/security_scanning.md#security_scanning_checkov_issue_threshold)`

### `security/sshd`
- `[sshd_backup_config](roles/security_sshd.md#sshd_backup_config)`
- `[sshd_disable_weak_keys](roles/security_sshd.md#sshd_disable_weak_keys)`
- `[sshd_use_strong_ciphers](roles/security_sshd.md#sshd_use_strong_ciphers)`
- `[sshd_allow_tcp_forwarding](roles/security_sshd.md#sshd_allow_tcp_forwarding)`
- `[sshd_allow_agent_forwarding](roles/security_sshd.md#sshd_allow_agent_forwarding)`
- `[sshd_allow_x11_forwarding](roles/security_sshd.md#sshd_allow_x11_forwarding)`
- `[sshd_permit_root_login](roles/security_sshd.md#sshd_permit_root_login)`
- `[sshd_password_authentication](roles/security_sshd.md#sshd_password_authentication)`
- `[sshd_config_path](roles/security_sshd.md#sshd_config_path)`
- `[sshd_enable_trusted_group_exceptions](roles/security_sshd.md#sshd_enable_trusted_group_exceptions)`
- `[sshd_trusted_groups](roles/security_sshd.md#sshd_trusted_groups)`

## Storage Variables

## Virtualization Variables

