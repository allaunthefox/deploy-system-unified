#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-SHS-400012
# Script Type: Metrics Collection Benchmark
# Description: Collects resource utilization metrics for K8s vs Podman
# Usage: ./benchmark_metrics.sh [podman|k8s] [duration_minutes]
# Last Updated: 2026-03-01
# Version: 1.1
# =============================================================================

set -eu

# Configuration
RUNTIME="${1:-podman}"
DURATION="${2:-60}"
OUTPUT_DIR="${OUTPUT_DIR:-/var/lib/deploy-system/evidence/benchmark}"
INTERVAL=5  # seconds between samples
OUTPUT_FORMAT="text"

# Parse arguments for --json
for arg in "$@"; do
    if [ "$arg" = "--json" ]; then
        OUTPUT_FORMAT="json"
    fi
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { if [ "$OUTPUT_FORMAT" != "json" ]; then printf "${GREEN}[INFO]${NC} %s\n" "$1"; fi; }
log_warn() { if [ "$OUTPUT_FORMAT" != "json" ]; then printf "${YELLOW}[WARN]${NC} %s\n" "$1"; fi; }
log_error() { printf "${RED}[ERROR]${NC} %s\n" "$1"; }

#===============================================================================
# Dependency Checks
#===============================================================================
check_dependencies() {
    missing_deps=""

    # Common dependencies
    for cmd in jq bc; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            missing_deps="$missing_deps $cmd"
        fi
    done

    # Runtime-specific dependencies
    if [ "$RUNTIME" = "podman" ]; then
        if ! command -v podman >/dev/null 2>&1; then
            missing_deps="$missing_deps podman"
        fi
    else
        if ! command -v kubectl >/dev/null 2>&1; then
            missing_deps="$missing_deps kubectl"
        fi
    fi

    # Optional: iostat for disk metrics
    if ! command -v iostat >/dev/null 2>&1; then
        log_warn "iostat not found - disk I/O metrics will be skipped"
    fi

    # Report missing required dependencies
    if [ -n "$missing_deps" ]; then
        log_error "Missing required dependencies:$missing_deps"
        log_info "Install with: apt-get install$missing_deps"
        exit 1
    fi

    log_info "All dependencies satisfied"
}

#===============================================================================
# Unit Conversion Helpers
#===============================================================================
convert_cpu_to_percent() {
    local cpu_value="$1"
    local num_cores
    num_cores=$(nproc 2>/dev/null || echo "1")

    case "$cpu_value" in
        *m)
            local millicores="${cpu_value%m}"
            echo "scale=2; $millicores / (100 * $num_cores)" | bc
            ;;
        *)
            echo "scale=2; $cpu_value * 100 / $num_cores" | bc
            ;;
    esac
}

convert_mem_to_percent() {
    local mem_value="$1"
    local total_mem
    total_mem=$(free -m | awk 'NR==2{print $2}')

    local mem_num
    mem_num=$(echo "$mem_value" | sed 's/[^0-9.]//g')
    local mem_unit
    mem_unit=$(echo "$mem_value" | sed 's/[0-9.]//g')

    if [ "$mem_unit" = "Gi" ]; then
        mem_num=$(echo "scale=2; $mem_num * 1024" | bc)
    fi

    echo "scale=2; $mem_num * 100 / $total_mem" | bc
}

#===============================================================================
# Main Collection Loop
#===============================================================================
main() {
    mkdir -p "$OUTPUT_DIR"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    LOG_FILE="$OUTPUT_DIR/${RUNTIME}_benchmark_${TIMESTAMP}.log"

    log_info "Starting $RUNTIME benchmark for $DURATION minutes..."
    log_info "Output directory: $OUTPUT_DIR"
    log_info "Log file: $LOG_FILE"

    check_dependencies

    local iterations=$((DURATION * 60 / INTERVAL))
    local count=0

    echo "timestamp,cpu_percent,mem_percent,container,cpu_usage,mem_usage" > "$LOG_FILE"

    while [ "$count" -lt "$iterations" ]; do
        local timestamp
        timestamp=$(date +%Y-%m-%dT%H:%M:%S)

       if [ "$OUTPUT_FORMAT" = "json" ]; then
        local CPU_STATS
        mapfile -t CPU_STATS < <(grep '^cpu ' /proc/stat)
        # Process first line of CPU stats
        local cpu_line="${CPU_STATS[0]}"
        local fields
        read -r -a fields <<< "$cpu_line"
        
        local IDLE_BEFORE=${fields[4]}
        local TOTAL_BEFORE=0
        for i in "${fields[@]:1}"; do TOTAL_BEFORE=$((TOTAL_BEFORE + i)); done
        
        sleep 0.1
        
        mapfile -t CPU_STATS < <(grep '^cpu ' /proc/stat)
        cpu_line="${CPU_STATS[0]}"
        read -r -a fields <<< "$cpu_line"
        
        local IDLE_AFTER=${fields[4]}
        local TOTAL_AFTER=0
        for i in "${fields[@]:1}"; do TOTAL_AFTER=$((TOTAL_AFTER + i)); done
        
        local CPU_USAGE
        CPU_USAGE=$(awk "BEGIN {print (1 - ($IDLE_AFTER - $IDLE_BEFORE) / ($TOTAL_AFTER - $TOTAL_BEFORE)) * 100}")
        
        local MEM_TOTAL
        MEM_TOTAL=$(grep MemTotal /proc/meminfo | awk '{print $2}')
        local MEM_FREE
        MEM_FREE=$(grep MemFree /proc/meminfo | awk '{print $2}')
        local MEM_BUFFERS
        MEM_BUFFERS=$(grep Buffers /proc/meminfo | awk '{print $2}')
        local MEM_CACHED
        MEM_CACHED=$(grep "^Cached" /proc/meminfo | awk '{print $2}')
        local MEM_USED=$((MEM_TOTAL - MEM_FREE - MEM_BUFFERS - MEM_CACHED))
        local MEM_USAGE_PERC
        MEM_USAGE_PERC=$(awk "BEGIN {print ($MEM_USED / $MEM_TOTAL) * 100}")
        
        echo "{ \"cpu_load_percent\": $CPU_USAGE, \"mem_usage_percent\": $MEM_USAGE_PERC }"
        exit 0
    fi
        local cpu_usage
        cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

        local mem_usage
        mem_usage=$(free -m | awk 'NR==2{printf "%.2f", $3*100/$2}' )

        echo "$timestamp,$cpu_usage,$mem_usage,system,0,0" >> "$LOG_FILE"

        if [ "$RUNTIME" = "podman" ]; then
            podman stats --no-stream --format json 2>/dev/null | while IFS= read -r line; do
                if [ -n "$line" ] && [ "$line" != "[]" ]; then
                    local cname
                    cname=$(echo "$line" | jq -r '.name // .id' 2>/dev/null || echo "unknown")
                    local cpu
                    cpu=$(echo "$line" | jq -r '.cpu_percent // 0' 2>/dev/null || echo "0")
                    local mem
                    mem=$(echo "$line" | jq -r '.mem_percent // 0' 2>/dev/null || echo "0")
                    echo "$timestamp,$cpu_usage,$mem_usage,$cname,$cpu,$mem" >> "$LOG_FILE"
                fi
            done
        else
            kubectl top pods --no-headers 2>/dev/null | while IFS= read -r line; do
                if [ -n "$line" ]; then
                    local cname
                    cname=$(echo "$line" | awk '{print $1}')
                    local cpu_raw
                    cpu_raw=$(echo "$line" | awk '{print $2}')
                    local mem_raw
                    mem_raw=$(echo "$line" | awk '{print $3}')

                    local cpu
                    cpu=$(convert_cpu_to_percent "$cpu_raw")
                    local mem
                    mem=$(convert_mem_to_percent "$mem_raw")

                    echo "$timestamp,$cpu_usage,$mem_usage,$cname,$cpu,$mem" >> "$LOG_FILE"
                fi
            done
        fi

        count=$((count + 1))
        sleep "$INTERVAL"
    done

    log_info "Benchmark complete. Results saved in $OUTPUT_DIR"

    local avg_cpu
    avg_cpu=$(awk -F',' 'NR>1 {sum+=$2; count++} END {if (count > 0) print sum/count; else print 0}' "$LOG_FILE")
    local avg_mem
    avg_mem=$(awk -F',' 'NR>1 {sum+=$3; count++} END {if (count > 0) print sum/count; else print 0}' "$LOG_FILE")

    log_info "Summary:"
    log_info "  Average CPU: ${avg_cpu}%"
    log_info "  Average Memory: ${avg_mem}%"
    log_info "  Samples collected: $iterations"
}

show_usage() {
    echo "Usage: $0 [podman|k8s] [duration_minutes]"
    echo ""
    echo "Arguments:"
    echo "  podman            - Collect Podman metrics"
    echo "  k8s              - Collect Kubernetes metrics"
    echo "  duration_minutes - How long to collect metrics (default: 60)"
    echo ""
    echo "Environment Variables:"
    echo "  OUTPUT_DIR       - Output directory (default: /var/lib/deploy-system/evidence/benchmark)"
}

case "${1:-}" in
    -h|--help)
        show_usage
        exit 0
        ;;
    podman|k8s)
        main
        ;;
    *)
        log_error "Invalid runtime: $1"
        show_usage
        exit 1
        ;;
esac
