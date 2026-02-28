# Documentation Style Guide

Standards for all documentation in Deploy-System-Unified, including wiki pages, role docs, and
inline comments.

---

## Wiki Page Conventions

**Source of truth**: Wiki pages live in `wiki_pages/` in the repository. The GitHub wiki is
auto-synced from this directory by the CI wiki-lint workflow. Do not edit the GitHub wiki directly
— changes will be overwritten on the next sync.

**File naming**: Wiki page filenames MUST use **SCREAMING_SNAKE_CASE.md**.

See **[NAMING_CONVENTION_STANDARD](NAMING_CONVENTION_STANDARD)** for the complete naming standard.

Examples: `ONTOLOGY.md`, `NON_COMINGLING.md`, `DEV_STYLE_YAML_STYLE_GUIDE.md`, `REF_VARS_CORE.md`.

**Internal links**: When linking to another wiki page from within a wiki page, use this format:

```markdown
[Page Title](wiki/PAGE_NAME)
```

Where `PAGE_NAME` matches the filename without the `.md` extension. Example:

```markdown
See [../wiki_pages/NON_COMINGLING](../wiki_pages/NON_COMINGLING) for the foundational rule (Separation of Concerns).
```

Do not use relative file paths (`../../wiki_pages/NON_COMINGLING.md`) or bare page names — only the `wiki/PAGE_NAME` format renders correctly in the GitHub wiki.

**Terminology:** Use "Separation of Concerns (SoC)" as the primary term.

---

## Heading Structure

Use ATX-style headings (`#` prefix). Start at `#` for the page title, then `##` for top-level
sections, `###` for sub-sections. Do not skip levels.

```markdown
# Page Title

## Section

### Sub-section
```

Do not bold the page title instead of using `#`. Do not use `---` underline-style headings.

---

## Voice and Tense

- Use **active voice** and **imperative mood** for instructions: "Run the playbook" not "The
  playbook should be run".
- Use **present tense** for descriptions: "This role configures NTP" not "This role will configure
  NTP".
- Avoid filler phrases: "Please note that", "It is important to", "In order to".

---

## Code Blocks

Always specify the language for syntax highlighting:

```yaml
# YAML example
deployment_profile: "hardened"
```

```bash
# Shell example
ansible-playbook PRODUCTION_DEPLOY.yml -i inventory/contabo.ini
```

Use inline code (backticks) for: file names, variable names, role names, command names, and values.
Example: The `deployment_profile` variable defaults to `hardened` when running `BASE_HARDENED.yml`.

---

## Tables

Use tables for structured reference content (role lists, variable references, mapping tables).
Do not use tables for prose that flows naturally as paragraphs.

Always include a header row and alignment separators:

```markdown
| Column A | Column B | Column C |
|---|---|---|
| value | value | value |
```

---

## Role Documentation

Every role in `wiki_pages/roles/` must document:

1. **Purpose** — one sentence stating what the role does and only what it does.
2. **Key variables** — the variables in `defaults/main.yml` that a deployer is likely to need.
3. **Tags** — the ansible tags that can be used to run or skip this role.
4. **Compliance** — which standards this role satisfies (CIS, NIST, ISO).

Do not document internal implementation details in the wiki. The task file is the source of truth
for implementation; the wiki page is the operator's reference.

---

## Terminology

The canonical definition of every term in this project — with its governing ISO or NIST citation
— is in [../wiki_pages/TERMINOLOGY](../wiki_pages/TERMINOLOGY). That document is the authoritative reference. Do not
invent new terms or use informal terminology as primary labels in documentation.

Use the **Formal Term** as the primary label in all documentation.

| Formal Term (Primary) | Do Not Use (Legacy/Informal) |
|---|---|
| Separation of Concerns (SoC) | "Anti-Comingling Rule", "non-comingling", "task isolation" |
| Audit Event Identifier | "audit event identifier", "audit code", "event ID" |
| Audit Log Retention Class | Forensic Grade | "forensic grade", "log level" |
| Security Observability | Forensic Intelligence | "forensic intelligence", "forensic stack" |
| Automated Recovery Verification | Autonomic Recovery | "autonomic recovery", "auto-restore" |
| Ephemeral Credentials | Volatile Secrets | "volatile secrets", "RAM secrets" |
| AI-Assisted Anomaly Detection | Cognitive Sentinel | "cognitive sentinel", "AI watchdog" |
| Configuration Drift | Distinction drift | "distinction drift", "profile drift" |
| Configuration Baseline Inheritance | Base Import Rule | "base import rule" |
| `deployment_profile` | — | "profile", "posture", "mode" |
| `virt_type` | — | "virtualization type", "infra type" |
| `ops/preflight` | — | "preflight role", "the preflight" |

---

## Linting

The wiki-lint CI workflow runs markdown linting against all files in `wiki_pages/`. Ensure pages
pass before committing. The primary checks are: valid heading hierarchy, no broken internal links,
and consistent code block formatting.
