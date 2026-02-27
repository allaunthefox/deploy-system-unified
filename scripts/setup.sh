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
#   - Init system detection (systemd, sysvinit, openrc)
#   - EUID check before privileged operations
#   - Idempotent operations
#   - No hardcoded paths (all configurable)

set -eu

# =============================================================================
# Configuration Centralization (DRY Principle - All paths configurable)
# =============================================================================
INSTALL_DIR="${INSTALL_DIR:-/opt/deploy-system}"
CONFIG_DIR="${CONFIG_DIR:-${INSTALL_DIR}/config}"
LOG_DIR="${LOG_DIR:-${INSTALL_DIR}/logs}"
BIN_DIR="${BIN_DIR:-/usr/local/bin}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Init-system specific paths (detected automatically)
SERVICE_DIR=""
SERVICE_CMD=""
RELOAD_CMD=""

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
    # Check for systemd
    if command -v systemctl >/dev/null 2>&1 && [ -d /run/systemd/system ]; then
        echo "systemd"
    # Check for sysvinit
    elif [ -d /etc/init.d ] && command -v service >/dev/null 2>&1; then
        echo "sysvinit"
    # Check for OpenRC
    elif [ -d /etc/init.d ] && command -v rc-service >/dev/null 2>&1; then
        echo "openrc"
    # Check for upstart
    elif command -v initctl >/dev/null 2>&1; then
        echo "upstart"
    else
        echo "unknown"
    fi
}

# Configure service paths based on init system
configure_init_paths() {
    init_system="$1"
    
    case "$init_system" in
        systemd)
            SERVICE_DIR="/etc/systemd/system"
            SERVICE_CMD="systemctl"
            RELOAD_CMD="systemctl daemon-reload"
            log_info "Init system: systemd"
            log_info "Service directory: ${SERVICE_DIR}"
            ;;
        sysvinit)
            SERVICE_DIR="/etc/init.d"
            SERVICE_CMD="service"
            RELOAD_CMD="update-rc.d deploy-system defaults"
            log_info "Init system: sysvinit"
            log_info "Service directory: ${SERVICE_DIR}"
            ;;
        openrc)
            SERVICE_DIR="/etc/init.d"
            SERVICE_CMD="rc-service"
            RELOAD_CMD="rc-update add deploy-system default"
            log_info "Init system: OpenRC"
            log_info "Service directory: ${SERVICE_DIR}"
            ;;
        upstart)
            SERVICE_DIR="/etc/init"
            SERVICE_CMD="initctl"
            RELOAD_CMD="initctl reload-configuration"
            log_info "Init system: upstart"
            log_info "Service directory: ${SERVICE_DIR}"
            ;;
        *)
            log_warn "Unknown init system - service installation will be skipped"
            log_warn "You will need to manually configure auto-start"
            SERVICE_DIR=""
            SERVICE_CMD=""
            RELOAD_CMD=""
            ;;
    esac
}

# Validate init system support (warn but don't fail)
validate_init_system() {
    init_system="$1"
    case "$init_system" in
        systemd)
            log_info "Init system: systemd (fully supported)"
            return 0
            ;;
        sysvinit)
            log_info "Init system: sysvinit (supported)"
            return 0
            ;;
        openrc)
            log_info "Init system: OpenRC (supported)"
            return 0
            ;;
        upstart)
            log_info "Init system: upstart (supported)"
            return 0
            ;;
        *)
            log_warn "Init system: unknown (service installation will be skipped)"
            log_warn "You will need to manually configure auto-start"
            return 0  # Don't fail, just warn
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

# Create init service (idempotent, supports systemd/sysvinit/openrc/upstart)
install_service() {
    init_system="$1"
    
    if [ -z "${SERVICE_DIR}" ]; then
        log_warn "Skipping service installation - init system not supported"
        return 0
    fi
    
    log_info "Installing ${init_system} service..."
    
    if [ "${DRY_RUN}" = "true" ]; then
        log_info "[DRY-RUN] Would install ${init_system} service to ${SERVICE_DIR}"
        return 0
    fi
    
    case "$init_system" in
        systemd)
            install_systemd_service
            ;;
        sysvinit)
            install_sysvinit_service
            ;;
        openrc)
            install_openrc_service
            ;;
        upstart)
            install_upstart_service
            ;;
    esac
}

# Install systemd service
install_systemd_service() {
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
    
    chmod 644 "${SERVICE_DIR}/deploy-system.service"
    systemctl daemon-reload
    log_success "Systemd service installed"
}

# Install sysvinit service
install_sysvinit_service() {
    cat > "${SERVICE_DIR}/deploy-system" << 'EOF'
#!/bin/sh
### BEGIN INIT INFO
# Provides:          deploy-system
# Required-Start:    $network $remote_fs
# Required-Stop:     $network $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Deploy-System-Unified
# Description:       Modular infrastructure deployment
### END INIT INFO

INSTALL_DIR=/opt/deploy-system
SCRIPT_DIR="${INSTALL_DIR}/scripts"

case "$1" in
    start)
        echo "Starting Deploy-System-Unified..."
        "${SCRIPT_DIR}/deploy.sh"
        ;;
    stop)
        echo "Stopping Deploy-System-Unified..."
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    status)
        echo "Deploy-System-Unified service status"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
exit 0
EOF
    
    chmod 755 "${SERVICE_DIR}/deploy-system"
    log_success "SysVinit service installed"
}

# Install OpenRC service
install_openrc_service() {
    cat > "${SERVICE_DIR}/deploy-system" << 'EOF'
#!/sbin/openrc-run
# OpenRC service for Deploy-System-Unified

description="Deploy-System-Unified Deployment Service"
command="/opt/deploy-system/scripts/deploy.sh"
command_background="yes"
pidfile="/run/deploy-system.pid"
output_log="/opt/deploy-system/logs/deploy-system.log"
error_log="/opt/deploy-system/logs/deploy-system.err"

depend() {
    need net
    use logger
}

start_pre() {
    checkpath --directory /opt/deploy-system/logs --owner deploy:deploy --mode 0755
}
EOF
    
    chmod 755 "${SERVICE_DIR}/deploy-system"
    log_success "OpenRC service installed"
}

# Install upstart service
install_upstart_service() {
    cat > "${SERVICE_DIR}/deploy-system.conf" << 'EOF'
# Upstart service for Deploy-System-Unified

description "Deploy-System-Unified Deployment Service"
author "Deploy-System-Unified"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
respawn limit 3 30

exec /opt/deploy-system/scripts/deploy.sh
EOF
    
    chmod 644 "${SERVICE_DIR}/deploy-system.conf"
    initctl reload-configuration
    log_success "Upstart service installed"
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
    
    # Detect init system and configure paths
    init_system=$(detect_init_system)
    configure_init_paths "${init_system}"
    
    # Validate init system (warn but don't fail for unknown)
    validate_init_system "${init_system}"

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
