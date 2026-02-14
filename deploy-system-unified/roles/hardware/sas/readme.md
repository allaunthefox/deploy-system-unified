# Hardware SAS Role (`hardware/sas`)

## Description

This role provides support for Serial Attached SCSI (SAS) infrastructure, spanning legacy SAS-2 (6G) to modern SAS-3 (12G) and SAS-4 (24G) storage fabrics. It handles driver loading, tooling, and performance tuning for queue depths.

## Capabilities

- **Driver Management**: Loads kernel modules for:
    - **Broadcom/LSI 9600 Series** (SAS-4 / 24Gbps): `mpi3mr`
    - **Broadcom/LSI 9300/9400 Series** (SAS-3 / 12Gbps): `mpt3sas`
    - **Legacy LSI**: `megaraid_sas`
    - **Adaptec/Microchip**: `aacraid`, `pm80xx`
- **Tooling**: Installs `lsscsi`, `sg3_utils`, `smp_utils` (SAS Management Protocol), and `sdparm`.
- **Performance Tuning**:
    - Adaptive Queue Depth adjustment (Default: 128, suitable for 12G+).
    - Checks device hardware limits (`queue_depth_max`) before applying settings.
    - Optional Write Cache (WCE) enabling.

## Requirements

- Physical hardware with a SAS controller.
- Supported OS: Ubuntu, RHEL, Arch Linux.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `hardware_sas_install_tools` | `true` | Install management utilities. |
| `hardware_sas_load_drivers` | `true` | Load kernel modules. |
| `hardware_sas_queue_depth` | `128` | Target queue depth. Increase to `256` for SAS-4 NVMe/SSDs. |
| `hardware_sas_enable_write_cache`| `false`| **RISK**: Enable disk Write Cache Enable (WCE). Only use with UPS/BBU. |

## Usage

### Standard SAS-3 (12Gbps) Deployment

```yaml
- role: hardware/sas
  vars:
    hardware_sas_queue_depth: 128
```

### High-Performance SAS-4 (24Gbps) Deployment

```yaml
- role: hardware/sas
  vars:
    hardware_sas_queue_depth: 256
    hardware_sas_drivers:
      - mpi3mr
      - mpt3sas
```
