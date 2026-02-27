#!/bin/sh
#===============================================================================
# benchmark_metrics.sh - Container Runtime Benchmark Metrics Collection
#===============================================================================
# Collects resource utilization metrics for Kubernetes vs Podman workloads
# Usage: ./benchmark_metrics.sh [podman|k8s] [duration_minutes]
#===============================================================================

set -eu

# Configuration
RUNTIME="${1:-podman}"
DURATION="${2:-60}"
OUTPUT_DIR="${OUTPUT_DIR:-/var/lib/deploy-system/evidence/benchmark}"
INTERVAL=5  # seconds between samples

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { printf "${GREEN}[INFO]${NC} %s\n" "$1"; }
log_warn() { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
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
# Convert K8s CPU millicores to percentage (assuming 1 core = 100%)
convert_cpu_to_percent() {
    cpu_value="$1"
    num_cores=$(nproc 2>/dev/null || echo "1")

    # If value ends in 'm', it's in millicores
    case "$cpu_value" in
        *m)
            millicores="${cpu_value%m}"
            echo "scale=2; $millicores / (100 * $num_cores)" | bc
            ;;
        *)
            # Assume cores, convert to percentage
            echo "scale=2; $cpu_value * 100 / $num_cores" | bc
            ;;
    esac
}

# Convert K8s memory (Mi/Gi) to percentage
convert_mem_to_percent() {
    mem_value="$1"
    total_mem=$(free -m | awk 'NR==2{print $2}')

    # Extract numeric value and unit using sed
    mem_num=$(echo "$mem_value" | sed 's/[^0-9.]//g')
    mem_unit=$(echo "$mem_value" | sed 's/[0-9.]//g')

    # Convert to Mi
    if [ "$mem_unit" = "Gi" ]; then
        mem_num=$(echo "scale=2; $mem_num * 1024" | bc)
    fi

    # Calculate percentage
    echo "scale=2; $mem_num * 100 / $total_mem" | bc
}

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Timestamp for output files
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$OUTPUT_DIR/${RUNTIME}_benchmark_${TIMESTAMP}.log"

log_info "Starting $RUNTIME benchmark for $DURATION minutes..."
log_info "Output directory: $OUTPUT_DIR"
log_info "Log file: $LOG_FILE"

# Check dependencies before starting
check_dependencies

#===============================================================================
# CPU Metrics Collection
#===============================================================================
collect_cpu() {
    timestamp=$(date +%s)

    if [ "$RUNTIME" = "podman" ]; then
        # Podman: use podman stats
        podman stats --no-stream --format json 2>/dev/null || echo "[]"
    else
        # K8s: use kubectl top
        kubectl top pods --no-headers 2>/dev/null || echo ""
    fi

    # System CPU
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}'
}

#===============================================================================
# Memory Metrics Collection
#===============================================================================
collect_memory() {
    if [ "$RUNTIME" = "podman" ]; then
        podman stats --no-stream --format json 2>/dev/null || echo "[]"
    else
        kubectl top pods --no-headers 2>/dev/null || echo ""
    fi

    # System memory
    free -m | awk 'NR==2{printf "%.2f", $3*100/$2}'
}

#===============================================================================
# Disk I/O Metrics
#===============================================================================
collect_disk() {
    iostat -dx 1 1 2>/dev/null | tail -n +4 | awk '{print $1,$4,$5}' || echo ""
}

#===============================================================================
# Network Metrics
#===============================================================================
collect_network() {
    cat /proc/net/dev | grep -v "lo:" | awk '{print $1,$2,$10}' || echo ""
}

#===============================================================================
# Startup Time Measurement
#===============================================================================
measure_startup() {
    container="$1"
    start_time=$(date +%s%N)

    if [ "$RUNTIME" = "podman" ]; then
        podman start "$container" >/dev/null 2>&1
    else
        kubectl rollout status deployment/"$container" --timeout=300s >/dev/null 2>&1
    fi

    end_time=$(date +%s%N)
    echo "scale=3; ($end_time - $start_time) / 1000000000" | bc
}

#===============================================================================
# Main Collection Loop
#===============================================================================
main() {
    iterations=$((DURATION * 60 / INTERVAL))
    count=0

    echo "timestamp,cpu_percent,mem_percent,container,cpu_usage,mem_usage" > "$LOG_FILE"

    while [ $count -lt "$iterations" ]; do
        timestamp=$(date +%Y-%m-%dT%H:%M:%S)

        # Collect system metrics
        cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

        mem_usage=$(free -m | awk 'NR==2{printf "%.2f", $3*100/$2}')

        echo "$timestamp,$cpu_usage,$mem_usage,system,0,0" >> "$LOG_FILE"

        # Collect container metrics
        if [ "$RUNTIME" = "podman" ]; then
            podman stats --no-stream --format json 2>/dev/null | while IFS= read -r line; do
                if [ -n "$line" ] && [ "$line" != "[]" ]; then
                    cname=$(echo "$line" | jq -r '.name // .id' 2>/dev/null || echo "unknown")
                    cpu=$(echo "$line" | jq -r '.cpu_percent // 0' 2>/dev/null || echo "0")
                    mem=$(echo "$line" | jq -r '.mem_percent // 0' 2>/dev/null || echo "0")
                    echo "$timestamp,$cpu_usage,$mem_usage,$cname,$cpu,$mem" >> "$LOG_FILE"
                fi
            done
        else
            kubectl top pods --no-headers 2>/dev/null | while IFS= read -r line; do
                if [ -n "$line" ]; then
                    cname=$(echo "$line" | awk '{print $1}')
                    cpu_raw=$(echo "$line" | awk '{print $2}')
                    mem_raw=$(echo "$line" | awk '{print $3}')

                    # Convert K8s units to percentages for consistency with Podman
                    cpu=$(convert_cpu_to_percent "$cpu_raw")
                    mem=$(convert_mem_to_percent "$mem_raw")

                    echo "$timestamp,$cpu_usage,$mem_usage,$cname,$cpu,$mem" >> "$LOG_FILE"
                fi
            done
        fi

        count=$((count + 1))
        sleep "$INTERVAL"
    done

    log_info "Benchmark complete. Results saved to: $LOG_FILE"

    # Generate summary
    avg_cpu=$(awk -F',' 'NR>1 {sum+=$2; count++} END {print sum/count}' "$LOG_FILE")
    avg_mem=$(awk -F',' 'NR>1 {sum+=$3; count++} END {print sum/count}' "$LOG_FILE")

    log_info "Summary:"
    log_info "  Average CPU: ${avg_cpu}%"
    log_info "  Average Memory: ${avg_mem}%"
    log_info "  Samples collected: $iterations"
}

#===============================================================================
# CLI Arguments
#===============================================================================
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
    echo ""
    echo "Example:"
    echo "  OUTPUT_DIR=/tmp/bench $0 podman 30"
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
