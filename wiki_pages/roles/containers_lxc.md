# containers_lxc

**Role Path**: `roles/containers/lxc`

## Description
**LXC GPU Passthrough**
Handles GPU slicing and passthrough configuration specifically for LXC containers.

## Key Tasks
- Determine LXC GPU slicing strategy based on virtualization type (auto strategy)
- Configure LXC container for GPU passthrough
- Load Vendor Specific Strategy Config
- Debug LXC GPU configuration

## Default Variables
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

---
*This page was automatically generated from role source code.*