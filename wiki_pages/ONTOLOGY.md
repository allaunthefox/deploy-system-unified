# ONTOLOGY

This is the decision-making reference for DSU taxonomy. It defines what every classification term means,
what values are valid, and how to choose between them. When a role, task, or profile decision requires
justification, the answer must trace back to this document.

---

## Core Principle

Non-comingling governs all classification decisions in this system. See [NON_COMINGLING](NON_COMINGLING).
The taxonomy below gives that rule operational structure: each axis answers a different question,
and no axis bleeds into another.

---

## Three Classification Axes

Every deployment in DSU is described by three independent axes. **Independent** means: changing the
value on one axis does not automatically change the value on another. A `container` host can be
`hardened`. A `bare-metal` host can be `dev`. The axes compose; they do not cascade.

---

### Axis 1 — Deployment Profile (`deployment_profile`)

**Question answered:** What is the security posture and operational intent of this host?

This is the primary governance axis. It controls which security roles are applied, what forensic
grade is required, and which playbook is the correct entrypoint. The valid values are declared in
`inventory/group_vars/` and enforced by `ops/preflight`.

| Profile | Security Class | Forensic Grade | Correct Entrypoint | Use when |
|---|---|---|---|---|
| `hardened` | Strict | Full (Loki + Grafana) | `base_hardened.yml` | Any persistent host. **This is the default.** |
| `production` | Strict | Compliance (Signed Logs + Loki) | `production_deploy.yml` | Persistent hosts running active workloads with SBOM and supply-chain verification |
| `ephemeral` | Strict | Minimal (Journal only) | `base_ephemeral.yml` or `ephemeral_edge.yml` | Disposable hosts: CI runners, test nodes, temporary ingress |
| `vps` | Strict | Standard (Rsyslog) | `base_hardened.yml` | Cloud VPS instances without the full Loki stack |
| `dev` | Permissive | None | `site.yml` | Local development and testing. `core_security_fail_secure: false` |

> **Note:** `workstation` and `backup` profile files exist in `inventory/group_vars/` as reserved
> placeholders. They are not yet active deployment targets.

**Decision rule:** If the host persists beyond a single session or holds live data and services,
use `hardened` or `production`. If it is disposable and state loss is acceptable, use `ephemeral`.
If it is a cloud VPS without a Loki stack, use `vps`. Never use `dev` outside of a local lab.

**What the profile controls in code:**

- `core_security_fail_secure`: `true` for all production profiles, `false` for `dev`
- `system_monitoring_loki_enabled`: `true` for `hardened` and `production`, `false` for `ephemeral` and `vps`
- `system_storage_hardened_integrity_mandatory`: only set to `true` for `production`
- PQC enforcement (post-quantum cryptography): only applied when `deployment_profile` is `hardened` or `production`

---

### Axis 2 — Infrastructure Type (`virt_type`)

**Question answered:** What is the hardware and virtualization context of this host?

This axis determines which hardware roles are applicable and which are skipped. It does **not**
change the security posture — that is Axis 1's sole responsibility.

`virt_type` is auto-detected by `ops/preflight` and then asserted against the list of valid values.
It can also be set explicitly in inventory when auto-detection is wrong.

**Valid values** (enforced by preflight assert `CIS 4.5.4`):

| Value | Description | Auto-detected when |
|---|---|---|
| `bare-metal` | Physical hardware, no hypervisor | `ansible_virtualization_role != 'guest'` |
| `virtual` | KVM or other hypervisor guest | Guest, but not a container and not `vps` profile |
| `container` | OCI container or LXC | `virtualization_type` is `docker`, `podman`, `container`, or `lxc` |
| `vps` | Cloud instance with managed hypervisor | `deployment_profile == 'vps'` and host is a guest |

> **Important:** The ONTOLOGY previously listed `kvm` as a valid value. The correct value is
> `virtual`. `kvm` will fail the preflight assertion.

Hardware roles gated on `virt_type`:
- `hardware/firmware` and `hardware/sas` — only run on `bare-metal`
- `hardware/virtual_guest` — only runs on `virtual`
- Container-specific network config — only runs on `container`

---

### Axis 3 — Architectural Profile

**Question answered:** What is the CPU architecture and GPU vendor of this host?

This axis governs which drivers, kernel parameters, and hardware-specific optimizations are
applied. All roles under `roles/hardware/` are gated on this axis. It is detected automatically
from Ansible facts.

| Architecture | GPU Vendor | Roles primarily affected |
|---|---|---|
| `x86_64` | `nvidia` | `hardware/gpu` (CUDA stack, NVENC) |
| `x86_64` | `intel` | `hardware/gpu` (Intel media drivers, VAAPI) |
| `x86_64` | none | Standard x86 kernel parameters only |
| `aarch64` | none | `hardware/firmware`, ARM-specific kernel flags |
| `riscv64` | none | Minimal hardware roles; most hardware roles skip |

Architecture-specific templates and tasks are located under `roles/*/arch/` subdirectories.

---

## Forensic Coverage

Forensic grade is **not** an independent axis. It is a property that derives directly from the
Deployment Profile (Axis 1). The profile's `group_vars` file sets the variables that control it.

Every action in DSU emits an Action Code. The forensic grade determines where those codes are
stored and for how long.

| Forensic Grade | Backend | Retention | Profiles that use it |
|---|---|---|---|
| Full (Loki + Grafana) | Loki stream + Grafana dashboards | Long-term | `hardened` |
| Compliance (Signed Logs) | Signed log files + Loki | Compliance period | `production` |
| Standard (Rsyslog) | Rsyslog remote | Standard rotation | `vps` |
| Minimal (Journal only) | systemd journal | Session only | `ephemeral` |
| None | No forensic backend | N/A | `dev` |

---

## Action Code Suites

Action Codes are the atomic audit unit. Each code maps one task execution to one compliance
requirement. The full registry is in [DSU_ACTION_CODES_COMPLETE](DSU_ACTION_CODES_COMPLETE).

Every task name in this project follows the pattern: `[Standard] | [Action Code] | [Name]`

| Suite | Range | Standard | Purpose |
|---|---|---|---|
| PQC Suite | 400100–400110 | ISO 27001 §10.1 | Post-quantum cryptography (hardened + production only) |
| Forensic Suite | 840030–840041 | ISO 27001 §12.4 | Loki/Grafana observability |
| Threat Analysis Suite | 480000–480010 | ISO 27001 Amd 1 | AI-driven log auditing |
| Autonomic Suite | 900000–900031 | ISO 27040 | Verified recovery and restore |
| SBOM Suite | 520040–520047 | ISO 27001 §14.2 | Supply chain verification |
| Guard Suite | 600030–600032 | ISO 9001 | Profile-based safety guards |
| Integrity Response Suite | 800510–800515 | NIST SI-7 | Hardware-bound state purge |

---

## Enforcement Rules

1. **Profile declaration:** Every supported `deployment_profile` must have a corresponding file in
   `inventory/group_vars/`. If it is not declared there, it cannot be applied.

2. **Preflight validation:** `ops/preflight` runs before any other role. It auto-detects `virt_type`,
   asserts the value is in the valid set, and halts execution if the detected combination is
   invalid. It cannot be skipped.

3. **Task naming:** Every task must follow `[Standard] | [Action Code] | [Name]`. This is
   machine-checked by `enforce_style_guide.sh` in CI.

4. **No manual security override:** Security flags are set exclusively through `deployment_profile`.
   Directly overriding profile-controlled variables in a playbook or task breaks the forensic
   signature chain and is not permitted.

5. **Base Import Rule:** Workloads never define infrastructure. They import it from a verified
   Base Layer. `production_deploy.yml` imports `base_hardened.yml`; it does not redeclare any of
   its roles. This is what makes the forensic signature chain auditable end-to-end.

---

## Related Documents

- [NON_COMINGLING](NON_COMINGLING) — The structural rule this taxonomy enforces
- [MODULAR_LAYERS](MODULAR_LAYERS) — The layer stack that implements this taxonomy
- [Quality_Idempotency_BLOCKERS](Quality_Idempotency_BLOCKERS) — Idempotency contract and known blockers
- [DSU_ACTION_CODES_COMPLETE](DSU_ACTION_CODES_COMPLETE) — Full Action Code registry
- [LLM_MAP](LLM_MAP) — AI agent usage guide for this project
