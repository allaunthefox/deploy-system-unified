# security/kernel

**Role Path**: `roles/security/kernel`

## Description
Tasks for security/kernel role - Mandatory Sysctl Hardening

## Key Tasks
- Detect Virtualization Environment (Internal)
- Apply kernel hardening parameters
- Configure Kernel to zero memory on free (GRUB)
- Apply Bare Metal OS-Layer Hardening

## Default Variables
- `kernel_profile`
- `kernel_enable_iommu`
- `kernel_restrict_dma`
- `kernel_hugepages_enabled`

---
*This page was automatically generated from role source code.*