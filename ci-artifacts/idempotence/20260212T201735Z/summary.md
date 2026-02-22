# CORE_ROLE_IDEMPOTENCE_BASELINE

- Started (UTC): 2026-02-12T20:17:35.403030+00:00
- Ended (UTC): 2026-02-12T20:26:07.930447+00:00
- Roles benchmarked: 12
- Idempotent: 4
- Non-idempotent: 0
- Failed: 8
- Errors: 0

## Per-Role Results

| Role | Status | Changed (2nd run) | Failed (2nd run) | Unreachable (2nd run) | Duration | Log |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| core/bootstrap | idempotent | 0 | 0 | 0 | 133.34s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_bootstrap.log` |
| core/entropy | failed | 0 | 1 | 0 | 10.86s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_entropy.log` |
| core/grub | failed | 0 | 1 | 0 | 11.91s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_grub.log` |
| core/hardware_support | failed | 0 | 1 | 0 | 9.54s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_hardware_support.log` |
| core/identity | idempotent | 0 | 0 | 0 | 10.83s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_identity.log` |
| core/logging | idempotent | 0 | 0 | 0 | 19.76s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_logging.log` |
| core/memory | failed | 0 | 1 | 0 | 7.54s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_memory.log` |
| core/repositories | failed | 0 | 1 | 0 | 118.21s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_repositories.log` |
| core/secrets | failed | 0 | 1 | 0 | 15.29s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_secrets.log` |
| core/systemd | failed | 0 | 1 | 0 | 7.39s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_systemd.log` |
| core/time | failed | 0 | 1 | 0 | 12.05s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_time.log` |
| core/updates | idempotent | 0 | 0 | 0 | 59.61s | `projects/deploy-system-unified/ci-artifacts/idempotence/20260212T201735Z/logs/core_updates.log` |

## First Failure Excerpts

- `core/entropy`: fatal: [localhost]: FAILED! => {"changed": false, "msg": "No package matching 'haveged' is available"}
- `core/grub`: fatal: [localhost]: FAILED! => {"msg": "Unsupported parameters for (ansible_collections.ansible.builtin.plugins.action.debug) module: warn. Supported parameters include: msg, var, verbosity."}
- `core/hardware_support`: fatal: [localhost]: FAILED! => {"changed": false, "msg": "Unsupported parameters for (ansible.legacy.command) module: pipefail. Supported parameters include: _raw_params, _uses_shell, argv, chdir, creates, executable, removes, stdin, stdin_add_newline, strip_empty_ends."}
- `core/memory`: fatal: [localhost]: FAILED! => {"changed": false, "msg": "Unsupported parameters for (ansible.legacy.command) module: pipefail. Supported parameters include: _raw_params, _uses_shell, argv, chdir, creates, executable, removes, stdin, stdin_add_newline, strip_empty_ends."}
- `core/repositories`: fatal: [localhost]: FAILED! => {"attempts": 5, "changed": false, "msg": "No package matching 'software-properties-common' is available"}
- `core/secrets`: fatal: [localhost]: FAILED! => {"censored": "the output has been hidden due to the fact that 'no_log: true' was specified for this result", "changed": false}
- `core/systemd`: fatal: [localhost]: FAILED! => {
- `core/time`: fatal: [localhost]: FAILED! => {"changed": false, "msg": "No package matching 'chrony' is available"}
