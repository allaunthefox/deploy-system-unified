# BATTLEMAGE_SETUP

This guide provides a technical walkthrough for deploying Intel Xe2 (Battlemage) and Arc (Alchemist) GPUs using the **Deploy-System-Unified** advanced GPU orchestration engine.

## 🛠 Pre-Deployment Checklist

Before running the `hardware/gpu` role, ensure the following hardware conditions are met:

1.  **Resizable BAR (ReBAR)**: Must be ENABLED in the BIOS.
    *   *Verification*: `dmesg | grep -i BAR` (Look for "huge BAR").
2.  **Kernel Version**: 
    *   **Recommended**: Linux 6.10+ (Native support).
    *   **Minimum**: Linux 6.8 (Requires `force_probe`).
3.  **Secure Boot**: If enabled, ensure you have a mechanism to sign the Intel drivers if using non-repo backports.

## 🔍 Step 1: Automated Discovery

The system can automatically detect your Intel hardware. In your host or group variables, set:

```yaml
gpu_stack_enable: true
gpu_stack_vendor: "auto"
```

The system will execute `gpu_discovery.py` and identify all Intel controllers (VGA, 3D, and Display classes).

## 🛡 Step 2: Enforcing Driver Integrity

To prevent conflicts with the generic `nouveau` or legacy `radeon` drivers, ensure your profile is set to `hardened`:

```yaml
deployment_profile: "hardened"
```

The system will:
1.  Detect if `nouveau` is currently loaded.
2.  Generate `/etc/modprobe.d/dsu-gpu-blacklist.conf`.
3.  Automatically trigger an initramfs update (`update-initramfs`, `dracut`, or `mkinitfs`).
4.  Notify you that a reboot is required.

## 🏗 Step 3: Precision Resource Allocation

If you have multiple Intel GPUs (e.g., a CPU iGPU and a discrete Battlemage card), use the allocation map to pin workloads.

### Example: Pinning Jellyfin to iGPU and AI to dGPU

```yaml
containers_gpu_allocation_map:
  - container_name: "jellyfin"
    pci_id: "0000:00:02.0"  # Your Integrated Graphics
  - container_name: "anubis-ai"
    pci_id: "0000:03:00.0"  # Your Battlemage discrete card
```

The role will automatically generate stable `/dev/dri/by-path/` links in the Quadlet configuration.

## 🚀 Step 4: Forcing Probe (Early Access)

If you are on an older kernel but have modern Battlemage hardware, enable the force-probe logic:

```yaml
gpu_battlemage_force_probe: true
```

This will inject `xe.force_probe=*` into your GRUB/bootloader configuration.

## ✅ Step 5: Verification

Once deployed, verify the stack using the built-in validation tasks:

### 1. Host Validation
Check `/var/lib/deploy-system/evidence/gpu/` for the latest discovery JSON. It contains raw PCI IDs and detected models.

### 2. Vulkan Projection
The role will automatically run a smoke test. To run it manually:
```bash
podman run --rm --device /dev/dri:/dev/dri:rw docker.io/library/ubuntu:24.04 
  sh -c "apt-get update && apt-get install -y vulkan-tools && vulkaninfo --summary"
```

## 📋 Distribution Specifics

| Distro | Pkg Manager | Boot Tool |
| :--- | :--- | :--- |
| **Ubuntu/Debian** | `apt` | `update-initramfs` |
| **Fedora** | `dnf` | `dracut` |
| **Archlinux** | `pacman` | `mkinitcpio` |
| **Alpine** | `apk` | `mkinitfs` |

The `hardware/gpu` role handles these variations automatically.
