# hardware/sas

**Role Path**: `roles/hardware/sas`

## Description
**Hardware SAS Role (`hardware/sas`)**
This role provides support for Serial Attached SCSI (SAS) infrastructure, spanning legacy SAS-2 (6G) to modern SAS-3 (12G) and SAS-4 (24G) storage fabrics. It handles driver loading, tooling, and performance tuning for queue depths.

## Key Tasks
- Set SAS packages for Arch Linux
- Install SAS management utilities
- Load SAS Kernel Modules
- Read kernel module lockdown state
- Warn when kernel modules are locked down
- Ensure SAS modules are loaded on boot
- Detect SAS Devices
- Display Detected SAS Devices
- tune sas queue depth (Adaptive)
- Check Write Caching (WCE) status on SAS SSDs
- Enable Write Caching (WCE) on SAS SSDs (Careful - Requires Battery/UPS)

## Default Variables
- `hardware_sas_install_tools`
- `hardware_sas_enable_monitoring`
- `hardware_sas_configure_smartd`
- `hardware_sas_load_drivers`
- `hardware_sas_drivers`
- `hardware_sas_packages`
- `hardware_sas_queue_depth`
- `hardware_sas_smartd_opts`

---
*This page was automatically generated from role source code.*