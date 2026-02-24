# GPU_DASHBOARDS

This guide covers GPU monitoring dashboards for Deploy-System-Unified.

## Overview

GPU monitoring is essential for workloads using NVIDIA, AMD, or Intel GPUs. This guide covers dashboard setup and metrics.

## GPU Discovery

Before setting up dashboards, discover your GPUs:

```bash
python3 roles/hardware/gpu/files/gpu_discovery.py --json
```

## NVIDIA GPU Monitoring

### nvidia-smi

```bash
# Basic stats
nvidia-smi

# Query specific metrics
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv

# Monitor continuously
nvidia-smi dmon -s um
```

### Prometheus Exporter

```bash
# Run node exporter with GPU metrics
docker run -d --runtime=nvidia --gpus all nvidia/node-exporter:latest --collector.textfile.directory=/prometheus
```

### Grafana Dashboard

Import NVIDIA GPU dashboard:
- Dashboard ID: `12214` (NVIDIA GPU Overview)
- Or create custom with queries:
```
nvidia_gpu_temperature_celsius
nvidia_gpu_utilization_percentage
nvidia_memory_used_bytes
nvidia_memory_total_bytes
```

## AMD GPU Monitoring

### rocm-smi

```bash
# Basic stats
rocm-smi

# Monitor continuously
rocm-smi dmon
```

### Prometheus Exporter

```bash
# AMD GPU exporter
docker run -d --device /dev/dri:/dev/dri amd/gpu_exporter
```

## Intel GPU Monitoring

### intel_gpu_top

```bash
# Real-time GPU usage
intel_gpu_top

# Check available engines
ls /sys/class/drm/
```

### Metrics Collection

```bash
# Query i915 metrics
cat /sys/class/drm/card0/gt_cur_freq_mhz
cat /sys/class/drm/card0/gt_boost_freq_mhz
```

## Custom Dashboard Panels

### GPU Utilization Panel

```
Metric: rate(gpu_utilization_seconds_total[5m])
Legend: {{gpu}},{{instance}}
```

### GPU Memory Panel

```
Metric: gpu_memory_used_bytes / gpu_memory_total_bytes * 100
Legend: {{gpu}} Memory %
Thresholds: 80% yellow, 90% red
```

### GPU Temperature Panel

```
Metric: gpu_temperature_celsius
Legend: {{gpu}},{{sensor}}
Thresholds: 70C yellow, 85C red
```

## Alert Rules

```yaml
groups:
  - name: gpu
    rules:
      - alert: HighGPUUtilization
        expr: gpu_utilization_percentage > 90
        for: 5m
        labels:
          severity: warning

      - alert: HighGPUMemory
        expr: gpu_memory_used_bytes / gpu_memory_total_bytes > 0.95
        for: 5m
        labels:
          severity: critical

      - alert: HighGPUTemperature
        expr: gpu_temperature_celsius > 85
        for: 5m
        labels:
          severity: critical
```

## Container GPU Monitoring

### Podman Stats

```bash
podman stats --no-stream --format "table {{.Name}}\t{{.CPU}}\t{{.MemUsage}}\t{{.GPUUtil}}\t{{.GPUTemperature}}"
```

### GPU Metrics in Containers

```bash
# NVIDIA container
docker run --gpus all nvidia/cuda:11.0 nvidia-smi

# Check GPU inside container
podman exec <container> nvidia-smi
```

## Related Documentation

- [GPU Stack Setup](GPU_STACK_SETUP.md)
- [GPU Slicing](GPU_SLICING.md)
- [Deployment Metrics](DEPLOYMENT_METRICS.md)
