# DATA_MAPPING

This document details exactly where legacy backup data moves during the migration process.

## 1. File Lifecycle

1. **Source**: `/home/prod/Workspaces/Offline_Research/system-backup-2026-01-13.tar.xz` (Legacy Backup)
2. **Staging**: `projects/deploy-system-unified/migration_assets/` (Extracted by `stage_migration_assets.sh`)
3. **Final**: `/srv/containers/` (Injected by `restore_data.yml`)

## 2. Detailed Mapping Table

| Application | File Type | Source Path (Inside Backup) | Staging Path (`migration_assets/`) | Destination on Host (Production) | Details |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Authentik** | SQL Dump | `databases/postgres/authentik.sql` | `databases/postgres/authentik.sql` | `(Imported to DB Container)` | Imported via `psql` to `authentik-db` |
| **Wiki.js** | SQL Dump | `databases/postgres/wikijs.sql` | `databases/postgres/wikijs.sql` | `(Imported to DB Container)` | Imported via `psql` to `wikijs-db` (Pending role) |
| **Jellyfin** | SQLite DB | `databases/jellyfin.db` | `databases/jellyfin.db` | `/srv/containers/media_config/default/jellyfin/data/jellyfin.db` | Replaces fresh DB |
| **Radarr** | SQLite DB | `databases/radarr.db` | `databases/radarr.db` | `/srv/containers/media_config/default/radarr/radarr.db` | Verify permissions 1000:1000 |
| **Sonarr** | SQLite DB | `databases/sonarr.db` | `databases/sonarr.db` | `/srv/containers/media_config/default/sonarr/sonarr.db` | Verify permissions 1000:1000 |
| **Vaultwarden**| Data Vol | `databases/volumes/vaultwarden.tar` | `databases/volumes/vaultwarden.tar` | `/srv/containers/ops_config/vaultwarden/` | Full `data` directory extraction |
| **Homarr** | Data Vol | `databases/volumes/homarr.tar` | `databases/volumes/homarr.tar` | `/srv/containers/ops_config/homarr/` | Configs and icons |
| **Wastebin** | Data Vol | `databases/volumes/wastebin.tar` | `databases/volumes/wastebin.tar` | `/srv/containers/ops_config/wastebin/` | Paste data (sqlite) |

## 3. Configuration Notes

- **Passwords**: Database passwords in the restored files (`config.xml` etc.) usually point to the *old* database.
- **Action**: The `restore_data.yml` playbook does *not* automatically patch XML/Config files yet. This must be done manually or via a `sed` task if the database password in `secrets.generated.yml` differs from the old backup.
- **Connectivity**:
    - Old Hostnames: `authentik-postgresql`, `radarr`
    - New Hostnames: `authentik-db-default`, `radarr-default`
    - *Self-Healing*: Most `system-unified` containers use `localhost` or specific internal DNS. Verify connections after start.

## 4. Verification

After running `playbooks/restore_data.yml`, verify mapping with:

```bash
ls -l /srv/containers/media_config/default/jellyfin/data/jellyfin.db
ls -l /srv/containers/ops_config/vaultwarden/
```
