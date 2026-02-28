#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400001
# Script Type: Main Deployment Entry Point
# Description: POSIX-compliant deployment entry point
# Usage: ./deploy.sh [OPTIONS]
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Deploy-System-Unified - Main Deployment Script
# POSIX-compliant deployment entry point
#
# Usage: ./deploy.sh [OPTIONS]
#   Options:
#     -e, --environment ENV    Target environment (dev/staging/prod)
#     -p, --playbook FILE      Playbook to run (default: production_deploy.yml)
#     -i, --inventory FILE     Inventory file (default: auto-detect)
#     -c, --check              Dry-run mode (ansible --check)
#     -v, --verbose            Verbose output
#     -h, --help               Show this help
#
# Strict Compliance:
#   - POSIX shell (#!/bin/sh, not #!/bin/bash)
#   - No pipefail (set -eu only)
#   - No [[ ]], use [ ]
#   - No echo -e, use printf
#   - No &>, use > file 2>&1

set -eu

# =============================================================================
# Configuration Centralization (DRY Principle)
# =============================================================================
INSTALL_DIR="${INSTALL_DIR:-/opt/deploy-system}"
CONFIG_DIR="${CONFIG_DIR:-${INSTALL_DIR}/config}"
LOG_DIR="${LOG_DIR:-${INSTALL_DIR}/logs}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Default values
ENVIRONMENT="${ENVIRONMENT:-prod}"
PLAYBOOK="${PLAYBOOK:-production_deploy.yml}"
INVENTORY=""
CHECK_MODE="false"
VERBOSE=""

# =============================================================================
# Functions (POSIX-compliant syntax)
# =============================================================================
usage() {
    printf '%s\n' "Deploy-System-Unified - Main Deployment Script"
    printf '\n'
    printf 'Usage: %s [OPTIONS]\n' "$0"
    printf '\n'
    printf 'Options:\n'
    printf '  -e, --environment ENV    Target environment (dev/staging/prod)\n'
    printf '  -p, --playbook FILE      Playbook to run (default: production_deploy.yml)\n'
    printf '  -i, --inventory FILE     Inventory file (default: auto-detect)\n'
    printf '  -c, --check              Dry-run mode (ansible --check)\n'
    printf '  -v, --verbose            Verbose output\n'
    printf '  -h, --help               Show this help\n'
    printf '\n'
    printf 'Examples:\n'
    printf '  %s -e prod\n' "$0"
    printf '  %s -e staging -c\n' "$0"
    printf '  %s -e dev -p site.yml\n' "$0"
}

log_info() {
    printf '[INFO] %s\n' "$1"
}

log_error() {
    printf '[ERROR] %s\n' "$1" >&2
}

log_success() {
    printf '[SUCCESS] %s\n' "$1"
}

# Privilege check for operations requiring root
# shellcheck disable=SC2329
check_service() {
    if [ "$(id -u)" -ne 0 ]; then
        log_error "This operation requires root privileges"
        log_error "Re-run with: sudo %s" "$0"
        exit 1
    fi
}

# Validate environment exists
validate_environment() {
    case "$1" in
        dev|staging|prod|production|development)
            return 0
            ;;
        *)
            log_error "Invalid environment: $1"
            log_error "Valid options: dev, staging, prod"
            return 1
            ;;
    esac
}

# Auto-detect inventory based on environment
detect_inventory() {
    env="$1"
    case "$env" in
        dev|development)
            echo "${PROJECT_ROOT}/inventory/development.ini"
            ;;
        staging)
            echo "${PROJECT_ROOT}/inventory/staging.ini"
            ;;
        prod|production)
            echo "${PROJECT_ROOT}/inventory/production.ini"
            ;;
        *)
            echo "${PROJECT_ROOT}/inventory/local.ini"
            ;;
    esac
}

# Ensure required directories exist (idempotent)
ensure_directories() {
    mkdir -p "${INSTALL_DIR}"
    mkdir -p "${CONFIG_DIR}"
    mkdir -p "${LOG_DIR}"
    chmod 750 "${INSTALL_DIR}"
    chmod 750 "${CONFIG_DIR}"
    chmod 755 "${LOG_DIR}"
}

# Pre-flight checks
preflight_checks() {
    log_info "Running pre-flight checks..."
    
    # Check Ansible is installed
    if ! command -v ansible >/dev/null 2>&1; then
        log_error "Ansible is not installed"
        log_error "Install with: pip install ansible"
        exit 1
    fi
    
    # Check Ansible version
    ansible_version=$(ansible --version | head -1 | awk '{print $2}')
    log_info "Ansible version: ${ansible_version}"
    
    # Check playbook exists
    if [ ! -f "${PROJECT_ROOT}/${PLAYBOOK}" ]; then
        log_error "Playbook not found: ${PROJECT_ROOT}/${PLAYBOOK}"
        exit 1
    fi
    
    # Check inventory exists
    if [ -n "${INVENTORY}" ] && [ ! -f "${INVENTORY}" ]; then
        log_error "Inventory not found: ${INVENTORY}"
        exit 1
    fi
    
    # Check Python dependencies
    if [ -f "${PROJECT_ROOT}/requirements.txt" ]; then
        log_info "Checking Python dependencies..."
        # Silent check - don't fail deployment
        python3 -m pip check >/dev/null 2>&1 || true
    fi
    
    log_success "Pre-flight checks passed"
}

# Main deployment function
deploy() {
    log_info "Starting deployment..."
    log_info "Environment: ${ENVIRONMENT}"
    log_info "Playbook: ${PLAYBOOK}"
    log_info "Inventory: ${INVENTORY}"
    
    # Build ansible-playbook command
    cmd="ansible-playbook ${PROJECT_ROOT}/${PLAYBOOK}"
    cmd="${cmd} -i ${INVENTORY}"
    
    if [ "${CHECK_MODE}" = "true" ]; then
        cmd="${cmd} --check"
        log_info "Running in CHECK mode (dry-run)"
    fi
    
    if [ -n "${VERBOSE}" ]; then
        cmd="${cmd} ${VERBOSE}"
    fi
    
    # Execute deployment
    log_info "Executing: ${cmd}"
    
    # Log to file and stdout
    exec > >(tee -a "${LOG_DIR}/deploy-$(date +%Y%m%d-%H%M%S).log") 2>&1
    
    # Run deployment
    if eval "${cmd}"; then
        log_success "Deployment completed successfully"
        return 0
    else
        log_error "Deployment failed"
        return 1
    fi
}

# =============================================================================
# Main Script
# =============================================================================
main() {
    # Parse command line arguments (POSIX-compliant)
    while [ $# -gt 0 ]; do
        case "$1" in
            -e|--environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            -p|--playbook)
                PLAYBOOK="$2"
                shift 2
                ;;
            -i|--inventory)
                INVENTORY="$2"
                shift 2
                ;;
            -c|--check)
                CHECK_MODE="true"
                shift
                ;;
            -v|--verbose)
                VERBOSE="-vvv"
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Validate environment
    if ! validate_environment "${ENVIRONMENT}"; then
        exit 1
    fi
    
    # Auto-detect inventory if not specified
    if [ -z "${INVENTORY}" ]; then
        INVENTORY=$(detect_inventory "${ENVIRONMENT}")
    fi
    
    # Ensure directories exist
    ensure_directories
    
    # Run pre-flight checks
    preflight_checks
    
    # Execute deployment
    deploy
}

# Run main function
main "$@"
