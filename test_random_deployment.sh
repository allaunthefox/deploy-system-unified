#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400013
# Script Type: Random Deployment Testing
# Description: Generates random stack combinations and deploys
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Random Deployment Test
# Generates a random combination of stacks and settings, then deploys

set -euo pipefail

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
CHARTS_DIR="/home/prod/Workspaces/repos/github/deploy-system-unified/charts"

# All available stacks
ALL_STACKS=(
    "monitoring-stack:monitoring"
    "media-stack:media"
    "database-stack:database"
    "auth-stack:auth"
    "backup-stack:backup"
    "logging-stack:logging"
    "network-stack:network"
)

# Randomly select 3-5 stacks
NUM_STACKS=$((RANDOM % 3 + 3))
echo "=== RANDOM DEPLOYMENT TEST ==="
echo "Selected $NUM_STACKS random stacks..."
echo ""

# Shuffle and select stacks
mapfile -t SELECTED_STACKS < <(printf '%s\n' "${ALL_STACKS[@]}" | shuf | head -n "$NUM_STACKS")

# Random settings
PERSISTENCE_ENABLED=$((RANDOM % 2))
GPU_ENABLED=$((RANDOM % 3))  # 33% chance

echo "Configuration:"
echo "  Stacks: ${SELECTED_STACKS[*]}"
echo "  Persistence: $([ "$PERSISTENCE_ENABLED" -eq 1 ] && echo 'enabled' || echo 'disabled')"
echo "  GPU: $([ "$GPU_ENABLED" -eq 1 ] && echo 'enabled' || echo 'disabled')"
echo ""

# Clean up any existing deployments
echo "Cleaning up previous deployments..."
for stack_info in "${SELECTED_STACKS[@]}"; do
    stack="${stack_info%%:*}"
    namespace="${stack_info##*:}"
    helm uninstall "$stack" -n "$namespace" 2>/dev/null || true
done
sleep 5
echo ""

# Deploy selected stacks
echo "Deploying stacks..."
for stack_info in "${SELECTED_STACKS[@]}"; do
    stack="${stack_info%%:*}"
    namespace="${stack_info##*:}"
    
    echo ""
    echo "--- Deploying: $stack -> $namespace ---"
    
    # Build helm args based on stack type
    EXTRA_ARGS=""
    
    if [ "$stack" = "monitoring-stack" ]; then
        if [ $PERSISTENCE_ENABLED -eq 0 ]; then
            EXTRA_ARGS="--set prometheus.persistence.enabled=false --set grafana.persistence.enabled=false"
        fi
    elif [ "$stack" = "media-stack" ]; then
        if [ $PERSISTENCE_ENABLED -eq 0 ]; then
            EXTRA_ARGS="--set jellyfin.persistence.config.enabled=false --set jellyfin.persistence.media.enabled=false --set radarr.persistence.config.enabled=false --set sonarr.persistence.config.enabled=false"
        fi
        if [ $GPU_ENABLED -eq 0 ]; then
            EXTRA_ARGS="$EXTRA_ARGS --set hardware.gpu.enabled=false"
        fi
    elif [ "$stack" = "database-stack" ]; then
        if [ $PERSISTENCE_ENABLED -eq 0 ]; then
            EXTRA_ARGS="--set postgresql.persistence.enabled=false --set redis.persistence.enabled=false"
        fi
    elif [ "$stack" = "auth-stack" ]; then
        if [ $PERSISTENCE_ENABLED -eq 0 ]; then
            EXTRA_ARGS="--set authentik.persistence.enabled=false"
        fi
    elif [ "$stack" = "backup-stack" ]; then
        if [ $PERSISTENCE_ENABLED -eq 0 ]; then
            EXTRA_ARGS="--set restic.persistence.enabled=false"
        fi
    elif [ "$stack" = "logging-stack" ]; then
        if [ $PERSISTENCE_ENABLED -eq 0 ]; then
            EXTRA_ARGS="--set loki.persistence.enabled=false --set promtail.persistence.enabled=false"
        fi
    elif [ "$stack" = "network-stack" ]; then
        EXTRA_ARGS="--set pihole.persistence.enabled=false"
    fi

    # Deploy
    if helm install "$stack" "$CHARTS_DIR/$stack" -n "$namespace" --create-namespace "$EXTRA_ARGS" --timeout=5m 2>&1 | tail -5; then
        echo "✅ $stack deployed"
    else
        echo "❌ $stack FAILED"
    fi
done

echo ""
echo "========================================="
echo "Waiting 60 seconds for pods to start..."
echo "========================================="
sleep 60

echo ""
echo "========================================="
echo "DEPLOYMENT RESULTS"
echo "========================================="
echo ""

# Check status of each deployed stack
for stack_info in "${SELECTED_STACKS[@]}"; do
    stack="${stack_info%%:*}"
    namespace="${stack_info##*:}"
    
    echo "--- $namespace ($stack) ---"
    kubectl get pods -n "$namespace" 2>&1 | tail -5 || echo "No resources"
    echo ""
done

echo "========================================="
echo "Summary"
echo "========================================="
kubectl get pods -A --field-selector=status.phase=Running 2>&1 | grep -E "NAMESPACE|${SELECTED_STACKS[*]}" | head -20 || echo "Unable to get summary"
