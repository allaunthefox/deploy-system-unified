# ops_connection_info

**role**: `ops/connection_info`

**Connection Management**
Manages SSH/Rsync connection metadata, randomization of ports, and ephemeral access.

## Variables

### encryption_method
- `encryption_method` — sops or vault (Default changed to plain for dev/test without keys)

### ssh_rsync_destination
- `ssh_rsync_destination`

### ops_rsync_enable
- `ops_rsync_enable`

### ops_rsync_allowlist
- `ops_rsync_allowlist`

### ops_rsync_ephemeral_allow
- `ops_rsync_ephemeral_allow`

### ssh_randomize_port
- `ssh_randomize_port`

### ssh_port_cache_dir
- `ssh_port_cache_dir`


