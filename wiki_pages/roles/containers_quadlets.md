# containers_quadlets

**role**: `containers/quadlets`

**Quadlets Role**

This role manages **Podman Quadlets**, which are Systemd generator files for containers. It ensures that container networks and services are managed natively by Systemd, providing robustness and auto-start capabilities.

## Variables

### containers_quadlet_network_name
- `containers_quadlet_network_name`

### containers_quadlet_create_network
- `containers_quadlet_create_network`

### containers_quadlet_network_subnet
- `containers_quadlet_network_subnet`

### containers_quadlet_network_gateway
- `containers_quadlet_network_gateway`

### containers_quadlet_network_iprange
- `containers_quadlet_network_iprange`

### containers_quadlet_custom_files
- `containers_quadlet_custom_files`

### containers_quadlet_arch_override
- `containers_quadlet_arch_override`

### containers_quadlet_enable_gpu_support
- `containers_quadlet_enable_gpu_support`

### containers_quadlet_gpu_vendor
- `containers_quadlet_gpu_vendor` — Options: nvidia, amd, intel

### containers_quadlet_gpu_devices
- `containers_quadlet_gpu_devices` — List of specific GPU devices to passthrough (e.g., ["/dev/nvidia0", "/dev/nvidia1"])

### containers_quadlet_gpu_capabilities
- `containers_quadlet_gpu_capabilities` — Linux capabilities only (CAP_*). Leave empty unless required.

### containers_quadlet_gpu_slicing
- `containers_quadlet_gpu_slicing`

### containers_quadlet_gpu_default_configs
- `containers_quadlet_gpu_default_configs`

### containers_quadlet_container_gpu_config
- `containers_quadlet_container_gpu_config` — Key-value map of container names to GPU config


