# UPDATING

This document explains how to update the GitHub Wiki content and keep it consistent.

## Quick checklist
- Run linter: `python3 .scripts/wiki_wiki_lint.py --json`
- If needed, auto-fix H1s and create placeholders: `python3 .scripts/wiki_wiki_lint.py --fix-h1 --create-placeholders`
- Include linter output in your PR description
- Do not change H1s silently on high-traffic pages—request review

## Page structure template
1. `# PAGE_SLUG` (top-level header matches filename)
2. Short summary (1-2 sentences)
3. Status: Draft | Stable | Deprecated
4. Canonical location: path to repository file (if applicable)
5. Examples & Usage
6. See also: `Role_Reference`, `Variable_Reference`

## How to add a placeholder
- Create `wiki_pages/NAME.md` and set a short note pointing to the canonical YAML or repo file.
- Prefer shorter page names (match existing pattern) and avoid punctuation in the file name.

## CI
- A GitHub Action `wiki-lint.yml` runs on PRs touching wiki files. It will fail the PR if the linter finds **warnings or errors**.

## Troubleshooting
- If the linter reports a missing page used by a sidebar, add a small placeholder page and link from the sidebar to that page.
- If you need to change existing H1s organization-wide, raise a PR explaining the reason and perform the change in a single commit with a migration note.
Auto-publish test: 2026-02-10

Auto-publish test 2: 2026-02-10
