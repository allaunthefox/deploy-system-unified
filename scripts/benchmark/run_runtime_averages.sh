#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400022
# Script Type: Benchmark Runner
# Description: Runs runtime benchmark suite for Podman and LXC
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# set -e disconnected to allow diagnostics

echo "[Fri Feb 27 11:24:52 PM CET 2026] [*] Starting Runtime Benchmark Suite"

# Podman
echo "[$(date)] [*] Starting Podman averages..."
python3 -u scripts/benchmark/benchmark_aggregator.py --name "podman_storage_100" -n 100 -w 5 -- podman exec bench-podman /bin/bash /workspace/benchmark/benchmark_storage.sh /tmp --json || echo "Podman Storage failed"
python3 -u scripts/benchmark/benchmark_aggregator.py --name "podman_network_100" -n 100 -w 5 -- podman exec bench-podman /bin/bash /workspace/benchmark/benchmark_network.sh 127.0.0.1 --json || echo "Podman Network failed"

# LXC
echo "[$(date)] [*] Starting LXC averages..."
python3 -u scripts/benchmark/benchmark_aggregator.py --name "lxc_storage_100" -n 100 -w 5 -- sudo lxc-attach -n bench-lxc -- /bin/bash /workspace/benchmark/benchmark_storage.sh /tmp --json || echo "LXC Storage failed"
python3 -u scripts/benchmark/benchmark_aggregator.py --name "lxc_network_100" -n 100 -w 5 -- sudo lxc-attach -n bench-lxc -- /bin/bash /workspace/benchmark/benchmark_network.sh 127.0.0.1 --json || echo "LXC Network failed"

# K3s (Restart service if needed)
sudo systemctl start k3s
echo "[$(date)] [*] Waiting for K3s..."
for _ in {1..12}; do
    if sudo kubectl get nodes >/dev/null 2>&1; then break; fi
    sleep 10
done

if sudo kubectl get nodes >/dev/null 2>&1; then
    echo "[$(date)] [*] Starting K3s averages..."
    python3 -u scripts/benchmark/benchmark_aggregator.py --name "k3s_storage_100" -n 100 -w 5 -- sudo kubectl exec benchmark-pod -- /bin/bash /workspace/benchmark/benchmark_storage.sh /tmp --json
    python3 -u scripts/benchmark/benchmark_aggregator.py --name "k3s_network_100" -n 100 -w 5 -- sudo kubectl exec benchmark-pod -- /bin/bash /workspace/benchmark/benchmark_network.sh 127.0.0.1 --json
else
    echo "[$(date)] [!] K3s not ready, skipping..."
fi

echo "[Fri Feb 27 11:24:52 PM CET 2026] [*] Runtime Benchmark Suite Complete"
