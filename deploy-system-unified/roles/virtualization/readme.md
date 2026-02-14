# Virtualization Role

This role manages virtualization hosts (Hypervisors).

## Sub-Components

* **kvm**: KVM/QEMU/Libvirt installation and configuration.
* **storage**: Storage pool management for virtual machines.

## Usage

Apply to nodes acting as hypervisors.

```yaml
- name: Setup KVM Host
  hosts: hypervisors
  roles:
    - virtualization
```
