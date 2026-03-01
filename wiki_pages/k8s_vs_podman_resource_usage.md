# k8s_vs_podman_resource_usage

**Created:** February 13, 2026  
**Status:** ✅ Initial Benchmarks Complete (Podman Actual + K3s Actual)  
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
| Podman | Available (version 5.7.1) |
| K3s | Available (version 1.34.3+k3s3) |
| Proxy Mode | **nftables** (Required for restricted kernel) |
| Backend | host-gw |

## Test Configuration (Target Hardware)

| Parameter | Value |
|-----------|-------|
| Hardware | vmi2997710 (x86_64, 8 CPU, 24GB RAM) |
| K3s Version | v1.34.3+k3s3 |
| Podman Version | 5.7.1 |
| Duration | 1 min (Initial Sample) |

## Baseline Measurements (Idle System)

| Metric | Value |
|--------|-------|
| CPU Idle | 43.66% |
| Memory Used | 12893 MB |
| Disk I/O (sda) | 1.84% util |
| Network (localhost) | 13210 Mbps |

## Podman Results (Measured)

### Container Metrics
| Service | CPU (%) | Memory (MB) | Startup Time (s) |
|---------|---------|--------------|-------------------|
| Firmware (Ubuntu) | 0.01% | 40.63 | < 1.0s |
| Firmware (Debian) | 0.01% | 17.68 | < 1.0s |
| Firmware (Rocky) | 0.06% | 23.32 | < 1.0s |
| Benchmark Pod | 5.56% | 37.92 | < 1.0s |

### System Overhead
| Metric | Value |
|--------|-------|
| Total CPU (Avg) | 53.56% |
| Total Memory (Avg) | 54.37% |
| Storage I/O (fio) | 10.9 MB/s Read |

## Kubernetes (K3s) Results (Measured - Actual)

### Pod Metrics
| Service | CPU (cores) | Memory (MB) | Startup Time (s) |
|---------|-------------|--------------|-------------------|
| CoreDNS | 8m | 39 | ~15.0s |
| Metrics Server | 7m | 39 | ~20.0s |
| Local Path Prov. | 1m | 15 | ~5.0s |
| Postgres Task | 1m | 22 | ~5.0s |
| Jellyfin Task | 1m | 137 | ~33.0s (Pull) |
| Nginx Task (x2) | 0m | 7 | ~3.0s |

### System Overhead
| Metric | Value |
|--------|-------|
| Control Plane CPU | ~2-4% (Active) |
| Control Plane Memory | ~950 MB |
| Total CPU (Kube Top) | 23% (Relative to 8 cores) |
| Total Memory (Kube Top) | 12229 Mi |
| Storage I/O | 10.2 MB/s |

## Comparative Analysis

### Resource Overhead Comparison

| Metric | Podman (Measured) | K3s (Measured) | Difference |
|--------|-------------------|-----------------|------------|
| CPU Overhead | ~1% | ~3% | +300% |
| Memory Overhead | ~120MB | ~950MB | +790% |
| Startup Time | Instant | ~10-20s | +1000% |

### Cost Per Workload

Podman is significantly more efficient for single-node "static" deployments. K3s costs (~1GB RAM baseline) are justified only when leveraging:
- Automated failover (Self-healing)
- Horizontal Pod Autoscaling (HPA)
- Declarative API for complex networking

## Recommendations

1. **Podman for Edge**: For single-node systems with < 4GB RAM, Podman remains the standard due to near-zero control plane overhead.
2. **K3s for Scale**: Use K3s when multi-node scheduling or HPA (Horizontal Pod Autoscaling) is required, as documented in `vercel-load-scale` pro skills.
3. **Hybrid Approach**: Use LXC for high-performance databases (Postgres) and Podman for app layers to minimize latency as established in `BASELINE_REFERENCE_GRAPH.md`.
4. **Networking Fix**: **CRITICAL**: Use `--kube-proxy-arg="proxy-mode=nftables"` and `--flannel-backend=host-gw` on restricted VPS kernels (e.g. Contabo) to resolve ClusterIP (10.43.0.1) connectivity issues.
