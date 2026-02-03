# Hardware Role

This role manages hardware-specific drivers and tuning.

## Sub-Components

*   **gpu**: GPU driver installation (NVIDIA, Intel, AMD).
*   **firmware**: Firmware updates and management.
*   **storage_tuning**: I/O scheduler and disk tuning.
*   **sas**: SAS controller configuration.
*   **virtual_guest**: Optimizations for running as a virtual guest.

## Usage

This role detects hardware or uses inventory variables to apply specific configurations.

```yaml
- name: Configure Hardware
  hosts: bare_metal
  roles:
    - hardware
```
