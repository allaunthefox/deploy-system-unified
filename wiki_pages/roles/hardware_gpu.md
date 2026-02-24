# hardware_gpu

**role**: `hardware/gpu`

**Unified GPU Stack (Integrated Battlemage)**
Automatic discovery and driver installation for AMD, Intel (including Arc/Battlemage), and NVIDIA GPUs across architectures (x86_64, aarch64, riscv64).

## Variables

### `gpu_stack_enable`{#gpustackenable}
- `gpu_stack_enable`

### `gpu_stack_vendor`{#gpustackvendor}
- `gpu_stack_vendor`

### `gpu_stack_mode`{#gpustackmode}
- `gpu_stack_mode`

### `gpu_stack_reservation`{#gpustackreservation}
- `gpu_stack_reservation`

### `gpu_stack_arch`{#gpustackarch}
- `gpu_stack_arch`

### `gpu_stack_enable_egpu`{#gpustackenableegpu}
- `gpu_stack_enable_egpu` — Enable support for External GPUs (Thunderbolt/USB4/OCuLink)

### `gpu_stack_egpu_interface`{#gpustackegpuinterface}
- `gpu_stack_egpu_interface` — Connection type: thunderbolt (default), oculink

### `gpu_stack_enable_rdma`{#gpustackenablerdma}
- `gpu_stack_enable_rdma` — Enable Remote Direct Memory Access support

### `gpu_stack_enable_dp_alt_mode`{#gpustackenabledpaltmode}
- `gpu_stack_enable_dp_alt_mode` — Enable DisplayPort Alt Mode handling

### `gpu_stack_enable_oneapi`{#gpustackenableoneapi}
- `gpu_stack_enable_oneapi` — Enable Intel OneAPI Base Toolkit (or runtime)

### `gpu_stack_enable_level_zero`{#gpustackenablelevelzero}
- `gpu_stack_enable_level_zero` — Enable Intel Level Zero (compute) support

### `gpu_stack_enable_cuda`{#gpustackenablecuda}
- `gpu_stack_enable_cuda` — Enable NVIDIA CUDA Toolkit (compiler/dev tools)

### `gpu_stack_enable_rocm`{#gpustackenablerocm}
- `gpu_stack_enable_rocm` — Enable AMD ROCm SDK

### `gpu_battlemage_force_probe`{#gpubattlemageforceprobe}
- `gpu_battlemage_force_probe` — Force probe for Intel Xe2 (Battlemage) GPUs

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

### `amd_rocm_gpg_key_url`{#amdrocmgpgkeyurl}
- `amd_rocm_gpg_key_url`

### `amd_rocm_gpg_keyring_path`{#amdrocmgpgkeyringpath}
- `amd_rocm_gpg_keyring_path`

### `amd_rocm_gpg_key_sha256`{#amdrocmgpgkeysha256}
- `amd_rocm_gpg_key_sha256`

### `amd_rocm_gpg_fingerprint`{#amdrocmgpgfingerprint}
- `amd_rocm_gpg_fingerprint`

### `amd_rocm_gpg_key_verify`{#amdrocmgpgkeyverify}
- `amd_rocm_gpg_key_verify`

### `nvidia_gpg_key_url`{#nvidiagpgkeyurl}
- `nvidia_gpg_key_url`

### `nvidia_gpg_key_sha256`{#nvidiagpgkeysha256}
- `nvidia_gpg_key_sha256`

### `nvidia_gpg_fingerprint`{#nvidiagpgfingerprint}
- `nvidia_gpg_fingerprint`

### `nvidia_gpg_key_verify`{#nvidiagpgkeyverify}
- `nvidia_gpg_key_verify`

### `gpu_desktop_enable_audio`{#gpudesktopenableaudio}
- `gpu_desktop_enable_audio` — Enable GPU Audio (HDMI/DP) - Ensures drivers are loaded

### `gpu_desktop_power_profile`{#gpudesktoppowerprofile}
- `gpu_desktop_power_profile` — Options: performance, balanced, power-saver

### `gpu_desktop_enable_wayland_support`{#gpudesktopenablewaylandsupport}
- `gpu_desktop_enable_wayland_support` — Enable DRM KMS for Wayland (essential for GNOME/KDE)

### `gpu_desktop_enable_x11_support`{#gpudesktopenablex11support}
- `gpu_desktop_enable_x11_support` — Ensure X11 drivers/utilities are present

### `gpu_desktop_grant_user_access`{#gpudesktopgrantuseraccess}
- `gpu_desktop_grant_user_access` — Grant 'video'/'render' group access to standard users

### `dsu_encrypt_evidence`{#dsuencryptevidence}
- `dsu_encrypt_evidence`

### `dsu_encrypt_checkpoints`{#dsuencryptcheckpoints}
- `dsu_encrypt_checkpoints`


