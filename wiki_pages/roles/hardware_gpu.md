# hardware_gpu

**Role Path**: `roles/hardware/gpu`

## Description
**Unified GPU Stack**
Automatic discovery and driver installation for AMD, Intel, and NVIDIA GPUs across architectures.

## Key Tasks
- Check if GPU Stack is enabled
- End play if GPU Stack is disabled
- Check for EFI Environment
- Set EFI Fact
- Normalize Architecture
- Normalize Vendor List (Single or Multi-Vendor)
- Detect Virtualization Environment
- Validate Global Config
- Auto-Detect Video Hardware (If Vendor is Auto/Generic)
- Normalize Vendor List (Re-eval after detection)
- Iterate over defined vendors
- Optional - Configure Hybrid Graphics (Prime/Optimus)
- Optional - Configure Desktop Environment Features
- Optional - Configure eGPU Support
- Optional - Configure RDMA Support
- Optional - Configure DP Alt Mode

## Default Variables
- `gpu_stack_enable`
- `gpu_stack_vendor`
- `gpu_stack_mode`
- `gpu_stack_reservation`
- `gpu_stack_arch`
- `gpu_stack_enable_egpu`
- `gpu_stack_egpu_interface`
- `gpu_stack_enable_rdma`
- `gpu_stack_enable_dp_alt_mode`
- `gpu_stack_enable_oneapi`
- `gpu_stack_enable_cuda`
- `gpu_stack_enable_rocm`
- `intel_oneapi_gpg_key_url`
- `intel_oneapi_gpg_keyring_path`
- `intel_oneapi_repo`
- `intel_oneapi_gpg_fingerprint`
- `intel_oneapi_gpg_fingerprint_verify`
- `amd_rocm_gpg_key_url`
- `amd_rocm_gpg_keyring_path`
- `amd_rocm_gpg_key_sha256`
- `amd_rocm_gpg_fingerprint`
- `amd_rocm_gpg_key_verify`
- `nvidia_gpg_key_url`
- `nvidia_gpg_key_sha256`
- `nvidia_gpg_fingerprint`
- `nvidia_gpg_key_verify`
- `gpu_desktop_enable_audio`
- `gpu_desktop_power_profile`
- `gpu_desktop_enable_wayland_support`
- `gpu_desktop_enable_x11_support`
- `gpu_desktop_grant_user_access`

---
*This page was automatically generated from role source code.*