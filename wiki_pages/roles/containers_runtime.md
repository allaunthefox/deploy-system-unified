# containers_runtime

**role**: `containers/runtime`

**Container Runtime Role**

This role handles the installation and configuration of the container runtime environment (Podman/Docker) and associated hardware support (GPU).

## Core Roles

## Variables

- <a id="containers_install_podman"></a>`containers_install_podman`
- <a id="containers_enable_socket"></a>`containers_enable_socket`
- <a id="podman_rootless_enabled"></a>`podman_rootless_enabled`
- <a id="podman_rootless_user"></a>`podman_rootless_user`
- <a id="podman_rootless_user_home"></a>`podman_rootless_user_home`
- <a id="podman_rootless_network_mode"></a>`podman_rootless_network_mode`
- <a id="podman_rootless_allow_privileged_ports"></a>`podman_rootless_allow_privileged_ports`
- <a id="podman_rootless_privileged_port_start"></a>`podman_rootless_privileged_port_start`
- <a id="containers_systemd_dir"></a>`containers_systemd_dir`
- <a id="containers_systemd_scope"></a>`containers_systemd_scope`
- <a id="containers_systemd_owner"></a>`containers_systemd_owner`
- <a id="containers_systemd_group"></a>`containers_systemd_group`
- <a id="containers_secrets_dir"></a>`containers_secrets_dir`
- <a id="containers_secrets_owner"></a>`containers_secrets_owner`
- <a id="containers_secrets_group"></a>`containers_secrets_group`
- <a id="containers_systemd_env"></a>`containers_systemd_env`
- <a id="intel_oneapi_gpg_key_url"></a>`intel_oneapi_gpg_key_url`
- <a id="intel_oneapi_gpg_keyring_path"></a>`intel_oneapi_gpg_keyring_path`
- <a id="intel_oneapi_repo"></a>`intel_oneapi_repo`
- <a id="intel_oneapi_gpg_fingerprint"></a>`intel_oneapi_gpg_fingerprint`
- <a id="intel_oneapi_gpg_fingerprint_verify"></a>`intel_oneapi_gpg_fingerprint_verify`
- <a id="containers_pull_retries"></a>`containers_pull_retries`
- <a id="containers_pull_delay"></a>`containers_pull_delay`
- <a id="containers_arch_override"></a>`containers_arch_override`
- <a id="containers_enable_gpu_support"></a>`containers_enable_gpu_support`
- <a id="containers_gpu_vendor"></a>`containers_gpu_vendor` — Options: nvidia, amd, intel
- <a id="containers_gpu_count"></a>`containers_gpu_count`
- <a id="containers_gpu_slicing"></a>`containers_gpu_slicing`
- <a id="containers_gpu_profiles"></a>`containers_gpu_profiles`
- <a id="containers_gpu_device_selectors"></a>`containers_gpu_device_selectors`

