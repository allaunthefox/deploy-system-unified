> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⚠️ **UNTESTABLE**: Intel Battlemage support is currently unverified and untestable.

> ⏸️ **POSTPONED**: Intel Battlemage support is unverified due to hardware delay.

# INTEL_GPU_GUIDE

This document outlines the configuration and deployment for Intel GPUs, ranging from integrated UHD/Iris graphics to high-performance discrete Arc and Battlemage cards.

## 🏛️ Supported Architectures
- **x86_64**: Primary support target for all Intel GPUs.

---

## 🔍 Automated Discovery
The system utilizes a specialized Python-based discovery engine (`gpu_discovery.py`) to automatically detect and identify Intel hardware.

*   **Logic**: Probes PCI classes `0300` (VGA), `0302` (3D), and `0380` (Display).
*   **Facts**: Exposes `primary_detected_vendor: intel` and lists specific PCI IDs.
*   **Audit**: Discovery results are saved to `/var/lib/deploy-system/evidence/gpu/`.

---

## 🛠️ Driver Profiles & Stacks

### 1. Modern Xe Driver (Recommended)
Default for **Battlemage (Xe2-HPG)** and **Alchemist (Arc)** GPUs. Requires Linux Kernel 6.10+ for optimal support.

### 2. Legacy i915 Driver
Used for UHD, Iris, and older generations.

### 3. Basic Video / Media (VAAPI)
Enables hardware acceleration for video decoding/encoding and display.
**Packages Installed:**
- `intel-media-va-driver-non-free`: Full HW acceleration (including proprietary codecs).
- `mesa-vulkan-drivers`: Vulkan support (Intel Anvil).
- `libgl1-mesa-dri`: OpenGL DRI drivers.

### 4. Compute (OneAPI / Level Zero)
Enables OpenCL and Level Zero support for AI/ML compute workloads.
Enable via: `gpu_stack_enable_oneapi: true`

---

## 🚀 Battlemage & Arc Specifics

### Force-Probe Automation
For early-access hardware (Battlemage) or older kernels (6.8), enable force-probe logic:
```yaml
gpu_battlemage_force_probe: true
```
This injects `xe.force_probe=*` into the GRUB configuration via the `core/grub` role.

### Pre-Deployment Checklist
1.  **Resizable BAR (ReBAR)**: Must be **ENABLED** in the BIOS.
2.  **Kernel Version**: 6.10+ recommended; 6.8 minimum (with force_probe).
3.  **Secure Boot**: Ensure drivers are signed if using backports.

---

## 🏗️ Container Integration

### Multi-GPU Pinning
If a system has multiple Intel GPUs (e.g., UHD iGPU + Arc dGPU), use the allocation map to pin workloads.

**Example Allocation:**
```yaml
containers_gpu_allocation_map:
  - container_name: "jellyfin"
    pci_id: "0000:00:02.0"  # Pin to iGPU
  - container_name: "anubis-ai"
    pci_id: "0000:03:00.0"  # Pin to Battlemage dGPU
```

### Vulkan Projection
The system verifies that Intel's Vulkan capabilities are correctly projected into the container namespace.
*   **Smoke Test**: Executes `vulkaninfo` inside a test container.
*   **Hardened Enforcement**: Deployment fails in `hardened` profiles if Vulkan access is not verified.

---

## ✅ Verification & Troubleshooting

### Host Verification
Check `/var/lib/deploy-system/evidence/gpu/` for the latest discovery JSON.

### Video Acceleration Test
```bash
podman run --rm -it --device /dev/dri:/dev/dri ubuntu:24.04 bash
apt update && apt install -y vainfo && vainfo
```

### Common Issues
*   **Symptom**: `clinfo` shows no devices.
    *   **Fix**: Set `gpu_stack_enable_oneapi: true`.
*   **Symptom**: `vulkaninfo` fails.
    *   **Fix**: Verify `/dev/dri/by-path/` exists on the host.

---

## 📋 Distribution Specifics

| Distro | Pkg Manager | Boot Tool |
| :--- | :--- | :--- |
| **Ubuntu/Debian** | `apt` | `update-initramfs` |
| **Fedora** | `dnf` | `dracut` |
| **Archlinux** | `pacman` | `mkinitcpio` |
| **Alpine** | `apk` | `mkinitfs` |
