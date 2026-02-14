# CORE_ROLE_IDEMPOTENCE_BASELINE

- Started (UTC): 2026-02-13T00:19:56.224439+00:00
- Ended (UTC): 2026-02-13T00:20:14.050948+00:00
- Roles benchmarked: 1
- Idempotent: 0
- Non-idempotent: 0
- Failed: 1
- Errors: 0

## Per-Role Results

| Role | Status | Changed (2nd run) | Failed (2nd run) | Unreachable (2nd run) | Duration | Log |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| core/bootstrap | failed | 0 | 1 | 0 | 17.82s | `deploy-system-unified/ci-artifacts/idempotence/20260213T001956Z/logs/core_bootstrap.log` |

## First Failure Excerpts

- `core/bootstrap`: fatal: [localhost]: FAILED! => {"ansible_facts": {}, "changed": false, "failed_modules": {"ansible.legacy.setup": {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3"}, "failed": true, "module_stderr": "sudo: a password is required\n", "module_stdout": "", "msg": "MODULE FAILURE\nSee stdout/stderr for the exact error", "rc": 1}}, "msg": "The following modules failed to execute: ansible.legacy.setup\n"}
