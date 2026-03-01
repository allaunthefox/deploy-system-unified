# MOLECULE_TESTING

This project uses [Molecule](https://molecule.readthedocs.io/) for testing Ansible roles and playbooks.

## Overview

All scenarios use the **Ansible-Native** configuration approach as recommended in Molecule v25.x. This provides full control over the testing lifecycle through custom create/destroy playbooks.

## Scenarios

| Scenario | Purpose | Image |
|----------|---------|-------|
| default | General testing | ubi9/ubi-init |
| development | Development testing | ubi9/ubi-init |
| ephemeral | Ephemeral testing | ubi9/ubi-init |
| production | Production validation | ubi9/ubi-init |
| kubernetes-master | K3s testing | centos:stream9 |
| gpu_slicing | GPU slicing tests | ubi9/ubi-init + /dev/dri |
| gpu_slicing_arm64 | ARM64 GPU tests | ubi9/ubi-init + ARM64 |
| ephemeral_desktop | Desktop testing | geerlingguy/docker-ubuntu2204-ansible |
| network | Network testing | cEOS (Arista) |

## Running Tests

### Local Development

```bash
# Test default scenario
molecule test -s default

# Test specific scenario
molecule test -s gpu_slicing

# Run only converge (faster iteration)
molecule converge -s default
```

### Using Makefile

```bash
# Run x86_64 GPU Slicing tests
make test-x86

# Run ARM64 tests (requires QEMU/hardware)
make test-arm64
```

## Ansible-Native Format

All scenarios use the ansible-native configuration format:

```yaml
# molecule.yml
ansible:
  executor:
    backend: ansible-playbook
    args:
      ansible_playbook:
        - --inventory=inventory/
  playbooks:
    create: create.yml
    destroy: destroy.yml
    converge: converge.yml

scenario:
  test_sequence:
    - create
    - converge
    - verify
    - destroy
```

## Creating New Scenarios

1. Create scenario directory:
   ```bash
   mkdir molecule/my_scenario
   ```

2. Create `molecule.yml` with ansible-native format

3. Create `create.yml` - uses `containers.podman.podman_container`

4. Create `destroy.yml` - cleans up containers

5. Create `inventory/hosts.yml` - defines test hosts

6. Add playbooks: converge.yml, prepare.yml, verify.yml

## Migration Notes

This project was migrated from the legacy `molecule.yml` format (with driver/platforms/provisioner sections) to the Ansible-Native format in February 2026.

See `Offline_Research/LLM_RESEARCH/planning/MOLECULE_ANSIBLE_NATIVE_MIGRATION_GUIDE.md` for detailed conversion information.

## Dependencies

- Podman (recommended) or Docker
- Ansible 2.15+
- ansible-lint
- containers.podman collection
