# ARCHITECTURE_MIGRATION_GUIDE

## Overview

As of February 2026, the `deploy-system-unified` project has undergone a major restructuring to support multi-architecture deployments (x86_64, aarch64, riscv64). This guide details the changes and required actions for migrating existing configurations.

## Critical Changes

### 1. Role Structure

Roles now use an `arch/<architecture>/<vendor>` directory structure for tasks that vary by hardware.

- **Old**: `roles/containers/runtime/tasks/main.yml` contained all logic mixed together.
- **New**: `roles/containers/runtime/tasks/main.yml` acts as a dispatcher. Specific logic is in:
    - `roles/containers/runtime/arch/x86_64/nvidia/`
    - `roles/containers/runtime/arch/aarch64/nvidia/` (etc)

### 2. Branch Templates

Templates are now organized by architecture.

- **Moved**: `gpu_slicing_bare_metal.yml` -> `branch_templates/x86_64/gpu_slicing_bare_metal.yml`
- **Created**: `branch_templates/aarch64/gpu_slicing_bare_metal.yml` (Optimized for ARM64)

### 3. Documentation

- Legacy `battlemage_setup.md` is deprecated. Use `INTEL_GPU_GUIDE`.
- New Architecture Guides available in `docs/deployment/`.

## Migration Actions

### For x86_64 Deployments

**No action required.** The dispatcher logic defaults to `x86_64` logic if `ansible_architecture` matches `amd64` or `x86_64`. Existing playbooks referencing the roles will continue to work.

### For ARM64 (Jetson/Server) Deployments

1. Ensure the inventory sets `ansible_host` to the correct IP.
2. If using templates, switch to using the files in `branch_templates/aarch64/`.
3. Set `containers_gpu_vendor: nvidia` (default) for both Jetson (Tegra) and Grace Hopper. The role now auto-detects the specific driver needs (skipping kernel drivers on Jetson L4T).

### For Custom Roles

If you maintain custom roles that interact with GPU hardware, verify they respect the `gpu_stack_*` variables defined in `docs/deployment/GPU_STACK_SETUP.md`.

## Troubleshooting

- **Error**: "No GPU support found for Arch: ..."
    - **Fix**: Ensure the `ansible_architecture` fact is correct. If running on a new architecture, a generic fallback may need to be added in the role structure.
