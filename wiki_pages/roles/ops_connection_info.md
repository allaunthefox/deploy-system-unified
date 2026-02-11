# ops_connection_info

**Role Path**: `roles/ops/connection_info`

## Description
**Connection Management**
Manages SSH/Rsync connection metadata, randomization of ports, and ephemeral access.

## Key Tasks
- Determine SSH port for connection info
- Create SSH connection info (idempotent)
- Determine SSH port cache directory (controller)
- Ensure SSH port cache directory exists (controller)
- Cache SSH port for host (controller)
- Create secure temporary file on controller for SSH connection info (idempotent)
- Set secure permissions on temporary file (idempotent)
- Copy SSH connection info to secure temp file (idempotent)
- Handle SOPS Encryption
- Handle Ansible Vault Encryption
- Set path for plaintext SSH info (insecure/dev only)
- Verify encryption succeeded (idempotent)
- Clean up plaintext temporary SSH file (idempotent)
- Rsync encrypted SSH connection info to specified destination (idempotent)

## Default Variables
- `encryption_method`
- `ssh_rsync_destination`
- `ops_rsync_enable`
- `ops_rsync_allowlist`
- `ops_rsync_ephemeral_allow`
- `ssh_randomize_port`
- `ssh_port_cache_dir`

---
*This page was automatically generated from role source code.*