# GPU Stack Deployment Guide

## Overview

The `hardware/gpu` role is the unified handler for installing GPU drivers, firmware, and compute stacks (CUDA, ROCm, OneAPI) across multiple architectures. It replaces legacy vendor-specific roles (like `battlemage`) with a normalized, architecture-first approach.

## Supported Architectures

This role is designed to be **Architecture First**, meaning it first detects the CPU architecture (`ansible_architecture`) and then applies vendor logic relevant to that hardware.

| Architecture | Supported Vendors | Notes |
| :--- | :--- | :--- |
| **x86_64** | NVIDIA, AMD, Intel | Standard desktop/server cards. PCIe support. |
| **aarch64** | NVIDIA, Generic | Jetson (Tegra), Grace Hopper, and ARM Servers (SBSA). |
| **riscv64** | AMD, Generic | Beginning support for experimental RISC-V boards (e.g., Milk-V). |

## Configuration

### Basic Enablement

```yaml
# In group_vars or inventory
gpu_stack_enable: true
gpu_stack_vendor: "nvidia"  # or "amd", "intel", "generic"
gpu_stack_mode: "server"    # "server", "desktop", "hybrid"
```

### Mixed Vendor Environments

You can specify multiple vendors for systems with mixed hardware (e.g., an Intel CPU with iGPU and an NVIDIA dGPU).

```yaml
gpu_stack_vendor:
  - "intel"
  - "nvidia"
```

### Compute Stacks

Enable development toolkits and runtimes.

```yaml
gpu_stack_enable_cuda: true    # NVIDIA CUDA Toolkit
gpu_stack_enable_rocm: true    # AMD ROCm SDK
gpu_stack_enable_oneapi: true  # Intel OneAPI Base Toolkit
```

### Advanced Features

```yaml
gpu_stack_enable_egpu: true         # Enable External GPU Support
gpu_stack_egpu_interface: thunderbolt # 'thunderbolt' (default) or 'oculink'
gpu_stack_enable_rdma: true         # Remote Direct Memory Access (GPUDirect)
gpu_stack_enable_dp_alt_mode: true  # USB-C DisplayPort Alt Mode
```

## Architecture Directory Structure

The role is organized to allow easy extension to new architectures (`arch/` directory):

```text
roles/hardware/gpu/
├── arch/
│   ├── x86_64/
│   │   ├── nvidia/
│   │   ├── amd/
│   │   ├── intel/
│   │   └── generic/
│   ├── aarch64/
│   │   ├── nvidia/  (Tegra vs Server logic inside)
│   │   ├── mali/
│   │   └── adreno/
│   └── riscv64/
│       └── amd/
```

## Integration with Container Runtimes

This role should run **before** `containers/runtime` or `containers/quadlets`. It ensures the kernel modules and device nodes (`/dev/nvidia0`, `/dev/dri/renderD128`) are present before the container runtime attempts to hook into them.

Branch templates like `gpu_slicing_bare_metal.yml` and `k8s_gpu_worker.yml` are pre-configured with this dependency order.

## Verify Installation

After deployment, the role provides a verification task that prints GPU status:

```bash
# Example verification output
"GPU Status: NVIDIA GPU detected. Driver: 535.129.03, CUDA: 12.2"
```

Required reboot is often handled via notify handlers (`Update initramfs`), but a manual reboot may be required for the first installation of kernel modules.
