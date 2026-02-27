#!/bin/sh
set -eu

USER="${SUDO_USER:-$USER}"

if command -v podman >/dev/null 2>&1; then
  if podman info >/dev/null 2>&1; then
    echo "Podman is accessible to user: $USER"
    exit 0
  else
    echo "Podman is installed but the socket is not accessible. Try: 'sudo systemctl enable --now podman.socket' and add your user to the socket group or enable rootless podman."
    echo "Example: 'sudo usermod -aG <group> \"${USER}\"' and then re-login."
    exit 1
  fi
else
  echo "Podman is not installed. Install Podman or run tests in an environment with Podman available."
  exit 1
fi
