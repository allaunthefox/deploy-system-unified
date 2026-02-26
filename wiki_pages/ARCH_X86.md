# ARCH_GUIDE_X86

## Overview

The `x86_64` (AMD64) architecture acts as the primary deployment target for High Performance Computing (HPC), AI Training, and standard desktop workstations. It has the widest support for GPU vendors (NVIDIA, AMD, Intel).

## Supported Hardware

| Component | Recommendations |
| :--- | :--- |
| **CPU** | AMD EPYC/Ryzen, Intel Xeon/Core. AVX2/AVX-512 support recommended for AI. |
| **GPU** | NVIDIA (Pascal+), AMD (RDNA2/CDNA), Intel (Arc/Flex/Max). |
| **Boot Mode** | UEFI is strictly required for GPU features (ReBAR, SRIOV). Legacy BIOS is unsupported for GPU roles. |

## Role Configuration

The detection of `x86_64` is automatic via `ansible_architecture`.

### NVIDIA Setup (x86_64)

Standard proprietary drivers are installed from CUDA network repositories (deb/rpm) rather than `.run` files for better maintainability.

```yaml
gpu_stack_vendor: nvidia
containers_gpu_slicing:
  strategy: mig # Recommended for A100/H100
```

### AMD Setup (x86_64)

Installs the ROCm stack. Requires consistent kernel versions.

```yaml
gpu_stack_vendor: amd
containers_gpu_slicing:
  strategy: passthrough # or sriov for MI-series
```

### Intel Setup (x86_64)

Supports both iGPU (Xe) and dGPU (Arc/Data Center).

```yaml
gpu_stack_vendor: intel
gpu_stack_enable_oneapi: true
```

## Known Issues

- **IOMMU Grouping**: On consumer x86_64 motherboards, GPUs may be grouped with USB controllers. Check IOMMU groups before attempting Passthrough.
- **ReBAR**: Must be enabled in BIOS for Intel Arc and NVIDIA performance.
