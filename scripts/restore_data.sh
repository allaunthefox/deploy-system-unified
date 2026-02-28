#!/bin/sh
# =============================================================================
# Audit Event Identifier: DSU-SHS-400009
# Script Type: Restore Operations
# Description: Wrapper for Restic restore operations
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
set -eu

# RESTORE_DATA.SH
# Wrapper for Restic restore operations

REPO="${RESTIC_REPOSITORY:-/srv/backups/restic}"
PASSWORD_FILE="${RESTIC_PASSWORD_FILE:-/etc/restic/password}"

if [ ! -f "$PASSWORD_FILE" ]; then
    echo "Error: Restic password file not found at $PASSWORD_FILE"
    exit 1
fi

export RESTIC_PASSWORD_FILE="$PASSWORD_FILE"
export RESTIC_REPOSITORY="$REPO"

echo "Available Snapshots:"
restic snapshots

echo ""
if [ -n "${RESTIC_SNAPSHOT_ID:-}" ]; then
    SNAP_ID="$RESTIC_SNAPSHOT_ID"
    echo "Using Snapshot ID from env: $SNAP_ID"
else
    printf "Enter Snapshot ID to restore (or 'latest'): "
    read -r SNAP_ID
    SNAP_ID="${SNAP_ID:-latest}"
fi

echo "Restoring snapshot '$SNAP_ID'..."
echo "WARNING: This will overwrite files in /var/lib/docker/volumes and /srv/..."
if [ "${AUTO_CONFIRM:-no}" != "yes" ]; then
    printf "Are you sure? (y/N) "
    read -r reply
    echo ""
    case "$reply" in
        [Yy]*) ;;
        *)
            echo "Aborted."
            exit 1
            ;;
    esac
fi

# Stop Docker to release file locks
if [ "${SKIP_DOCKER_STOP:-no}" != "yes" ]; then
    echo "Stopping Docker..."
    systemctl stop docker
fi

RESTORE_TARGET="${RESTIC_RESTORE_TARGET:-/}"

echo "Restoring..."
restic restore "$SNAP_ID" --target "$RESTORE_TARGET"

if [ "${SKIP_DOCKER_STOP:-no}" != "yes" ]; then
    echo "Restarting Docker..."
    systemctl start docker
fi

echo "Restore complete."
