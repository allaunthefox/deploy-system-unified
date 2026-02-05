# SSH Idempotence Guardrails

This document captures the guardrails that keep SSH configuration deterministic across runs.
These practices exist to prevent drift, duplicate directives, and port mismatches.

## Core Guardrails

- **Single port source of truth**: `ssh_effective_port` is the only port used by SSHD, firewall rules, Fail2Ban, and connection info.
- **Randomization precedence**: When `ssh_randomize_port` is enabled, the randomized port always overrides `system_ssh_port`.
- **Endlessh gating**: Port 22 is only opened automatically when `system_enable_endlessh` is enabled.
- **Single owner of sshd_config**: `roles/security/sshd` is the only role that writes SSHD directives.
- **Duplicate prevention**: `roles/security/sshd` validates that `sshd_config` contains exactly one global `Port` directive and no duplicate global SSH directives (Match blocks are ignored).
- **Bootstrap discovery**: `playbooks/bootstrap_ssh.yml` probes candidate ports and updates `ansible_ssh_port` for the run, using a controller-side cache to avoid drift after reboots.

## Operational Notes

- If `ssh_randomize_port: true`, treat `system_ssh_port` as the fallback only. The effective port becomes the randomized port.
- If Endlessh is enabled, it takes port 22 for the honeytrap. SSHD remains on `ssh_effective_port`.
- When troubleshooting, verify `ssh_effective_port` in the inventory or output of the pre-connection phase.
- The port cache lives in `inventory/.ssh_port_cache/` by default and can be overridden with `ssh_port_cache_dir`.
- To scan randomized ranges, enable `ssh_bootstrap_scan_enabled` and set `ssh_bootstrap_scan_range_start` / `ssh_bootstrap_scan_range_end`. Use `ssh_bootstrap_scan_max_ports` to bound the scan (set a positive integer to limit probe count; `0` means no limit). When `ssh_randomize_port` is true and `ssh_bootstrap_scan_max_ports` is unset (or `0`), the bootstrap scanner defaults to a **full-range scan** across the configured range to avoid accidental lockout; set `ssh_bootstrap_scan_max_ports` to a small value to shorten the scan duration if needed. When bounded, the scan samples evenly across the range.
- If `ssh_randomize_port` is true, bootstrap scanning is enabled automatically unless `ssh_bootstrap_scan_enabled` is explicitly set.

## Recommended Practices

- Validate SSH config with `sshd -t` after any changes.
- Keep port changes and firewall updates in the same run (roles already enforce this via `ssh_effective_port`).
- Avoid editing `/etc/ssh/sshd_config` outside Ansible-managed blocks.

## Related Docs

- `docs/deployment/OS_CONFIGURATION.md`
- `docs/deployment/SSH_INCIDENT_POSTMORTEM.md`
