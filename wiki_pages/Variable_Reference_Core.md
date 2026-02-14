# Variable_Reference_Core

## Core Variables

### `core/bootstrap`
- [`core_install_base_packages`](roles/core_bootstrap.md#coreinstallbasepackages)
- [`system_base_packages`](roles/core_bootstrap.md#systembasepackages)
- [`system_standard_directories`](roles/core_bootstrap.md#systemstandarddirectories)

### `core/entropy`
- [`entropy_service_mapping`](roles/core_entropy.md#entropyservicemapping)

### `core/grub`
- [`core_grub_enabled`](roles/core_grub.md#coregrubenabled)
- [`core_grub_base_params`](roles/core_grub.md#coregrubbaseparams)
- [`core_grub_security_params`](roles/core_grub.md#coregrubsecurityparams)
- [`core_grub_hardware_params`](roles/core_grub.md#coregrubhardwareparams)
- [`core_grub_isolation_params`](roles/core_grub.md#coregrubisolationparams)
- [`core_grub_performance_params`](roles/core_grub.md#coregrubperformanceparams)
- [`core_grub_extra_params`](roles/core_grub.md#coregrubextraparams)
- [`core_grub_config_path`](roles/core_grub.md#coregrubconfigpath)
- [`core_grub_force_update`](roles/core_grub.md#coregrubforceupdate)

### `core/hardware_support`
- [`enable_hardware_discovery`](roles/core_hardware_support.md#enablehardwarediscovery)
- [`require_avx`](roles/core_hardware_support.md#requireavx)
- [`require_aes_ni`](roles/core_hardware_support.md#requireaesni)
- [`require_crypto_extensions`](roles/core_hardware_support.md#requirecryptoextensions)
- [`warn_on_missing_avx`](roles/core_hardware_support.md#warnonmissingavx)
- [`warn_on_missing_crypto`](roles/core_hardware_support.md#warnonmissingcrypto)

### `core/identity`
- [`identity_set_hostname`](roles/core_identity.md#identitysethostname)
- [`identity_domain`](roles/core_identity.md#identitydomain)

### `core/logging`
- [`logging_journal_remote_packages`](roles/core_logging.md#loggingjournalremotepackages)
- [`logging_rate_limit_interval`](roles/core_logging.md#loggingratelimitinterval)
- [`logging_rate_limit_burst`](roles/core_logging.md#loggingratelimitburst)
- [`logging_max_file_sec`](roles/core_logging.md#loggingmaxfilesec)
- [`logging_max_retention_sec`](roles/core_logging.md#loggingmaxretentionsec)

### `core/memory`
- [`core_memory_compression_strategy`](roles/core_memory.md#corememorycompressionstrategy)
- [`core_memory_shared_vram`](roles/core_memory.md#corememorysharedvram)
- [`core_memory_workload_profile`](roles/core_memory.md#corememoryworkloadprofile)
- [`core_memory_thp_state`](roles/core_memory.md#corememorythpstate)
- [`core_memory_zram_size_percent`](roles/core_memory.md#corememoryzramsizepercent)
- [`core_memory_zram_algorithm`](roles/core_memory.md#corememoryzramalgorithm)
- [`core_memory_zram_priority`](roles/core_memory.md#corememoryzrampriority)
- [`core_memory_zswap_compressor`](roles/core_memory.md#corememoryzswapcompressor)
- [`core_memory_zswap_zpool`](roles/core_memory.md#corememoryzswapzpool)
- [`core_memory_zswap_max_pool_percent`](roles/core_memory.md#corememoryzswapmaxpoolpercent)
- [`core_memory_swappiness`](roles/core_memory.md#corememoryswappiness)
- [`core_memory_cache_pressure`](roles/core_memory.md#corememorycachepressure)
- [`core_memory_dirty_bytes`](roles/core_memory.md#corememorydirtybytes)
- [`core_memory_dirty_background_bytes`](roles/core_memory.md#corememorydirtybackgroundbytes)

### `core/repositories`
- [`rpmfusion_free_url`](roles/core_repositories.md#rpmfusionfreeurl)
- [`rpmfusion_nonfree_url`](roles/core_repositories.md#rpmfusionnonfreeurl)
- [`rpmfusion_free_sha256`](roles/core_repositories.md#rpmfusionfreesha256)
- [`rpmfusion_nonfree_sha256`](roles/core_repositories.md#rpmfusionnonfreesha256)
- [`rpmfusion_verify_checksum`](roles/core_repositories.md#rpmfusionverifychecksum)

### `core/secrets`
- *No variables defined in defaults/main.yml*

### `core/systemd`
- [`systemd_configure_journald`](roles/core_systemd.md#systemdconfigurejournald)
- [`systemd_configure_resolved`](roles/core_systemd.md#systemdconfigureresolved)
- [`systemd_persistent_journal`](roles/core_systemd.md#systemdpersistentjournal)

### `core/time`
- [`time_service_mapping`](roles/core_time.md#timeservicemapping)

### `core/updates`
- *No variables defined in defaults/main.yml*

