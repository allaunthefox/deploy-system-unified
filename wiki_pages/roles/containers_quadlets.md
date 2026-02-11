# containers/quadlets

**Role Path**: `roles/containers/quadlets`

## Description
Container quadlets role - Systemd quadlet management

## Key Tasks
- Ensure checkpoint directory exists
- Check for Quadlet checkpoint
- Read existing checkpoint
- Restore object UUID from checkpoint
- Generate new Network UUID (if no checkpoint)
- Ensure quadlet directory exists
- Create quadlet network configuration
- Deploy custom quadlet files
- Reload systemd to pick up quadlets
- List generated quadlet services
- Display available quadlet services
- Set containers quadlets completion flag
- Save Quadlet checkpoint

## Default Variables
- `containers_quadlet_network_name`
- `containers_quadlet_create_network`
- `containers_quadlet_network_subnet`
- `containers_quadlet_network_gateway`
- `containers_quadlet_network_iprange`
- `containers_quadlet_custom_files`
- `containers_quadlet_arch_override`
- `containers_quadlet_enable_gpu_support`
- `containers_quadlet_gpu_vendor`
- `containers_quadlet_gpu_devices`
- `containers_quadlet_gpu_capabilities`
- `containers_quadlet_gpu_slicing`
- `containers_quadlet_gpu_default_configs`
- `containers_quadlet_container_gpu_config`

---
*This page was automatically generated from role source code.*