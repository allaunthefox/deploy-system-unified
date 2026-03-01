# SEPARATION_OF_CONCERNS

> **Formal standard:** This document describes the project's implementation of the **Separation
> of Concerns (SoC)** principle, as defined in ISO/IEC 25010:2011 §4.2.7 (Modularity) and
> required by NIST SP 800-53 Rev 5 SA-8 (Security and Privacy Engineering Principles).
>
> See [TERMINOLOGY](TERMINOLOGY.md) for formal definitions with ISO/NIST citations.

The foundational rule of this project is:

> **Complexity is not a problem, but violating Separation of Concerns is.**

---

## What is a Concern Violation?

A concern violation occurs when a single role or task manages more than one logical concern. This
creates hidden dependencies, makes configuration baseline management inaccurate, and produces
audit records that cannot be cleanly attributed to a single control.

A role has a concern violation if its purpose cannot be described in a single sentence without
using "and".

### Anti-Patterns (Concern Violations)

| Role | Violation |
|---|---|
| A `security` role that installs `ntp` | Security policy concern + System services concern |
| A `bootstrap` role that configures a `firewall` | Initialization concern + Perimeter defense concern |
| A `hardened_ssh` task that generates an operator report | Target posture concern + Operational reporting concern |

### Correct Patterns (Separated Concerns)

| Role | Single concern — and only this |
|---|---|
| `core/time` | Manages NTP/Chrony time synchronization |
| `networking/firewall` | Manages the L3/L4 network perimeter |
| `ops/connection_info` | Manages operator reporting and output encryption |
| `security/sshd` | Manages SSH daemon configuration |
| `core/secrets` | Manages SOPS/Age secret access |

---

## Why It Matters

**Audit traceability (ISO/IEC 27001:2022 §8.15):** Every Audit Event Identifier points to one
role, and that role must point to one concern. When `core/time` emits a failure record, the
responsible control is immediately identifiable. A comingled "Security Framework" role that fails
produces an ambiguous audit record — the control that failed cannot be determined without reading
the source.

**Configuration baseline accuracy (ISO/IEC 27001:2022 §8.9, NIST CM-2):** A security auditor
reviewing `networking/firewall` should only encounter firewall logic. If package installation or
time configuration is embedded in the same role, the configuration baseline for that role is
inaccurate — it describes more than one component.

**Replaceability (ISO/IEC 25010:2011 §4.2.7 — Modularity):** A correctly separated role can be
replaced with an alternative implementation without touching any other role. Replacing `core/time`
with a different time synchronization method requires changes only within `core/time`. In a
comingled system, the same change requires auditing every role the time concern was bundled with.

---

## Configuration Baseline Inheritance

Separation of Concerns applies at the playbook level as well as the role level:

> **Workloads never define infrastructure. They import it from a verified configuration baseline.**

Governing standard: ISO/IEC 27001:2022 §8.9; NIST SP 800-53 CM-2.

In practice:

- `PRODUCTION_DEPLOY.yml` imports `BASE_HARDENED.yml`. It does not redeclare core, security, or
  networking roles. The infrastructure concern belongs to the base layer.
- `ephemeral_edge.yml` declares only workload roles (`containers/caddy`, `containers/anubis`).
  The infrastructure is declared separately or assumed to be converged.
- Application roles in `roles/containers/` install and configure services. They do not configure
  firewalls, manage system users, or set kernel parameters. Those concerns belong to the base
  layer roles (`networking/firewall`, `security/access`, `security/kernel`).

A violation of this rule means a workload role has an implicit dependency on infrastructure it
did not declare. That hidden dependency is a concern violation at the playbook level.

---

## Enforcement

**`enforce_style_guide.sh`** — Static analysis of role structure, nesting depth, and naming
patterns. Flags roles whose task list crosses detectable concern boundaries.

**Audit Event Identifier suite tagging** — Every task carries a suite-tagged Audit Event
Identifier. If a `core/time` task carries an identifier from the Security Observability Suite,
that is a signal of a concern violation and will be flagged in review. The suite boundary is a
machine-readable expression of the concern boundary.

**DSU001 lint rule** — Enforces that `main.yml` files at the project root contain no top-level
`roles:` block. Role lists belong in named playbooks. This prevents the orchestration surface
from accumulating infrastructure concerns.
