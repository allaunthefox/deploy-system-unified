# DP_ALT_MODE

This guide covers using DisplayPort Alt Mode via USB-C for external GPU (eGPU) and display connections.

## Overview

DisplayPort Alt Mode allows USB-C ports to carry DisplayPort video output, enabling:
- External monitors via USB-C cables
- eGPU enclosures with display output
- Docking stations with video output
- USB-C to HDMI/DP adapters
- High-bandwidth GPU compute via Thunderbolt/USB4

## USB-C Port Types

| Port Type | Video | Data | Power | Notes |
|-----------|-------|------|-------|-------|
| USB-C 3.1 | No | 10Gbps | 15W | Standard |
| USB-C with DP Alt | Yes | 10Gbps | 15W | Requires cable |
| Thunderbolt 3 | Yes | 40Gbps | 15W | PCIe tunnel |
| Thunderbolt 4 | Yes | 40Gbps | 15W | PCIe 4.0 |
| USB4 | Yes | 40Gbps | 15W | Thunderolt compat |

## Prerequisites

- USB-C port with DP Alt Mode support (look for "DP" or "Thunderbolt" symbol)
- Compatible cable (USB-C with DP support)
- GPU with display output capability
- For eGPU: Thunderbolt enclosure or USB4 dock

## Checking DP Alt Mode Support

### Using GPU Discovery Script

```bash
python3 roles/hardware/gpu/files/gpu_discovery.py --dp-alt-mode --egpu-check
```

### Manual Check

```bash
# Check USB-C ports and capabilities
lsusb -t | grep -i dp

# Check Thunderbolt devices
boltctl list

# Check for DisplayPort interfaces
lspci | grep -i display

# Check connected displays
xrandr --listmonitors
# or
wlr-randr

# Check USB4/Thunderbolt controller
lspci | grep -i thunderbolt
```

## USB-C Hub/Dock Configuration

### USB-C to Multi-Display Setup

```bash
# Connect USB-C hub with multiple video outputs
# Check what displays are detected
xrandr --listmonitors

# Configure display arrangement
xrandr --output USB-C-1 --primary --mode 3840x2160 --rate 60
xrandr --output HDMI-1 --right-of USB-C-1 --mode 1920x1080 --rate 60
```

### USB-C Dock with Ethernet + Display

```yaml
# inventory/group_vars/all/network.yml
# Configure dock networking
ansible_facts:
  nameservers:
    - 8.8.8.8
    - 1.1.1.1
```

## eGPU with DP Alt Mode

### Setup eGPU Enclosure

```bash
# Check Thunderbolt/eGPU status
boltctl list

# Verify GPU is detected
lspci | grep -E "VGA|3D"

# Check DP output from eGPU
xrandr --listproviders
```

### Running Containers with eGPU + Display

```bash
# For NVIDIA eGPU with display
podman run --rm -it \
  --gpus all \
  --device /dev/dri:/dev/dri \
  --device /dev/nvidia0:/dev/nvidia0 \
  --device /dev/nvidiactl:/dev/nvidiactl \
  --device /dev/nvidia-uvm:/dev/nvidia-uvm \
  -e DISPLAY=${DISPLAY} \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  nvidia/container-toolkit:latest \
  bash
```

## USB-C Dock with Display

### Connecting Monitor via USB-C

```bash
# Check monitor detection
dmesg | grep -i usb

# List connected displays
xrandr --listmonitors

# For Wayland
wlr-randr
```

### Configuration for Docked Workstation

```yaml
# inventory/group_vars/all/gpu.yml
gpu_stack_enable: true
gpu_stack_vendor: nvidia
gpu_stack_mode: desktop
gpu_stack_egpu_enabled: true
gpu_stack_egpu_interface: thunderbolt
```

## Troubleshooting

### No Display Detected

1. Verify cable supports DP Alt Mode
2. Check BIOS/UEFI settings for USB-C configuration
3. Update GPU drivers

```bash
# Check kernel messages
dmesg | grep -E "usb|drm|nouveau|amdgpu|i915"

# Check X11/Wayland logs
journalctl -b | grep -E "display|wayland|xorg"
```

### Black Screen on Connect

```bash
# Force display re-detection
xrandr --auto

# For NVIDIA
nvidia-settings

# For AMD
amdconfig --initial
```

## Security

- Thunderbolt security levels can block eGPU: check BIOS settings
- USB-C cable quality matters for stable display output
- Some ports only support USB data, not DP Alt Mode

## Related Links

- 
- [Vulkan Examples](VULKAN_EXAMPLES.md)
- 
