# hardware/sas

**Role Path**: `roles/hardware/sas`

## Description
Tasks for hardware/sas

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