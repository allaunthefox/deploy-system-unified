# GitHub Wiki Update Instructions

## Summary

All documentation changes have been prepared and pushed to a pull request branch. The changes include:

- **Terminology Standardization**: All formal terms from TERMINOLOGY.md are now used consistently
- **Formal Language**: Second-person informal language replaced with passive voice
- **Broken Links Fixed**: 32 broken internal links corrected
- **Stub Pages Consolidated**: 17 placeholder pages merged into parent documents
- **New Documents Added**: TERMINOLOGY.md, DSU_6767_REGISTRY.md, style guides

## Pull Request

**Branch:** `docs/terminology-formality-update`  
**PR URL:** https://github.com/allaunthefox/deploy-system-unified/pull/new/docs/terminology-formality-update

### Changes Summary

| Category | Files Changed | Lines Changed |
|----------|--------------|---------------|
| New Documents | 10 created | +1,500 |
| Terminology Updates | 23 modified | +100, -100 |
| Link Fixes | 6 modified | +50, -50 |
| Stub Consolidation | 17 deleted | -200 |
| **Total** | **85 files** | **+3,071, -350** |

### Key Documents Updated

1. **TERMINOLOGY.md** (new) - Formal definitions with ISO/NIST citations
2. **ONTOLOGY.md** - Updated to use formal terms
3. **SEPARATION_OF_CONCERNS.md** - Updated to reference SoC as primary term
4. **DOCUMENTATION_STYLE_GUIDE.md** (new) - Documentation standards
5. **ANSIBLE_STYLE_GUIDE.md** (new) - Ansible code standards
6. **DSU_6767_REGISTRY.md** (new) - Internal standard registry
7. **Home.md** - Updated terminology
8. **Documentation_Index.md** - Updated navigation
9. **_Sidebar.md** - Updated navigation

## GitHub Wiki Sync

The `wiki_pages/` directory contains all wiki content. To sync to GitHub Wiki:

### Option 1: Manual Sync (Recommended)

```bash
# Clone the wiki repository
git clone git@github.com:allaunthefox/deploy-system-unified.wiki.git /tmp/wiki-sync
cd /tmp/wiki-sync

# Copy all files from wiki_pages/
cp -r /home/prod/Workspaces/repos/github/deploy-system-unified/wiki_pages/* .

# Remove files that no longer exist
for file in *; do
    if [ "$file" != ".git" ] && [ ! -e "/home/prod/Workspaces/repos/github/deploy-system-unified/wiki_pages/$file" ]; then
        rm -rf "$file"
    fi
done

# Commit and push
git add -A
git commit -m "Sync wiki pages from wiki_pages/ directory

Automated sync from wiki_pages/ directory.
Date: $(date -Iseconds)
"
git push origin master
```

### Option 2: Use Sync Script

```bash
cd /home/prod/Workspaces/repos/github/deploy-system-unified
./scripts/sync_wiki.sh
```

**Note:** Requires SSH key configured for GitHub wiki repository access.

## Wiki Link Format

All internal wiki links use this format:
```markdown
[Page Title](PAGE_NAME)
```

Where `PAGE_NAME` matches the filename without `.md` extension.

Example:
```markdown
See [SEPARATION_OF_CONCERNS](SEPARATION_OF_CONCERNS.md) for the foundational rule.
```

## Files Deleted (Stub Consolidation)

The following stub pages were consolidated into parent documents:

- `Quality_Idempotency_BREAKERS_*.md` (3 files)
- `Quality_Idempotency_CRITICAL_BLOCKERS_*.md` (3 files)
- `Quality_Idempotency_REMEDIATION_*.md` (2 files)
- `Testing_Negative_CURRENT_STATE_*.md` (2 files)
- `Testing_Negative_REMEDIATION_*.md` (2 files)
- `Testing_Negative_VERIFICATION_*.md` (2 files)
- `Plan_Testing_Negative_PLAN_PHASE*.md` (3 files)

Content from these pages has been merged into:
- `Quality_Idempotency_BLOCKERS.md`
- `Testing_Negative_IMPLEMENTATION.md`

## Terminology Changes

| Old Term | New Formal Term |
|----------|-----------------|
| Action Code | Audit Event Identifier |
| Forensic Grade | Audit Log Retention Class |
| Forensic Intelligence | Security Observability |
| Autonomic Recovery | Automated Recovery Verification |
| Volatile Secrets | Ephemeral Credentials |
| Separation of Concerns | Separation of Concerns (SoC) |
| Base Import Rule | Configuration Baseline Inheritance |

## Next Steps

1. **Create Pull Request:**
   - Go to: https://github.com/allaunthefox/deploy-system-unified/pull/new/docs/terminology-formality-update
   - Review changes
   - Merge to main

2. **Sync GitHub Wiki:**
   - Run `./scripts/sync_wiki.sh` or use manual sync above
   - Verify wiki links work correctly

3. **Verify Links:**
   - Check `_Sidebar.md` navigation
   - Test `Documentation_Index.md` links
   - Verify all cross-references work

## Contact

For questions about these changes, refer to:
- `docs/architecture/TERMINOLOGY.md` - Formal term definitions
- `docs/development/DOCUMENTATION_STYLE_GUIDE.md` - Documentation standards
- `wiki_pages/DSU_6767_REGISTRY.md` - Internal standard registry
