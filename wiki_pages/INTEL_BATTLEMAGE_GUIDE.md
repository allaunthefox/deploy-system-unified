# INTEL_BATTLEMAGE_GUIDE

## Overview

This guide details the deployment of Intel's discrete GPUs (Battlemage, Alchemist) and Data Center GPUs (Flex, Max) within the unified architecture. It leverages the **Sprint 3: Advanced GPU Orchestration** features for automated discovery and validation.

## 🔍 Automated Discovery

The system now utilizes a specialized Python-based discovery engine (`gpu_discovery.py`) to automatically detect and identify Intel hardware.

*   **Logic**: Probes PCI classes `0300`, `0302`, and `0380`.
*   **Facts**: Exposes `primary_detected_vendor: intel` and lists specific PCI IDs for all detected Intel controllers.
*   **Audit**: Discovery results are saved to `/var/lib/deploy-system/evidence/gpu/` with a UTC timestamp for forensic audit.

## 🚀 Battlemage Specifics (Xe2-HPG)

Battlemage requires Linux Kernel 6.10+ for optimal support. 

### Force-Probe Automation
For early-access hardware or older kernels (6.8), the system can automatically inject required kernel parameters.

**Configuration:**
```yaml
gpu_battlemage_force_probe: true
```

When enabled, the `core/grub` role is automatically notified to inject `i915.force_probe` or `xe.force_probe` parameters into the boot configuration. A system reboot is required to apply these changes.

## 🏗 Container Integration

### Multi-GPU Pinning
If a system has multiple Intel GPUs (e.g., UHD Graphics iGPU + Arc dGPU), you can pin specific workloads to specific cards.

**Example Allocation:**
```yaml
containers_enable_gpu_support: true
containers_gpu_allocation_map:
  - container_name: "jellyfin"
    pci_id: "0000:00:02.0"  # Pin to integrated graphics
  - container_name: "stable-diffusion"
    pci_id: "0000:03:00.0"  # Pin to Battlemage discrete card
```

### Vulkan Projection Verification
The system automatically verifies that Intel's Vulkan capabilities are correctly projected into the container namespace.

*   **Smoke Test**: Executes `vulkaninfo` inside a test container.
*   **Hardened Enforced**: In `hardened` profiles, the deployment will fail if the container cannot access host Vulkan devices, ensuring isolation integrity.

## 🛠 Driver Stacks

1.  **Xe Driver (Modern)**: Default for Battlemage and Alchemist.
2.  **i915 Driver (Legacy)**: Used for UHD/Iris/older generations.
3.  **OneAPI / Level Zero**: Required for AI/Compute. Enable via `gpu_stack_enable_oneapi: true`.

## 🛡 Security & Hardening

*   **Access Control**: Standard users are automatically added to `video` and `render` groups in `workstation` profiles.
*   **Encrypted State**: In `hardened` profiles, the hardware discovery evidence is encrypted with Ansible Vault at-rest.

## Troubleshooting

**Symptom**: `vulkaninfo` fails in container.
**Fix**: Verify `/dev/dri/by-path/` exists on host. Alpine hosts may require manual `udev` rule creation if symlinks are missing.

**Symptom**: `clinfo` shows no devices.
**Fix**: Ensure `gpu_stack_enable_oneapi` is set to `true` to install the Level Zero compute runtime.
