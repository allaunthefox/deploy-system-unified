# containers_runtime

**role**: `containers/runtime`

**Container Runtime Role**

This role handles the installation and configuration of the container runtime environment (Podman/Docker) and associated hardware support (GPU).

## Core Roles

## Variables

### `containers_install_podman`{#containersinstallpodman}
- `containers_install_podman`

### `containers_enable_socket`{#containersenablesocket}
- `containers_enable_socket`

### `podman_rootless_enabled`{#podmanrootlessenabled}
- `podman_rootless_enabled`

### `podman_rootless_user`{#podmanrootlessuser}
- `podman_rootless_user`

### `podman_rootless_user_home`{#podmanrootlessuserhome}
- `podman_rootless_user_home`

### `podman_rootless_network_mode`{#podmanrootlessnetworkmode}
- `podman_rootless_network_mode`

### `podman_rootless_allow_privileged_ports`{#podmanrootlessallowprivilegedports}
- `podman_rootless_allow_privileged_ports`

### `podman_rootless_privileged_port_start`{#podmanrootlessprivilegedportstart}
- `podman_rootless_privileged_port_start`

### `containers_systemd_dir`{#containerssystemddir}
- `containers_systemd_dir`

### `containers_systemd_scope`{#containerssystemdscope}
- `containers_systemd_scope`

### `containers_systemd_owner`{#containerssystemdowner}
- `containers_systemd_owner`

### `containers_systemd_group`{#containerssystemdgroup}
- `containers_systemd_group`

### `containers_secrets_dir`{#containerssecretsdir}
- `containers_secrets_dir`

### `containers_secrets_owner`{#containerssecretsowner}
- `containers_secrets_owner`

### `containers_secrets_group`{#containerssecretsgroup}
- `containers_secrets_group`

### `containers_systemd_env`{#containerssystemdenv}
- `containers_systemd_env`

### `intel_oneapi_gpg_key_url`{#inteloneapigpgkeyurl}
- `intel_oneapi_gpg_key_url`

### `intel_oneapi_gpg_keyring_path`{#inteloneapigpgkeyringpath}
- `intel_oneapi_gpg_keyring_path`

### `intel_oneapi_repo`{#inteloneapirepo}
- `intel_oneapi_repo`

### `intel_oneapi_gpg_fingerprint`{#inteloneapigpgfingerprint}
- `intel_oneapi_gpg_fingerprint`

### `intel_oneapi_gpg_fingerprint_verify`{#inteloneapigpgfingerprintverify}
- `intel_oneapi_gpg_fingerprint_verify`

### `containers_pull_retries`{#containerspullretries}
- `containers_pull_retries`

### `containers_pull_delay`{#containerspulldelay}
- `containers_pull_delay`

### `containers_cosign_enable`{#containerscosignenable}
- `containers_cosign_enable`

### `containers_cosign_version`{#containerscosignversion}
- `containers_cosign_version`

### `containers_cosign_checksum`{#containerscosignchecksum}
- `containers_cosign_checksum` — Optional SHA256 checksum for binary

### `containers_cosign_arch`{#containerscosignarch}
- `containers_cosign_arch`

### `containers_arch_override`{#containersarchoverride}
- `containers_arch_override`

### `containers_enable_gpu_support`{#containersenablegpusupport}
- `containers_enable_gpu_support`

### `containers_gpu_vendor`{#containersgpuvendor}
- `containers_gpu_vendor` — Options: nvidia, amd, intel

### `containers_gpu_count`{#containersgpucount}
- `containers_gpu_count`

### `containers_gpu_allocation_map`{#containersgpuallocationmap}
- `containers_gpu_allocation_map`

### `containers_gpu_slicing`{#containersgpuslicing}
- `containers_gpu_slicing`

### `containers_gpu_profiles`{#containersgpuprofiles}
- `containers_gpu_profiles`

### `containers_gpu_device_selectors`{#containersgpudeviceselectors}
- `containers_gpu_device_selectors`


