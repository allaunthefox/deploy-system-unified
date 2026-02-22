# RESTRUCTURING_PLAN_2026

## Overview

Restructure the entire Deploy-System-Unified project to use an architecture-based approach (x86, ARM, RISC-V) with vendor-specific subprofiles. This will make the project more maintainable and future-proof for non-x86 deployments (like Milk-V, Spacemit, etc.).

## Current Structure

projects/deploy-system-unified/ ├── roles/ │ └── core/ │ └── battlemage/ │ ├── defaults/ │ ├── tasks/ │ ├── templates/ │ ├── vars/ │ └── molecule/

## Proposed Structure

projects/deploy-system-unified/ ├── roles/ │ ├── core/ │ │ ├── battlemage/ │ │ │ ├── arch/ │ │ │ │ ├── x86_64/ │ │ │ │ │ ├── nvidia/ │ │ │ │ │ ├── amd/ │ │ │ │ │ ├── intel/ │ │ │ │ │ └── generic/ │ │ │ │ ├── arm64/ │ │ │ │ │ ├── nvidia/ │ │ │ │ │ ├── amd/ │ │ │ │ │ ├── intel/ │ │ │ │ │ ├── milkv/ │ │ │ │ │ ├── spacemit/ │ │ │ │ │ └── generic/ │ │ │ │ └── riscv64/ │ │ │ │ ├── nvidia/ │ │ │ │ ├── amd/ │ │ │ │ ├── intel/ │ │ │ │ ├── milkv/ │ │ │ │ ├── spacemit/ │ │ │ │ └── generic/ │ │ │ ├── defaults/ │ │ │ ├── tasks/ │ │ │ ├── templates/ │ │ │ ├── vars/ │ │ │ └── molecule/ │ │ └── ... (other core roles)

## Implementation Steps

### Phase 1: Role Structure Restructuring (DONE)

1. Analyze all existing roles to identify architecture and vendor dependencies
2. Create architecture-based subdirectories for all roles (`tasks/arch/`)
3. Move vendor-specific tasks, templates, and vars to appropriate directories
4. Update main tasks to use conditional includes based on ansible_architecture and GPU vendor
5. Integrated legacy `core/battlemage` into unified `hardware/gpu` role.

### Phase 2: Branch Templates Restructuring (DONE)

1. Create architecture-specific branch templates (`branch_templates/<arch>/`)
2. Add vendor-specific configuration options
3. Update existing templates to support new structure

### Phase 3: Documentation Restructuring (IN PROGRESS)

1. Update Role Reference and specialized guides (Battlemage)
2. Create architecture-specific installation and configuration guides
3. Update GPU slicing and Kubernetes documentation

### Phase 4: Testing and Validation (DONE)

1. Verified restructuring via comprehensive idempotence benchmark script.
2. 100% success rate on 12/12 core roles.
3. Fixed Podman-specific container permission issues in benchmark suite.

### Phase 5: Integration and Deployment

1. Test the restructured roles in various environments
2. Update CI/CD pipeline to support architecture-based testing
3. Document any breaking changes and migration guide

## Benefits

- **Maintainability**: Clear separation of architecture and vendor-specific code
- **Scalability**: Easy to add support for new GPU vendors and architectures
- **Future-proofing**: Prevents hard blockers for non-x86 deployments (ARM, RISC-V)
- **Flexibility**: Architecture and vendor can be specified dynamically based on inventory
- **Consistency**: Uniform structure across all GPU-related roles

## Potential Challenges

- **Complexity**: Increased number of files and directories
- **Duplication**: Need to manage shared code across architectures
- **Testing**: More test scenarios to maintain
- **Migration**: Existing configurations may need to be updated

## Risk Mitigation

- Keep existing structure as fallback for compatibility
- Use conditional includes to maintain backward compatibility
- Document all changes thoroughly
- Test in stages before full deployment

## Timeline

- **Phase 1**: 2 weeks (Role Structure)
- **Phase 2**: 1 week (Branch Templates)
- **Phase 3**: 1 week (Documentation)
- **Phase 4**: 2 weeks (Testing)
- **Phase 5**: 1 week (Integration)

Total: 7 weeks
