# networking/container_networks

**Role Path**: `roles/networking/container_networks`

## Description
Tasks for networking/container_networks - Container Isolation

## Key Tasks
- Apply Kernel Networking Prerequisites
- Ensure {{ containers_systemd_dir }} exists
- Deploy Container Networks
- Remove legacy frontend network definitions
- Create Backend Network Segment (Application Layer)
- Create Management Network Segment (Logging/Forensics)

## Default Variables
- `container_networks_enable`
- `podman_rootless_enabled`
- `podman_rootless_user`
- `podman_rootless_user_home`
- `containers_systemd_dir`
- `containers_systemd_scope`
- `containers_systemd_owner`
- `containers_systemd_group`
- `containers_systemd_env`
- `container_networks_list`

---
*This page was automatically generated from role source code.*