# GPU_SLICING

## Overview

This document outlines the architecture for implementing GPU slicing capabilities in the deploy-system-unified project. The solution will support vendor-specific GPU slicing technologies for NVIDIA, AMD, and Intel GPUs.

## Architecture Goals

1. Vendor-agnostic GPU resource management
2. Support for multiple slicing technologies per vendor
3. Idempotent configuration management
4. Container runtime integration
5. State management and validation
6. Hybrid environment support (bare metal, virtualization, container orchestration)

## Slicing Technology Mapping

### NVIDIA

| Technology | GPU Models | Type | Key Features |
|------------|-----------|------|--------------|
| MIG (Multi-Instance GPU) | A100, A30, H100, H200, GH200 | Hardware | Fixed configurations, guaranteed QoS, hardware isolation |
| Time-Slicing | All CUDA-capable GPUs | Software | cgroups-based sharing, no QoS guarantees, flexible |
| vGPU (Virtual GPU) | Enterprise GPUs | Hypervisor | Virtualization-based, license required, cloud-focused |

### AMD

| Technology | GPU Models | Type | Key Features |
|------------|-----------|------|--------------|
| SR-IOV (MxGPU) | MI-series (MI50, MI100, MI210, MI250, MI300) | Hardware | Virtual Functions (VFs), 1:4 or 1:8 ratios, PCIe passthrough |
| ROCm Container | All ROCm-capable GPUs | Software | cgroups-based resource limiting, rocm-smi integration |

### Intel

| Technology | GPU Models | Type | Key Features |
|------------|-----------|------|--------------|
| SR-IOV | Data Center GPU Flex/Max series (see roles/containers/runtime/vars/intel_gpu_models.yml) | Hardware | Virtual Functions, PCIe passthrough |
| Level Zero API | Arc, Flex/Max, and Xe iGPUs (see roles/containers/runtime/vars/intel_gpu_models.yml) | Software | API-level partitioning, scheduler-based sharing |

## Architecture Components

### 1. GPU Discovery & Detection

```yaml
containers_gpu_discovery:
  method: "auto"  # auto, manual
  devices: []     # Manually specified GPU devices
  vendor_detection: "lspci"  # lspci, nvidia-smi, rocm-smi, intel-gpu-tools
```

### 2. Slicing Configuration

```yaml
containers_gpu_slicing:
  enabled: false
  strategy: "none"  # none, mig, time-slicing, sriov, vgpu, level-zero
  
  # MIG Configuration
  mig:
    enabled: false
    profiles: []  # e.g., ["1g.5gb", "2g.10gb"]
    gpu_instance_count: 1
    compute_instance_count: 1
  
  # Time-Slicing Configuration
  time_slicing:
    enabled: false
    max_instance_count: 8
    slice_duration: 100ms
    share_policy: "equal"  # equal, weighted
  
  # SR-IOV Configuration
  sriov:
    enabled: false
    vf_count: 4
    pf_device: ""
    vf_devices: []
  
  # vGPU Configuration
  vgpu:
    enabled: false
    profile: ""
    license_server: ""
  
  # Level Zero Configuration
  level_zero:
    enabled: false
    partitions: []
```

### 3. Container Runtime Integration

```yaml
containers_gpu_container_integration:
  runtime: "crun"  # crun, runc
  device_plugin: "nvidia"  # nvidia, amd, intel
  resource_limits:
    memory_gb: 8
    compute_units: 4
    gpu_instances: 1
```

### 4. State Management

```yaml
containers_gpu_state_management:
  apply_strategy: "auto"  # auto, force, skip
  reboot_required: false
  validation: true
  health_check: true
```

## Implementation Structure

### Roles Structure

```
roles/containers/runtime/
├── defaults/main.yml          # Default GPU slicing configuration
├── tasks/
│   ├── main.yml               # Main runtime task
│   ├── gpu_discovery.yml      # GPU discovery and detection
│   ├── gpu_slicing.yml        # Slicing configuration
│   ├── gpu_validation.yml     # Validation and health checks
│   └── gpu_containers.yml     # Container runtime integration
├── templates/
│   ├── mig_config.j2          # MIG profile configuration
│   ├── time_slicing_config.j2 # Time-slicing configuration
│   └── sriov_config.j2        # SR-IOV configuration
└── vars/
    ├── nvidia_gpu_models.yml  # NVIDIA GPU model profiles
    ├── amd_gpu_models.yml     # AMD GPU model profiles
    └── intel_gpu_models.yml   # Intel GPU model profiles
```

### Task Flow

1. **GPU Discovery**: Detect GPU devices and vendor information
2. **Slicing Strategy Selection**: Determine slicing method based on GPU model
3. **Configuration Application**: Apply slicing configuration
4. **Validation**: Verify configuration and detect errors
5. **Container Integration**: Configure runtime for sliced GPUs
6. **Health Monitoring**: Continuously monitor GPU health

## Supported GPU Models

### NVIDIA MIG-Capable GPUs

```yaml
nvidia_mig_gpus:
  - model: "A100"
    supported_profiles: ["1g.5gb", "2g.10gb", "3g.20gb", "4g.40gb", "7g.80gb"]
    max_instances: 7
  - model: "H100"
    supported_profiles: ["1g.10gb", "2g.20gb", "3g.40gb", "4g.80gb", "7g.160gb"]
    max_instances: 7
  - model: "A30"
    supported_profiles: ["1g.6gb", "2g.12gb", "4g.24gb"]
    max_instances: 4
```

## Error Handling & Recovery

### Common Error Scenarios

1. **GPU Mode Change**: Requires reboot or GPU reset
2. **Profile Mismatch**: GPU does not support requested profile
3. **Resource Conflict**: Configuration conflicts with existing state
4. **Validation Failure**: GPU not responding or configuration invalid

### Recovery Strategies

1. **Idempotent Reconfiguration**: Safe retry mechanisms
2. **Rollback Support**: Revert to previous configuration
3. **Health Checks**: Proactive monitoring and alerting

## Integration Points

### Container Runtime

- Podman Quadlet integration
- GPU device passthrough
- Resource limiting (cgroups v2)

### System Management

- Systemd service management
- Kernel module configuration
- Device node creation

## Performance Considerations

### MIG Performance

- Fixed memory allocation
- Guaranteed compute resources
- Low overhead

### Time-Slicing Performance

- Variable latency
- No resource guarantees
- High resource utilization

### SR-IOV Performance

- Low latency
- Direct PCIe access
- Limited context switching

## Security Considerations

### Device Isolation

- PCIe passthrough isolation
- Memory protection
- Compute resource isolation

### Container Security

- Rootless containers support
- SELinux/AppArmor profiles
- Capability bounding

## Future Enhancements

### Roadmap

1. **Kubernetes Integration**: GPU device plugin support
2. **Dynamic Slicing**: Runtime adjustment of GPU resources
3. **Multi-GPU Coordination**: Multi-GPU slicing strategies
4. **Performance Monitoring**: GPU metrics collection and analysis
5. **Automated Profile Selection**: ML-based profile recommendations

### Research Areas

- GPU sharing policies
- Workload-aware slicing
- Energy efficiency optimization
