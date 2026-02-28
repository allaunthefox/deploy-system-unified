#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400007
# Script Type: Chart Deployment
# Description: Deploys all 10 Helm chart stacks to Kubernetes
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Deploy All Helm Charts
# Deploys all 10 stacks to the Kubernetes cluster

set -euo pipefail

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
CHARTS_DIR="/home/prod/Workspaces/repos/github/deploy-system-unified/charts"

echo "========================================"
echo "Deploying All Helm Charts"
echo "========================================"
echo ""

# Define all stacks with their namespaces and default values
declare -A STACKS=(
    ["auth-stack"]="auth"
    ["backup-stack"]="backup"
    ["database-stack"]="database"
    ["logging-stack"]="logging"
    ["media-stack"]="media"
    ["monitoring-stack"]="monitoring"
    ["network-stack"]="network"
    ["ops-stack"]="ops"
    ["proxy-stack"]="proxy"
    ["security-stack"]="security"
)

# Track deployment status
declare -A DEPLOYMENT_STATUS

echo "Step 1: Creating namespaces..."
echo "----------------------------------------"
for stack in "${!STACKS[@]}"; do
    namespace="${STACKS[$stack]}"
    echo "Creating namespace: $namespace"
    kubectl create namespace "$namespace" --dry-run=client -o yaml | kubectl apply -f - 2>&1 || true
done
echo ""

echo "Step 2: Deploying Helm charts..."
echo "----------------------------------------"
for stack in "${!STACKS[@]}"; do
    namespace="${STACKS[$stack]}"
    echo ""
    echo "Deploying: $stack -> namespace: $namespace"
    
    # Custom values for each stack
    extra_args=""
    case "$stack" in
        "monitoring-stack")
            extra_args="--set prometheus.persistence.enabled=false --set grafana.persistence.enabled=false"
            ;;
        "media-stack")
            extra_args="--set jellyfin.persistence.config.enabled=false --set jellyfin.persistence.media.enabled=false --set radarr.persistence.config.enabled=false --set radarr.persistence.media.enabled=false --set sonarr.persistence.config.enabled=false --set sonarr.persistence.media.enabled=false --set hardware.gpu.enabled=false"
            ;;
        "database-stack")
            extra_args="--set postgresql.persistence.enabled=false --set redis.persistence.enabled=false"
            ;;
        "backup-stack")
            extra_args="--set restic.persistence.enabled=false --set rclone.persistence.enabled=false"
            ;;
        "logging-stack")
            extra_args="--set loki.persistence.enabled=false --set promtail.persistence.enabled=false"
            ;;
        "auth-stack")
            extra_args="--set authentik.persistence.enabled=false --set postgresql.persistence.enabled=false --set redis.persistence.enabled=false"
            ;;
        "security-stack")
            extra_args="--set crowdsec.persistence.enabled=false --set trivy.persistence.enabled=false"
            ;;
        "network-stack")
            extra_args="--set pihole.persistence.enabled=false"
            ;;
        "proxy-stack")
            extra_args="--set caddy.persistence.enabled=false"
            ;;
        "ops-stack")
            extra_args=""
            ;;
    esac

    # Deploy the chart
    if helm install "$stack" "$CHARTS_DIR/$stack" -n "$namespace" --create-namespace "$extra_args" --timeout=5m 2>&1; then
        DEPLOYMENT_STATUS["$stack"]="✅ DEPLOYED"
    else
        DEPLOYMENT_STATUS["$stack"]="❌ FAILED"
    fi
done

echo ""
echo "========================================"
echo "Deployment Summary"
echo "========================================"
for stack in "${!DEPLOYMENT_STATUS[@]}"; do
    printf "%-20s %s\n" "$stack:" "${DEPLOYMENT_STATUS[$stack]}"
done
echo ""

echo "========================================"
echo "Waiting for pods to start (60 seconds)..."
echo "========================================"
sleep 60

echo ""
echo "========================================"
echo "Pod Status Across All Namespaces"
echo "========================================"
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded 2>&1 | head -50 || echo "Unable to get pod status"

echo ""
echo "========================================"
echo "Running Pods Summary"
echo "========================================"
kubectl get pods -A 2>&1 | grep -E "NAMESPACE|Running|Completed" | head -50 || echo "Unable to get running pods"

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo ""
echo "To check status of specific stack:"
echo "  kubectl get pods -n <namespace>"
echo ""
echo "To access services:"
echo "  kubectl get services -A"
