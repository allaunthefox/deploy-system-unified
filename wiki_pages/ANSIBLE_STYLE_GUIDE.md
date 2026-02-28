# Ansible Style Guide

Standards for all Ansible playbooks, roles, and tasks in Deploy-System-Unified.

---

## Task Naming Convention

**This is the most important style rule in the project.** Every task name must encode its
compliance lineage. The format is:

```
"[Standards] | [Audit Event Identifier (if applicable)] | [Description]"
```

Standards are listed in this order when present: `CIS` → `STIG` → `NIST` → `ISO`. Not every task
maps to all four standards. Include only the ones that apply. The Audit Event Identifier is required on
compliance-critical tasks; it is optional on helper/prerequisite tasks.

**Examples from the codebase:**

```yaml
# Full compliance task with Audit Event Identifier
- name: "CIS 5.4.1 | STIG V-230270 | NIST AU-8 | ISO 27001 §8.17 | Audit Code 300001 | Configure secure time synchronization (idempotent)"

# Multi-standard task without Audit Event Identifier (prerequisite step)
- name: "CIS 5.4.1 | STIG V-230270 | NIST AU-8 | Refresh package cache for time synchronization dependencies (Debian/Ubuntu)"

# Single-standard task
- name: "ISO 9001 | 600013 | Set preflight completion facts"
```

**Rules:**
- Pipe characters (`|`) are the delimiter between fields — one space on each side.
- Descriptions must be imperative mood: "Configure X", not "Configures X" or "X is configured".
- Add `(idempotent)` to the description when the task uses a state check to avoid re-execution.
- Add the OS qualifier in parentheses when a task is platform-specific: `(Debian/Ubuntu)`, `(RHEL)`.

---

## Custom DSU Lint Rules

These four rules run automatically via `make lint`. Every contributor must understand what they
enforce and how to handle exceptions.

### DSU001 — No Top-Level Roles in `main.yml`

`main.yml` files at the project root must not contain a top-level `roles:` block. Role lists
belong in `branch_templates/*.yml` or named playbooks like `SITE.YML` and `PRODUCTION_DEPLOY.yml`.

```yaml
# WRONG — in main.yml
- hosts: all
  roles:
    - core/bootstrap

# CORRECT — in main.yml (only imports are allowed)
- ansible.builtin.import_playbook: playbooks/PREFLIGHT_ASSERTIONS.YML
```

This enforces Configuration Baseline Inheritance: `main.yml` stays a pristine orchestration surface.

### DSU002 — No Invalid Capabilities

Capability lists (`capabilities`, `quadlet_gpu_capabilities`) must contain only Linux kernel
`CAP_*` values. Strings like `"gpu"`, `"compute"`, `"video"`, `"display"` are not kernel
capabilities and will fail.

```yaml
# WRONG
capabilities:
  - gpu
  - compute

# CORRECT
capabilities:
  - CAP_NET_ADMIN
  - CAP_SYS_PTRACE
```

### DSU003 — No Direct Placeholder Comparisons

Do not compare variables directly to `CHANGE_ME` or `CHANGE_ME_IN_*` placeholder values. Use a
defensive pattern that checks for definition and non-empty length.

```yaml
# WRONG
when: my_secret == "CHANGE_ME"
when: my_secret != "CHANGE_ME"

# CORRECT
when:
  - my_secret is defined
  - my_secret | length > 0
```

**Exception — intentional placeholder guards in preflight:** If you are explicitly validating that
a placeholder has been replaced (as in `ops/preflight`), suppress the rule inline:

```yaml
value: "{{ vault_my_secret | default('') }}"  # noqa DSU003
```

DSU003 is automatically skipped for `molecule/`, `defaults/`, `templates/`, `docs/`, and
`inventory/` directories.

### DSU004 — Shim Least Privilege

Applies to `ansiblelint/__init__.py` only. Shim files must be explicitly gated (via env var,
repo-origin check, or CI detection), must set `__dsu_shim__ = True`, must emit a structured
audit log tagged `DSU-SHIM`, and must not perform network or subprocess operations at import time.

---

## Includes vs Imports

| Use | When |
|---|---|
| `ansible.builtin.include_tasks` | Dynamic inclusion — the task list is determined at runtime (e.g., looped role execution via `tasks/RUN_ROLE.YML`) |
| `ansible.builtin.import_playbook` | Static inclusion — the playbook is always included and parsed at load time |
| `ansible.builtin.import_tasks` | Static inclusion — always parsed, no conditionals on the import itself |

The DSU pattern for executing roles dynamically uses `include_tasks` with a loop:

```yaml
tasks:
  - name: Execute roles
    ansible.builtin.include_tasks: tasks/RUN_ROLE.YML
    loop: "{{ role_list }}"
    loop_control:
      loop_var: role_item
```

---

## General Standards

**Idempotency**: Every task must be idempotent. For `shell` and `command` tasks, implement an
explicit state check (e.g., read `/sys/`, `/proc/`, or a sentinel file) rather than running
unconditionally. A second playbook run against a converged host must produce `changed=0`.

**Loops**: Use `loop` instead of deprecated `with_items` and other `with_*` constructs.

**Handlers**: Use handlers for services that should only restart when configuration changes.
Triggering a restart on every run is an idempotency violation.

**Conditionals**: Use `when` clauses for platform or profile conditions. Do not use shell
conditionals inside `command` or `shell` tasks when an Ansible `when` clause can do the same job.

**Secrets**: Never hardcode secrets in playbooks or role files. All secrets are managed via SOPS/Age
through `core/secrets`. See [SECRETS_MANAGEMENT](SECRETS_MANAGEMENT).

**Variables**: Define defaults in `defaults/main.yml`. Use descriptive, namespaced names
(`rolename_thing_action`, e.g., `core_time_service_enabled`).

**Tags**: Every task must have at least one tag. Tag names use underscores and lowercase.
Compliance tags mirror the task name fields: `cis_5_4_1`, `nist_au_8`, `iso_27001_8_17`.

---

## Role Structure

Every role follows the standard Ansible Galaxy directory structure:

```
roles/category/rolename/
├── defaults/main.yml     # All configurable variables with safe defaults
├── handlers/main.yml     # Service restart handlers
├── meta/main.yml         # Dependencies, role metadata
├── molecule/             # Test scenarios
├── tasks/main.yml        # Task list
├── templates/            # Jinja2 templates
├── tests/                # Testinfra tests
└── vars/main.yml         # Non-configurable role constants
```

Roles must not cross category boundaries. A role in `security/` does not install packages that
belong to `core/`. A role in `containers/` does not configure the firewall. See
[NON_COMINGLING](NON_COMINGLING).

---

## Running the Linter

```bash
make lint
```

This runs `ansible-lint -x internal-error .` from the project root, applying all built-in
ansible-lint rules plus the four custom DSU rules in `ansiblelint/rules/`.
