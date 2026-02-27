#!/bin/sh
# Podman Docker Compatibility Setup Script
# Enables Docker socket compatibility for seamless Docker CLI usage with Podman
#
# Usage: sudo ./setup-podman-docker-compat.sh
#
# This script:
#   1. Installs Podman if not present
#   2. Creates docker group for non-root access
#   3. Enables Podman's Docker compatibility socket
#   4. Configures systemd services
#   5. Validates Docker CLI compatibility

set -eu

# Configuration
PODMAN_SOCKET="/var/run/docker.sock"
PODMAN_COMPAT_SERVICE="podman-docker-compat.service"
PODMAN_COMPAT_SOCKET="podman-docker-compat.socket"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Logging functions
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

# Check if running as root
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        log_error "This script must run as root"
        log_error "Usage: sudo $0"
        exit 1
    fi
}

# Detect init system
detect_init() {
    if command -v systemctl >/dev/null 2>&1; then
        echo "systemd"
    else
        log_error "Only systemd is supported for Docker compatibility mode"
        exit 1
    fi
}

# Install Podman if not present
install_podman() {
    log_info "Checking Podman installation..."
    
    if command -v podman >/dev/null 2>&1; then
        log_info "Podman is already installed: $(podman --version)"
        return 0
    fi
    
    log_info "Installing Podman..."
    
    # Detect package manager
    if command -v apt >/dev/null 2>&1; then
        # Debian/Ubuntu
        apt-get update
        apt-get install -y podman
    elif command -v dnf >/dev/null 2>&1; then
        # RHEL/Fedora
        dnf install -y podman
    elif command -v yum >/dev/null 2>&1; then
        # Older RHEL/CentOS
        yum install -y podman
    else
        log_error "Unsupported package manager"
        log_error "Please install Podman manually: https://podman.io/docs/installation"
        exit 1
    fi
    
    log_success "Podman installed: $(podman --version)"
}

# Create docker group for compatibility
create_docker_group() {
    log_info "Setting up Docker compatibility group..."
    
    # Create docker group if it doesn't exist
    if ! getent group docker >/dev/null 2>&1; then
        groupadd docker
        log_info "Created 'docker' group"
    else
        log_info "'docker' group already exists"
    fi
    
    # Add current user to docker group
    current_user="${SUDO_USER:-$(whoami)}"
    if ! id -nG "$current_user" 2>/dev/null | grep -qw docker; then
        usermod -aG docker "$current_user"
        log_info "Added '$current_user' to 'docker' group"
        log_warn "You need to log out and log back in for group changes to take effect"
    else
        log_info "User '$current_user' is already in 'docker' group"
    fi
}

# Install systemd services
install_systemd_services() {
    log_info "Installing Podman Docker compatibility services..."
    
    # Copy service files
    cp "${SCRIPT_DIR}/podman-docker-compat.socket" "/etc/systemd/system/${PODMAN_COMPAT_SOCKET}"
    cp "${SCRIPT_DIR}/podman-docker-compat.service" "/etc/systemd/system/${PODMAN_COMPAT_SERVICE}"
    
    # Set permissions
    chmod 644 "/etc/systemd/system/${PODMAN_COMPAT_SOCKET}"
    chmod 644 "/etc/systemd/system/${PODMAN_COMPAT_SERVICE}"
    
    log_success "Systemd services installed"
}

# Enable and start services
enable_services() {
    log_info "Enabling Podman Docker compatibility..."
    
    # Reload systemd
    systemctl daemon-reload
    
    # Enable socket (starts on demand)
    systemctl enable "${PODMAN_COMPAT_SOCKET}"
    
    # Start socket
    systemctl start "${PODMAN_COMPAT_SOCKET}"
    
    # Check status
    if systemctl is-active --quiet "${PODMAN_COMPAT_SOCKET}"; then
        log_success "Podman Docker compatibility socket is active"
    else
        log_error "Failed to start Podman Docker compatibility socket"
        exit 1
    fi
}

# Validate Docker compatibility
validate_compatibility() {
    log_info "Validating Docker compatibility..."
    
    # Wait for socket to be ready
    sleep 2
    
    # Check if socket exists
    if [ ! -S "${PODMAN_SOCKET}" ]; then
        log_error "Docker socket not found at ${PODMAN_SOCKET}"
        exit 1
    fi
    
    # Test with Docker CLI if available
    if command -v docker >/dev/null 2>&1; then
        log_info "Testing Docker CLI compatibility..."
        
        if docker ps >/dev/null 2>&1; then
            log_success "Docker CLI compatibility validated"
        else
            log_warn "Docker CLI test failed - Podman socket may still be starting"
            log_warn "Try: docker ps (in a few seconds)"
        fi
    else
        log_info "Docker CLI not installed - skipping CLI validation"
        log_info "Install with: apt install docker.io or dnf install docker"
    fi
    
    # Test with curl (alternative validation)
    if command -v curl >/dev/null 2>&1; then
        log_info "Testing Podman socket with curl..."
        
        if curl --unix-socket "${PODMAN_SOCKET}" -s http://localhost/version >/dev/null 2>&1; then
            log_success "Podman socket is responding"
        else
            log_warn "Podman socket not responding yet - may need a moment to start"
        fi
    fi
}

# Display summary
show_summary() {
    printf '\n'
    log_success "=== Podman Docker Compatibility Setup Complete ==="
    printf '\n'
    log_info "Podman socket: ${PODMAN_SOCKET}"
    log_info "Service: ${PODMAN_COMPAT_SERVICE}"
    log_info "Socket: ${PODMAN_COMPAT_SOCKET}"
    printf '\n'
    log_info "You can now use Docker CLI commands with Podman:"
    log_info "  docker ps"
    log_info "  docker images"
    log_info "  docker-compose up -d"
    printf '\n'
    log_info "Quadlet containers are also accessible via Docker:"
    log_info "  docker ps (shows deploy-system container)"
    printf '\n'
    log_warn "IMPORTANT: If you added user to 'docker' group, log out and back in"
    printf '\n'
}

# Main function
main() {
    check_root
    init_system=$(detect_init)
    install_podman
    create_docker_group
    install_systemd_services
    enable_services
    validate_compatibility
    show_summary
}

# Run main function
main "$@"
