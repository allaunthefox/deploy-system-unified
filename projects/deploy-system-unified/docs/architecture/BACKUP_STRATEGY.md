# Backup & Disaster Recovery Strategy
This project implements a tiered backup strategy to ensure data persistence and system recoverability across all solution stacks.

## 🏗 Tiered Backup Model
### 1. System Snapshots (`backup/timeshift`)
- **Focus**: System-level recovery (Root partition).
- **Usage**: Primarily for `bare_metal_hardened` and `virtual_hypervisor`.
- **Logic**: Creates rsync or Btrfs-based snapshots of the OS state.

### 2. Deduplicated Data Backups (`backup/restic`)
- **Focus**: Application data, container volumes, and secrets.
- **Usage**: Mandatory for `production_servers`.
- **Logic**: High-performance, encrypted, and deduplicated backups to local or remote repositories.
### 3. Cloud Synchronization (`backup/rclone`)
- **Focus**: Off-site replication.
- **Usage**: Cross-branch.
- **Logic**: Syncs local backup repositories (created by restic) to encrypted cloud providers (S3, B2, Drive).

## 🛠 Operational Workflow
1. **Infrastructure**: `storage/filesystems/btrfs` provides the snapshots capability.
2. **Workload**: `backup/restic` packages the application data.
3. **Exfiltration**: `backup/rclone` pushes the data out of the failure domain.

