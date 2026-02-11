# core/systemd

**Role Path**: `roles/core/systemd`

## Description
Core systemd role - Systemd configuration and hardening

## Key Tasks
- Ensure systemd is available
- Configure systemd journald
- Configure systemd resolved if available
- Enable persistent journal storage
- Reload systemd daemon
- Set core systemd completion flag

## Default Variables
- `systemd_configure_journald`
- `systemd_configure_resolved`
- `systemd_persistent_journal`

---
*This page was automatically generated from role source code.*