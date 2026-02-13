# GPU Orchestration Architecture

## Directory Structure
The GPU orchestration follows an architecture-based approach with vendor-specific subprofiles:

```
roles/hardware/gpu/
├── arch/
│   ├── x86_64/
│   │   ├── nvidia/
│   │   ├── amd/
│   │   ├── intel/
│   │   └── generic/
│   ├── aarch64/
│   │   └── ...
│   └── riscv64/
│       └── ...
├── files/
│   └── gpu_discovery.py  # Advanced discovery script
└── tasks/
    ├── detect_video.yml  # Invokes discovery
    └── validate_slicing.yml # Capability validation
```

## Discovery Facts
The `gpu_discovery.py` script emits JSON with:
- `detected_vendor_list`: List of vendors (nvidia, amd, intel, generic)
- `primary_detected_vendor`: Preferred vendor for single-GPU configs
- `gpu_count`: Number of detected controllers
- `is_multi_gpu`: Boolean
- `is_multi_vendor`: Boolean

## Slicing Strategies
- `passthrough`: Standard IOMMU/VFIO
- `sriov`: Single Root I/O Virtualization
- `mig`: NVIDIA Multi-Instance GPU
- `mps`: NVIDIA Multi-Process Service
- `vgpu`: NVIDIA Virtual GPU (requires license server)
