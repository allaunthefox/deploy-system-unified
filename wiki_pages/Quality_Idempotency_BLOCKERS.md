# IDEMPOTENCY_BLOCKERS

Audit date: 2026-02-03
Scope: `deploy-system-unified` (all roles + branch templates)
Method: static analysis (repo scan + YAML parse). No playbooks executed.

This document lists **hard blockers** (things that can make a run fail or silently do the wrong thing) and **idempotency breakers** (things that always change, always restart, or drift every run), with **concrete fixes**.

## Fix Patterns (Use These Everywhere)

1. Prefer Ansible modules over `shell`/`command` whenever possible.
2. Only use `ansible.builtin.command` for real executables.
   - `command -v ...` is a shell builtin, not an executable.
   - Redirects like `> /dev/null` and operators like `|` / `&&` require `shell`, not `command`.
3. If you use `set -o pipefail`, force bash:
   - Add `args: { executable: /bin/bash }`
   - Or remove `pipefail` and structure the command so failure is explicit.
4. For "check" commands, set `changed_when: false`.
5. For "do" commands, gate them with `creates:`/`removes:` or a prior check + conditional.

## Critical Blockers

For detailed information about critical blockers, see:
- **[Critical Blockers - POSIX Syntax Issues](IDEMPOTENCY_CRITICAL_BLOCKERS_POSIX)**
- **[Critical Blockers - Shell Command Issues](IDEMPOTENCY_CRITICAL_BLOCKERS_SHELL)**
- **[Critical Blockers - Ansible Module Issues](IDEMPOTENCY_CRITICAL_BLOCKERS_ANSIBLE)**

## Idempotency Breakers

For detailed information about idempotency breakers, see:
- **[Idempotency Breakers - Timestamp Issues](IDEMPOTENCY_BREAKERS_TIMESTAMPS)**
- **[Idempotency Breakers - Randomization Issues](IDEMPOTENCY_BREAKERS_RANDOMIZATION)**
- **[Idempotency Breakers - Service Restart Issues](IDEMPOTENCY_BREAKERS_SERVICES)**

## Remediation Steps

For detailed remediation steps, see:
- **[Remediation Guide - Automated Fixes](IDEMPOTENCY_REMEDIATION_AUTOMATED)**
- **[Remediation Guide - Manual Fixes](IDEMPOTENCY_REMEDIATION_MANUAL)**