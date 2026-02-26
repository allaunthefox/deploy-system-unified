# DOCUMENTATION_BRIDGE

## Overview

This document serves as a bridge between the main project documentation in `projects/deploy-system-unified/docs/` and the GitHub wiki documentation in `wiki_pages/`. It helps users navigate between the two documentation systems and understand how they complement each other.

## Relationship Between Documentation Systems

### Main Project Documentation
- **Location**: `projects/deploy-system-unified/docs/`
- **Purpose**: Core project documentation, architectural decisions, development guidelines
- **Audience**: Developers, system administrators, contributors
- **Content Type**: Technical specifications, architectural decisions, development workflows

### GitHub Wiki Documentation
- **Location**: `wiki_pages/` (mirrors GitHub wiki structure)
- **Purpose**: User-focused guides, role documentation, variable references
- **Audience**: End users, deployers, operators
- **Content Type**: How-to guides, reference documentation, best practices

## Cross-References

### Style Guides
- **Project**: `docs/development/STYLE_GUIDE.md` (overview)
- **Wiki**: 
  - `YAML_Style_Guide.md` - YAML-specific standards
  - `Ansible_Style_Guide.md` - Ansible-specific standards  
  - `Shell_Style_Guide.md` - Shell-specific standards
  - `Documentation_Style_Guide.md` - Documentation-specific standards

### Variable References
- **Project**: Variables mentioned in `docs/deployment/` guides
- **Wiki**: 
  - `VARIABLE_REFERENCE.md` (overview)
  - `VARIABLE_REFERENCE_Containers.md` - Container-related variables
  - `VARIABLE_REFERENCE_Core.md` - Core system variables
  - `VARIABLE_REFERENCE_Security.md` - Security-related variables
  - `VARIABLE_REFERENCE_Networking.md` - Networking variables
  - `VARIABLE_REFERENCE_Storage.md` - Storage variables

### Role Documentation
- **Project**: High-level role descriptions in `docs/architecture/`
- **Wiki**: Detailed role documentation in `wiki_pages/roles/`

## Navigation Tips

1. **Start with Project Docs**: Begin with the main project documentation for architectural understanding
2. **Deep Dive in Wiki**: Use the wiki for detailed operational guidance and variable references
3. **Follow Cross-Links**: Both systems contain links to complementary information in the other system
4. **Check Both Systems**: Some information may be duplicated or expanded in one system vs. the other

## Maintenance Guidelines

When updating documentation:
1. Update both systems if information is duplicated
2. Ensure cross-links remain valid
3. Follow the style guides in both documentation systems
4. Test all internal links after updates

## Integration Points

The following files serve as key integration points between the two documentation systems:
- `README.md` - Entry point with links to both systems
- `docs/INDEX.md` - Main project documentation index
- `wiki_pages/DOCUMENTATION_INDEX.md` - Wiki documentation index
- `docs/development/CONTRIBUTING.md` - Contribution guidelines mentioning both systems