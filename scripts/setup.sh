#!/bin/sh
# Deploy-System-Unified - Initial System Setup Script
# POSIX-compliant setup for new deployment targets
#
# Usage: sudo ./setup.sh [OPTIONS]
#   Options:
#     -f, --force              Force re-installation
#     -d, --dry-run            Show what would be done
#     -v, --verbose            Verbose output
#     -h, --help               Show this help
#
# Strict Compliance:
#   - POSIX shell (#!/bin/sh)
#   - No pipefail (set -eu only)
#   - Init system detection (systemd only supported)
#   - EUID check before privileged operations
#   - Idempotent operations

set -eu

# =============================================================================
# Configuration Centralization (DRY Principle)
# =============================================================================
INSTALL_DIR="${INSTALL_DIR:-/opt/deploy-system}"
CONFIG_DIR="${CONFIG_DIR:-${INSTALL_DIR}/config}"
LOG_DIR="${LOG_DIR:-${INSTALL_DIR}/logs}"
BIN_DIR="${BIN_DIR:-/usr/local/bin}"
SERVICE_DIR="${SERVICE_DIR:-/etc/systemd/system}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Default values
FORCE="false"
DRY_RUN="false"
VERBOSE=""

# =============================================================================
# Functions (POSIX-compliant syntax)
# =============================================================================
usage() {
    printf '%s\n' "Deploy-System-Unified - Initial System Setup"
    printf '\n'
    printf 'Usage: sudo %s [OPTIONS]\n' "$0"
    printf '\n'
    printf 'Options:\n'
    printf '  -f, --force              Force re-installation\n'
    printf '  -d, --dry-run            Show what would be done\n'
    printf '  -v, --verbose            Verbose output\n'
    printf '  -h, --help               Show this help\n'
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

log_warn() {
    printf '[WARN] %s\n' "$1" >&2
}

# CRITICAL: Privilege check - must run as root
check_euid() {
    if [ "$(id -u)" -ne 0 ]; then
        log_error "Setup must run as root"
        log_error "Re-run with: sudo %s" "$0"
        exit 1
    fi
}

# Init system detection (portability)
detect_init_system() {
    if command -v systemctl >/dev/null 2>&1; then
        echo "systemd"
    elif command -v service >/dev/null 2>&1; then
        echo "sysvinit"
    else
        echo "unknown"
    fi
}

# Validate init system support
validate_init_system() {
    init_system="$1"
    case "$init_system" in
        systemd)
            log_info "Init system: systemd (supported)"
            return 0
            ;;
        sysvinit)
            log_warn "Init system: sysvinit (limited support)"
            return 0
            ;;
        *)
            log_error "Unsupported init system: ${init_system}"
            log_error "This deployment requires systemd or sysvinit"
            return 1
            ;;
    esac
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Python 3
    if ! command -v python3 >/dev/null 2>&1; then
        log_error "Python 3 is required but not installed"
        log_error "Install with: apt install python3 or yum install python3"
        exit 1
    fi
    
    # Check Ansible
    if ! command -v ansible >/dev/null 2>&1; then
        log_info "Ansible not found - will install"
    fi
    
    # Check disk space (minimum 5GB)
    available_kb=$(df -P "${INSTALL_DIR}" 2>/dev/null | tail -1 | awk '{print $4}' || echo "0")
    available_gb=$((available_kb / 1024 / 1024))
    if [ "$available_gb" -lt 5 ]; then
        log_error "Insufficient disk space: ${available_gb}GB available, 5GB required"
        exit 1
    fi
    log_info "Disk space: ${available_gb}GB available"
    
    # Check memory (minimum 1GB)
    if [ -f /proc/meminfo ]; then
        mem_kb=$(grep MemTotal /proc/meminfo | awk '{print $2}')
        mem_gb=$((mem_kb / 1024 / 1024))
        if [ "$mem_gb" -lt 1 ]; then
            log_warn "Low memory: ${mem_gb}GB available, 1GB recommended"
        fi
    fi
    
    log_success "System requirements check passed"
}

# Create directories (idempotent)
create_directories() {
    log_info "Creating directories..."
    
    if [ "${DRY_RUN}" = "true" ]; then
        log_info "[DRY-RUN] Would create: ${INSTALL_DIR}"
        log_info "[DRY-RUN] Would create: ${CONFIG_DIR}"
        log_info "[DRY-RUN] Would create: ${LOG_DIR}"
        return 0
    fi
    
    # Idempotent directory creation
    mkdir -p "${INSTALL_DIR}"
    mkdir -p "${CONFIG_DIR}"
    mkdir -p "${LOG_DIR}"
    
    # Set permissions
    chmod 750 "${INSTALL_DIR}"
    chmod 750 "${CONFIG_DIR}"
    chmod 755 "${LOG_DIR}"
    
    log_success "Directories created"
}

# Install Python dependencies (idempotent)
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    if [ "${DRY_RUN}" = "true" ]; then
        log_info "[DRY-RUN] Would install dependencies from requirements.txt"
        return 0
    fi
    
    if [ -f "${PROJECT_ROOT}/requirements.txt" ]; then
        # Check if pip is available
        if ! command -v pip3 >/dev/null 2>&1; then
            log_error "pip3 is not installed"
            log_error "Install with: apt install python3-pip or yum install python3-pip"
            exit 1
        fi
        
        # Install dependencies (idempotent - pip handles this)
        pip3 install --quiet --upgrade pip
        pip3 install --quiet -r "${PROJECT_ROOT}/requirements.txt"
        
        log_success "Dependencies installed"
    else
        log_warn "requirements.txt not found - skipping dependency installation"
    fi
}

# Install Ansible collections (idempotent)
install_collections() {
    log_info "Installing Ansible collections..."
    
    if [ "${DRY_RUN}" = "true" ]; then
        log_info "[DRY-RUN] Would install collections from requirements.yml"
        return 0
    fi
    
    if [ -f "${PROJECT_ROOT}/requirements.yml" ]; then
        # Install collections (idempotent - ansible-galaxy handles this)
        ansible-galaxy collection install --quiet -r "${PROJECT_ROOT}/requirements.yml" --force
        
        log_success "Collections installed"
    else
        log_warn "requirements.yml not found - skipping collection installation"
    fi
}

# Create systemd service (idempotent)
install_service() {
    init_system="$1"
    
    log_info "Installing systemd service..."
    
    if [ "${DRY_RUN}" = "true" ]; then
        log_info "[DRY-RUN] Would install systemd service"
        return 0
    fi
    
    if [ "${init_system}" != "systemd" ]; then
        log_warn "Skipping systemd service - not running systemd"
        return 0
    fi
    
    # Create service file (idempotent - overwrites if exists)
    cat > "${SERVICE_DIR}/deploy-system.service" << 'EOF'
[Unit]
Description=Deploy-System-Unified Deployment Service
After=network.target

[Service]
Type=oneshot
ExecStart=/opt/deploy-system/scripts/deploy.sh
WorkingDirectory=/opt/deploy-system
StandardOutput=journal
StandardError=journal
RemainAfterExit=no

[Install]
WantedBy=multi-user.target
EOF
    
    # Set permissions
    chmod 644 "${SERVICE_DIR}/deploy-system.service"
    
    # Reload systemd (idempotent)
    systemctl daemon-reload
    
    log_success "Systemd service installed"
}

# Create wrapper script in /usr/local/bin (idempotent)
install_wrapper() {
    log_info "Installing wrapper script..."
    
    if [ "${DRY_RUN}" = "true" ]; then
        log_info "[DRY-RUN] Would create symlink in ${BIN_DIR}"
        return 0
    fi
    
    # Create wrapper script
    cat > "${BIN_DIR}/deploy-system" << EOF
#!/bin/sh
# Deploy-System-Unified Wrapper Script
exec "${INSTALL_DIR}/scripts/deploy.sh" "\$@"
EOF
    
    # Set permissions (idempotent)
    chmod 755 "${BIN_DIR}/deploy-system"
    
    log_success "Wrapper script installed: ${BIN_DIR}/deploy-system"
}

# Display installation summary
show_summary() {
    printf '\n'
    log_info "=== Installation Summary ==="
    printf '\n'
    printf 'Installation Directory: %s\n' "${INSTALL_DIR}"
    printf 'Config Directory:       %s\n' "${CONFIG_DIR}"
    printf 'Log Directory:          %s\n' "${LOG_DIR}"
    printf 'Wrapper Script:         %s/deploy-system\n' "${BIN_DIR}"
    printf '\n'
    log_info "Next steps:"
    log_info "  1. Configure inventory: ls ${PROJECT_ROOT}/inventory/"
    log_info "  2. Run deployment: ${BIN_DIR}/deploy-system -e prod"
    log_info "  3. View logs: tail -f ${LOG_DIR}/deploy-*.log"
    printf '\n'
}

# =============================================================================
# Main Script
# =============================================================================
main() {
    # Parse command line arguments (POSIX-compliant)
    while [ $# -gt 0 ]; do
        case "$1" in
            -f|--force)
                FORCE="true"
                shift
                ;;
            -d|--dry-run)
                DRY_RUN="true"
                shift
                ;;
            -v|--verbose)
                VERBOSE="true"
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
    
    # CRITICAL: Check root privileges FIRST
    check_euid
    
    # Detect and validate init system
    init_system=$(detect_init_system)
    if ! validate_init_system "${init_system}"; then
        exit 1
    fi
    
    # Check system requirements
    check_requirements
    
    # Create directories
    create_directories
    
    # Install dependencies
    install_dependencies
    
    # Install collections
    install_collections
    
    # Install systemd service
    install_service "${init_system}"
    
    # Install wrapper script
    install_wrapper
    
    # Show summary
    show_summary
    
    log_success "Setup completed successfully"
}

# Run main function
main "$@"
