# Variable_Reference_Core

## Core Variables

### `core/bootstrap`
- `[core_install_base_packages](roles/core_bootstrap.md#coreinstallbasepackages)`
- `[system_base_packages](roles/core_bootstrap.md#systembasepackages)`
- `[system_standard_directories](roles/core_bootstrap.md#systemstandarddirectories)`

### `core/entropy`
- `[entropy_service_mapping](roles/core_entropy.md#entropyservicemapping)`

### `core/hardware_support`
- `[enable_hardware_discovery](roles/core_hardware_support.md#enablehardwarediscovery)`
- `[require_avx](roles/core_hardware_support.md#requireavx)`
- `[require_aes_ni](roles/core_hardware_support.md#requireaesni)`
- `[require_crypto_extensions](roles/core_hardware_support.md#requirecryptoextensions)`
- `[warn_on_missing_avx](roles/core_hardware_support.md#warnonmissingavx)`
- `[warn_on_missing_crypto](roles/core_hardware_support.md#warnonmissingcrypto)`

### `core/identity`
- `[identity_set_hostname](roles/core_identity.md#identitysethostname)`
- `[identity_domain](roles/core_identity.md#identitydomain)`

### `core/logging`
- `[logging_journal_remote_packages](roles/core_logging.md#loggingjournalremotepackages)`

### `core/memory`
- `[core_memory_compression_strategy](roles/core_memory.md#corememorycompressionstrategy)`
- `[core_memory_shared_vram](roles/core_memory.md#corememorysharedvram)`
- `[core_memory_workload_profile](roles/core_memory.md#corememoryworkloadprofile)`
- `[core_memory_thp_state](roles/core_memory.md#corememorythpstate)`
- `[core_memory_zram_size_percent](roles/core_memory.md#corememoryzramsizepercent)`
- `[core_memory_zram_algorithm](roles/core_memory.md#corememoryzramalgorithm)`
- `[core_memory_zram_priority](roles/core_memory.md#corememoryzrampriority)`
- `[core_memory_zswap_compressor](roles/core_memory.md#corememoryzswapcompressor)`
- `[core_memory_zswap_zpool](roles/core_memory.md#corememoryzswapzpool)`
- `[core_memory_zswap_max_pool_percent](roles/core_memory.md#corememoryzswapmaxpoolpercent)`
- `[core_memory_swappiness](roles/core_memory.md#corememoryswappiness)`
- `[core_memory_cache_pressure](roles/core_memory.md#corememorycachepressure)`
- `[core_memory_dirty_bytes](roles/core_memory.md#corememorydirtybytes)`
- `[core_memory_dirty_background_bytes](roles/core_memory.md#corememorydirtybackgroundbytes)`

### `core/repositories`
- `[rpmfusion_free_url](roles/core_repositories.md#rpmfusionfreeurl)`
- `[rpmfusion_nonfree_url](roles/core_repositories.md#rpmfusionnonfreeurl)`
- `[rpmfusion_free_sha256](roles/core_repositories.md#rpmfusionfreesha256)`
- `[rpmfusion_nonfree_sha256](roles/core_repositories.md#rpmfusionnonfreesha256)`
- `[rpmfusion_verify_checksum](roles/core_repositories.md#rpmfusionverifychecksum)`

### `core/secrets`
- `[secrets_validation_enabled](roles/core_secrets.md#secretsvalidationenabled)`
- `[secrets_validation_mode](roles/core_secrets.md#secretsvalidationmode)`
- `[secrets_validation_strict](roles/core_secrets.md#secretsvalidationstrict)`
- `[secrets_validation_negative_test](roles/core_secrets.md#secretsvalidationnegativetest)`
- `[secrets_validation_positive_test](roles/core_secrets.md#secretsvalidationpositivetest)`
- `[secrets_validation_timeout](roles/core_secrets.md#secretsvalidationtimeout)`
- `[secrets_validation_retries](roles/core_secrets.md#secretsvalidationretries)`
- `[secrets_validation_delay](roles/core_secrets.md#secretsvalidationdelay)`

### `core/systemd`
- `[systemd_configure_journald](roles/core_systemd.md#systemdconfigurejournald)`
- `[systemd_configure_resolved](roles/core_systemd.md#systemdconfigureresolved)`
- `[systemd_persistent_journal](roles/core_systemd.md#systemdpersistentjournal)`

### `core/time`
- `[time_service_mapping](roles/core_time.md#timeservicemapping)`

### `core/updates`
- `[automatic_updates_enabled](roles/core_updates.md#automaticupdatesenabled)`
- `[automatic_updates_type](roles/core_updates.md#automaticupdatestype)`
- `[automatic_updates_download](roles/core_updates.md#automaticupdatesdownload)`
- `[automatic_updates_apply](roles/core_updates.md#automaticupdatesapply)`
- `[automatic_updates_notify](roles/core_updates.md#automaticupdatesnotify)`
- `[automatic_updates_reboot](roles/core_updates.md#automaticupdatesreboot)`
- `[automatic_updates_reboot_time](roles/core_updates.md#automaticupdatesreboottime)`
