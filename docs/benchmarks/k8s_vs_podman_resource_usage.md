# K8s vs Podman Resource Usage Benchmark

**Created:** February 13, 2026  
**Status:** Ready (Awaiting Target Hardware)  
**Task:** T4 - Scalability Benchmark

## Benchmark Ready

The benchmark infrastructure is ready. Execute on target hardware:

```bash
# Podman baseline (24h recommended)
./scripts/benchmark/benchmark_metrics.sh podman 1440

# K3s comparison
./scripts/benchmark/benchmark_metrics.sh k8s 1440
```

## Current Environment

| Parameter | Value |
|-----------|-------|
| Podman | Available (idle containers) |
| K3s | Not available in this environment |
| Benchmark Script | Ready |
| Methodology | Documented |

## Test Configuration (Target Hardware)

| Parameter | Value |
|-----------|-------|
| Hardware | Target x86_64/aarch64/riscv64 |
| K3s Version | v1.28+ |
| Podman Version | 4.x |
| Duration | 24h (1440 min) recommended |

## Baseline Measurements (No Containers)

| Metric | Value |
|--------|-------|
| CPU Idle | TBD |
| Memory Used | TBD |
| Disk I/O | TBD |
| Network | TBD |

## Podman Results

### Container Metrics
| Service | CPU (%) | Memory (MB) | Startup Time (s) |
|---------|---------|--------------|-------------------|
| Jellyfin | TBD | TBD | TBD |
| Radarr | TBD | TBD | TBD |
| Sonarr | TBD | TBD | TBD |
| Homarr | TBD | TBD | TBD |
| Vaultwarden | TBD | TBD | TBD |

### System Overhead
| Metric | Value |
|--------|-------|
| Total CPU | TBD |
| Total Memory | TBD |
| Storage I/O | TBD |

## Kubernetes (K3s) Results

### Pod Metrics
| Service | CPU (%) | Memory (MB) | Startup Time (s) |
|---------|---------|--------------|-------------------|
| Jellyfin | TBD | TBD | TBD |
| Radarr | TBD | TBD | TBD |
| Sonarr | TBD | TBD | TBD |
| Homarr | TBD | TBD | TBD |
| Vaultwarden | TBD | TBD | TBD |

### System Overhead
| Metric | Value |
|--------|-------|
| Control Plane CPU | TBD |
| Control Plane Memory | TBD |
| Total CPU | TBD |
| Total Memory | TBD |
| Storage I/O | TBD |

## Comparative Analysis

### Resource Overhead Comparison

| Metric | Podman | K8s | Difference |
|--------|--------|-----|------------|
| CPU Overhead | TBD | TBD | TBD% |
| Memory Overhead | TBD | TBD | TBD% |
| Startup Time | TBD | TBD | TBD% |

### Cost Per Workload

Calculate based on resource overhead.

## Recommendations

_To be filled after benchmark execution._
