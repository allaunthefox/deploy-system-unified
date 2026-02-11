# containers_quadlets

**role**: `containers/quadlets`

**Quadlets Role**

This role manages **Podman Quadlets**, which are Systemd generator files for containers. It ensures that container networks and services are managed natively by Systemd, providing robustness and auto-start capabilities.

## Variables

- <a id="containers_quadlet_network_name"></a>`containers_quadlet_network_name`
- <a id="containers_quadlet_create_network"></a>`containers_quadlet_create_network`
- <a id="containers_quadlet_network_subnet"></a>`containers_quadlet_network_subnet`
- <a id="containers_quadlet_network_gateway"></a>`containers_quadlet_network_gateway`
- <a id="containers_quadlet_network_iprange"></a>`containers_quadlet_network_iprange`
- <a id="containers_quadlet_custom_files"></a>`containers_quadlet_custom_files`
- <a id="containers_quadlet_arch_override"></a>`containers_quadlet_arch_override`
- <a id="containers_quadlet_enable_gpu_support"></a>`containers_quadlet_enable_gpu_support`
- <a id="containers_quadlet_gpu_vendor"></a>`containers_quadlet_gpu_vendor` — Options: nvidia, amd, intel
- <a id="containers_quadlet_gpu_devices"></a>`containers_quadlet_gpu_devices` — List of specific GPU devices to passthrough (e.g., ["/dev/nvidia0", "/dev/nvidia1"])
- <a id="containers_quadlet_gpu_capabilities"></a>`containers_quadlet_gpu_capabilities` — Linux capabilities only (CAP_*). Leave empty unless required.
- <a id="containers_quadlet_gpu_slicing"></a>`containers_quadlet_gpu_slicing`
- <a id="containers_quadlet_gpu_default_configs"></a>`containers_quadlet_gpu_default_configs`
- <a id="containers_quadlet_container_gpu_config"></a>`containers_quadlet_container_gpu_config` — Key-value map of container names to GPU config

