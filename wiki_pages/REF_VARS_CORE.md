# VARIABLE_REFERENCE_Core

## Core Variables

### `core/bootstrap`
- [`core_install_base_packages`](core_bootstrap#coreinstallbasepackages)
- [`system_base_packages`](core_bootstrap#systembasepackages)
- [`system_standard_directories`](core_bootstrap#systemstandarddirectories)

### `core/entropy`
- [`entropy_service_mapping`](core_entropy#entropyservicemapping)

### `core/grub`
- [`core_grub_enabled`](core_grub#coregrubenabled)
- [`core_grub_base_params`](core_grub#coregrubbaseparams)
- [`core_grub_security_params`](core_grub#coregrubsecurityparams)
- [`core_grub_hardware_params`](core_grub#coregrubhardwareparams)
- [`core_grub_isolation_params`](core_grub#coregrubisolationparams)
- [`core_grub_performance_params`](core_grub#coregrubperformanceparams)
- [`core_grub_extra_params`](core_grub#coregrubextraparams)
- [`core_grub_config_path`](core_grub#coregrubconfigpath)
- [`core_grub_force_update`](core_grub#coregrubforceupdate)

### `core/hardware_support`
- [`enable_hardware_discovery`](core_hardware_support#enablehardwarediscovery)
- [`require_avx`](core_hardware_support#requireavx)
- [`require_aes_ni`](core_hardware_support#requireaesni)
- [`require_crypto_extensions`](core_hardware_support#requirecryptoextensions)
- [`warn_on_missing_avx`](core_hardware_support#warnonmissingavx)
- [`warn_on_missing_crypto`](core_hardware_support#warnonmissingcrypto)

### `core/identity`
- [`identity_set_hostname`](core_identity#identitysethostname)
- [`identity_domain`](core_identity#identitydomain)

### `core/logging`
- [`logging_journal_remote_packages`](core_logging#loggingjournalremotepackages)
- [`logging_rate_limit_interval`](core_logging#loggingratelimitinterval)
- [`logging_rate_limit_burst`](core_logging#loggingratelimitburst)
- [`logging_max_file_sec`](core_logging#loggingmaxfilesec)
- [`logging_max_retention_sec`](core_logging#loggingmaxretentionsec)

### `core/memory`
- [`core_memory_compression_strategy`](core_memory#corememorycompressionstrategy)
- [`core_memory_shared_vram`](core_memory#corememorysharedvram)
- [`core_memory_workload_profile`](core_memory#corememoryworkloadprofile)
- [`core_memory_thp_state`](core_memory#corememorythpstate)
- [`core_memory_zram_size_percent`](core_memory#corememoryzramsizepercent)
- [`core_memory_zram_algorithm`](core_memory#corememoryzramalgorithm)
- [`core_memory_zram_priority`](core_memory#corememoryzrampriority)
- [`core_memory_zswap_compressor`](core_memory#corememoryzswapcompressor)
- [`core_memory_zswap_zpool`](core_memory#corememoryzswapzpool)
- [`core_memory_zswap_max_pool_percent`](core_memory#corememoryzswapmaxpoolpercent)
- [`core_memory_swappiness`](core_memory#corememoryswappiness)
- [`core_memory_cache_pressure`](core_memory#corememorycachepressure)
- [`core_memory_dirty_bytes`](core_memory#corememorydirtybytes)
- [`core_memory_dirty_background_bytes`](core_memory#corememorydirtybackgroundbytes)

### `core/repositories`
- [`rpmfusion_free_url`](core_repositories#rpmfusionfreeurl)
- [`rpmfusion_nonfree_url`](core_repositories#rpmfusionnonfreeurl)
- [`rpmfusion_free_sha256`](core_repositories#rpmfusionfreesha256)
- [`rpmfusion_nonfree_sha256`](core_repositories#rpmfusionnonfreesha256)
- [`rpmfusion_verify_checksum`](core_repositories#rpmfusionverifychecksum)

### `core/secrets`
- *No variables defined in defaults/main.yml*

### `core/systemd`
- [`systemd_configure_journald`](core_systemd#systemdconfigurejournald)
- [`systemd_configure_resolved`](core_systemd#systemdconfigureresolved)
- [`systemd_persistent_journal`](core_systemd#systemdpersistentjournal)

### `core/time`
- [`core_time_service_mapping`](core_time#coretimeservicemapping)

### `core/updates`
- *No variables defined in defaults/main.yml*

