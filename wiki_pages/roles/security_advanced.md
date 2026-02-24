# security_advanced

**role**: `security/advanced`

**Advanced Security Hardening Role**
This role provides optional advanced security hardening features that can be enabled in profile branches. These features are designed to be optional additions to the standard security configuration and should not affect the main branch functionality.

## Variables

### `advanced_security_hardening_enabled`{#advancedsecurityhardeningenabled}
- `advanced_security_hardening_enabled`

### `ssh_randomize_port`{#sshrandomizeport}
- `ssh_randomize_port`

### `ssh_random_port_range_start`{#sshrandomportrangestart}
- `ssh_random_port_range_start`

### `ssh_random_port_range_end`{#sshrandomportrangeend}
- `ssh_random_port_range_end`

### `ssh_random_port_file_dest`{#sshrandomportfiledest}
- `ssh_random_port_file_dest`

### `ssh_rsync_destination`{#sshrsyncdestination}
- `ssh_rsync_destination`

### `ssh_key_rotation_enabled`{#sshkeyrotationenabled}
- `ssh_key_rotation_enabled`

### `ssh_key_rotation_interval_days`{#sshkeyrotationintervaldays}
- `ssh_key_rotation_interval_days`

### `tmux_session_for_deployment`{#tmuxsessionfordeployment}
- `tmux_session_for_deployment`

### `tmux_session_name`{#tmuxsessionname}
- `tmux_session_name`

### `encryption_method`{#encryptionmethod}
- `encryption_method` — Options: sops, vault


