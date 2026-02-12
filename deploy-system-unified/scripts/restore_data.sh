#!/bin/bash
set -euo pipefail

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
if [[ -n "${RESTIC_SNAPSHOT_ID:-}" ]]; then
    SNAP_ID="$RESTIC_SNAPSHOT_ID"
    echo "Using Snapshot ID from env: $SNAP_ID"
else
    read -p "Enter Snapshot ID to restore (or 'latest'): " SNAP_ID
    SNAP_ID=${SNAP_ID:-latest}
fi

echo "Restoring snapshot '$SNAP_ID'..."
echo "WARNING: This will overwrite files in /var/lib/docker/volumes and /srv/..."
if [[ "${AUTO_CONFIRM:-no}" != "yes" ]]; then
    read -p "Are you sure? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Stop Docker to release file locks
if [[ "${SKIP_DOCKER_STOP:-no}" != "yes" ]]; then
    echo "Stopping Docker..."
    systemctl stop docker
fi

RESTORE_TARGET="${RESTIC_RESTORE_TARGET:-/}"

echo "Restoring..."
restic restore "$SNAP_ID" --target "$RESTORE_TARGET"

if [[ "${SKIP_DOCKER_STOP:-no}" != "yes" ]]; then
    echo "Restarting Docker..."
    systemctl start docker
fi

echo "Restore complete."
