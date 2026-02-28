#!/bin/sh
# =============================================================================
# Audit Event Identifier: DSU-CNT-850004
# Script Type: Container Entrypoint
# Description: POSIX-compliant entrypoint for deploy-system container
# Usage: docker run deploy-system [OPTIONS]
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Deploy-System-Unified - Container Entrypoint
# POSIX-compliant entrypoint script
#
# Usage: docker run deploy-system [OPTIONS]
#   Options: Same as deploy.sh

set -eu

# Configuration
INSTALL_DIR="${INSTALL_DIR:-/opt/deploy-system}"
LOG_DIR="${LOG_DIR:-${INSTALL_DIR}/logs}"

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

# Log function
log() {
    printf '[%s] %s\n' "$(date +%Y-%m-%dT%H:%M:%S)" "$1"
}

# Health check endpoint (for container orchestration)
health_check() {
    if python3 -c "import ansible; import sys; sys.exit(0)" 2>/dev/null; then
        printf 'OK\n'
        exit 0
    else
        printf 'FAIL\n'
        exit 1
    fi
}

# Handle health check command
if [ "${1:-}" = "healthcheck" ]; then
    health_check
fi

# Log startup
log "Starting Deploy-System-Unified container..."
log "Install directory: ${INSTALL_DIR}"

# Check if running as root (should not be)
if [ "$(id -u)" -eq 0 ]; then
    log "WARN: Running as root - this is not recommended"
fi

# Execute main command
if [ $# -gt 0 ]; then
    # Run user-provided command
    log "Executing: $*"
    exec "$@"
else
    # Default: show help
    exec "${INSTALL_DIR}/scripts/deploy.sh" --help
fi
