# SSH Idempotence and Security Guardrails

## Overview

This document defines the guardrails, architectural decisions, and operational procedures for managing SSH configuration (`/etc/ssh/sshd_config`) within the `deploy-system-unified` environment.

These measures were introduced following the [SSH Incident Postmortem](./SSH_INCIDENT_POSTMORTEM.md) to prevent configuration drift, duplicate directives, and service failures.

## Core Principles

1.  **Single Source of Truth**: The Ansible `security/sshd` role is the *only* authorized entity to modify `sshd_config`. Manual edits will be overwritten or cause validation failures.
2.  **Idempotence**: Re-running the playbook must result in a deterministic state without adding duplicate lines.
3.  **Validation**: No configuration change is applied without passing `sshd -t` syntax validation.
4.  **Atomic Updates**: Configuration sections are managed via `blockinfile` to ensure cohesion.

## Technical Guardrails

### 1. Duplicate Directive Detection
To prevent the "multiple conflicting Port directives" issue, the Ansible role includes a strict verification step:

-   **Mechanism**: A custom `awk` script runs during the role execution.
-   **Check**: Scans `sshd_config` for global-scope directives (ignoring `Match` blocks) like `Port`, `PermitRootLogin`, `PasswordAuthentication`.
-   **Failure Condition**: If any critical directive appears more than once, the playbook **fails immediately** with a descriptive error.

### 2. Syntax Validation
Every task that modifies the configuration uses the Ansible `validate` parameter:

```yaml
validate: '/usr/sbin/sshd -t -f %s'
```

If the generated configuration is invalid, the file on disk is *not* updated, and the service is *not* restarted, preventing lockout.

### 3. Managed Blocks
We use `ansible.builtin.blockinfile` with clear markers to manage sections:
-   `# ANSIBLE MANAGED - SECURITY ALGORITHMS`: Ciphers, MACs, KexAlgorithms.
-   `# ANSIBLE MANAGED - ENHANCED SECURITY SETTINGS`: General operational settings (Logging, Timeouts, Auth).
-   `# ANSIBLE MANAGED - TRUSTED SSH EXCEPTIONS`: Conditional Match blocks.

### 4. Legacy Cleanup
Before applying new settings, the role proactively comments out unmanaged instances of conflicting keys (`PermitRootLogin`, `PasswordAuthentication`) found in the default distribution config.

## Operational Guidance

### 1. Single port source of truth
`ssh_effective_port` is the only port used by SSHD, firewall rules, Fail2Ban, and connection info.

### 2. Randomization precedence
When `ssh_randomize_port` is enabled, the randomized port always overrides `system_ssh_port`.

### 3. Endlessh gating
Port 22 is only opened automatically when `system_enable_endlessh` is enabled.

### 4. Changing SSH Configuration
**DO NOT** edit `/etc/ssh/sshd_config` manually. Use the `system_ssh_port`, `sshd_permit_root_login`, etc., variables instead.

### 5. Recovery
The role automatically creates a backup of the original configuration before the first run (`sshd_config.backup`).
If you are locked out and have console access:
1.  Restore the backup: `cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config`
2.  Restart SSH: `systemctl restart sshd`

## Related Docs

- `docs/deployment/OS_CONFIGURATION.md`
- `docs/deployment/SSH_INCIDENT_POSTMORTEM.md`