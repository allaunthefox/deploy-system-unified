# SUMMARY

This file is the planning index and the single place to see what is actively targeted now.

## Current Target Window

**Window:** February 2026 (next 2-4 weeks)  
**Canonical execution board:** `docs/planning/STABILITY_EXECUTION_PLAN_2026.md`

### Active Targets

1. ✅ Execute idempotence benchmark across all `roles/core/*` roles (`12/12` idempotent in run `20260212T204126Z`).
2. Draft SOPS migration guide and key rotation SOP (documentation + runbook quality).
3. Implement `roles/ops/health_check` and wire post-deploy health summary into production flow.

## Planning Document Map

### Active (Execution)

- `docs/planning/STABILITY_EXECUTION_PLAN_2026.md`
  - Operational target board, near-term tasks, and success criteria.

### Active (Strategy)

- `docs/planning/STABILITY_PLAN.md`
  - Strategic workstreams and milestone framing for stability.

### Active (Domain Support)

- `docs/planning/SECRETS_MANAGEMENT.md`
  - SOPS transition design and migration checklist.
- `docs/planning/MIGRATION_PLAN.md`
  - Legacy data migration and credential rotation strategy.
- `docs/planning/DATA_MAPPING.md`
  - Migration source/staging/destination mapping details.

### Backlog / Later-Phase Plans

- `docs/planning/GPU_ENHANCED_PLAN.md`
- `docs/planning/RESTRUCTURING_PLAN_2026.md`
- `docs/planning/COMMUNITY_ENHANCEMENT_PLAN.md`

### Completed / Historical Reference

- `docs/planning/WIKI_IMPROVEMENT_PLAN.md`
- `docs/planning/IMPLEMENTATION_REVIEW.md`
- `docs/planning/MEDIA_STACK_V2.md`

### Alias / Redirect

- `docs/planning/MIGRATION_STRATEGY.md`
  - Redirects to canonical migration plan location.

## Operating Rules

1. If a task is not listed in `STABILITY_EXECUTION_PLAN_2026.md` near-term actions, it is not considered current sprint scope.
2. Strategy docs define direction; execution docs define what gets done now.
3. Backlog docs can be promoted only by adding concrete near-term tasks to the execution board.
