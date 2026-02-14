# Restic Backup Role

This role configures **Restic** for automated, deduplicated, and encrypted backups of system data and container volumes.

## Features

- **Automated**: Uses Systemd Timers for reliable scheduling.
- **Secure**:
    - Validates that the password is not default.
    - Configuration files are locked down (`0700`/`0600`).
    - Runs as a background service with low I/O priority.
- **Efficient**: Uses Restic's incremental deduplication.
- **Maintainable**: Includes a wrapper script (`restic_wrapper.sh`) for manual execution and debugging.

## Role Variables

### Enable/Disable

| Variable | Default | Description |
|----------|---------|-------------|
| `restic_enable` | `true` | Set to `false` to skip role execution. |

### Repository

| Variable | Default | Description |
|----------|---------|-------------|
| `restic_repo` | `/srv/backups/restic` | Target location. Supports local paths or Rclone remotes (e.g., `rclone:drive:backup`). |
| `restic_password` | `CHANGE_ME_IN_VAULT` | **REQUIRED**. The encryption password for the repository. Must be overridden securely. |

### Backup Targets

| Variable | Default | Description |
|----------|---------|-------------|
| `restic_backup_sources` | `['/etc/containers/secrets', '/srv/containers']` | List of directories to back up. |

### Retention Policy

| Variable | Default | Description |
|----------|---------|-------------|
| `restic_keep_daily` | `7` | Number of daily snapshots to keep. |
| `restic_keep_weekly` | `4` | Number of weekly snapshots to keep. |
| `restic_keep_monthly` | `6` | Number of monthly snapshots to keep. |

### Scheduling

| Variable | Default | Description |
|----------|---------|-------------|
| `restic_schedule_on_calendar` | `daily` | Systemd calendar expression for the backup schedule. |

## Usage

### 1. Configure Secrets

**CRITICAL**: You must define `restic_password` in your encrypted inventory variables (e.g., `group_vars/all/secrets.yml`). The role will fail if the default placeholder is used.

```yaml
# group_vars/all/secrets.yml (via ansible-vault or sops)
restic_password: "correct-horse-battery-staple"
```

### 2. Manual Backup

You can trigger a backup manually using the wrapper script deployed to the target host:

```bash
sudo /usr/local/bin/restic_wrapper.sh
```

### 3. Restore

To restore data, use the standard Restic CLI on the host:

```bash
# List snapshots
export RESTIC_PASSWORD_FILE=/etc/restic/password
export RESTIC_REPOSITORY=/srv/backups/restic
restic snapshots

# Restore specific snapshot
restic restore <snapshot-id> --target /tmp/restore
```

## Logs

Logs are written to `/var/log/restic/backup.log`.
