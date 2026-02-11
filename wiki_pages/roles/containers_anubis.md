# containers/anubis

**Role Path**: `roles/containers/anubis`

## Description
**Web AI Firewall**
Deploys the Anubis Web AI Firewall to protect ingress traffic.

## Key Tasks
- Create Anubis Network Quadlet
- Validate Quadlet GPU capabilities (Linux CAP_* only)
- Create Anubis container quadlet
- Enable and start Anubis service (if systemd is available and running)

## Default Variables
- `anubis_enabled`
- `anubis_port`
- `anubis_difficulty`
- `anubis_target_url`
- `anubis_image`
- `anubis_container_name`
- `quadlet_enable_gpu_support`
- `quadlet_gpu_capabilities`

---
*This page was automatically generated from role source code.*