# Contabo Cloud VPS Environment Analysis (vmi2997710)
## Instance Details

**Instance Name**: BigBoi
**Host System**: 25135
**Region**: EU
**IP Address**: 38.242.222.130
**MAC Address**: 00:50:56:5f:4d:ba
**IPv6 Address**: 2a02:c207:2299:7710::1/64
**Creation Date**: Dec 30, 2025
## Hardware Specifications

| Resource | Specification |
|----------|----------------|
| **CPU** | AMD EPYC Processor (8 cores, 8 threads) |
| **Memory** | 24 GB (23 GiB available) |
| **Swap** | 12 GB |
| **Storage** | 800 GB SSD |
| **Current Usage** | 23 GB used, 775 GB available |
| **Architecture** | x86_64 (64-bit) |
| **Virtualization** | Proxmox/KVM (full virtualization) |
## Proxmox Virtualization Details

- **Hypervisor Vendor**: KVM (Kernel-based Virtual Machine)
- **Hypervisor Type**: Full virtualization (not paravirtualized)
- **Host System**: 25135 (Proxmox host identifier)
- **CPU Flags**: Supports advanced features (AVX2, AES-NI, SHA)
- **Network**: Virtual network interface (VMXNET3 or virtio-net)
## Network Configuration

**Interface**: eth0 (QEMU virtual interface)
- **IPv4**: 38.242.222.130/20
- **IPv6**: 2a02:c207:2299:7710::1/64
- **MAC Address**: 00:50:56:5f:4d:ba
- **Current MTU**: 1500 (not optimized for Contabo's tunnel environment)
- **Network Vendor**: QEMU virtual bridge
## Current System State

**OS**: Arch Linux
**Kernel**: Linux 6.18.5-arch1-1
**Hostname**: vmi2997710.contaboserver.net
**Boot Mode**: systemd (PID 1)
## Contabo-Specific Optimizations in Project

### Network Optimization Required
The current MTU is set to 1500, but Contabo's virtual bridge environment recommends MTU 1450 to avoid fragmentation in tunnel networks.

### TCP Forwarding
The project's `vps_hardened.yml` template enables TCP forwarding:
```yaml
vars:
    # Allow TCP forwarding for VPS environments (required for Contabo)
    sshd_allow_tcp_forwarding: true
```

### Existing Contabo Role
The `roles/core/vps_optimization/tasks/providers/contabo.yml` includes:
1. **Reverse Path Filtering**: Enables strict RP filtering (net.ipv4.conf.all.rp_filter = 1)
2. **MTU Optimization**: Sets MTU to 1450 bytes for the primary interface

## Detection Challenge
The system vendor detection (`ansible_system_vendor`) reports "QEMU" rather than "Contabo" because the VM is running on Proxmox/KVM. This means:

- Automatic provider detection will fail
- Contabo-specific optimizations won't be applied unless explicitly configured
- Need to set `vps_provider: "contabo"` in inventory/group_vars
## Recommended Configuration

### Inventory Configuration (`group_vars/all/vps.yml`)
```yaml
# Force Contabo provider detection for Proxmox/KVM instances
vps_provider: "contabo"
```
### Manual MTU Optimization (if role fails)
```bash
# Set MTU to 1450 on primary interface
ip link set dev eth0 mtu 1450
# Verify
ip a show eth0
```

## Performance Characteristics
- **CPU**: AMD EPYC (high performance for cloud workloads)
- **Memory**: 24 GB RAM (ample for most deployments)
- **Storage**: 800 GB SSD (fast for data-intensive applications)
- **Network**: 1 Gbps (typical for Contabo Cloud VPS 30 SSD)

## Project Compatibility
This instance is well-suited for:
- **Production workloads**: 8 cores + 24 GB RAM can handle significant traffic
- **Container orchestration**: Kubernetes or Docker Swarm
- **Storage applications**: Large SSD capacity for databases or storage services
- **Development/Testing**: Ample resources for CI/CD pipelines

## Summary
This Contabo Cloud VPS 30 SSD instance (vmi2997710) is a high-performance virtual machine running on Proxmox/KVM with:
- 8 AMD EPYC cores
- 24 GB RAM
- 800 GB SSD storage
- Full virtualization support
- IPv4 + IPv6 connectivity

The project includes specific optimizations for Contabo environments, but they need to be explicitly configured due to the Proxmox/KVM vendor detection challenge.
