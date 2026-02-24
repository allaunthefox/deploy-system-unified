# containers_runtime

**role**: `containers/runtime`

**Container Runtime Role**

This role handles the installation and configuration of the container runtime environment (Podman/Docker) and associated hardware support (GPU).

## Core Roles

## Variables

### `containers_install_podman` {#containers-install-podman}
- `containers_install_podman`

### `containers_enable_socket` {#containers-enable-socket}
- `containers_enable_socket`

### `podman_rootless_enabled` {#podman-rootless-enabled}
- `podman_rootless_enabled`

### `podman_rootless_user` {#podman-rootless-user}
- `podman_rootless_user`

### `podman_rootless_user_home` {#podman-rootless-user-home}
- `podman_rootless_user_home`

### `podman_rootless_network_mode` {#podman-rootless-network-mode}
- `podman_rootless_network_mode`

### `podman_rootless_allow_privileged_ports` {#podman-rootless-allow-privileged-ports}
- `podman_rootless_allow_privileged_ports`

### `podman_rootless_privileged_port_start` {#podman-rootless-privileged-port-start}
- `podman_rootless_privileged_port_start`

### `containers_systemd_dir` {#containers-systemd-dir}
- `containers_systemd_dir`

### `containers_systemd_scope` {#containers-systemd-scope}
- `containers_systemd_scope`

### `containers_systemd_owner` {#containers-systemd-owner}
- `containers_systemd_owner`

### `containers_systemd_group` {#containers-systemd-group}
- `containers_systemd_group`

### `containers_secrets_dir` {#containers-secrets-dir}
- `containers_secrets_dir`

### `containers_secrets_owner` {#containers-secrets-owner}
- `containers_secrets_owner`

### `containers_secrets_group` {#containers-secrets-group}
- `containers_secrets_group`

### `containers_systemd_env` {#containers-systemd-env}
- `containers_systemd_env`

### `intel_oneapi_gpg_key_url` {#intel-oneapi-gpg-key-url}
- `intel_oneapi_gpg_key_url`

### `intel_oneapi_gpg_keyring_path` {#intel-oneapi-gpg-keyring-path}
- `intel_oneapi_gpg_keyring_path`

### `intel_oneapi_repo` {#intel-oneapi-repo}
- `intel_oneapi_repo`

### `intel_oneapi_gpg_fingerprint` {#intel-oneapi-gpg-fingerprint}
- `intel_oneapi_gpg_fingerprint`

### `intel_oneapi_gpg_fingerprint_verify` {#intel-oneapi-gpg-fingerprint-verify}
- `intel_oneapi_gpg_fingerprint_verify`

### `containers_pull_retries` {#containers-pull-retries}
- `containers_pull_retries`

### `containers_pull_delay` {#containers-pull-delay}
- `containers_pull_delay`

### `containers_cosign_enable` {#containers-cosign-enable}
- `containers_cosign_enable`

### `containers_cosign_version` {#containers-cosign-version}
- `containers_cosign_version`

### `containers_cosign_checksum` {#containers-cosign-checksum}
- `containers_cosign_checksum` — Optional SHA256 checksum for binary

### `containers_cosign_arch` {#containers-cosign-arch}
- `containers_cosign_arch`

### `containers_arch_override` {#containers-arch-override}
- `containers_arch_override`

### `containers_enable_gpu_support` {#containers-enable-gpu-support}
- `containers_enable_gpu_support`

### `containers_gpu_vendor` {#containers-gpu-vendor}
- `containers_gpu_vendor` — Options: nvidia, amd, intel

### `containers_gpu_count` {#containers-gpu-count}
- `containers_gpu_count`

### `containers_gpu_allocation_map` {#containers-gpu-allocation-map}
- `containers_gpu_allocation_map`

### `containers_gpu_slicing` {#containers-gpu-slicing}
- `containers_gpu_slicing`

### `containers_gpu_profiles` {#containers-gpu-profiles}
- `containers_gpu_profiles`

### `containers_gpu_device_selectors` {#containers-gpu-device-selectors}
- `containers_gpu_device_selectors`


