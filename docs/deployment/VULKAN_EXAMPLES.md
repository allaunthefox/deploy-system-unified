# VULKAN_EXAMPLES

This guide provides examples for running Vulkan applications in containers with GPU acceleration.

## Prerequisites

- GPU with Vulkan support (NVIDIA, AMD, or Intel)
- Container runtime with GPU support configured
- Vulkan validation role completed (`roles/hardware/gpu/tasks/features/vulkan_validation.yml`)

## Running Vulkan Applications

### NVIDIA GPU

```bash
# Pull Vulkan-enabled image
podman pull nvidia/vulkan:latest

# Run with NVIDIA GPU access
podman run --rm -it \
  --gpus all \
  --device /dev/dri:/dev/dri \
  nvidia/vulkan:latest \
  vulkaninfo
```

### AMD GPU

```bash
# Pull ROCm Vulkan image
podman pull rocm/vulkan:latest

# Run with AMD GPU access
podman run --rm -it \
  --device /dev/dri:/dev/dri \
  --device /dev/kfd:/dev/kfd \
  --group-add video \
  rocm/vulkan:latest \
  vulkaninfo
```

### Intel GPU (Xe/Battlemage)

```bash
# Run with Intel GPU
podman run --rm -it \
  --device /dev/dri:/dev/dri \
  --device /dev/mali0:/dev/mali0 \
  --group-add video \
  intel/vulkan:base \
  vulkaninfo
```

## Running Games with MangoHud

For gaming with performance overlay:

```bash
podman run --rm -it \
  --gpus all \
  --device /dev/dri:/dev/dri \
  --device /dev/input:/dev/input \
  -v "$XDG_RUNTIME_DIR:/xdr" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e XDG_RUNTIME_DIR=/xdr \
  -e DISPLAY=${DISPLAY} \
  mangohud mangohud --dlsym ./game-executable
```

## Running Vulkan Benchmarks

### VulkanMark

```bash
podman run --rm -it \
  --gpus all \
  --device /dev/dri:/dev/dri \
  gltflab/vulkanmark:latest
```

### VKMark

```bash
podman run --rm -it \
  --gpus all \
  --device /dev/dri:/dev/dri \
  --workdir /tmp \
  ghcr.io/axL/vkmark:latest \
  vkmark
```

## Vulkan with SDL2

```python
# Example SDL2 + Vulkan application
import sdl2
import sdl2.ext
from sdl2.vulkan import *

def run_vulkan_app():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    
    # Get Vulkan extension function
    vkGetInstanceProcAddr = SDL_Vulkan_GetVkGetInstanceProcAddr()
    
    # Your Vulkan rendering code here
    
    sdl2.SDL_Quit()

if __name__ == "__main__":
    run_vulkan_app()
```

Build and run:
```bash
podman build -t vulkan-sdl2 -f Dockerfile.vulkan-sdl2 .
podman run --rm -it --gpus all vulkan-sdl2
```

## Troubleshooting

### Check Vulkan Availability

```bash
# Inside container
vulkaninfo

# Or use GPU discovery script
python3 /path/to/gpu_discovery.py --json
```

### Common Issues

1. **VK_ERROR_DEVICE_LOST**: GPU hung or reset
   - Check dmesg for errors
   - Try updating GPU drivers

2. **VK_ERROR_INITIALIZATION_FAILED**: Driver not loaded
   - Verify GPU is detected: `lspci | grep -i vga`
   - Check container runtime GPU config

3. **Missing /dev/dri**: No GPU device
   - Ensure `--device /dev/dri:/dev/dri` is passed
   - Check container has proper permissions

## Security Considerations

- Run containers with `--security-opt` options
- Limit GPU access to specific devices when possible
- Use read-only filesystem where applicable
