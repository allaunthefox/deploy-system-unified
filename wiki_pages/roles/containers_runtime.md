# containers_runtime

**role**: `containers/runtime`

**Container Runtime Role**

This role handles the installation and configuration of the container runtime environment (Podman/Docker) and associated hardware support (GPU).

## Core Roles

## Variables

### containers_install_podman
- `containers_install_podman`

### containers_enable_socket
- `containers_enable_socket`

### podman_rootless_enabled
- `podman_rootless_enabled`

### podman_rootless_user
- `podman_rootless_user`

### podman_rootless_user_home
- `podman_rootless_user_home`

### podman_rootless_network_mode
- `podman_rootless_network_mode`

### podman_rootless_allow_privileged_ports
- `podman_rootless_allow_privileged_ports`

### podman_rootless_privileged_port_start
- `podman_rootless_privileged_port_start`

### containers_systemd_dir
- `containers_systemd_dir`

### containers_systemd_scope
- `containers_systemd_scope`

### containers_systemd_owner
- `containers_systemd_owner`

### containers_systemd_group
- `containers_systemd_group`

### containers_secrets_dir
- `containers_secrets_dir`

### containers_secrets_owner
- `containers_secrets_owner`

### containers_secrets_group
- `containers_secrets_group`

### containers_systemd_env
- `containers_systemd_env`

### intel_oneapi_gpg_key_url
- `intel_oneapi_gpg_key_url`

### intel_oneapi_gpg_keyring_path
- `intel_oneapi_gpg_keyring_path`

### intel_oneapi_repo
- `intel_oneapi_repo`

### intel_oneapi_gpg_fingerprint
- `intel_oneapi_gpg_fingerprint`

### intel_oneapi_gpg_fingerprint_verify
- `intel_oneapi_gpg_fingerprint_verify`

### containers_pull_retries
- `containers_pull_retries`

### containers_pull_delay
- `containers_pull_delay`

### containers_arch_override
- `containers_arch_override`

### containers_enable_gpu_support
- `containers_enable_gpu_support`

### containers_gpu_vendor
- `containers_gpu_vendor` — Options: nvidia, amd, intel

### containers_gpu_count
- `containers_gpu_count`

### containers_gpu_slicing
- `containers_gpu_slicing`

### containers_gpu_profiles
- `containers_gpu_profiles`

### containers_gpu_device_selectors
- `containers_gpu_device_selectors`


