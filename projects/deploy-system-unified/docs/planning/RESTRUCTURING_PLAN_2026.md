# RESTRUCTURING_PLAN_2026

**Status:** Backlog (Not in current 2-4 week target window)  
**Activation Rule:** Break into scoped execution tasks and add to `STABILITY_EXECUTION_PLAN_2026.md` before implementation.

## Overview

Restructure the entire Deploy-System-Unified project to use an architecture-based approach (x86, ARM, RISC-V) with vendor-specific subprofiles. This will make the project more maintainable and future-proof for non-x86 deployments (like Milk-V, Spacemit, etc.). Additionally, address community engagement deficits identified through analysis to improve project accessibility and sustainability.

## Current Structure

projects/deploy-system-unified/ ├── roles/ │ └── core/ │ └── battlemage/ │ ├── defaults/ │ ├── tasks/ │ ├── templates/ │ ├── vars/ │ └── molecule/

## Identified Deficits (to be addressed in restructuring)

Based on analysis using the Qwen agent system, the following deficits were identified and will be addressed as part of this restructuring:

1. **Missing Essential Documentation**:
   - CONTRIBUTING.md: Guidelines for contributors
   - CHANGELOG.md: Record of changes between versions
   - ROADMAP.md: Future development plans
   - SECURITY.md: Security policy and disclosure procedure
   - CODE_OF_CONDUCT.md: Community guidelines

2. **Dependency Management Issues**:
   - Missing requirements.yml or similar file to define external dependencies

## Proposed Structure

projects/deploy-system-unified/ ├── roles/ │ ├── core/ │ │ ├── battlemage/ │ │ │ ├── arch/ │ │ │ │ ├── x86_64/ │ │ │ │ │ ├── nvidia/ │ │ │ │ │ ├── amd/ │ │ │ │ │ ├── intel/ │ │ │ │ │ └── generic/ │ │ │ │ ├── arm64/ │ │ │ │ │ ├── nvidia/ │ │ │ │ │ ├── amd/ │ │ │ │ │ ├── intel/ │ │ │ │ │ ├── milkv/ │ │ │ │ │ ├── spacemit/ │ │ │ │ │ └── generic/ │ │ │ │ └── riscv64/ │ │ │ │ ├── nvidia/ │ │ │ │ ├── amd/ │ │ │ │ ├── intel/ │ │ │ │ ├── milkv/ │ │ │ │ ├── spacemit/ │ │ │ │ └── generic/ │ │ │ ├── defaults/ │ │ │ ├── tasks/ │ │ │ ├── templates/ │ │ │ ├── vars/ │ │ │ └── molecule/ │ │ └── ... (other core roles)

## Implementation Steps

### Phase 1: Role Structure Restructuring

1. Analyze all existing roles to identify architecture and vendor dependencies
2. Create architecture-based subdirectories for all roles
3. Move vendor-specific tasks, templates, and vars to appropriate directories
4. Update main tasks to use conditional includes based on ansible_architecture and GPU vendor

### Phase 2: Branch Templates Restructuring

1. Create architecture-specific branch templates
2. Add vendor-specific configuration options
3. Update existing templates to support new structure

### Phase 3: Documentation Restructuring (Addressing Community Deficits)

1. Update battlemage_setup.md to reflect the Intel GPU drivers (Battlemage) context and the architecture-based approach
2. Create architecture-specific installation and configuration guides
3. Update GPU slicing and Kubernetes documentation
4. **ADD NEW DOCUMENTATION TO ADDRESS DEFICITS**:
   - Create CONTRIBUTING.md with contribution guidelines
   - Create SECURITY.md with security policy and disclosure process
   - Create CODE_OF_CONDUCT.md with community guidelines
   - Create CHANGELOG.md to track changes between versions
   - Create ROADMAP.md outlining future development plans
5. Add requirements.yml to define external dependencies

### Phase 4: Testing and Validation

1. Update molecule tests to support multiple architectures
2. Create architecture-specific test scenarios
3. Validate the restructuring with existing and new tests

### Phase 5: Integration and Deployment

1. Test the restructured roles in various environments
2. Update CI/CD pipeline to support architecture-based testing
3. Document any breaking changes and migration guide
4. Implement dependency management processes

## Benefits

- **Maintainability**: Clear separation of architecture and vendor-specific code
- **Scalability**: Easy to add support for new GPU vendors and architectures
- **Future-proofing**: Prevents hard blockers for non-x86 deployments (ARM, RISC-V)
- **Flexibility**: Architecture and vendor can be specified dynamically based on inventory
- **Consistency**: Uniform structure across all GPU-related roles
- **Community Engagement**: Enhanced documentation improves contributor experience
- **Project Sustainability**: Clear governance and contribution processes
- **Security**: Established security disclosure and response procedures

## Potential Challenges

- **Complexity**: Increased number of files and directories
- **Duplication**: Need to manage shared code across architectures
- **Testing**: More test scenarios to maintain
- **Migration**: Existing configurations may need to be updated
- **Community Adoption**: Ensuring new processes are followed consistently

## Risk Mitigation

- Keep existing structure as fallback for compatibility
- Use conditional includes to maintain backward compatibility
- Document all changes thoroughly
- Test in stages before full deployment
- Gradually implement new community processes
- Communicate changes clearly to existing users

## Timeline

- **Phase 1**: 2 weeks (Role Structure)
- **Phase 2**: 1 week (Branch Templates)
- **Phase 3**: 2 weeks (Documentation - including community deficits)
- **Phase 4**: 2 weeks (Testing)
- **Phase 5**: 1 week (Integration)

Total: 8 weeks

## Dependencies

- Team availability for documentation creation
- Security contact information for SECURITY.md
- Community feedback mechanisms
- CI/CD pipeline adjustments for new structure
