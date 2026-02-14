# CORE_ROLE_IDEMPOTENCE_BASELINE

- Started (UTC): 2026-02-13T00:18:56.554675+00:00
- Ended (UTC): 2026-02-13T00:18:59.775387+00:00
- Roles benchmarked: 1
- Idempotent: 0
- Non-idempotent: 0
- Failed: 1
- Errors: 0

## Per-Role Results

| Role | Status | Changed (2nd run) | Failed (2nd run) | Unreachable (2nd run) | Duration | Log |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| core/bootstrap | failed | - | - | - | 3.22s | `Workspaces/deploy-system-unified/ci-artifacts/idempotence/20260213T001856Z/logs/core_bootstrap.log` |

## First Failure Excerpts

- `core/bootstrap`: ERROR! the role 'core/bootstrap' was not found in /workspace/Workspaces/deploy-system-unified/ci-artifacts/idempotence/20260213T001856Z/playbooks/roles:/workspace/projects/deploy-system-unified/roles:/workspace/projects/deploy-system-unified:/workspace/Workspaces/deploy-system-unified/ci-artifacts/idempotence/20260213T001856Z/playbooks
