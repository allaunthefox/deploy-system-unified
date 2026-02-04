# GPU Compatibility & Interaction Matrix

This document defines the supported combinations of GPU vendors, architectures, and deployment environments within the `deploy-system-unified` project. It also analyzes potential interactions and edge cases, particularly for hybrid and virtualized setups.

## 1. Architecture & Vendor Support Matrix

| Architecture | NVIDIA | AMD | Intel | Mali (ARM) | Adreno (ARM) | IMG (RISC-V) | Generic |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **x86_64** | ✅ Stable | ✅ Stable | ✅ Stable | ❌ N/A | ❌ N/A | ❌ N/A | ✅ Stable |
| **aarch64** | ✅ Stable (Server/Jetson) | ⚠️ Experimental | ❌ Unsupported | ⚠️ Planned | ⚠️ Planned | ❌ N/A | ✅ Stable |
| **riscv64** | ❌ Unsupported | ⚠️ Experimental | ❌ Unsupported | ❌ N/A | ❌ N/A | ⚠️ Planned | ✅ Stable |

### Notes

* **NVIDIA on ARM**: Fully supported for Server (Grace Hopper) and Edge (Jetson/Orin).
* **AMD on ARM/RISC-V**: Open source drivers (`amdgpu`) theoretically work but user-space stacks (ROCm) are often x86-only or experimental on non-x86.
* **Mobile GPUs (Mali/Adreno)**: Support relies on mesa-panfrost/freedreno and is highly SoC-dependent.

## 2. Deployment Environment Matrix

How the `hardware/gpu` role behaves in different execution contexts.

| Environment | Kernel Modules | Initramfs Updates | Userspace Tools | Service Management | Driver Install |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Bare Metal** | ✅ Loaded | ✅ Updated | ✅ Installed | ✅ Managed | ✅ Full |
| **VM Guest** | ✅ Loaded | ✅ Updated | ✅ Installed | ✅ Managed | ✅ Full |
| **VM Host (VFIO)** | ⛔ **Skipped** (Reserved) | ✅ Updated | ⚠️ Partial | ⛔ Skipped | ⚠️ Firmware Only |
| **Container (LXC/Docker)** | ⛔ **Skipped** (Host Kernel) | ⛔ **Skipped** | ✅ Installed | ⛔ Skipped | ⚠️ Libs Only |
| **Chroot / Packer** | ⛔ **Skipped** (Unsafe) | ⛔ **Skipped** | ✅ Installed | ⛔ Skipped | ⚠️ Libs Only |

### Key Behaviors

1. **VFIO Reservation**: If `gpu_stack_reservation: vfio` is set, the role specifically avoids loading host kernel drivers to prevent them from seizing the GPU before `vfio-pci` can bind to it.
2. **Container Safety**: The role detects containers (`_gpu_is_container`) and forces a "Safe Mode" that installs libraries (CUDA, Vulkan, OpenCL) for applications but touches nothing system-level.

## 3. Hybrid Graphics (Mixed Vendor) Scenarios

The system supports `gpu_stack_mode: hybrid`. Below are the interaction definitions.

| Primary (iGPU) | Secondary (dGPU) | Configuration Strategy | Tools Used | Potential Issues |
| :--- | :--- | :--- | :--- | :--- |
| **Intel** | **NVIDIA** | **Prime (On-Demand)** | `nvidia-prime`, `switcheroo-control` | Power usage high if Prime profile stuck on 'nvidia'. Wayland support varies. |
| **AMD** | **NVIDIA** | **Prime (On-Demand)** | `nvidia-prime`, `switcheroo-control` | Similar to Intel. Ensure iGPU uses correct `mesa` drivers. |
| **Intel** | **AMD** | **DRI_PRIME Offload** | Native Mesa (`DRI_PRIME=1`) | Very stable. Fully open source stack. |
| **AMD** | **INTEL** | **DRI_PRIME Offload** | Native Mesa (`DRI_PRIME=1`) | Rare config (dGPU Intel Arc + AMD APU). Works via standard DRI3. |
| **NVIDIA** | **NVIDIA** | **SLI / NVLink** | Proprietary Driver | Typically handled internally by driver. Not strictly "Hybrid". |

### Feature Flag

To enable switching logic:

```yaml
gpu_stack_mode: hybrid
gpu_stack_vendor: ['intel', 'nvidia']
```

## 4. Interaction Risk Analysis

### A. Firejail vs. GPU Passthrough

**Issue**: Firejail prevents access to `/dev/dri` and `/dev/nvidia*` by default for sandboxed apps.
**Resolution**: `security/firejail` role now supports `firejail_enable_gpu: true`. This writes a global override whitelist (`/etc/firejail/globals.local`) to allow GPU device nodes.

### B. VFIO Stubbing vs. Host Driver

**Issue**: Standard GPU role installation loads `nvidia.ko` or `amdgpu.ko` immediately. If the user intends to pass this GPU to a VM, the host driver "steals" it.
**Resolution**:

* Set `gpu_stack_reservation: vfio`.
* Role installs firmware/tools but **skips** `modprobe`.
* Allows separate VFIO role to bind `vfio-pci` cleanly.

### C. Container Build Pipelines (Packer/Guestfish)

**Issue**: Running the role inside a chroot to build an OS image would previously crash when trying to run `update-initramfs` or `sysctl`.
**Resolution**: Detailed environment detection triggers "Container Mode" automatically if `ansible_is_chroot` or `ansible_virtualization_type` indicates a non-native environment.

### D. Multi-GPU Slicing (MIG / SR-IOV)

**Issue**: Slicing configuration often requires resetting the GPU, which can kill the display manager if done on the primary display GPU.
**Mitigation**: Slicing tasks (in `containers/runtime`) generally default to targeting secondary GPUs or headless setups. Caution recommended when enabling MIG on a single-GPU workstation.

## 5. Testing & Validation Matrix

When changing GPU roles, validatation must cover these permutations:

1. **Hardware Check**:
    * Single Vendor (Clean environment)
    * Dual Vendor (Conflict check)
    * No GPU (Graceful degradation)

2. **OS Family Check**:
    * Debian/Ubuntu (`apt`, `update-initramfs`)
    * RHEL-compatible (AlmaLinux/Rocky/CentOS Stream) (`dnf`, `dracut`)
    * Alpine (`apk`, `mkinitfs`)

3. **Virtualization Check**:
    * Run inside Docker (`molecule test`) -> Should pass, no kernel errors.
    * Run inside VM -> Should install drivers.
