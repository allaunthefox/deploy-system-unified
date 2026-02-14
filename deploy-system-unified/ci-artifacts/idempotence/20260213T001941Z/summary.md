# CORE_ROLE_IDEMPOTENCE_BASELINE

- Started (UTC): 2026-02-13T00:19:41.938895+00:00
- Ended (UTC): 2026-02-13T00:19:44.610992+00:00
- Roles benchmarked: 1
- Idempotent: 0
- Non-idempotent: 0
- Failed: 1
- Errors: 0

## Per-Role Results

| Role | Status | Changed (2nd run) | Failed (2nd run) | Unreachable (2nd run) | Duration | Log |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| core/bootstrap | failed | - | - | - | 2.67s | `deploy-system-unified/ci-artifacts/idempotence/20260213T001941Z/logs/core_bootstrap.log` |

## First Failure Excerpts

- `core/bootstrap`: ERROR! couldn't resolve module/action 'community.general.pacman'. This often indicates a misspelling, missing collection, or incorrect module path.
