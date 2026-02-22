# K8s vs Podman Scalability Benchmark Methodology

**Created:** February 13, 2026  
**Status:** In Progress  
**Task:** T4 - Scalability Benchmark

## Objective

Compare resource utilization and performance characteristics of running containerized workloads on Kubernetes (K3s) vs. Podman on identical hardware to provide data-driven guidance for the hybrid deployment strategy.

## Test Environment

### Hardware Profile
- **Target:** x86_64, aarch64, riscv64 (multi-arch support)
- **Memory:** Minimum 4GB RAM per node
- **Storage:** SSD-backed storage recommended
- **Network:** Standard Ethernet connectivity

### Software Versions
- **Kubernetes:** K3s v1.28+ (latest stable)
- **Container Runtime:** Podman 4.x
- **Benchmark Tools:** Custom metrics collection script

## Workload Specifications

### Test Container Images
| Service | Image | Resource Profile |
|---------|-------|------------------|
| Jellyfin | jellyfin/jellyfin | CPU: 2 cores, RAM: 4GB |
| Radarr | binhex/arch-radarr | CPU: 1 core, RAM: 512MB |
| Sonarr | binhex/arch-sonarr | CPU: 1 core, RAM: 512MB |
| Homarr | ajnart/homarr | CPU: 0.5 core, RAM: 256MB |
| Vaultwarden | vaultwarden/server | CPU: 1 core, RAM: 1GB |

## Metrics Collection

### Resource Metrics
1. **CPU Usage**
   - Idle vs. active utilization
   - Per-container breakdown
   - System overhead

2. **Memory Usage**
   - Working set size
   - Resident memory
   - Swap activity

3. **Storage I/O**
   - Read/write throughput
   - Latency

4. **Network**
   - Bandwidth consumption
   - Connection overhead

### Performance Metrics
1. **Startup Time**
   - Time to ready (first HTTP 200)
   - Cold start vs. warm start

2. **Scalability**
   - Pod/container spawn time
   - Concurrent workload handling

## Benchmark Methodology

### Phase 1: Baseline Measurements
1. Measure bare-metal resource availability
2. Record system metrics without containers

### Phase 2: Podman Deployment
1. Deploy all services as Podman Quadlets
2. Collect metrics over 24-hour period
3. Record startup times and resource spikes
4. Test concurrent access patterns

### Phase 3: K3s Deployment
1. Deploy K3s cluster (single-node for comparison)
2. Deploy all services via Helm charts
3. Collect identical metrics
4. Record startup times and resource spikes
5. Test concurrent access patterns

### Phase 4: Analysis
1. Compare resource overhead (K8s vs Podman)
2. Calculate cost-per-workload
3. Document operational complexity differences

## Expected Deliverables

1. `k8s_vs_podman_resource_usage.md` - Raw metrics data
2. `k8s_vs_podman_analysis.md` - Comparative analysis
3. `benchmark_metrics.sh` - Automated collection script

## Decision Criteria

- If K8s overhead > 30% of Podman for identical workload → favor Podman
- If operational complexity significantly higher for K8s → document tradeoffs
- If K8s provides meaningful benefits (scaling, HA) → recommend hybrid approach

## Notes

- Benchmark should be run on actual target hardware
- Multiple iterations required for statistical significance
- Include edge case testing (high load, network partition)
