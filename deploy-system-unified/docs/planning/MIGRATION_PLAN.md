# MIGRATION_PLAN

**Status:** Active domain support (execute when migration window is scheduled)  
**Relationship to Current Window:** Not a default near-term target unless explicitly promoted in the execution board.

## Overview

This document outlines the strategy to migrate legacy backups from `SystemBackups` into the new `deploy-system-unified` architecture. The key objective is to restore data while **rotating all sensitive credentials** to match the new strengthened security posture.

## Source Data

Location: `/home/prod/Workspaces/Offline_Research/system-backup-2026-01-13.tar.xz`

* **Postgres Dumps**:
    * `databases/postgres/authentik.sql` (Confirmed 46MB, healthy)
    * `databases/postgres/wikijs.sql`
* **SQLite Databases**: Jellyfin, Radarr, Sonarr, Kavita, Jellyseerr
* **Volume Archives**: Vaultwarden, Homarr, Wastebin, Audiobookshelf, Lidarr, Navidrome

## Migration Strategy

### 1. Database Reconciliation (PostgreSQL)

**Challenge**: SQL dumps contain hardcoded `CREATE ROLE ... PASSWORD 'hash'`.
**Solution**: "Restore & Rotate"

1. **Deploy** the new empty Postgres containers using the *new* generated secrets.
2. **Restore** the SQL dump (excluding `CREATE ROLE` commands if possible, or allowing them and immediately overriding).
3. **Rotate**: Immediately execute `ALTER USER <user> WITH PASSWORD '<new_secret>';` to sync the database with the `secrets.sops.yml` inventory.

| Application | Dump File | New Secret Variable | Destination Role |
| :--- | :--- | :--- | :--- |
| Authentik | `postgres/authentik.sql` | `authentik_pg_password` | `containers/authentik` |
| Wiki.js | `postgres/wikijs.sql` | `wikijs_pg_password` | `containers/ops` |

### 2. Application Configuration (SQLite/Flat Files)

**Challenge**: Configuration files usually contain internal API keys (e.g., Sonarr -> Radarr) and admin passwords.
**Solution**: "Extract & Patch"

1. **Extract** files to the new `config_dir` paths defined in roles.
2. **Patch**: Use Ansible `lineinfile` or manual `sed` during migration to update connections (e.g., pointing Sonarr to `postgres` instead of `sqlite` if upgrading, or updating API Keys).
3. **Permissions**: Ensure `chown` matches the new PUID/PGID strategy (usually rootless or 1000:1000).

| Application | Source | Destination Path |
| :--- | :--- | :--- |
| Jellyfin | `databases/jellyfin.db` | `/srv/containers/media_config/default/jellyfin/data/jellyfin.db` |
| Sonarr | `databases/sonarr.db` | `/srv/containers/media_config/default/sonarr/sonarr.db` |
| Vaultwarden | `volumes/vaultwarden.tar` | `/srv/containers/ops_config/vaultwarden` |
| Homarr | `volumes/homarr.tar` | `/srv/containers/ops_config/homarr` |

### 3. Secret Regeneration Plan

We will generate new high-entropy secrets for the target environment. The migration scripts will force the restored applications to accept these new credentials.

**New Secrets Required:**

1. `authentik_secret_key` (Internal App Key)
2. `authentik_pg_password` (DB Password)
3. `wikijs_pg_password` (DB Password)
4. `vaultwarden_admin_token` (Admin Panel Token)

## Execution Steps

### Phase 1: Generate Secrets

Populate `inventory/group_vars/all/secrets.generated.yml` with new keys for all migrated services.

### Phase 2: Deploy Infrastructure

Run `production_deploy.yml` from the repo root to create the structure, users, and networks. (Services will start empty). Use `branch_templates/` only as reference.

### Phase 3: Dry-Run Migration

Run a temporary migration playbook that:

1. Stops the specific container.
2. Injects the backup data.
3. Patches the database users.
4. Fixes permissions.
5. Restarts the container.

### Phase 4: Validation

Log in to each service with the *new* credentials (where applicable) or verify data integrity.

## Migration Playbook Sketch

```yaml
- name: Restore Authentik
  hosts: all
  tasks:
    - name: Copy SQL Dump
      copy: src=authentik.sql dest=/tmp/authentik.sql
    - name: Restore DB
      command: podman exec -i authentik-db psql -U postgres -d authentik < /tmp/authentik.sql
    - name: Rotate Password
      command: >
        podman exec -i authentik-db psql -U postgres -c 
        "ALTER USER authentik WITH PASSWORD '{{ authentik_pg_password }}';"
```
