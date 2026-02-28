#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400010
# Script Type: Storage Benchmark
# Description: Uses fio to measure random/sequential read/write performance
# Target: /srv/containers and /var/lib/deploy-system
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
#===============================================================================
# benchmark_storage.sh - Storage Performance Benchmark
#===============================================================================
# Uses fio to measure random/sequential read/write performance.
# Targets /srv/containers (hardened storage) and /var/lib/deploy-system.
#===============================================================================

set -eu

# Configuration
TARGET_DIR="${1:-/var/lib/deploy-system/evidence/benchmark}"
FILE_SIZE="128M"
RUNTIME=5
OUTPUT_FORMAT="text"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --json)
            OUTPUT_FORMAT="json"
            shift
            ;;
        *)
            TARGET_DIR="$1"
            shift
            ;;
    esac
done

# Ensure directory exists
mkdir -p "$TARGET_DIR"
TEST_FILE="$TARGET_DIR/fio_test_file"

# check fio
if ! command -v fio >/dev/null 2>&1; then
    echo "Error: fio not found"
    exit 1
fi

# Run fio benchmark
# --minimal for easy parsing or just use grep/sed if needed.
# Since we want JSON for the aggregator, we can use JSON output if requested.

if [ "$OUTPUT_FORMAT" = "json" ]; then
    # Run a simple random read/write test and output specific metrics as JSON
    RESULT=$(fio --name=randrw --ioengine=libaio --direct=1 --bs=4k --size=$FILE_SIZE --rw=randrw --rwmixread=75 --numjobs=1 --iodepth=16 --runtime=$RUNTIME --time_based --filename="$TEST_FILE" --output-format=json)
    
    READ_IOPS=$(echo "$RESULT" | jq '.jobs[0].read.iops')
    WRITE_IOPS=$(echo "$RESULT" | jq '.jobs[0].write.iops')
    READ_BW=$(echo "$RESULT" | jq '.jobs[0].read.bw')
    WRITE_BW=$(echo "$RESULT" | jq '.jobs[0].write.bw')
    
    echo "{ \"read_iops\": $READ_IOPS, \"write_iops\": $WRITE_IOPS, \"read_bw_kb\": $READ_BW, \"write_bw_kb\": $WRITE_BW }"
else
    echo "[*] Starting storage benchmark on $TARGET_DIR"
    fio --name=randrw --ioengine=libaio --direct=1 --bs=4k --size=$FILE_SIZE --rw=randrw --rwmixread=75 --numjobs=1 --iodepth=16 --runtime=$RUNTIME --time_based --filename="$TEST_FILE"
fi

# Cleanup
rm -f "$TEST_FILE"
