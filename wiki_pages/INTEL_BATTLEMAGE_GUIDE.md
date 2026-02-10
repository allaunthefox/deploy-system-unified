# INTEL_BATTLEMAGE_GUIDE

## Overview

This guide details the deployment of Intel's discrete GPUs (Battlemage, Alchemist) and Data Center GPUs (Flex, Max) within the unified architecture. It replaces the legacy `battlemage` instructions.

## Architecture Support

* **x86_64**: Primary support (Xeon, Core).
* **Aarch64**: Experimental PCIe support (Ampere Altra).

## Driver Stacks

We support two distinct driver paths for Intel GPUs:

1. **In-Tree Kernel Driver (`i915` / `xe`)**
    * **Modern**: The new `xe` kernel driver is default for Battlemage and newer.
    * **Legacy**: `i915` handles older generations.
    * **Config**: Managed automatically by kernel version.

2. **Compute Stack (OneAPI / Level Zero)**
    * Required for AI/Compute workloads.
    * Installs user-space libraries: `intel-level-zero-gpu`, `intel-opencl-icd`.

## Configuration in deploy-system-unified

To enable Intel GPU support:

```yaml
gpu_stack_enable: true
gpu_stack_vendor: intel
gpu_stack_enable_oneapi: true  # Installs Base Toolkit
```

### Battlemage Specifics (Xe2-HPG)

Battlemage requires Linux Kernel 6.8+ (recommended 6.10+) for stable support.

**Kernel Parameters:**
If on an older kernel (6.8), force the new driver probe:
`i915.force_probe=!9a49 xe.force_probe=9a49` (Check PCI ID).

### GPU Slicing Support

| Tech | Supported Hardware | Config |
| :--- | :--- | :--- |
| **SR-IOV** | Data Center Flex/Max | `strategy: sriov` |
| **Time-Slicing** | All (Arc, iGPU) | `strategy: time-slicing` |
| **Passthrough** | All | `strategy: passthrough` |

## Troubleshooting

**Symptom**: `clinfo` shows no devices.
**Fix**: Ensure the user is in the `render` group.
`usermod -aG render <user>`

**Symptom**: Low performance on Arc.
**Fix**: Verify ReBAR is enabled.
`dmesg | grep BAR` should show "huge BAR".
