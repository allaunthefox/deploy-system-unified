# K8s vs Podman Resource Usage Benchmark

**Created:** February 13, 2026  
**Status:** Pending (Awaiting Benchmark Execution)  
**Task:** T4 - Scalability Benchmark

## TODO: Execute Benchmark and Fill Results

This document will contain the actual benchmark results after running `scripts/benchmark/benchmark_metrics.sh`.

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Hardware | TBD |
| K3s Version | TBD |
| Podman Version | TBD |
| Duration | TBD minutes |
| Date | TBD |

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
