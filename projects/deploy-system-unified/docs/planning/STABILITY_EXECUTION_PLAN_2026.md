# STABILITY_EXECUTION_PLAN_2026

**Updated:** February 12, 2026  
**Status:** Phase 2 Active (Operational Maturity)  
**Scope:** Production playbooks, secrets hygiene, idempotence maturity, and post-deploy health verification.

## Purpose

This document is the execution board for current work. It defines what is in scope now and what evidence is required to call it complete.

## Current Target Window (Next 2-4 Weeks)

### Target Board

| ID | Target | Status | Required Output | Evidence Path |
| :--- | :--- | :--- | :--- | :--- |
| T1 | Core role idempotence benchmark | Complete (12/12 idempotent) | Repeat-run benchmark across all `roles/core/*` roles with failures tracked | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/` |
| T2 | SOPS migration guide + key rotation SOP | Not Started | Operator guide covering migration sequence, rollback, and rotation cadence | `docs/deployment/` |
| T3 | Post-deploy health check role | Not Started | New `ops/health_check` role + machine-readable health summary in deployment flow | `roles/ops/health_check/` + playbook output artifact |

## In Scope (This Window)

1. Idempotence hardening and measurable repeat-run stability for core roles.
2. Secrets process maturity through documentation and safe migration procedure design.
3. Operational observability through standardized post-deploy checks.

## Out of Scope (This Window)

1. Full architecture restructuring work from `RESTRUCTURING_PLAN_2026.md`.
2. Long-horizon GPU expansion phases from `GPU_ENHANCED_PLAN.md`.
3. Broad community/process expansion beyond docs required for the active targets.

## Accomplishments (Phase 1 Complete)

- ✅ PR consolidation and repository cleanup completed.
- ✅ Stability gates added (`verify_idempotence.sh`, `smoke_test_production.sh`, `preflight_assertions.yml`).
- ✅ CI status checks hardened for `main`.
- ✅ Deployment entrypoint hygiene enforced (`production_deploy.yml` as canonical deploy path).

## Execution Tracks (Phase 2)

### Track A: Idempotence Hardening

- Run `scripts/verify_idempotence.sh` per core role play path.
- Record each non-idempotent task and remediation commit.
- Publish baseline and post-fix benchmark logs.

#### Baseline Evidence (February 12, 2026)

- ✅ Baseline benchmark executed across all `roles/core/*` roles using `scripts/benchmark_core_idempotence.py`.
- ✅ Machine-readable and Markdown artifacts published:
  - `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/summary.json`
  - `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/summary.md`
- Baseline result snapshot: **4/12 idempotent, 8/12 failed**.
- Immediate remediation clusters:
  1. Unsupported module args (`debug.warn`, `command.pipefail`).
  2. Environment/package assumptions (`chrony`, `haveged`, `software-properties-common` in container baseline).
  3. Role-specific failure in `core/secrets` and `core/systemd` requiring focused fix pass.
- ✅ Post-remediation benchmark rerun completed:
  - `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/summary.json`
  - `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/summary.md`
- Post-remediation result snapshot: **12/12 idempotent, 0 failed**.

### Track B: Secrets Maturity (Design-to-Execution)

- Draft SOPS migration guide with gate checks and fallback to Vault.
- Draft key rotation SOP (frequency, custodianship, emergency rotation procedure).
- Define explicit cutover criteria before enabling SOPS as active provider.

### Track C: Observability & Health

- Implement `roles/ops/health_check` with checks for systemd units, container runtime health, disk thresholds, and critical service reachability.
- Emit a final deployment health summary in machine-readable format.
- Fail deploy when mandatory health checks fail.

## Near-Term Actions

- [x] Execute idempotence benchmark across all `core/` roles.
- [x] Remediate failures from baseline benchmark and rerun until all `core/` roles pass second-run idempotence.
- [ ] Draft SOPS migration guide and key rotation SOP.
- [ ] Implement `ops/health_check` role for post-deploy verification.

## Success Criteria (Phase 2)

1. ✅ 100% of `core` roles pass idempotence gate on second run (`20260212T204126Z`).
2. Production deployments emit a machine-readable health summary artifact.
3. SOPS migration guide and rotation SOP are approved and usable by operators.

## Dependencies and Risks

1. Secrets tooling transition must not conflict with active Vault gate enforcement.
2. GPU variability may introduce environment-specific idempotence noise.
3. CI runtime limits may require batching idempotence benchmark jobs.
