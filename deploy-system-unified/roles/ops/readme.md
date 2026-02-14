# Ops Role

This role contains operational tools and maintenance tasks.

## Sub-Components

* **preflight**: Pre-deployment checks and validation.
* **session**: Deployment session management.
* **connection_info**: SSH connection details management.
* **monitoring**: System monitoring tools.
* **cloud_init**: Cloud-init status checks and integration.
* **guest_management**: Management helpers for virtual guests.
* **health_check**: Post-deploy health verification and summary artifact generation.

## Usage

Often used for utility tasks rather than permanent configuration.

```yaml
- name: Run Preflight Checks
  hosts: all
  roles:
    - ops/preflight
```
