# virtualization_kvm

**Role Path**: `roles/virtualization/kvm`

## Description
**Virtualization Layer**
Configures the KVM hypervisor layer, including CPU features and kernel modules for virtualization.

## Key Tasks
- Assign Hypervisor Instance UUID
- Install QEMU and KVM virtualization packages
- Report TPM Status
- Ensure NBD kernel module is loaded (Disk Mounting)
- Ensure KVM kernel modules are loaded
- Enable and start libvirtd service
- Configure QEMU security settings (Restrictive)

---
*This page was automatically generated from role source code.*