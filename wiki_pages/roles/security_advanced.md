# security_advanced

**role**: `security/advanced`

**Advanced Security Hardening Role**
This role provides optional advanced security hardening features that can be enabled in profile branches. These features are designed to be optional additions to the standard security configuration and should not affect the main branch functionality.

## Variables

- <a id="advanced_security_hardening_enabled"></a>`advanced_security_hardening_enabled`
- <a id="ssh_randomize_port"></a>`ssh_randomize_port`
- <a id="ssh_random_port_range_start"></a>`ssh_random_port_range_start`
- <a id="ssh_random_port_range_end"></a>`ssh_random_port_range_end`
- <a id="ssh_random_port_file_dest"></a>`ssh_random_port_file_dest`
- <a id="ssh_rsync_destination"></a>`ssh_rsync_destination`
- <a id="ssh_key_rotation_enabled"></a>`ssh_key_rotation_enabled`
- <a id="ssh_key_rotation_interval_days"></a>`ssh_key_rotation_interval_days`
- <a id="tmux_session_for_deployment"></a>`tmux_session_for_deployment`
- <a id="tmux_session_name"></a>`tmux_session_name`
- <a id="encryption_method"></a>`encryption_method` — Options: sops, vault

