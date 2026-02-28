#!/bin/sh
# =============================================================================
# Audit Event Identifier: DSU-SHS-400015
# Script Type: Access Configuration (Docker)
# Description: Ensures Docker socket is accessible to user
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
set -eu

USER="${SUDO_USER:-$USER}"

if docker info >/dev/null 2>&1; then
  echo "Docker is accessible to user: $USER"
  exit 0
fi

echo "Docker socket is not accessible. Attempting to add user '$USER' to 'docker' group (requires sudo)."
if sudo usermod -aG docker "$USER"; then
  echo "User '$USER' added to 'docker' group. You need to log out and log back in (or reboot) for the group change to take effect."
  exit 0
else
  echo "Failed to add user to docker group. Please run: sudo usermod -aG docker $USER and then relogin."
  exit 1
fi
