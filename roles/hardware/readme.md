# Hardware Role

This role manages hardware-specific drivers and tuning.

## Sub-Components

* **gpu**: GPU driver installation (NVIDIA, Intel, AMD).
* **firmware**: Firmware updates and management.
* **storage_tuning**: I/O scheduler and disk tuning.
* **sas**: SAS controller configuration.
* **virtual_guest**: Optimizations for running as a virtual guest.

## Usage

This role detects hardware or uses inventory variables to apply specific configurations.

```yaml
- name: Configure Hardware
  hosts: bare_metal
  roles:
    - hardware
```

## Storage Tuning Strategy

The `storage_tuning` component implements a topology-aware optimization strategy that treats virtual and physical disks differently.

### Device Assignments

| Device Type | Device Names | I/O Scheduler | Rationael |
| :--- | :--- | :--- | :--- |
| **Physical SSD/NVMe** | `sd*`, `nvme*` | `mq-deadline` | Low latency, optimized for flash storage. Avoids complex re-ordering unnecessary for non-rotational media. |
| **Flash Media (SD/USB)** | `mmcblk*`, `sd*` (removable) | `mq-deadline` | Efficient handling for slower flash media without the overhead of heavy sorting. |
| **Virtual Disk (VirtIO)** | `vd*` | `none`, `mq-deadline` | Delegates scheduling to the Hypervisor (Host) to prevent "Double Scheduling" latency penalties. |
| **Virtual Disk (Xen/AWS)** | `xvd*` | `none`, `mq-deadline` | Same as VirtIO; optimized for cloud instances. |
| **RAM Disks** | `zram*`, `ram*` | `none` | Pure in-memory storage; zero seek latency requires no scheduling logic. |

### Readahead Optimization

The role parses device geometry (`lsblk`) to apply aligned read-ahead settings for large storage arrays.

* **Threshold**: Drives > 1TB.
* **Target**: 2MB (4096 sectors) or aligned to `OPT-IO` (Optimal I/O size) if reported by hardware RAID.
* **Safety**: Only applies if physical sector size is standard (512b or 4k).

### Unit Normalization

Capacity is normalized to **Megabytes (MB)** using a universal parser that supports:

* **SI Units**: MB, GB, TB, PB, EB
* **IEC Units**: MiB, GiB, TiB, PiB, EiB
* **Legacy/Error State**: Bits, Nibbles, Bytes (Failure recovery fallback)
