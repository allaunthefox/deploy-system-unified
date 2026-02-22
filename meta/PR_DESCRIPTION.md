# Fix Wiki Documentation Linking Issues

## Summary

This PR addresses the wiki documentation issues identified by the linter, specifically the "missing anchor" errors that were occurring due to incorrect path resolution in the linter script. The main issue was that the linter was not properly recognizing anchors in role documentation files.

## Changes Made

### 1. Fixed Linter Path Resolution
- Updated `wiki_check_fix.py` to use relative paths instead of just filenames when building the file_headers dictionary
- Changed from `file_headers[p.name]` to `file_headers[str(p.relative_to(root))]` to properly map anchors to their files
- This ensures that links like `roles/containers_anubis.md#anubisenabled` correctly resolve to the appropriate file

### 2. Improved Role Documentation Generation
- Updated `generate_role_pages.py` to create proper Markdown headings for variables that the linter can recognize
- Changed from HTML-style anchors `<a id="...">` to proper Markdown headings `### VariableName`
- This ensures the linter's slugify function can properly match anchor references

### 3. Enhanced Variable Reference Linking
- Updated `link_variable_reference.py` to properly link to role documentation anchors
- Ensured variable reference files link to the correct anchor format in role documentation

### 4. Documentation Structure Improvements
- Split overly long documentation files into focused, manageable sections
- Created specialized style guides (YAML, Ansible, Shell, Documentation)
- Created categorized variable references (Containers, Core, Security, Networking, Storage)
- Maintained all cross-references between documents

## Verification

- All previously reported "missing anchor" errors for containers roles have been resolved
- Linter now reports 0 missing page links
- Documentation structure is more maintainable and user-friendly
- All internal navigation paths continue to work correctly

## Impact

This fixes the core documentation integrity issues while improving the overall structure and maintainability of the wiki documentation system.