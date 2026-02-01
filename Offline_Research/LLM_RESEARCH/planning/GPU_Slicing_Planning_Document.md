# GPU Slicing for Deploy-System-Unified - Comprehensive Planning Document

## 1. Project Overview

### 1.1. Background
The Deploy-System-Unified project is a comprehensive infrastructure deployment and configuration tool built on Ansible. It follows a layered architecture philosophy with strict security guidelines. The goal of this document is to plan the implementation of GPU slicing support for the project.

### 1.2. Objectives
- Implement GPU slicing support for NVIDIA, AMD, and Intel GPUs
- Support multiple container runtimes: Podman, Kubernetes, and LXC
- Handle different virtualization scenarios: bare metal, virtual hosts, and virtual guests
- Follow the project's security-first and "assume nothing" philosophy
- Provide modular, idempotent GPU configuration management

## 2. Current GPU Implementation Status

### 2.1. Existing GPU Support
- Located in `/roles/containers/runtime/`
- Provides basic GPU passthrough for NVIDIA, AMD, and Intel GPUs
- Uses quadlet configuration for Podman containers
- Supports NVIDIA device plugin for Kubernetes (not yet implemented)

### 2.2. Virtualization Detection
- The project detects virtualization type using `core/bootstrap` role
- Variables available:
  - `virt_type`: Type of virtualization (kvm, docker, lxc, etc.)
  - `is_virtualized`: Boolean indicating if running in virtual environment
  - `ansible_virtualization_role`: "host" or "guest"

## 3. GPU Slicing Technologies

### 3.1. NVIDIA GPU Slicing
1. **MIG (Multi-Instance GPU)**: Hardware partitioning for A100/A30/H100 GPUs
2. **vGPU (Virtual GPU)**: Virtualization-based slicing for NVIDIA GRID
3. **Time-Slicing**: Software-based sharing for all CUDA-capable GPUs

### 3.2. AMD GPU Slicing
1. **MxGPU (SR-IOV)**: PCIe passthrough virtualization for AMD GPUs
2. **ROCm Slicing**: Software-based resource partitioning using ROCm

### 3.3. Intel GPU Slicing
1. **SR-IOV**: Virtual function passthrough for Intel GPUs
2. **Level Zero API**: OneAPI-based software partitioning
3. **Intel OneAPI**: Comprehensive toolkit for cross-architecture development

#### Intel OneAPI Details:
- **Unified Programming Model**: Single codebase for CPU, GPU, and other accelerators
- **DPC++ (Data Parallel C++)**: Extended C++ for parallel programming
- **OneAPI Toolkit Components**:
  - Base Toolkit: Core libraries and compilers
  - HPC Toolkit: High-performance computing libraries
  - AI Analytics Toolkit: Machine learning and data analytics
  - Rendering Toolkit: 3D rendering and visualization
- **GPU Acceleration**: Direct access to Intel GPU resources through Level Zero API
- **Container Support**: Pre-built containers with OneAPI tools and libraries

## 4. Runtime Support

### 4.1. Podman (Quadlet)
- Container runtime configuration in `/etc/containers/containers.conf`
- GPU device passthrough via device cgroups and capabilities
- Resource limits using cgroups v2

### 4.2. Kubernetes
- GPU device plugins for each vendor
- Node labeling for GPU selection
- Resource requests and limits in pod specifications

### 4.3. LXC/LXD
- Container configuration via `/var/lib/lxc/<container>/config`
- GPU passthrough using lxc.cgroup2.devices.allow
- Resource limits using lxc.cgroup2.memory and lxc.cgroup2.cpu

## 5. Virtualization Scenarios

### 5.1. Bare Metal (Host)
- Full GPU management capabilities
- Support for hardware slicing technologies (MIG, SR-IOV)
- Maximum performance and isolation

### 5.2. Virtual Host (KVM/QEMU)
- GPU sharing among virtual machines
- Support for vGPU and SR-IOV
- Host-level GPU resource management

### 5.3. Virtual Guest (VM)
- GPU passthrough from host to VM
- Guest OS GPU driver installation
- Container runtime GPU access within VM

## 6. Implementation Plan with Completion Metrics

### 6.1. Phase 1: Foundation (1 week, 100% completion = 3 tasks)
```
- [ ] Enhance virtualization detection with GPU-specific info (33% complete)
  - Completion metric: `ansible_facts.gpu_virtualization_support` variable exists with correct values
  - Completion metric: Virtualization type detection accuracy > 95%
- [ ] Add virtualization-aware GPU slicing configuration variables (67% complete)
  - Completion metric: All variables defined in `defaults/main.yml` with safe defaults
  - Completion metric: Configuration schema validated against existing project standards
- [ ] Implement GPU discovery and detection logic (100% complete)
  - Completion metric: GPU vendor, model, and capabilities detected correctly in 3/3 test scenarios
  - Completion metric: GPU discovery task runs in < 30 seconds
```

### 6.2. Phase 2: Vendor-Specific Implementations (2 weeks, 100% completion = 9 tasks)
```
- [ ] Create NVIDIA MIG support (bare metal only) (11.1% complete)
  - Completion metric: MIG profiles created and managed correctly
  - Completion metric: MIG devices detected in container runtime
- [ ] Create NVIDIA vGPU support (guest only, requires license) (22.2% complete)
  - Completion metric: vGPU device passthrough configured for VM
  - Completion metric: Container runtime accesses vGPU resources
- [ ] Create NVIDIA time-slicing support (both environments) (33.3% complete)
  - Completion metric: Time-slicing configuration applied correctly
  - Completion metric: GPU resource limits enforced per container
- [ ] Create AMD SR-IOV support (bare metal and host) (44.4% complete)
  - Completion metric: Virtual functions created and managed
  - Completion metric: SR-IOV devices passed to containers
- [ ] Create AMD passthrough support (guest) (55.5% complete)
  - Completion metric: AMD GPU passthrough configured for VM
  - Completion metric: Container runtime accesses AMD GPU
- [ ] Create Intel SR-IOV support (bare metal and host) (66.6% complete)
  - Completion metric: Intel GPU virtual functions created
  - Completion metric: SR-IOV devices available in containers
- [ ] Create Intel Level Zero support (bare metal) (77.7% complete)
  - Completion metric: Level Zero partitions configured
  - Completion metric: Container applications use Level Zero API
- [ ] Create Intel OneAPI support (both environments) (88.8% complete)
  - Completion metric: OneAPI toolkit installed and configured
  - Completion metric: Container applications use OneAPI libraries and tools
- [ ] Create Intel passthrough support (guest) (100% complete)
  - Completion metric: Intel GPU passthrough configured for VM
  - Completion metric: Container runtime accesses Intel GPU
```

### 6.3. Phase 3: Runtime Integration (1 week, 100% completion = 9 tasks)
```
- [ ] Update container runtime for virtualization-aware GPU access (11% complete)
  - Completion metric: Runtime detects virtualization context correctly
  - Completion metric: GPU access configured appropriately for each virtualization type
- [ ] Enhance quadlet support for different GPU types (22% complete)
  - Completion metric: Quadlet configurations generated for 3/3 GPU vendors
  - Completion metric: Containers run successfully with quadlet GPU configs
- [ ] Add virtualization-specific device cgroup configurations (33% complete)
  - Completion metric: Cgroup2 device permissions set correctly per virtualization type
  - Completion metric: GPU devices properly isolated
- [ ] Add Kubernetes GPU device plugin support (44% complete)
  - Completion metric: Device plugins installed as daemonsets
  - Completion metric: Kubernetes recognizes GPU resources
- [ ] Create Kubernetes GPU resource limits and node labels (55% complete)
  - Completion metric: Node labels applied with GPU capabilities
  - Completion metric: Pod resource requests and limits honored
- [ ] Add LXC-aware GPU slicing configuration variables (66% complete)
  - Completion metric: LXC-specific GPU config variables defined
  - Completion metric: Variables integrate with existing LXC role
- [ ] Create LXC GPU passthrough support (77% complete)
  - Completion metric: LXC container config includes GPU device allow rules
  - Completion metric: Container can access GPU devices
- [ ] Create LXC GPU resource limit configuration (88% complete)
  - Completion metric: Cgroup2 resource limits applied to LXC containers
  - Completion metric: GPU memory and compute limits enforced
- [ ] Create LXC GPU container examples (100% complete)
  - Completion metric: Example LXC configs available for 3/3 GPU vendors
  - Completion metric: Examples tested and working
```

### 6.4. Phase 4: Deployment Templates (1 week, 100% completion = 5 tasks)
```
- [ ] Create GPU slicing templates for virtualization hosts (20% complete)
  - Completion metric: Template includes host GPU management configuration
  - Completion metric: Template validated in virtualization host test scenario
- [ ] Create GPU slicing templates for virtualization guests (40% complete)
  - Completion metric: Template includes guest GPU passthrough configuration
  - Completion metric: Template validated in virtual guest test scenario
- [ ] Create GPU slicing templates for Kubernetes nodes (60% complete)
  - Completion metric: Template includes Kubernetes GPU device plugin support
  - Completion metric: Template tested in Kubernetes cluster
- [ ] Create GPU slicing templates for LXC containers (80% complete)
  - Completion metric: Template includes LXC GPU configuration
  - Completion metric: Template validated with LXC container test
- [ ] Create GPU workstation templates for both scenarios (100% complete)
  - Completion metric: Templates for both virtualized and bare metal GPU workstations
  - Completion metric: Templates include common GPU workload configurations
```

### 6.5. Phase 5: Validation & Testing (1 week, 100% completion = 12 tasks)
```
- [ ] Create Molecule tests for GPU slicing scenarios (8% complete)
  - Completion metric: Molecule scenarios defined for each slicing technology
  - Completion metric: Tests run successfully in CI pipeline
- [ ] Add preflight checks for GPU slicing prerequisites (17% complete)
  - Completion metric: Preflight checks cover 90% of failure scenarios
  - Completion metric: Checks provide clear error messages
- [ ] Implement GPU health and validation checks (25% complete)
  - Completion metric: Health checks for 3/3 GPU vendors
  - Completion metric: Checks detect GPU issues before they impact workloads
- [ ] Create integration tests for container GPU access (33% complete)
  - Completion metric: Tests verify container GPU access for 3/3 runtimes
  - Completion metric: Tests run in < 5 minutes per scenario
- [ ] Test Kubernetes GPU device plugin installation (42% complete)
  - Completion metric: Device plugin installation test passes
  - Completion metric: Plugin status checked and validated
- [ ] Test Kubernetes node GPU labeling (50% complete)
  - Completion metric: Node labels applied correctly
  - Completion metric: Label values match detected GPU capabilities
- [ ] Test Kubernetes pod GPU resource allocation (58% complete)
  - Completion metric: Pod resource requests honored
  - Completion metric: GPU resources correctly isolated between pods
- [ ] Test Podman container GPU access (67% complete)
  - Completion metric: Podman containers run with GPU access
  - Completion metric: GPU resources allocated as requested
- [ ] Test quadlet GPU configuration (75% complete)
  - Completion metric: Quadlet GPU configs generate correctly
  - Completion metric: Containers started from quadlets have GPU access
- [ ] Test LXC container GPU access (83% complete)
  - Completion metric: LXC containers configured with GPU devices
  - Completion metric: Container applications use GPU resources
- [ ] Test GPU slicing with multi-node Kubernetes clusters (92% complete)
  - Completion metric: Multi-node GPU resource allocation test passes
  - Completion metric: Pods scheduled to nodes with available GPU resources
- [ ] Documentation and examples (100% complete)
  - Completion metric: All slicing technologies documented
  - Completion metric: Examples provided for common use cases
  - Completion metric: Documentation follows project style guidelines
```

## 7. Configuration Variables

### 7.1. Main Configuration
```yaml
containers_gpu_slicing:
  strategy: "auto"  # auto, mig, vgpu, time-slicing, sriov, level-zero, oneapi, passthrough
  auto_strategy:
    bare_metal: "mig"
    virtual_host: "sriov"
    virtual_guest: "passthrough"
  
  # Strategy-specific configurations
  mig: { enabled: false }
  vgpu: { enabled: false, profile: "", license_server: "" }
  time_slicing: { enabled: false, max_instances: 4 }
  sriov: { enabled: false, vf_count: 4 }
  level_zero: { enabled: false, partitions: [] }
  oneapi: { enabled: false, toolkit: "base", components: ["compiler", "mpi", "tbb"] }
  passthrough: { devices: [] }
```

### 7.2. Runtime-Specific Configuration
```yaml
# Kubernetes
containers_gpu_slicing.kubernetes:
  enabled: true
  device_plugins:
    - name: "nvidia-device-plugin"
      version: "v0.13.0"
      image: "nvcr.io/nvidia/k8s-device-plugin:v0.13.0"
  node_labels:
    - "nvidia.com/gpu.count={{ containers_gpu_count }}"

# Podman
containers_gpu_slicing.podman:
  enabled: true
  quadlet:
    capabilities: ["CAP_SYS_ADMIN"]
    device_cgroups: ["/dev/nvidia*", "/dev/dri"]
    mounts: ["/usr/bin/nvidia-smi:/usr/bin/nvidia-smi:ro"]

# LXC
containers_gpu_slicing.lxc:
  enabled: true
  config:
    cgroup2:
      devices:
        allow: ["/dev/nvidia*", "/dev/dri"]
      memory: "8Gi"
      cpu: "4"
```

## 8. Preflight Validation

### 8.1. General Preflight Checks
```yaml
- name: Validate GPU hardware support
  ansible.builtin.assert:
    that:
      - ansible_facts.nvidia_gpus | default([]) | length > 0
      - containers_gpu_slicing.strategy in ["auto", "mig", "vgpu", "time-slicing", "sriov", "level-zero", "oneapi", "passthrough"]
    fail_msg: "GPU hardware or strategy not supported"
```

### 8.2. Virtualization-Aware Checks
```yaml
- name: Validate NVIDIA vGPU license (virtual guest)
  ansible.builtin.assert:
    that:
      - containers_gpu_slicing.vgpu.license_server | length > 0
    fail_msg: "NVIDIA vGPU requires license server configuration"
  when: 
    - is_virtualized
    - containers_gpu_vendor == "nvidia"
    - containers_gpu_slicing.strategy == "vgpu"

- name: Validate SR-IOV support (bare metal)
  ansible.builtin.assert:
    that:
      - containers_gpu_slicing.sriov.pf_device | length > 0
    fail_msg: "SR-IOV requires physical device configuration"
  when:
    - not is_virtualized
    - containers_gpu_slicing.strategy == "sriov"

- name: Validate Intel OneAPI support
  ansible.builtin.assert:
    that:
      - containers_gpu_vendor == "intel"
    fail_msg: "Intel OneAPI requires an Intel GPU"
  when:
    - containers_gpu_slicing.strategy == "oneapi"
```

## 9. Testing and Validation

### 9.1. Molecule Test Scenarios
```
- default: Basic GPU passthrough and device plugin installation
- kubernetes: Kubernetes node with GPU device plugin support
- podman: Podman quadlet GPU configuration
- lxc: LXC container GPU passthrough
- virtualization: Virtual machine GPU passthrough
- multi_node: Multi-node Kubernetes GPU resource allocation
- intel_oneapi: Intel GPU with OneAPI toolkit support
```

### 9.2. Health Checks
```yaml
- name: Check NVIDIA device plugin status
  ansible.builtin.command: kubectl get daemonsets -n kube-system nvidia-device-plugin-daemonset
  register: nvidia_plugin_status
  changed_when: false

- name: Verify GPU devices in container
  ansible.builtin.command: podman exec {{ container_name }} nvidia-smi
  register: nvidia_smi_output
  changed_when: false

- name: Verify Intel OneAPI installation
  ansible.builtin.command: podman exec {{ container_name }} oneapi_version
  register: oneapi_version_output
  changed_when: false
  when:
    - containers_gpu_vendor == "intel"
    - containers_gpu_slicing.strategy == "oneapi"
```

## 10. Project Style Compliance

### 10.1. Style Guide Adherence
- All YAML follows 2-space indentation, lowercase booleans
- FQCN module usage (ansible.builtin.copy instead of copy)
- Comprehensive error handling with block/rescue/always
- Proper variable prefixing (containers_gpu_slicing_*)
- Safe defaults for all variables

### 10.2. Architecture Philosophy
- **Layered Approach**: GPU slicing is a container runtime extension
- **Modular Design**: Each slicing technology implemented as separate task files
- **No Role Comingling**: GPU functionality remains within containers/runtime role
- **Security First**: Default configurations are restrictive with explicit enable flags

## 11. Branch Templates

### 11.1. Existing Templates to Update
1. `gpu_workstations.yml` - Add GPU slicing examples

### 11.2. New Branch Templates
1. `k8s_gpu_node.yml` - Kubernetes node with GPU device plugin support
2. `k8s_gpu_worker.yml` - Kubernetes worker node with GPU slicing
3. `k8s_gpu_workload.yml` - Kubernetes workload with GPU resource requests
4. `lxc_gpu_container.yml` - LXC container with GPU passthrough
5. `gpu_slicing_bare_metal.yml` - Full GPU management for physical hosts
6. `gpu_slicing_virtual_host.yml` - GPU sharing for virtualization hosts
7. `gpu_slicing_virtual_guest.yml` - GPU passthrough for virtual machines

## 12. Files to Modify

### 12.1. Existing Files
1. `/roles/containers/runtime/defaults/main.yml` - Add slicing configuration variables
2. `/roles/containers/runtime/tasks/main.yml` - Integrate GPU slicing tasks
3. `/roles/containers/quadlets/defaults/main.yml` - Add quadlet slicing support
4. `/roles/containers/quadlets/tasks/main.yml` - Update quadlet creation with slicing
5. `/branch_templates/gpu_workstations.yml` - Add GPU slicing examples
6. `/branch_templates/README.md` - Document new slicing capabilities

### 12.2. New Files to Create
1. `/roles/containers/runtime/tasks/gpu_discovery.yml` - GPU detection logic
2. `/roles/containers/runtime/tasks/gpu_slicing.yml` - Slicing configuration
3. `/roles/containers/runtime/tasks/gpu_validation.yml` - Validation and health checks
4. `/roles/containers/runtime/templates/mig_config.j2` - MIG profile configuration
5. `/roles/containers/runtime/templates/time_slicing_config.j2` - Time-slicing configuration
6. `/roles/containers/runtime/templates/sriov_config.j2` - SR-IOV configuration
7. `/roles/containers/runtime/vars/nvidia_gpu_models.yml` - NVIDIA GPU model profiles
8. `/roles/containers/runtime/vars/amd_gpu_models.yml` - AMD GPU model profiles
9. `/roles/containers/runtime/vars/intel_gpu_models.yml` - Intel GPU model profiles
10. `/roles/orchestration/k8s_node/tasks/gpu.yml` - Kubernetes GPU device plugin deployment
11. `/roles/orchestration/k8s_node/defaults/gpu.yml` - Kubernetes GPU configuration variables
12. `/roles/orchestration/k8s_node/templates/nvidia-device-plugin.yml.j2` - NVIDIA device plugin manifest
13. `/roles/orchestration/k8s_node/templates/amd-device-plugin.yml.j2` - AMD device plugin manifest
14. `/roles/orchestration/k8s_node/templates/intel-gpu-plugin.yml.j2` - Intel GPU device plugin manifest
15. `/roles/containers/lxc/defaults/main.yml` - LXC GPU configuration variables
16. `/roles/containers/lxc/tasks/main.yml` - LXC GPU configuration tasks
17. `/roles/containers/lxc/templates/lxc-gpu-config.j2` - LXC GPU configuration template

## 13. Timeline and Resources

### 13.1. Estimated Timeline
- **Phase 1**: 1 week - Foundation and basic GPU discovery
- **Phase 2**: 2 weeks - Vendor-specific implementations
- **Phase 3**: 1 week - Runtime integration
- **Phase 4**: 1 week - Deployment templates
- **Phase 5**: 1 week - Testing and validation

### 13.2. Required Resources
- NVIDIA GPU (A100/A30/H100) for MIG testing
- AMD GPU (MI-series) for SR-IOV testing
- Intel GPU (Data Center GPU) for Level Zero and OneAPI testing
- Kubernetes cluster for device plugin testing
- LXC installation for container testing
- Virtualization environment (KVM/QEMU) for vGPU testing
- Intel OneAPI Toolkit installation for development and testing

## 14. Risks and Mitigation

### 14.1. Hardware Availability
- **Risk**: Limited access to high-end GPUs for testing
- **Mitigation**: Use cloud instances with GPU capabilities, mock devices for basic testing

### 14.2. Virtualization Compatibility
- **Risk**: GPU passthrough may not work in some virtualization environments
- **Mitigation**: Validate hardware virtualization support, use nested virtualization for testing

### 14.3. Driver Compatibility
- **Risk**: GPU driver versions may conflict with container runtimes
- **Mitigation**: Pin driver versions, test combinations in Molecule

### 14.4. Complexity Management
- **Risk**: Project complexity may increase significantly
- **Mitigation**: Keep GPU slicing modular, use clear error handling, document thoroughly

## 15. Success Criteria

1. **GPU Detection**: System correctly identifies GPU vendor, model, and capabilities
2. **Configuration**: GPU slicing parameters are correctly applied to container runtimes
3. **Performance**: Containerized applications can access and utilize GPU resources
4. **Isolation**: GPU slices are properly isolated with resource limits enforced
5. **Validation**: Preflight checks and health checks detect issues early
6. **Idempotency**: Configurations can be applied multiple times without adverse effects
7. **Documentation**: Comprehensive documentation exists for all slicing technologies and scenarios

## 16. OS Settings Integration

### 16.1. System Configuration Requirements

GPU slicing requires specific OS-level configurations to function properly. These settings will be managed through the existing core role structure:

#### 16.1.1. Kernel Modules
```yaml
# NVIDIA GPU support
- name: Load NVIDIA kernel modules
  community.general.modprobe:
    name: "{{ item }}"
    state: present
  loop:
    - nvidia
    - nvidia_uvm
    - nvidia_modeset
  when: containers_gpu_vendor == "nvidia"

# AMD GPU support
- name: Load AMD kernel modules
  community.general.modprobe:
    name: "{{ item }}"
    state: present
  loop:
    - amdgpu
    - amdkfd
  when: containers_gpu_vendor == "amd"

# Intel GPU support
- name: Load Intel kernel modules
  community.general.modprobe:
    name: "{{ item }}"
    state: present
  loop:
    - i915
    - xe
  when: containers_gpu_vendor == "intel"
```

#### 16.1.2. System Limits
```yaml
- name: Increase file descriptor limits for GPU workloads
  ansible.builtin.lineinfile:
    path: /etc/security/limits.conf
    line: "{{ item }}"
    create: true
  loop:
    - "* soft nofile 65536"
    - "* hard nofile 65536"
    - "root soft nofile 65536"
    - "root hard nofile 65536"

- name: Increase process limits for GPU workloads
  ansible.builtin.lineinfile:
    path: /etc/security/limits.conf
    line: "{{ item }}"
    create: true
  loop:
    - "* soft nproc 65536"
    - "* hard nproc 65536"
    - "root soft nproc 65536"
    - "root hard nproc 65536"
```

#### 16.1.3. Huge Pages (for Intel GPU)
```yaml
- name: Configure huge pages for Intel GPU
  ansible.builtin.lineinfile:
    path: /etc/default/grub
    regexp: '^GRUB_CMDLINE_LINUX_DEFAULT='
    line: 'GRUB_CMDLINE_LINUX_DEFAULT="default_hugepagesz=2M hugepagesz=2M hugepages=1024"'
  when: containers_gpu_vendor == "intel"

- name: Update GRUB configuration
  ansible.builtin.command: update-grub
  when: containers_gpu_vendor == "intel"
```

### 16.2. Role Integration

#### 16.2.1. Core Role Updates
- `/roles/core/hardware_support/`: Add GPU-specific hardware detection and configuration
- `/roles/core/kernel/`: Add kernel module management for GPU vendors
- `/roles/core/systemd/`: Add systemd service management for GPU daemons

#### 16.2.2. New Core Role Files
```
/roles/core/hardware_support/tasks/gpu_detection.yml
/roles/core/hardware_support/vars/gpu_vendors.yml
/roles/core/kernel/tasks/gpu_modules.yml
/roles/core/systemd/tasks/gpu_services.yml
```

### 16.3. Configuration Variables

#### 16.3.1. Core Role Variables
```yaml
# /roles/core/defaults/main.yml
core_gpu_support_enabled: true
core_gpu_vendor_detection: true
core_gpu_kernel_modules: []
core_gpu_huge_pages: false
core_gpu_huge_pages_size: "2M"
core_gpu_huge_pages_count: 1024
```

#### 16.3.2. GPU-Specific Variables
```yaml
# /roles/core/hardware_support/vars/gpu_vendors.yml
nvidia_gpu_modules:
  - nvidia
  - nvidia_uvm
  - nvidia_modeset

amd_gpu_modules:
  - amdgpu
  - amdkfd

intel_gpu_modules:
  - i915
  - xe
```

### 16.4. Preflight Checks
```yaml
- name: Check kernel module support
  ansible.builtin.command: modinfo {{ item }}
  register: module_info
  changed_when: false
  failed_when: false
  loop: "{{ core_gpu_kernel_modules }}"

- name: Verify kernel module loading
  ansible.builtin.command: lsmod | grep {{ item }}
  register: module_loaded
  changed_when: false
  failed_when: false
  loop: "{{ core_gpu_kernel_modules }}"
```

## 17. Conclusion

This planning document outlines a comprehensive approach to implementing GPU slicing support for the Deploy-System-Unified project. The implementation will follow the project's strict architectural guidelines, focusing on security, modularity, and idempotency. By supporting multiple GPU vendors, container runtimes, and virtualization scenarios, this solution will provide a flexible and robust GPU resource management system for various use cases.

The OS settings integration ensures that all necessary system configurations are properly managed through the existing core role structure, maintaining consistency and adhering to the project's architectural constraints.
