# core_systemd

**Role Path**: `roles/core/systemd`

## Description
**Systemd Configuration & Hardening**
Ensures systemd components (journald, resolved) are configured and hardened according to project standards.

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