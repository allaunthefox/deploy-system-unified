# Storage Role

This role manages filesystem formatting and backup strategies.

## Sub-Components

* **filesystems**: Filesystem creation and mounting (BTRFS, ZFS, etc.).
* **backup**: Backup tool configuration (Restic, Timeshift, etc.).

## Usage

```yaml
- name: Configure Storage
  hosts: storage_nodes
  roles:
    - storage
```
