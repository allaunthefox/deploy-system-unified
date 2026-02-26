# ONTOLOGY

This is the decision-making reference for DSU taxonomy. It defines what every classification
term means, what values are valid, and how to choose between them. When a role, task, or profile
decision requires justification, the answer must trace back to this document.

For formal definitions of every term used here, including governing ISO and NIST citations, see
[TERMINOLOGY](TERMINOLOGY).

---

## Core Principle

**Separation of Concerns (SoC)** governs all classification decisions in this system. See [NON_COMINGLING](NON_COMINGLING) for the project's implementation of this principle.

The taxonomy below gives SoC operational structure: each axis answers a different question and
no axis bleeds into another.

---

## Three Classification Axes

Every deployment in DSU is described by three independent axes. **Independent** means: changing
the value on one axis does not automatically change the value on another. A `container` host can
be `hardened`. A `bare-metal` host can be `dev`. The axes compose; they do not cascade.

---

### Axis 1 — Deployment Profile (`deployment_profile`)

**Question answered:** What is the security configuration baseline and operational intent of
this host?

This is the primary governance axis. It controls which security roles are applied, what Audit Log
Retention Class is required, and which playbook is the correct entrypoint. Valid values are
declared in `inventory/group_vars/` and enforced by `ops/preflight`.

| Profile | Security Class | Audit Log Retention Class | Correct Entrypoint | Use when |
|---|---|---|---|---|
| `hardened` | Strict | Full (Loki + Grafana) | `BASE_HARDENED.yml` | Any persistent host. **This is the default.** |
| `production` | Strict | Compliance (Signed Logs + Loki) | `PRODUCTION_DEPLOY.yml` | Persistent hosts running active workloads with SBOM and supply-chain verification |
| `ephemeral` | Strict | Minimal (Journal only) | `BASE_EPHEMERAL.yml` or `ephemeral_edge.yml` | Disposable hosts: CI runners, test nodes, temporary ingress |
| `vps` | Strict | Standard (Rsyslog) | `BASE_HARDENED.yml` | Cloud VPS instances without the full Loki stack |
| `dev` | Permissive | None | `site.yml` | Local development and testing. `core_security_fail_secure: false` |

> **Note:** `workstation` and `backup` profile files exist in `inventory/group_vars/` as reserved
> placeholders. They are not yet active deployment targets.

**Decision rule:** If the host persists beyond a single session or holds live data and services,
use `hardened` or `production`. If it is disposable and state loss is acceptable, use `ephemeral`.
If it is a cloud VPS without a Loki stack, use `vps`. Never use `dev` outside a local lab.

**What the profile controls in code:**

- `core_security_fail_secure` — `true` for all production profiles, `false` for `dev`
- `system_monitoring_loki_enabled` — `true` for `hardened` and `production`, `false` for `ephemeral` and `vps`
- `system_storage_hardened_integrity_mandatory` — only `true` for `production`
- Post-Quantum Cryptography (PQC) enforcement — only applied when `deployment_profile` is `hardened` or `production`

---

### Axis 2 — Infrastructure Type (`virt_type`)

**Question answered:** What is the hardware and virtualization context of this host?

This axis determines which hardware roles are applicable and which are skipped. It does **not**
change the security configuration baseline — that is Axis 1's sole responsibility.

`virt_type` is auto-detected by `ops/preflight` and asserted against the valid value set. It can
be set explicitly in inventory when auto-detection is insufficient.

**Valid values** (enforced by preflight assert `CIS 4.5.4`):

| Value | Description | Auto-detected when |
|---|---|---|
| `bare-metal` | Physical hardware, no hypervisor | `ansible_virtualization_role != 'guest'` |
| `virtual` | Hypervisor guest (KVM, QEMU, etc.) | Guest, not a container, not `vps` profile |
| `container` | OCI container or LXC instance | `virtualization_type` is `docker`, `podman`, `container`, or `lxc` |
| `vps` | Cloud instance with managed hypervisor | `deployment_profile == 'vps'` and host is a guest |

> **Important:** `kvm` is not a valid value. The correct value for a KVM guest is `virtual`.
> Using `kvm` will fail the preflight assertion.

Hardware roles gated on `virt_type`:
- `hardware/firmware` and `hardware/sas` — only run on `bare-metal`
- `hardware/virtual_guest` — only runs on `virtual`
- Container-specific network configuration — only runs on `container`

---

### Axis 3 — Architectural Profile

**Question answered:** What is the CPU architecture and GPU vendor of this host?

This axis governs which drivers, kernel parameters, and hardware-specific optimizations are
applied. All roles under `roles/hardware/` are gated on this axis. Architecture is detected
automatically from Ansible facts.

| Architecture | GPU Vendor | Roles primarily affected |
|---|---|---|
| `x86_64` | `nvidia` | `hardware/gpu` (CUDA stack, NVENC) |
| `x86_64` | `intel` | `hardware/gpu` (Intel media drivers, VAAPI) |
| `x86_64` | none | Standard x86 kernel parameters only |
| `aarch64` | none | `hardware/firmware`, ARM-specific kernel flags |
| `riscv64` | none | Minimal hardware roles; most hardware roles skip |

Architecture-specific templates and tasks live in `roles/*/arch/` subdirectories.

---

## Audit Log Retention Class

The Audit Log Retention Class is not an independent axis. It is a derived property of the
Deployment Profile (Axis 1). The profile's `group_vars` file sets the variables that control it.

Every action in DSU emits an Audit Event Identifier. The Audit Log Retention Class determines
where those identifiers and their associated records are stored and for how long.

Governing standard: ISO/IEC 27001:2022 §8.15, §8.16; ISO/IEC 27037:2012.

| Class | Backend | Retention | Profiles |
|---|---|---|---|
| Full | Loki + Grafana | Long-term | `hardened` |
| Compliance | Signed log files + Loki | Compliance period | `production` |
| Standard | Rsyslog remote | Standard rotation | `vps` |
| Minimal | systemd journal | Session only | `ephemeral` |
| None | No backend | N/A | `dev` |

---

## Audit Event Identifier Suites

Each task in DSU is assigned an Audit Event Identifier that maps the execution to exactly one
compliance control. Identifiers are grouped into suites by concern domain.

Governing standard: ISO/IEC 27001:2022 §8.15; NIST SP 800-53 Rev 5 AU-3.

The full registry is in [DSU_ACTION_CODES_COMPLETE](DSU_ACTION_CODES_COMPLETE).

Every task name follows the pattern: `[Standard] | [Audit Event Identifier] | [Description]`

| Suite | Range | Governing Standard | Purpose |
|---|---|---|---|
| PQC Suite | 400100–400110 | ISO 27001 §10.1, NIST FIPS 203/204 | Post-Quantum Cryptography (`hardened` + `production` only) |
| Security Observability Suite | 840030–840041 | ISO 27001 §8.15/§8.16 | Loki/Grafana SIEM stack |
| AI-Assisted Anomaly Detection Suite | 480000–480010 | ISO 27001:2022/Amd 1:2024 | AI-driven log auditing |
| Automated Recovery Verification Suite | 900000–900031 | ISO 27040 §8.3, ISO 27031 | Verified restore operations |
| SBOM Suite | 520040–520047 | ISO/IEC 5962:2021, ISO 27001 §8.15 | Supply chain verification |
| Configuration Baseline Guard Suite | 600030–600032 | ISO 9001, ISO 27001 §8.9 | Profile-based safety guards |
| Hardware Integrity Response Suite | 800510–800515 | NIST SP 800-193, NIST SI-7 | Hardware-bound state purge |

---

## Enforcement Rules

1. **Profile declaration:** Every supported `deployment_profile` must have a corresponding file
   in `inventory/group_vars/`. If it is not declared there, it cannot be applied.

2. **Preflight validation:** `ops/preflight` runs before any other role. It auto-detects
   `virt_type`, asserts the value is in the valid set, and halts execution if the combination is
   invalid. It cannot be skipped.

3. **Task naming:** Every task must follow `[Standard] | [Audit Event Identifier] | [Description]`.
   Machine-checked by `enforce_style_guide.sh` in CI.

4. **No manual security override:** Security flags are set exclusively through
   `deployment_profile`. Directly overriding profile-controlled variables breaks the audit
   traceability chain and is not permitted.
   Governing standard: ISO/IEC 27001:2022 §8.9.

5. **Configuration Baseline Inheritance:** Workloads never define infrastructure. They import it
   from a verified configuration baseline. `PRODUCTION_DEPLOY.yml` imports `BASE_HARDENED.yml`
   and does not redeclare any of its roles. This makes the audit traceability chain verifiable
   end-to-end. Governing standard: ISO/IEC 27001:2022 §8.9, NIST CM-2.

---

## Related Documents

- [TERMINOLOGY](TERMINOLOGY) — Formal definitions with ISO/NIST citations for every term
- [NON_COMINGLING](NON_COMINGLING) — SoC implementation
- [MODULAR_LAYERS](MODULAR_LAYERS) — The 7-layer defense-in-depth architecture
- [../development/ISO_TAGGING_STANDARD](../development/ISO_TAGGING_STANDARD) — Tag naming and compliance mapping
- [../wiki_pages/QUALITY_IDEMPOTENCY_BLOCKERS](../wiki_pages/QUALITY_IDEMPOTENCY_BLOCKERS) — Idempotency contract
- [DSU_ACTION_CODES_COMPLETE](DSU_ACTION_CODES_COMPLETE) — Full Audit Event Identifier registry
- [../development/LLM_MAP](../development/LLM_MAP) — AI agent usage guide
