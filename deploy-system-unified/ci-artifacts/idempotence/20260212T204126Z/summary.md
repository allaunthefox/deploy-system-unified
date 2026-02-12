# CORE_ROLE_IDEMPOTENCE_BASELINE

- Started (UTC): 2026-02-12T20:41:26.457273+00:00
- Ended (UTC): 2026-02-12T20:50:46.717731+00:00
- Roles benchmarked: 12
- Idempotent: 12
- Non-idempotent: 0
- Failed: 0
- Errors: 0

## Per-Role Results

| Role | Status | Changed (2nd run) | Failed (2nd run) | Unreachable (2nd run) | Duration | Log |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| core/bootstrap | idempotent | 0 | 0 | 0 | 142.82s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_bootstrap.log` |
| core/entropy | idempotent | 0 | 0 | 0 | 45.79s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_entropy.log` |
| core/grub | idempotent | 0 | 0 | 0 | 15.74s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_grub.log` |
| core/hardware_support | idempotent | 0 | 0 | 0 | 19.98s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_hardware_support.log` |
| core/identity | idempotent | 0 | 0 | 0 | 16.07s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_identity.log` |
| core/logging | idempotent | 0 | 0 | 0 | 26.29s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_logging.log` |
| core/memory | idempotent | 0 | 0 | 0 | 20.05s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_memory.log` |
| core/repositories | idempotent | 0 | 0 | 0 | 120.97s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_repositories.log` |
| core/secrets | idempotent | 0 | 0 | 0 | 25.88s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_secrets.log` |
| core/systemd | idempotent | 0 | 0 | 0 | 15.67s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_systemd.log` |
| core/time | idempotent | 0 | 0 | 0 | 48.45s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_time.log` |
| core/updates | idempotent | 0 | 0 | 0 | 62.51s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T204126Z/logs/core_updates.log` |

## First Failure Excerpts

