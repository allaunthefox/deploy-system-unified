# hardware_gpu

**role**: `hardware/gpu`

**Unified GPU Stack (Integrated Battlemage)**
Automatic discovery and driver installation for AMD, Intel (including Arc/Battlemage), and NVIDIA GPUs across architectures (x86_64, aarch64, riscv64).

## Variables

### `gpu_stack_enable` {#gpu-stack-enable}
- `gpu_stack_enable`

### `gpu_stack_vendor` {#gpu-stack-vendor}
- `gpu_stack_vendor`

### `gpu_stack_mode` {#gpu-stack-mode}
- `gpu_stack_mode`

### `gpu_stack_reservation` {#gpu-stack-reservation}
- `gpu_stack_reservation`

### `gpu_stack_arch` {#gpu-stack-arch}
- `gpu_stack_arch`

### `gpu_stack_enable_egpu` {#gpu-stack-enable-egpu}
- `gpu_stack_enable_egpu` — Enable support for External GPUs (Thunderbolt/USB4/OCuLink)

### `gpu_stack_egpu_interface` {#gpu-stack-egpu-interface}
- `gpu_stack_egpu_interface` — Connection type: thunderbolt (default), oculink

### `gpu_stack_enable_rdma` {#gpu-stack-enable-rdma}
- `gpu_stack_enable_rdma` — Enable Remote Direct Memory Access support

### `gpu_stack_enable_dp_alt_mode` {#gpu-stack-enable-dp-alt-mode}
- `gpu_stack_enable_dp_alt_mode` — Enable DisplayPort Alt Mode handling

### `gpu_stack_enable_oneapi` {#gpu-stack-enable-oneapi}
- `gpu_stack_enable_oneapi` — Enable Intel OneAPI Base Toolkit (or runtime)

### `gpu_stack_enable_level_zero` {#gpu-stack-enable-level-zero}
- `gpu_stack_enable_level_zero` — Enable Intel Level Zero (compute) support

### `gpu_stack_enable_cuda` {#gpu-stack-enable-cuda}
- `gpu_stack_enable_cuda` — Enable NVIDIA CUDA Toolkit (compiler/dev tools)

### `gpu_stack_enable_rocm` {#gpu-stack-enable-rocm}
- `gpu_stack_enable_rocm` — Enable AMD ROCm SDK

### `gpu_battlemage_force_probe` {#gpu-battlemage-force-probe}
- `gpu_battlemage_force_probe` — Force probe for Intel Xe2 (Battlemage) GPUs

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

### `amd_rocm_gpg_key_url` {#amd-rocm-gpg-key-url}
- `amd_rocm_gpg_key_url`

### `amd_rocm_gpg_keyring_path` {#amd-rocm-gpg-keyring-path}
- `amd_rocm_gpg_keyring_path`

### `amd_rocm_gpg_key_sha256` {#amd-rocm-gpg-key-sha256}
- `amd_rocm_gpg_key_sha256`

### `amd_rocm_gpg_fingerprint` {#amd-rocm-gpg-fingerprint}
- `amd_rocm_gpg_fingerprint`

### `amd_rocm_gpg_key_verify` {#amd-rocm-gpg-key-verify}
- `amd_rocm_gpg_key_verify`

### `nvidia_gpg_key_url` {#nvidia-gpg-key-url}
- `nvidia_gpg_key_url`

### `nvidia_gpg_key_sha256` {#nvidia-gpg-key-sha256}
- `nvidia_gpg_key_sha256`

### `nvidia_gpg_fingerprint` {#nvidia-gpg-fingerprint}
- `nvidia_gpg_fingerprint`

### `nvidia_gpg_key_verify` {#nvidia-gpg-key-verify}
- `nvidia_gpg_key_verify`

### `gpu_desktop_enable_audio` {#gpu-desktop-enable-audio}
- `gpu_desktop_enable_audio` — Enable GPU Audio (HDMI/DP) - Ensures drivers are loaded

### `gpu_desktop_power_profile` {#gpu-desktop-power-profile}
- `gpu_desktop_power_profile` — Options: performance, balanced, power-saver

### `gpu_desktop_enable_wayland_support` {#gpu-desktop-enable-wayland-support}
- `gpu_desktop_enable_wayland_support` — Enable DRM KMS for Wayland (essential for GNOME/KDE)

### `gpu_desktop_enable_x11_support` {#gpu-desktop-enable-x11-support}
- `gpu_desktop_enable_x11_support` — Ensure X11 drivers/utilities are present

### `gpu_desktop_grant_user_access` {#gpu-desktop-grant-user-access}
- `gpu_desktop_grant_user_access` — Grant 'video'/'render' group access to standard users

### `dsu_encrypt_evidence` {#dsu-encrypt-evidence}
- `dsu_encrypt_evidence`

### `dsu_encrypt_checkpoints` {#dsu-encrypt-checkpoints}
- `dsu_encrypt_checkpoints`


