# Molecule Drivers
## Overview
Molecule drivers define the platform where test instances are created. Each driver provides a different way to create and manage test environments.

## Supported Drivers
### Docker Driver
The most common driver for container-based testing:
```yaml
driver:
  name: docker
  host: localhost
  volumes:
    - /sys/fs/cgroup:/sys/fs/cgroup:ro
  privileged: true
  tmpfs:
    - /tmp
    - /run
  capabilities:
    - SYS_ADMIN
```

### Podman Driver
Alternative container driver for rootless containers:
```yaml
driver:
  name: podman
  host: localhost
```
### Vagrant Driver
Virtual machine driver using Vagrant:
```yaml
driver:
  name: vagrant
  provider:
    name: virtualbox
  box: geerlingguy/ubuntu2004
  memory: 512
  cpus: 1
```

### EC2 Driver
Amazon Web Services driver:
```yaml
driver:
  name: ec2
  region: us-east-1
  image: ami-12345678
  instance_type: t2.micro
```
### GCE Driver
Google Cloud Platform driver:
```yaml
driver:
  name: gce
  zone: us-central1-a
  image: ubuntu-2004-focal-v20210708
  machine_type: n1-standard-1
```

### Azure Driver
Microsoft Azure driver:
```yaml
driver:
  name: azure
  subscription_id: abc-123
  location: East US
  vm_size: Standard_B1s
```
## Driver Configuration Options

### Common Options
- `name`: Driver name
- `options`: Driver-specific options
- `safe_files`: Files to preserve during destroy
### Docker/Podman Options
- `volumes`: Volume mounts
- `tmpfs`: Temporary file systems
- `capabilities`: Container capabilities
- `privileged`: Privileged mode
- `network_mode`: Network mode
- `cgroupns_mode`: Cgroup namespace mode

### Vagrant Options
- `box`: Base box image
- `memory`: VM memory allocation
- `cpus`: Number of CPUs
- `provider`: Virtualization provider
### Cloud Provider Options
- `region`: Geographic region
- `instance_type`: VM size/type
- `image`: Base image
- `security_groups`: Security group configuration

## Driver Selection Criteria
Choose a driver based on:
- **Speed**: Docker/Podman are fastest
- **Isolation**: VMs provide better isolation
- **Platform**: Match target deployment platform
- **Resources**: Available system resources
- **Access**: Required access level
- **Cost**: Cloud vs local resources
## Custom Drivers
Molecule supports custom drivers for specialized platforms. Custom drivers implement the driver interface and provide platform-specific functionality.

## Driver Best Practices
- Use Docker/Podman for fast local testing
- Use VMs for better isolation
- Match test platform to production platform
- Consider resource constraints
- Use cloud providers for scale testing
- Document driver-specific requirements
