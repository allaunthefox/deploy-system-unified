# hardware_sas

**role**: `hardware/sas`

**Hardware SAS Role (`hardware/sas`)**
This role provides support for Serial Attached SCSI (SAS) infrastructure, spanning legacy SAS-2 (6G) to modern SAS-3 (12G) and SAS-4 (24G) storage fabrics. It handles driver loading, tooling, and performance tuning for queue depths.

## Variables

- <a id="hardware_sas_install_tools"></a>`hardware_sas_install_tools`
- <a id="hardware_sas_enable_monitoring"></a>`hardware_sas_enable_monitoring`
- <a id="hardware_sas_configure_smartd"></a>`hardware_sas_configure_smartd`
- <a id="hardware_sas_load_drivers"></a>`hardware_sas_load_drivers`
- <a id="hardware_sas_drivers"></a>`hardware_sas_drivers`
- <a id="hardware_sas_packages"></a>`hardware_sas_packages`
- <a id="hardware_sas_queue_depth"></a>`hardware_sas_queue_depth`
- <a id="hardware_sas_smartd_opts"></a>`hardware_sas_smartd_opts` — Often SAS drives behind HBAs need this, or specific passthrough

