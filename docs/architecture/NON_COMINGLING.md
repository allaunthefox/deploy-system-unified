# NON_COMINGLING

The foundational rule of this project is:

> **Complexity is not a problem, but comingling tasks is.**

---

## What is Comingling?

Comingling occurs when a single Role or Task manages more than one logical concern. The damage it
causes is not always visible immediately — it shows up as hidden dependencies, unpredictable
failures, and audit traces that can't be cleanly attributed to a single cause.

A role is comingled if you cannot describe its function in a single sentence without using "and".

### Anti-Patterns

| Comingled Role | Problem |
|---|---|
| A `security` role that installs `ntp` | Security concern + System Services concern |
| A `bootstrap` role that configures a `firewall` | Initialization concern + Perimeter Defense concern |
| A `hardened_ssh` task that generates an operator report | Target Posture concern + Operational Reporting concern |

### Correct Patterns

| Role | What it does — and only this |
|---|---|
| `core/time` | Manages NTP/Chrony |
| `networking/firewall` | Manages the L3/L4 perimeter |
| `ops/connection_info` | Manages operator reporting and output encryption |
| `security/sshd` | Manages the SSH daemon configuration |
| `core/secrets` | Manages SOPS/Age secret access |

---

## Why It Matters

**Forensic Clarity.** When `core/time` fails, you know exactly what failed. When a comingled
"Security Framework" role fails, you don't know if the cause was a network error, a bad package,
a config issue, or a credential problem. The Action Code in the log points to one role, and that
role must point to one concern.

**Auditability.** A security auditor reviewing `networking/firewall` should only have to read
firewall logic. If unrelated package installation lives in that role, the audit scope expands
unpredictably. The compliance tagging system (`ISO | Action Code | Task Name`) only works when
each role has a single, auditable purpose.

**Replaceability.** You can replace `core/time` with a different time sync implementation without
touching any security role, any networking role, or any ops role. In a comingled system, swapping
one component requires auditing every other component it was bundled with.

---

## The Base Import Rule

This is the enforcement of non-comingling at the playbook level:

> **Workloads never define infrastructure. They import it from a verified Base Layer.**

In practice:

- `production_deploy.yml` imports `base_hardened.yml` — it does not redeclare core, security, or
  networking roles.
- `ephemeral_edge.yml` declares only the workload roles (`containers/caddy`, `containers/anubis`)
  — the base infrastructure is assumed to be provided or declared separately.
- Application stacks under `roles/containers/` install services. They do not configure firewalls,
  manage users, or set kernel parameters. Those concerns belong to the Base Layer.

A violation of this rule means a workload role is implicitly depending on infrastructure it
doesn't declare. That hidden dependency is comingling at the playbook level.

---

## Enforcement

Two mechanisms enforce this in CI:

1. **`enforce_style_guide.sh`** — Audits role structure, nesting depth, and naming patterns. Fails
   if a role's task list crosses concern boundaries detectable by static analysis.

2. **The task naming convention** — Every task must be named `[Standard] | [Action Code] | [Name]`.
   The Action Code is suite-tagged. If a `core/time` task carries an Action Code from the Security
   Suite, that is a signal of comingling and will be flagged in review.
