# security_kernel

**Role Path**: `roles/security/kernel`

## Description
**Sysctl Hardening**
Mandatory sysctl-based kernel hardening (network stack, process memory, and ASLR settings).

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