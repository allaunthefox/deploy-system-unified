# security/advanced

**Role Path**: `roles/security/advanced`

## Description
**Advanced Security Hardening Role**
This role provides optional advanced security hardening features that can be enabled in profile branches. These features are designed to be optional additions to the standard security configuration and should not affect the main branch functionality.

## Key Tasks
- Set effective SSH port to randomized value (idempotent)
- Update SSH configuration with random port (idempotent)
- Enable SSH key rotation if enabled (idempotent)
- Schedule SSH key rotation task (idempotent)
- Create SSH key rotation script with secure permissions (idempotent)

## Default Variables
- `advanced_security_hardening_enabled`
- `ssh_randomize_port`
- `ssh_random_port_range_start`
- `ssh_random_port_range_end`
- `ssh_random_port_file_dest`
- `ssh_rsync_destination`
- `ssh_key_rotation_enabled`
- `ssh_key_rotation_interval_days`
- `tmux_session_for_deployment`
- `tmux_session_name`
- `encryption_method`

---
*This page was automatically generated from role source code.*