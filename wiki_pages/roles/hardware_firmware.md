# hardware/firmware

**Role Path**: `roles/hardware/firmware`

## Description
**Bare Metal Foundation**
Manages microcode, firmware updates, and low-level system attributes for physical hardware.

## Key Tasks
- Detect Virtualization Environment (Internal)
- Detect CPU Tier (Server vs Consumer)
- Report CPU Profile
- Install Hardware Security Tools
- Detect Hardware TPM support
- Set TPM fact
- Report TPM Status
- Configure Hardware Clock (RTC) to UTC
- Enable NTP-based RTC synchronization
- Report Hardware Clock status
- Set distribution-specific hardware package names
- Install CPU microcode updates (Intel/AMD)
- Install hardware monitoring and watchdog tools
- Configure hardware watchdog
- Enable and start hardware services

## Default Variables
- `cpu_tier`
- `is_server_cpu`
- `hardware_monitor_temp`
- `hardware_enable_watchdog`

---
*This page was automatically generated from role source code.*