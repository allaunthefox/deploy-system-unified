---
name: gpu-orchestrator
description: Expert guidance for GPU discovery, orchestration, and validation across x86_64, aarch64, and riscv64. Use when implementing or debugging GPU-related Ansible roles, discovery scripts, or container runtime GPU support.
---

# GPU Orchestrator Skill

This skill provides procedural knowledge for managing the universal GPU stack in the `deploy-system-unified` project.

## Workflows

### 1. Hardware Discovery
When adding support for a new GPU or architecture:
1. Update `roles/hardware/gpu/files/gpu_discovery.py` with relevant PCI Vendor IDs.
2. Ensure `tasks/detect_video.yml` correctly captures and exposes facts.
3. Validate results on the target architecture.

### 2. Slicing Validation
Before applying slicing configurations:
1. Include `tasks/validate_slicing.yml`.
2. Check `gpu_slicing_iommu_active`, `gpu_slicing_sriov_supported`, and vendor-specific facts.
3. Assert that `gpu_stack_slicing_strategy` is compatible with detected hardware.

### 3. Container Runtime Integration
To enable GPU support in Podman/Docker:
1. Use `roles/containers/runtime/tasks/gpu_discovery.yml` to inherit facts from the hardware role.
2. Validate runtime integrity using `tasks/gpu_validation.yml`.
3. Perform a containerized smoke test (e.g., `nvidia-smi` in a test container).

## References
- See [gpu_architecture.md](references/gpu_architecture.md) for the role structure and fact schema.

## Constraints
- **Idempotence**: Hardware probes must not change system state unless explicitly requested.
- **Security**: Never expose raw PCI IDs or device paths without proper permission gating.
- **Compatibility**: Always check `ansible_architecture` before applying vendor-specific logic.
