#!/bin/sh
set -euo pipefail

WORKSPACES_ROOT="${WORKSPACES_ROOT:-$HOME/Workspaces}"
BACKUP_FILE="${WORKSPACES_ROOT}/Offline_Research/system-backup-2026-01-13.tar.xz"
STAGING_DIR="$(dirname "$0")/../migration_assets"

echo "Starting extraction from $BACKUP_FILE..."

# Ensure staging dir exists
mkdir -p "$STAGING_DIR"

# 1. Extract Postgres Dumps
echo "Extracting SQL dumps..."
tar -xf "$BACKUP_FILE" -C "$STAGING_DIR" \
    databases/postgres/authentik.sql \
    databases/postgres/wikijs.sql

# 2. Extract SQLite Databases
echo "Extracting SQLite DBs..."
tar -xf "$BACKUP_FILE" -C "$STAGING_DIR" \
    databases/jellyfin.db \
    databases/radarr.db \
    databases/sonarr.db \
    databases/kavita.db \
    databases/jellyseerr.db

# 3. Extract Volume Archives (Configs)
echo "Extracting Volume Archives..."
tar -xf "$BACKUP_FILE" -C "$STAGING_DIR" \
    databases/volumes/vaultwarden.tar \
    databases/volumes/homarr.tar \
    databases/volumes/wastebin.tar \
    databases/volumes/lidarr.tar \
    databases/volumes/navidrome.tar \
    databases/volumes/caddy_config.tar.gz

echo "Extraction complete. staged in $STAGING_DIR"
ls -R "$STAGING_DIR"
