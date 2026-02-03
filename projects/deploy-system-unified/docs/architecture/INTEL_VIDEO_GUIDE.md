# Intel Video & GPU Support Guide

This document outlines the configuration provided for Intel GPUs, specifically focusing on "Basic Video" (Media/Display) and "Compute" (OneAPI) profiles.

## Supported Architectures

- **x86_64**: Primary support target.

## Driver Profiles

### 1. Basic Video / Media (Default)

Enables hardware acceleration for video decoding/encoding (VAAPI) and display (Vulkan/OpenGL).
**Packages Installed:**

- `intel-media-va-driver-non-free`: Full HW acceleration (including proprietary codecs).
- `mesa-vulkan-drivers`: Vulkan support (Intel Anvil).
- `libgl1-mesa-dri`: OpenGL DRI drivers.
- `firmware-misc-nonfree`: Required for GuC/HuC firmware on newer iGPUs (Gen9+).

**Kernel Configuration:**

- `i915.enable_guc=3`: Enables GuC/HuC firmware loading for hardware video scheduling and bitrate control.
- `xe.force_probe=*`: Enabled on newer kernels for experimental Xe driver support (Battlemage readiness).

**Container Configuration:**

- Device Groups: `video`, `render`.
- Devices: `/dev/dri/card*` (Display), `/dev/dri/renderD*` (Compute/Encode).

### 3. Legacy (i8xx) and Minimal Providers

Designed for ancient Intel chipsets (i810/i815) and server BMC graphics (Matrox G200, Aspeed).
**Packages Installed:**

- `xserver-xorg-video-intel`: Legacy DDX for Gen2-4 Intel graphics.
- `xserver-xorg-video-vesa`: Universal VESA fallback.
- `xserver-xorg-video-mga`: Matrox G200 series support.
- `xserver-xorg-video-ast`: Aspeed AST2400/2500/2600 support.
- *Note*: Hardware acceleration is minimal or non-existent (mostly 2D or Framebuffer).

### 4. Compute (OneAPI)

Enables OpenCL and Level Zero support for compute workloads (AI/ML).
**Packages Installed:**

- `intel-basekit`: Full OneAPI Base Toolkit (if `gpu_stack_enable_oneapi` is true).

## Container Runtime

Containers are configured to inherit the correct device nodes.

- Podman/Docker will receive `--device /dev/dri/...` via the `video` and `render` groups.
- `default_capabilities` updated to include `gpu` (generic hook) but device groups are the primary mechanism for Intel.

## Testing

To verify video acceleration inside a container:

```bash
podman run --rm -it --device /dev/dri:/dev/dri ubuntu:22.04 bash
apt update && apt install -y vainfo
vainfo
```

Output should show `VA-API version` and a list of supported profiles (H.264, VP9, AV1, etc.).
