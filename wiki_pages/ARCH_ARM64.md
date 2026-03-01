> 🧪 **EXPERIMENTAL**: Deployment on aarch64 is currently in early-stage testing.

> 🧪 **EXPERIMENTAL**: Deployment on aarch64 is currently in early-stage testing.

# ARCH_GUIDE_ARM64

## Overview

The `aarch64` architecture covers broadly different use cases ranging from Edge AI (Jetson) to High Performance Cloud (Grace Hopper, Ampere).

## Platform Profiles

### 1. NVIDIA Jetson (Edge AI)

Embedded SoCs like Orin, Xavier.

- **Boot**: L4T (Linux for Tegra). Custom kernel is mandatory.
- **GPU**: Integrated iGPU, addressed via CUDA.
- **Constraint**: Cannot use standard upstream kernel drivers. `hardware/gpu` role skips driver installation on Jetson to avoid breaking the BSP.

### 2. Server ARM (Cloud Native)

Ampere Altra, AWS Graviton, NVIDIA Grace.

- **Boot**: SBSA (Server Base System Architecture) / UEFI.
- **GPU**: PCIe Discrete Cards (A100/H100/L40S) or NVLink (Grace Hopper).
- **Driver**: Standard NVIDIA Data Center drivers (Open Kernel modules).

### 3. Generic ARM / SBC (Mali)

Rockchip (RK3588), Amlogic, Allwinner.

- **Driver**: Mesa (Panfrost/Panthor) for open source, or vendor blobs.
- **Support**: `hardware/gpu` installs Mesa stack. `containers/runtime` maps `/dev/dri/renderD128`.

## Configuration

Set `gpu_stack_arch: aarch64` (or rely on auto-detection).

```yaml
# Example for Grace Hopper Superchip
gpu_stack_vendor: nvidia
gpu_stack_mode: server
containers_gpu_slicing:
  strategy: mig
```

```yaml
# Example for Jetson Orin AGX
gpu_stack_vendor: nvidia
gpu_stack_mode: edge
containers_gpu_slicing:
  strategy: time-slicing # Hardware isolation (MIG) not supported on SoCs
```

```yaml
# Example for Rockchip (Mali)
gpu_stack_vendor: mali
containers_gpu_vendor: mali
containers_gpu_slicing:
  strategy: passthrough
```

## Setup Notes

- **Kernel Headers**: Often missing on custom ARM boards. Ensure BSP headers are installed before running `hardware/gpu`.
- **Containers**: Requires `nvidia-container-toolkit` with `csv-mode` enabled on older JetPack versions, although newer versions support CDI.
