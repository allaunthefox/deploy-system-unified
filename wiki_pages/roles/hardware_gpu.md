# hardware_gpu

**role**: `hardware/gpu`

**Unified GPU Stack**
Automatic discovery and driver installation for AMD, Intel, and NVIDIA GPUs across architectures.

## Variables

### `gpu_stack_enable`
- `gpu_stack_enable`

### `gpu_stack_vendor`
- `gpu_stack_vendor`

### `gpu_stack_mode`
- `gpu_stack_mode`

### `gpu_stack_reservation`
- `gpu_stack_reservation`

### `gpu_stack_arch`
- `gpu_stack_arch`

### `gpu_stack_enable_egpu`
- `gpu_stack_enable_egpu` — Enable support for External GPUs (Thunderbolt/USB4/OCuLink)

### `gpu_stack_egpu_interface`
- `gpu_stack_egpu_interface` — Connection type: thunderbolt (default), oculink

### `gpu_stack_enable_rdma`
- `gpu_stack_enable_rdma` — Enable Remote Direct Memory Access support

### `gpu_stack_enable_dp_alt_mode`
- `gpu_stack_enable_dp_alt_mode` — Enable DisplayPort Alt Mode handling

### `gpu_stack_enable_oneapi`
- `gpu_stack_enable_oneapi` — Enable Intel OneAPI Base Toolkit (or runtime)

### `gpu_stack_enable_cuda`
- `gpu_stack_enable_cuda` — Enable NVIDIA CUDA Toolkit (compiler/dev tools)

### `gpu_stack_enable_rocm`
- `gpu_stack_enable_rocm` — Enable AMD ROCm SDK

### `intel_oneapi_gpg_key_url`
- `intel_oneapi_gpg_key_url`

### `intel_oneapi_gpg_keyring_path`
- `intel_oneapi_gpg_keyring_path`

### `intel_oneapi_repo`
- `intel_oneapi_repo`

### `intel_oneapi_gpg_fingerprint`
- `intel_oneapi_gpg_fingerprint`

### `intel_oneapi_gpg_fingerprint_verify`
- `intel_oneapi_gpg_fingerprint_verify`

### `amd_rocm_gpg_key_url`
- `amd_rocm_gpg_key_url`

### `amd_rocm_gpg_keyring_path`
- `amd_rocm_gpg_keyring_path`

### `amd_rocm_gpg_key_sha256`
- `amd_rocm_gpg_key_sha256`

### `amd_rocm_gpg_fingerprint`
- `amd_rocm_gpg_fingerprint`

### `amd_rocm_gpg_key_verify`
- `amd_rocm_gpg_key_verify`

### `nvidia_gpg_key_url`
- `nvidia_gpg_key_url`

### `nvidia_gpg_key_sha256`
- `nvidia_gpg_key_sha256`

### `nvidia_gpg_fingerprint`
- `nvidia_gpg_fingerprint`

### `nvidia_gpg_key_verify`
- `nvidia_gpg_key_verify`

### `gpu_desktop_enable_audio`
- `gpu_desktop_enable_audio` — Enable GPU Audio (HDMI/DP) - Ensures drivers are loaded

### `gpu_desktop_power_profile`
- `gpu_desktop_power_profile` — Options: performance, balanced, power-saver

### `gpu_desktop_enable_wayland_support`
- `gpu_desktop_enable_wayland_support` — Enable DRM KMS for Wayland (essential for GNOME/KDE)

### `gpu_desktop_enable_x11_support`
- `gpu_desktop_enable_x11_support` — Ensure X11 drivers/utilities are present

### `gpu_desktop_grant_user_access`
- `gpu_desktop_grant_user_access` — Grant 'video'/'render' group access to standard users


