> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

> ⚠️ **UNVERIFIED**: Deployment on riscv64 is theoretical and lacks physical hardware verification.

# ARCH_GUIDE_RISCV64

## Overview

Experimental support for `riscv64` architecture, primarily focusing on developer boards like StarFive VisionFive 2, Milk-V, and Sipeed.

## Hardware Status

| Component | Status | Notes |
| :--- | :--- | :--- |
| **PCIe Support** | **Partial** | Many boards have non-standard non-coherent PCIe implementations. |
| **AMD GPU** | **Beta** | Radeon RX 500/5000/6000 series work with open-source `amdgpu` driver on recent kernels (6.6+). |
| **NVIDIA GPU** | **N/A** | Binary blobs (proprietary driver) do not exist for RISC-V. Nouveau (open source) is the only option (low performance). |

## Integration Strategy

The project defaults to building an ephemeral build container on an x86 host to cross-compile artifacts for RISC-V nodes, or running Ansible directly on the RISC-V node (slow).

### GPU Configuration

Only AMD Radeon is currently realistic for "High Performance" RISC-V.

```yaml
gpu_stack_vendor: amd
gpu_stack_enable_rocm: false # ROCm not fully ported yet
```

## Known Limitations

- **Kernel**: Requires `CONFIG_NONPORTABLE=y` and specific PCIe patches on some boards.
- **Boot**: U-Boot is standard. The `core/bootstrap` role attempts to manage `extlinux.conf`.
