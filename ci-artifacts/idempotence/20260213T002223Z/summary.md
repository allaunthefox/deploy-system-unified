# CORE_ROLE_IDEMPOTENCE_BASELINE

- Started (UTC): 2026-02-13T00:22:23.800120+00:00
- Ended (UTC): 2026-02-13T00:22:42.016452+00:00
- Roles benchmarked: 2
- Idempotent: 0
- Non-idempotent: 0
- Failed: 2
- Errors: 0

## Per-Role Results

| Role | Status | Changed (2nd run) | Failed (2nd run) | Unreachable (2nd run) | Duration | Log |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| core/hardware_support | failed | - | - | - | 9.15s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002223Z/logs/core_hardware_support.log` |
| core/memory | failed | - | - | - | 9.06s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002223Z/logs/core_memory.log` |

## First Failure Excerpts

- `core/hardware_support`: ERROR! 'failed_when' is not a valid attribute for a TaskInclude
- `core/memory`: ERROR! 'failed_when' is not a valid attribute for a TaskInclude
