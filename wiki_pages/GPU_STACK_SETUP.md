# GPU_STACK_SETUP

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
gpu_stack_vendor: "auto"    # Recommended: automatically detects hardware
gpu_stack_mode: "server"    # "server", "desktop", "hybrid"
```

### Automated Hardware Discovery

The system now features an **Advanced Discovery Engine** (`gpu_discovery.py`):
*   **Auto-Detection**: Setting `gpu_stack_vendor: auto` enables the Python-based probe.
*   **Conflict Detection**: Automatically detects and blacklists conflicting drivers (e.g., Nouveau vs NVIDIA) if `deployment_profile: hardened` is active.
*   **Evidence Logs**: Raw hardware data is stored in `/var/lib/deploy-system/evidence/gpu/` for audit purposes.

### Precision Resource Allocation (Pinning)

For multi-GPU systems, you can pin specific containers to specific hardware using stable PCI paths.

```yaml
containers_gpu_allocation_map:
  - container_name: "jellyfin"
    pci_id: "0000:00:02.0"  # Map Integrated Intel GPU
  - container_name: "transcoder"
    vendor: "nvidia"
    index: 0                # Map first discrete NVIDIA card
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

### RHEL-Compatible (AlmaLinux/Rocky/CentOS Stream) GPG Key Verification (Optional)

For hardened environments, you can enable repository key verification for NVIDIA CUDA and AMD ROCm on RHEL-compatible distributions (AlmaLinux/Rocky/CentOS Stream). Verification is **opt-in** to avoid breaking when vendors rotate keys.

```yaml
# NVIDIA (RHEL-compatible)
nvidia_gpg_key_verify: true
nvidia_gpg_key_sha256: "<sha256-of-nvidia-pubkey>"
nvidia_gpg_fingerprint: "<fingerprint>"

# AMD ROCm (RHEL-compatible)
amd_rocm_gpg_key_verify: true
amd_rocm_gpg_key_sha256: "<sha256-of-rocm-pubkey>"
amd_rocm_gpg_fingerprint: "<fingerprint>"
```

If verification is enabled and the checksum or fingerprint does not match, the play will fail with a clear error. Update these values whenever a vendor rotates keys.

### CI Test: RHEL-Compatible GPG Key Verification (AlmaLinux)

A small CI-style test playbook validates NVIDIA + ROCm key verification logic in both success and failure scenarios.

```bash
ansible-playbook -i tests/inventory/ci_rhel_compat.ini tests/validate_rhel_compat_gpg_keys.yml \
  -e test_verify_enabled=true \
  -e test_nvidia_key_url="https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/D42D0685.pub" \
  -e test_nvidia_key_sha256="<sha256>" \
  -e test_nvidia_key_fingerprint="<fingerprint>" \
  -e test_rocm_key_url="https://repo.radeon.com/rocm/rocm.gpg.key" \
  -e test_rocm_key_sha256="<sha256>" \
  -e test_rocm_key_fingerprint="<fingerprint>"
```

The playbook also runs an expected-failure path with intentionally invalid checksums.

You can run this workflow manually from GitHub Actions: Actions → "Verify RHEL-Compatible (AlmaLinux) GPG Keys" → Run workflow.

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

After deployment, the role provides a verification task that prints GPU status and Vulkan capabilities:

*   **Host Status**: Prints detected driver version and compute stack health.
*   **Vulkan Check**: Validates `vulkaninfo` on the host (in `desktop` or `hybrid` mode).
*   **Container Projection**: Executes a smoke test container to verify hardware acceleration is available within the OCI runtime.

Required reboot is often handled via notify handlers (`Update initramfs`), but a manual reboot may be required for the first installation of kernel modules.

## GPU Discovery Script

The project includes an enhanced GPU discovery script (`roles/hardware/gpu/files/gpu_discovery.py`) that provides comprehensive hardware detection:

### Usage

```bash
# Basic GPU detection
python3 roles/hardware/gpu/files/gpu_discovery.py

# JSON output for automation
python3 roles/hardware/gpu/files/gpu_discovery.py --json

# Vendor validation
python3 roles/hardware/gpu/files/gpu_discovery.py -c nvidia

# Container runtime GPU support
python3 roles/hardware/gpu/files/gpu_discovery.py --container-check

# eGPU hot-swap detection
python3 roles/hardware/gpu/files/gpu_discovery.py --egpu-check

# DisplayPort Alt Mode
python3 roles/hardware/gpu/files/gpu_discovery.py --dp-alt-mode

# RDMA support
python3 roles/hardware/gpu/files/gpu_discovery.py --rdma

# eGPU + RDMA integration
python3 roles/hardware/gpu/files/gpu_discovery.py --egpu-rdma
```

### Features

- Vendor validation against configured hardware
- Multi-GPU detection and reporting
- Intel GPU generation detection (Gen9-Gen12, Xe, Battlemage)
- Driver version detection (NVIDIA, AMDGPU, Intel)
- Container runtime GPU support (Podman/Docker)
- eGPU hot-swap detection (Thunderbolt, USB4, OCuLink)
- DisplayPort Alt Mode via USB-C
- RDMA support (InfiniBand, RoCE, iWARP)
- eGPU + RDMA integration checking

## Related Documentation

- [Vulkan Examples](../deploy-system-unified/docs/deployment/VULKAN_EXAMPLES.md) - Running Vulkan applications in containers
- [DisplayPort Alt Mode Guide](../deploy-system-unified/docs/deployment/DP_ALT_MODE.md) - USB-C/Thunderbolt eGPU setup
- [GPU Slicing](GPU_SLICING.md) - Slicing strategies and configuration
