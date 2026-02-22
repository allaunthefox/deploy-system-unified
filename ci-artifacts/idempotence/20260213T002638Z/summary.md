# CORE_ROLE_IDEMPOTENCE_BASELINE

- Started (UTC): 2026-02-13T00:26:38.703030+00:00
- Ended (UTC): 2026-02-13T00:34:21.769068+00:00
- Roles benchmarked: 12
- Idempotent: 12
- Non-idempotent: 0
- Failed: 0
- Errors: 0

## Per-Role Results

| Role | Status | Changed (2nd run) | Failed (2nd run) | Unreachable (2nd run) | Duration | Log |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| core/bootstrap | idempotent | 0 | 0 | 0 | 122.47s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_bootstrap.log` |
| core/entropy | idempotent | 0 | 0 | 0 | 42.35s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_entropy.log` |
| core/grub | idempotent | 0 | 0 | 0 | 13.96s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_grub.log` |
| core/hardware_support | idempotent | 0 | 0 | 0 | 15.37s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_hardware_support.log` |
| core/identity | idempotent | 0 | 0 | 0 | 17.42s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_identity.log` |
| core/logging | idempotent | 0 | 0 | 0 | 21.87s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_logging.log` |
| core/memory | idempotent | 0 | 0 | 0 | 17.26s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_memory.log` |
| core/repositories | idempotent | 0 | 0 | 0 | 93.4s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_repositories.log` |
| core/secrets | idempotent | 0 | 0 | 0 | 19.39s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_secrets.log` |
| core/systemd | idempotent | 0 | 0 | 0 | 11.48s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_systemd.log` |
| core/time | idempotent | 0 | 0 | 0 | 40.53s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_time.log` |
| core/updates | idempotent | 0 | 0 | 0 | 47.55s | `deploy-system-unified/ci-artifacts/idempotence/20260213T002638Z/logs/core_updates.log` |

## First Failure Excerpts

