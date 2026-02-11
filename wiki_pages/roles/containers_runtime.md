# containers/runtime

**Role Path**: `roles/containers/runtime`

## Description
Tasks for containers/runtime role

## Key Tasks
- Apply rootless Podman prerequisites
- Install Podman and Core Dependencies
- Warn on weak/default credentials (container policy)
- Setup GPU Container Support
- Discover GPU devices and capabilities
- Validate GPU slicing configuration
- Configure GPU slicing
- Report GPU configuration status
- Set containers runtime completion flag

## Default Variables
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
- `containers_gpu_slicing.kubernetes`
- `containers_gpu_slicing.podman`
- `containers_gpu_slicing.lxc`
- `containers_gpu_profiles`
- `containers_gpu_device_selectors`

---
*This page was automatically generated from role source code.*