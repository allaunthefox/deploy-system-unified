# hardware_gpu

**role**: `hardware/gpu`

**Unified GPU Stack**
Automatic discovery and driver installation for AMD, Intel, and NVIDIA GPUs across architectures.

## Variables

- <a id="gpu_stack_enable"></a>`gpu_stack_enable`
- <a id="gpu_stack_vendor"></a>`gpu_stack_vendor`
- <a id="gpu_stack_mode"></a>`gpu_stack_mode`
- <a id="gpu_stack_reservation"></a>`gpu_stack_reservation`
- <a id="gpu_stack_arch"></a>`gpu_stack_arch`
- <a id="gpu_stack_enable_egpu"></a>`gpu_stack_enable_egpu` — Enable support for External GPUs (Thunderbolt/USB4/OCuLink)
- <a id="gpu_stack_egpu_interface"></a>`gpu_stack_egpu_interface` — Connection type: thunderbolt (default), oculink
- <a id="gpu_stack_enable_rdma"></a>`gpu_stack_enable_rdma` — Enable Remote Direct Memory Access support
- <a id="gpu_stack_enable_dp_alt_mode"></a>`gpu_stack_enable_dp_alt_mode` — Enable DisplayPort Alt Mode handling
- <a id="gpu_stack_enable_oneapi"></a>`gpu_stack_enable_oneapi` — Enable Intel OneAPI Base Toolkit (or runtime)
- <a id="gpu_stack_enable_cuda"></a>`gpu_stack_enable_cuda` — Enable NVIDIA CUDA Toolkit (compiler/dev tools)
- <a id="gpu_stack_enable_rocm"></a>`gpu_stack_enable_rocm` — Enable AMD ROCm SDK
- <a id="intel_oneapi_gpg_key_url"></a>`intel_oneapi_gpg_key_url`
- <a id="intel_oneapi_gpg_keyring_path"></a>`intel_oneapi_gpg_keyring_path`
- <a id="intel_oneapi_repo"></a>`intel_oneapi_repo`
- <a id="intel_oneapi_gpg_fingerprint"></a>`intel_oneapi_gpg_fingerprint`
- <a id="intel_oneapi_gpg_fingerprint_verify"></a>`intel_oneapi_gpg_fingerprint_verify`
- <a id="amd_rocm_gpg_key_url"></a>`amd_rocm_gpg_key_url`
- <a id="amd_rocm_gpg_keyring_path"></a>`amd_rocm_gpg_keyring_path`
- <a id="amd_rocm_gpg_key_sha256"></a>`amd_rocm_gpg_key_sha256`
- <a id="amd_rocm_gpg_fingerprint"></a>`amd_rocm_gpg_fingerprint`
- <a id="amd_rocm_gpg_key_verify"></a>`amd_rocm_gpg_key_verify`
- <a id="nvidia_gpg_key_url"></a>`nvidia_gpg_key_url`
- <a id="nvidia_gpg_key_sha256"></a>`nvidia_gpg_key_sha256`
- <a id="nvidia_gpg_fingerprint"></a>`nvidia_gpg_fingerprint`
- <a id="nvidia_gpg_key_verify"></a>`nvidia_gpg_key_verify`
- <a id="gpu_desktop_enable_audio"></a>`gpu_desktop_enable_audio` — Enable GPU Audio (HDMI/DP) - Ensures drivers are loaded
- <a id="gpu_desktop_power_profile"></a>`gpu_desktop_power_profile` — Options: performance, balanced, power-saver
- <a id="gpu_desktop_enable_wayland_support"></a>`gpu_desktop_enable_wayland_support` — Enable DRM KMS for Wayland (essential for GNOME/KDE)
- <a id="gpu_desktop_enable_x11_support"></a>`gpu_desktop_enable_x11_support` — Ensure X11 drivers/utilities are present
- <a id="gpu_desktop_grant_user_access"></a>`gpu_desktop_grant_user_access` — Grant 'video'/'render' group access to standard users

