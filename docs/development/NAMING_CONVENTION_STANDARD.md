# Naming Convention Standard

**Document Type:** Project Standard  
**Classification:** STD-CORE (Standard)  
**Version:** 1.0.0  
**Date:** 2026-02-26  
**Purpose:** Define mandatory file naming conventions for all project documentation

---

## Overview

This standard defines the mandatory naming convention for all files in the Deploy-System-Unified project. Consistent naming ensures:

- Predictable file locations
- Easy navigation and discovery
- Automated tooling compatibility
- Professional documentation appearance

---

## Primary Convention: SCREAMING_SNAKE_CASE

**All wiki pages and documentation files MUST use SCREAMING_SNAKE_CASE.**

### Format

```
WORD1_WORD2_WORD3.md
```

### Rules

1. **All uppercase letters** - Every letter must be uppercase (A-Z)
2. **Underscores as separators** - Words are separated by underscores (_)
3. **No spaces** - Spaces are not permitted in filenames
4. **No mixed case** - Lowercase letters are not permitted
5. **Numbers allowed** - Numbers can be included where appropriate (e.g., `PLAN_2026.md`)
6. **Hyphens in version numbers** - Use hyphens only in version identifiers (e.g., `ISO-27001.md`)

---

## Examples

### Correct ✅

| Category | Example |
|----------|---------|
| Architecture Guides | `ARCH_X86.md`, `ARCH_ARM64.md`, `ARCH_MIGRATION_GUIDE.md` |
| Base Profiles | `BASE_HARDENED.md`, `BASE_EPHEMERAL.md` |
| Style Guides | `DEV_STYLE_ANSIBLE_STYLE_GUIDE.md`, `DOCUMENTATION_STYLE_GUIDE.md` |
| Plans | `PLAN_SECURITY_ENHANCEMENT_PLAN_2026.md`, `PLAN_MIGRATION_PLAN.md` |
| Reference | `REF_VARS_CONTAINERS.md`, `REF_ROLES_SECURITY.md`, `ROLE_REFERENCE.md` |
| Quality | `QUALITY_IDEMPOTENCY_BLOCKERS.md`, `TESTING_NEGATIVE_IMPLEMENTATION.md` |
| Compliance | `ISO_TAGGING_STANDARD.md`, `COMPLIANCE_GAP_ANALYSIS.md`, `SECURITY_AUDIT_REPORT.md` |
| Operations | `UNIVERSAL_DEPLOYMENT_GUIDE.md`, `DEPLOYMENT_STATUS.md`, `RESTORE_RUNBOOK.md` |

### Incorrect ❌

| Incorrect | Correct |
|-----------|---------|
| `Arch_X86.md` | `ARCH_X86.md` |
| `base_hardened.md` | `BASE_HARDENED.md` |
| `Dev_Style_Ansible.md` | `DEV_STYLE_ANSIBLE_STYLE_GUIDE.md` |
| `Plan_Security_2026.md` | `PLAN_SECURITY_ENHANCEMENT_PLAN_2026.md` |
| `ref_vars.md` | `REF_VARS_CONTAINERS.md` |
| `quality_blockers.md` | `QUALITY_IDEMPOTENCY_BLOCKERS.md` |
| `iso-tagging.md` | `ISO_TAGGING_STANDARD.md` |
| `home.md` | `HOME.md` |

---

## Category Prefixes

Standard prefixes help organize files by category:

| Prefix | Category | Examples |
|--------|----------|----------|
| `ARCH_` | Architecture Guides | `ARCH_X86.md`, `ARCH_MIGRATION_GUIDE.md` |
| `BASE_` | Base Profiles | `BASE_HARDENED.md`, `BASE_EPHEMERAL.md` |
| `DEV_STYLE_` | Development Style Guides | `DEV_STYLE_ANSIBLE_STYLE_GUIDE.md` |
| `PLAN_` | Plans & Roadmaps | `PLAN_MIGRATION_PLAN.md`, `PLAN_SECURITY_*.md` |
| `REF_` | Reference Documents | `REF_VARS_*.md`, `REF_ROLES_*.md` |
| `QUALITY_` | Quality Standards | `QUALITY_IDEMPOTENCY_BLOCKERS.md` |
| `TESTING_` | Testing Documentation | `TESTING_NEGATIVE_IMPLEMENTATION.md` |
| `DSU_` | DSU Standards | `DSU_AUDIT_EVENT_IDENTIFIERS.md`, `DSU_ACTION_CODES_COMPLETE.md`, `DSU_6767_REGISTRY.md` |

---

## Exceptions

### Allowed Non-Standard Names

| File | Reason |
|------|--------|
| `_Sidebar.md` | GitHub Wiki convention for sidebar navigation |
| `README.md` | Universal convention for project root |
| `roles/` | Directory for auto-generated role pages |

### Playbook Files

Playbook files in the repository root use lowercase with underscores:

- `SITE.YML`
- `BASE_HARDENED.YML`
- `PRODUCTION_DEPLOY.YML`
- `ephemeral_edge.yml`

This follows Ansible convention and distinguishes playbooks from documentation.

---

## Enforcement

### Automated Checks

The wiki-lint workflow enforces naming conventions:

```bash
# Run wiki linter
python3 .scripts/wiki_wiki_lint.py

# Check for non-compliant filenames
ls wiki_pages/*.md | grep -vE "^[A-Z]+(_[A-Z0-9]+)*\.md$"
```

### Pre-commit Hooks

Pre-commit hooks can be configured to reject non-compliant filenames:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: filename-case
      name: Check SCREAMING_SNAKE_CASE
      entry: ^[A-Z]+(_[A-Z0-9]+)*\.md$
      language: pygrep
      files: ^wiki_pages/.*\.md$
```

---

## Migration Guide

### For New Files

1. Always use SCREAMING_SNAKE_CASE for new documentation files
2. Use appropriate category prefix (ARCH_, PLAN_, REF_, etc.)
3. Keep names descriptive but concise

### For Existing Files

If renaming existing files:

1. Rename the file to SCREAMING_SNAKE_CASE
2. Update all internal links (use find/replace)
3. Update external references (scripts, CI/CD, etc.)
4. Test all links before committing

```bash
# Example: Find all references to old filename
grep -rn "old_filename.md" --include="*.md" .

# Update all references
find . -name "*.md" -exec sed -i 's|old_filename|NEW_FILENAME|g' {} \;
```

---

## Related Documents

- **[DOCUMENTATION_STYLE_GUIDE](DOCUMENTATION_STYLE_GUIDE.md)** - General documentation standards
- **[TERMINOLOGY](TERMINOLOGY.md)** - Formal terminology definitions
- **[STYLE_GUIDE](STYLE_GUIDE.md)** - Overall project style guide

---

## Compliance

All project documentation MUST comply with this standard. Non-compliant files will be renamed during the next documentation update cycle.

**Effective Date:** 2026-02-26  
**Review Date:** 2026-05-26  
**Owner:** Documentation Team
