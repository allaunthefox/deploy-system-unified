# STABILITY_PLAN

**Status:** Strategic reference (active)  
**Execution Source of Truth:** `STABILITY_EXECUTION_PLAN_2026.md`

**Date:** February 7, 2026  
**Scope:** Production and development playbooks, base hardening, container stack, secrets handling, backups, and observability.

## Goals

- Deterministic, idempotent runs with minimal drift.
- Reproducible dependencies and consistent deployment inputs.
- Safe rollback and verified recovery procedures.
- Continuous validation of core roles and production templates.
- Clear operational visibility and health checks.

## Current Baseline (Reference Points)

- Production template: `production_deploy.yml`.
- Reference templates: `branch_templates/` (do not deploy directly).
- Hardened base: `base_hardened.yml`.
- SSH idempotence guardrails: `docs/deployment/SSH_IDEMPOTENCE_GUARDRAILS.md`.
- Deployment readiness snapshot: `docs/deployment/DEPLOYMENT_STATUS.md`.

## Workstreams

### 1. Idempotence and Drift Control

- Add a standard check-mode gate for production templates (`--check --diff`).
- Expand idempotence guardrails to other critical configs (sudoers, sysctl, firewall, container runtime).
- Add a simple drift report task that summarizes changed files across a run.
- Ensure all "write" tasks are atomic and have explicit ownership/permissions.
- Centralize GRUB management: remove direct `/etc/default/grub` edits in role tasks, route all kernel params through `core/grub`, and consolidate `update-grub` handlers to a single source of truth.

### 2. Dependency Pinning and Reproducibility

- Add `collections.yml` with pinned versions for required Ansible collections.
- Add `requirements.yml` for external roles and vendor content.
- Document OS package baselines and repository pinning strategy.
- Track container image tags used by production templates.

### 3. Testing and CI Coverage

- Expand Molecule coverage for core, security, and container roles.
- Add `ansible-lint`, `yamllint`, and `shellcheck` to CI.
- Add a minimal "production template smoke test" using a stub inventory.
- Add a regression check that a second run produces zero changes.

### 4. Secrets and Configuration Stability

- Keep Vault as the active secrets provider until SOPS keys are finalized.
- Add validation to ensure `secrets.generated.yml` remains encrypted.
- Document a secrets rotation workflow (frequency, ownership, and recovery steps).
- Define a minimal set of required secrets for production templates.

### 5. Backup, Restore, and Rollback

- Document RPO/RTO targets and tie them to backup schedules.
- Add a restore runbook for core services and data paths.
- Add a monthly restore verification checklist.
- Define a rollback method for config changes (inventory snapshot, git tag, container image tag).

### 6. Observability and Health Checks

- Add post-deploy checks for systemd units and container health.
- Add log retention policy and disk usage alerts.
- Implement a basic "deployment health report" summary task.
- Document escalation paths and on-host troubleshooting steps.

## Milestones

- Phase 1 (Weeks 1-2): Idempotence and dependency pinning.
- Phase 2 (Weeks 3-4): Testing and CI coverage.
- Phase 3 (Weeks 5-6): Backup/restore and rollback runbooks.
- Phase 4 (Weeks 7-8): Observability and health checks.

## Success Metrics

- Second run produces zero changes on production template.
- CI check-mode gate remains green for supported platforms.
- Restore verification succeeds monthly with documented evidence.
- Deployment health report completes in under 10 minutes post-run.

## Risks and Open Questions

- Vault password handling for automated CI runs.
- SOPS migration dependencies (real Age keys and updated `.sops.yaml`).
- GPU vendor variability in test coverage and runtime behavior.

## Historical Immediate Actions (Phase 1 Snapshot)

This section is retained for historical context from the original stability planning pass.
Current execution priorities are tracked in `STABILITY_EXECUTION_PLAN_2026.md`.

- Create `collections.yml` and `requirements.yml` with pinned versions.
- Add a CI job for `--check --diff` against the production template.
- Draft the restore runbook and include a first verification checklist.
- Audit GRUB parameter writers and eliminate direct file edits outside `core/grub`.
