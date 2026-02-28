#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400011
# Script Type: Network Benchmark
# Description: Uses iperf3 for throughput and ping for latency
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
#===============================================================================
# benchmark_network.sh - Network Latency and Throughput Benchmark
#===============================================================================
# Uses iperf3 for throughput and ping for latency.
# Tests localhost for baseline performance.
#===============================================================================

set -eu

# Configuration
TEST_HOST="127.0.0.1"
DURATION=5
OUTPUT_FORMAT="text"

# Internal Networking Policy (ISO 27001 §13.1)
# Favor static 10.0.0.0/8 range over localhost to avoid loopback contamination.
PREFER_RANGE="10.0.0.0/8"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --json)
            OUTPUT_FORMAT="json"
            shift
            ;;
        *)
            TEST_HOST="$1"
            shift
            ;;
    esac
done

# Check for localhost reliance
if [[ "$TEST_HOST" == "127.0.0.1" ]] || [[ "$TEST_HOST" == "localhost" ]]; then
    echo "WARNING: Relying on localhost ($TEST_HOST) for benchmarks is non-compliant with Internal Networking Policy." >&2
    echo "         Prefer static ranges in $PREFER_RANGE (e.g. 10.42.x.x) to avoid loopback contamination." >&2
fi

# check dependencies
for cmd in iperf3 ping jq; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Error: $cmd not found"
        exit 1
    fi
done

# Ensure iperf3 server is running on localhost
if ! pgrep -x "iperf3" > /dev/null; then
    iperf3 -s -D >/dev/null 2>&1
    sleep 1
fi

if [ "$OUTPUT_FORMAT" = "json" ]; then
    # Latency (ping)
    LATENCY_RAW=$(ping -c 5 -q "$TEST_HOST" | tail -1 | cut -d/ -f5)
    
    # Throughput (iperf3)
    IPERF_RESULT=$(iperf3 -c "$TEST_HOST" -t "$DURATION" -J)
    THROUGHPUT_MBPS=$(echo "$IPERF_RESULT" | jq '.end.sum_sent.bits_per_second / 1000000')

    echo "{ \"latency_ms\": $LATENCY_RAW, \"throughput_mbps\": $THROUGHPUT_MBPS }"
else
    echo "[*] Starting network benchmark to $TEST_HOST"
    echo "[*] Testing latency..."
    ping -c 5 "$TEST_HOST"
    echo "[*] Testing throughput..."
    iperf3 -c "$TEST_HOST" -t "$DURATION"
fi
