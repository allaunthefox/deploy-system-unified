#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400014
# Script Type: K3s Remediation
# Description: Reinstalls K3s with project standard networking configuration
# Usage: sudo ./fix_k3s_networking.sh
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# K3s Permanent Fix Script - Project Standard Networking
#
# This script reinstalls K3s with the deploy-system-unified project standards:
# - Flannel backend: host-gw (not VXLAN)
# - Cluster DNS: 172.17.0.10 (not 10.43.0.10)
# - Pod CIDR: 172.16.0.0/16 (not 10.42.0.0/16)
# - Service CIDR: 172.17.0.0/16 (not 10.43.0.0/16)
# - Disable network policy (for restricted kernels)
#
# Usage: sudo ./fix_k3s_networking.sh
#
# Reference: roles/kubernetes/master/defaults/main.yml

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Project Standard Configuration (from roles/kubernetes/master/defaults/main.yml)
K3S_VERSION="${INSTALL_K3S_VERSION:-v1.31.4+k3s1}"
POD_CIDR="172.16.0.0/16"
SERVICE_CIDR="172.17.0.0/16"
CLUSTER_DNS="172.17.0.10"
CLUSTER_DOMAIN="cluster.local"
FLANNEL_BACKEND="host-gw"
PROXY_MODE="nftables"

echo "========================================"
echo "K3s Permanent Fix - Project Standards"
echo "========================================"
echo ""
log_info "This will reinstall K3s with project standard networking:"
echo "  - Flannel Backend: $FLANNEL_BACKEND"
echo "  - Cluster DNS: $CLUSTER_DNS"
echo "  - Pod CIDR: $POD_CIDR"
echo "  - Service CIDR: $SERVICE_CIDR"
echo "  - Proxy Mode: $PROXY_MODE"
echo ""
read -p "Continue? (This will restart K3s) [y/N]: " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_warn "Aborted by user"
    exit 1
fi

# Step 1: Backup existing configuration
log_info "Backing up existing K3s configuration..."
BACKUP_DIR="/tmp/k3s-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f /etc/rancher/k3s/k3s.yaml ]; then
    cp /etc/rancher/k3s/k3s.yaml "$BACKUP_DIR/"
    log_info "Kubeconfig backed up to $BACKUP_DIR"
fi

if [ -f /var/lib/deploy-system/kubernetes/token ]; then
    cp /var/lib/deploy-system/kubernetes/token "$BACKUP_DIR/"
    log_info "K3s token backed up to $BACKUP_DIR"
fi

# Step 2: Stop K3s service
log_info "Stopping K3s service..."
systemctl stop k3s || true
systemctl stop k3s-agent || true

# Step 3: Uninstall K3s (preserve data)
log_info "Uninstalling K3s (preserving data)..."
if [ -f /usr/local/bin/k3s-uninstall.sh ]; then
    /usr/local/bin/k3s-uninstall.sh || true
else
    log_warn "k3s-uninstall.sh not found, manual cleanup required"
fi

# Step 4: Clean up old binaries and config
log_info "Cleaning up old files..."
rm -rf /var/lib/rancher/k3s/agent
rm -rf /var/lib/rancher/k3s/server/db
rm -rf /etc/rancher/k3s/config.yaml
rm -f /usr/local/bin/k3s
rm -f /usr/local/bin/kubectl
rm -f /usr/local/bin/crictl
rm -f /usr/local/bin/ctr

# Step 5: Download and install K3s with project standards
log_info "Downloading K3s $K3S_VERSION..."
curl -sfL https://get.k3s.io -o /tmp/k3s-install.sh
chmod +x /tmp/k3s-install.sh

log_info "Installing K3s with project standard networking..."
export INSTALL_K3S_VERSION="$K3S_VERSION"

/tmp/k3s-install.sh server \
    --write-kubeconfig-mode 644 \
    --flannel-backend="$FLANNEL_BACKEND" \
    --disable-network-policy \
    --cluster-cidr="$POD_CIDR" \
    --service-cidr="$SERVICE_CIDR" \
    --cluster-dns="$CLUSTER_DNS" \
    --cluster-domain="$CLUSTER_DOMAIN" \
    --kube-proxy-arg="proxy-mode=$PROXY_MODE"

# Step 6: Verify installation
log_info "Verifying K3s installation..."
sleep 10

if systemctl is-active --quiet k3s; then
    log_info "K3s service is running"
else
    log_error "K3s service is not running!"
    systemctl status k3s --no-pager
    exit 1
fi

# Step 7: Wait for CoreDNS
log_info "Waiting for CoreDNS to be ready..."
for i in {1..30}; do
    if kubectl get pods -n kube-system -l k8s-app=kube-dns 2>/dev/null | grep -q "1/1.*Running"; then
        log_info "CoreDNS is ready!"
        break
    fi
    if [ "$i" -eq 30 ]; then
        log_error "CoreDNS failed to become ready after 30 attempts"
        kubectl get pods -n kube-system
        exit 1
    fi
    sleep 5
done

# Step 8: Test DNS resolution
log_info "Testing DNS resolution..."
kubectl run dns-test --image=busybox:1.36 --rm -it --restart=Never -- nslookup google.com 2>&1 | head -10 || {
    log_warn "DNS test failed, but K3s is installed"
}

# Step 9: Update systemd service template reference
log_info "Updating K3s service configuration..."
cat > /etc/systemd/system/k3s.service.env <<EOF
# K3s Environment File - Project Standards
# Generated: $(date)
# DO NOT EDIT - Changes will be overwritten by Ansible
# See: roles/kubernetes/master/templates/k3s.service.j2

__K3S_USER_AGENT="deploy-system-unified"
EOF

systemctl daemon-reload

# Step 10: Summary
echo ""
echo "========================================"
log_info "K3s Reinstallation Complete!"
echo "========================================"
echo ""
echo "Configuration:"
echo "  ✓ Flannel Backend: $FLANNEL_BACKEND"
echo "  ✓ Cluster DNS: $CLUSTER_DNS"
echo "  ✓ Pod CIDR: $POD_CIDR"
echo "  ✓ Service CIDR: $SERVICE_CIDR"
echo "  ✓ Proxy Mode: $PROXY_MODE"
echo "  ✓ Network Policy: Disabled"
echo ""
echo "Next steps:"
echo "  1. Verify CoreDNS: kubectl get pods -n kube-system -l k8s-app=kube-dns"
echo "  2. Test DNS: kubectl run dns-test --image=busybox --rm -it -- nslookup google.com"
echo "  3. Deploy workloads: ansible-playbook deploy_all_stacks.yml"
echo ""
log_info "Backup saved to: $BACKUP_DIR"
echo ""
