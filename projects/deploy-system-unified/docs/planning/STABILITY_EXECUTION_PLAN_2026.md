# Stability Execution Plan (2026)

**Date:** February 7, 2026  
**Scope:** Production playbooks, secrets hygiene, linting and style compliance, idempotence gates, and deployment entrypoint clarity.

## Guiding Principles

- Assume nothing: explicit configuration, explicit validation, and fail-fast checks.
- Security-first defaults in every role and playbook.
- Deterministic, idempotent runs with minimal drift.
- Single source of truth for production deployments.

## Current Signals

- Secrets provider: Ansible Vault (`inventory/group_vars/all/secrets.generated.yml`).
- Linting configuration: `.ansible-lint.yml` points to `ansiblelint/rules`.
- Production entrypoint: `production_deploy.yml` (templates in `branch_templates/` are reference-only).

## Execution Tracks

### 1. Secrets Hygiene (Vault-First)

- Keep Vault as the only active provider until SOPS keys are real and validated.
- Ensure no placeholder `.sops.yaml` exists at repo root.
- Add a preflight assertion that `secrets.generated.yml` is encrypted before deployment runs.

### 2. Linting and Style Enforcement

- Run `ansible-lint` from repo root using the custom ruleset in `ansiblelint/rules`.
- Add `yamllint` and the style guide enforcement script to CI gates.
- Establish a lint gate for all changes under `roles/`, `tasks/`, and `playbooks/`.

### 3. Deployment Entrypoint Hygiene

- Treat `production_deploy.yml` as the deployment entrypoint.
- Keep `branch_templates/` as reference-only and include explicit warnings in header comments.
- Update documentation to prevent accidental deployment from template files.

### 4. Check-Mode and Idempotence Gate

- Require `--check --diff` for production template dry-runs.
- Add a second-run guard: a repeat run must produce zero changes.
- Record and track drift in a simple post-run report.

### 5. Preflight Validation (Assume Nothing)

- Validate inventory file paths and required variables with `ansible.builtin.assert`.
- Verify connectivity and privilege escalation before any write tasks.
- Fail fast when security defaults are overridden.

### 6. Observability and Post-Deploy Checks

- Add post-run checks for systemd units and container health.
- Capture log retention status and disk usage thresholds.
- Emit a short deployment health summary at the end of each run.

## Near-Term Actions (Next 2 Weeks)

- Remove or avoid placeholder SOPS configuration; document SOPS migration prerequisites.
- Promote linting and style enforcement into pre-merge gates.
- Confirm production entrypoint conventions in docs and templates.
- Create a minimal production smoke test with a stub inventory.
- Archive one clean check-mode run log as a baseline artifact.

## Success Criteria

- `production_deploy.yml` check-mode runs complete with zero changes on a second pass.
- Lint gates remain green for playbook and role updates.
- No placeholder secrets tooling files remain in the repository.
