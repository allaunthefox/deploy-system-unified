# ops_connection_info

**role**: `ops/connection_info`

**Connection Management**
Manages SSH/Rsync connection metadata, randomization of ports, and ephemeral access.

## Variables

- <a id="encryption_method"></a>`encryption_method` — sops or vault (Default changed to plain for dev/test without keys)
- <a id="ssh_rsync_destination"></a>`ssh_rsync_destination`
- <a id="ops_rsync_enable"></a>`ops_rsync_enable`
- <a id="ops_rsync_allowlist"></a>`ops_rsync_allowlist`
- <a id="ops_rsync_ephemeral_allow"></a>`ops_rsync_ephemeral_allow`
- <a id="ssh_randomize_port"></a>`ssh_randomize_port`
- <a id="ssh_port_cache_dir"></a>`ssh_port_cache_dir`

