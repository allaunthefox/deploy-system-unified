# TERMINOLOGY

This document is the canonical reference for terminology used across Deploy-System-Unified.
Every term has a formal definition grounded in an ISO, IEC, NIST, or established industry
standard. Where DSU uses alternative terminology, the governing standard is cited and the
mapping is explicit.

All documentation in this project must use the **Formal Term** as the primary label.

---

## Glossary

---

### Audit Event Identifier
**DSU Shorthand:** Audit Event Identifier

**Definition:** A unique numeric identifier assigned to each auditable system event, enabling
bidirectional tracing between a task execution and the compliance control it satisfies.

**Governing Standard:**
- ISO/IEC 27001:2022 §8.15 — *Logging* requires that audit records include identifiers that
  uniquely associate the event with a control.
- NIST SP 800-53 Rev 5 AU-3 — *Content of Audit Records* mandates event identifiers that
  support correlation across systems.

**In DSU:** Audit Event Identifiers are 6-digit integers (e.g., `300001`) grouped into suites
by concern domain. They appear in every task name following the pattern
`[Standard] | [Identifier] | [Description]`. The full catalog is in
[DSU_AUDIT_EVENT_IDENTIFIERS](DSU_AUDIT_EVENT_IDENTIFIERS).

---

### Audit Log Retention Class
**DSU Shorthand:** Forensic Grade

**Definition:** A classification tier defining how audit log records are stored, protected, and
retained based on the operational and regulatory requirements of the host environment.

**Governing Standard:**
- ISO/IEC 27001:2022 §8.15 — *Logging* defines that log storage, protection, and retention
  must match the sensitivity of the information and applicable legal requirements.
- ISO/IEC 27037:2012 — *Guidelines for identification, collection, acquisition and preservation
  of digital evidence* establishes that evidence integrity must be maintained through appropriate
  storage mechanisms.

**In DSU:** The Audit Log Retention Class is a property of the Deployment Profile. It is not
independently configurable. The four classes map to profiles as follows:

| Class | Backend | Profile |
|---|---|---|
| Full | Loki + Grafana, long-term retention | `hardened` |
| Compliance | Signed log files + Loki | `production` |
| Standard | Rsyslog remote | `vps` |
| Minimal | systemd journal, session only | `ephemeral` |
| None | No log backend | `dev` |

---

### Automated Recovery Verification
**DSU Shorthand:** Autonomic Recovery

**Definition:** A process in which backup restoration is executed automatically on a scheduled
basis into an isolated environment, with results verified against a known-good state, confirming
recoverability without human intervention.

**Governing Standard:**
- ISO/IEC 27040:2024 §8.3 — *Data recovery* requires that recovery procedures be tested
  periodically to verify that data can be restored within required timeframes.
- ISO/IEC 27031:2011 §7 — *ICT readiness for business continuity* establishes that recovery
  capability must be validated through testing, not assumed.

**In DSU:** Implemented by `storage/backup/restic` using Audit Event Identifier Suite
900000–900031. Restores execute into isolated namespaces and are verified cryptographically.

---

### Configuration Drift
**DSU Shorthand:** Distinction drift

**Definition:** The divergence of a system's actual configuration from its declared baseline,
caused by manual changes, partial deployment, or inconsistent application of controls across
environments.

**Governing Standard:**
- ISO/IEC 27001:2022 §8.9 — *Configuration management* requires that baseline configurations
  be maintained and deviations detected and remediated.
- NIST SP 800-53 Rev 5 CM-2 — *Baseline Configuration* mandates that configuration baselines
  be established and changes be controlled to prevent unauthorized drift.

**In DSU:** Configuration drift is prevented through the Idempotency Contract — every playbook
run produces `changed=0` on a converged host — and through profile-locked security variables
that cannot be overridden at runtime. See [../wiki_pages/QUALITY_IDEMPOTENCY_BLOCKERS](QUALITY_IDEMPOTENCY_BLOCKERS).

---

### Ephemeral Credentials
**DSU Shorthand:** Volatile Secrets

**Definition:** Cryptographic keys or secrets stored exclusively in volatile memory (RAM) with no
persistence to disk, automatically destroyed on system shutdown, reboot, or a defined lifecycle
event.

**Governing Standard:**
- NIST SP 800-57 Part 1 Rev 5 §5.3 — *Cryptoperiod* defines the principle that key material
  must be destroyed when no longer needed. Volatile storage enforces automatic destruction.
- ISO/IEC 27001:2022 §8.24 — *Use of cryptography* requires that cryptographic keys be protected
  against unauthorized access and destroyed securely.

**In DSU:** Ephemeral credentials are implemented as SOPS-managed secrets backed by a 64 MB
RAM-disk (`tmpfs`), managed by `core/secrets` with TPM integrity attestation from
`security/tpm_guard`.

---

### Separation of Concerns
**Formal Term:** Separation of Concerns (SoC)  
**DSU Shorthand:** None (historical: "Separation of Concerns")

**Definition:** The architectural principle that each software component addresses exactly one
distinct concern, with no component managing responsibilities that belong to another. A concern
is a distinct aspect of functionality that can be defined independently and changed without
affecting other components.

**Governing Standard:**
- ISO/IEC 25010:2011 §4.2.7 — *Modularity* defines this quality characteristic as the degree
  to which a system is composed of discrete components such that a change to one has minimal
  impact on others.
- ISO/IEC 27001:2022 §8.9 — *Configuration management* establishes that components must have
  clearly bounded responsibilities to enable accurate configuration baseline management.
- NIST SP 800-53 Rev 5 SA-8 — *Security and Privacy Engineering Principles* explicitly lists
  Separation of Concerns as a required design principle for secure systems.

**Origin:** Formally stated by Edsger W. Dijkstra in *On the Role of Scientific Thought* (1974).

**In DSU:** Separation of Concerns is the primary term used throughout documentation. SoC is
enforced at three levels: task (one module call, one action), role (one role, one technology
concern), and playbook (one playbook, one infrastructure concern). See
[SEPARATION_OF_CONCERNS](SEPARATION_OF_CONCERNS).

---

### Security Observability
**DSU Shorthand:** Forensic Intelligence

**Definition:** The continuous collection, aggregation, indexing, and visualization of
security-relevant event data to enable real-time detection, investigation, and audit of system
behavior. Commonly implemented as a Security Information and Event Management (SIEM) system.

**Governing Standard:**
- ISO/IEC 27001:2022 §8.15 — *Logging* and §8.16 — *Monitoring activities* together define the
  requirement for continuous collection and review of security-relevant events.
- ISO/IEC 27037:2012 — Establishes principles for digital evidence integrity in monitoring
  contexts.

**In DSU:** Implemented by the Forensic Suite (Audit Event Identifiers 840030–840041) using Loki
as the aggregation engine, Promtail as the collector, and Grafana as the visualization layer.
Deployed by `containers/monitoring`.

---

### AI-Assisted Anomaly Detection
**DSU Shorthand:** Cognitive Sentinel

**Definition:** An automated process applying machine learning or language model inference to
security event streams to identify patterns indicative of unauthorized activity, policy
violations, or system compromise.

**Governing Standard:**
- ISO/IEC 27001:2022/Amd 1:2024 — *AI Security* addresses the use of AI systems in security
  monitoring contexts, including requirements for model integrity verification and output
  auditability.

**In DSU:** Planned capability mapped to Audit Event Identifier Suite 480000–480010 (Threat
Analysis Suite). Implementation target is `security/automated_threat_analysis`. Currently in
development; see [../wiki_pages/PLAN_SECURITY_ENHANCEMENT_PLAN_2026](PLAN_SECURITY_ENHANCEMENT_PLAN_2026).

---

## Confirmed ISO/Industry Standard Terms

The following terms are used correctly in DSU documentation. No mapping required. Listed here
to confirm their standard origin and prevent unnecessary renaming.

| Term | Governing Standard |
|---|---|
| Defense-in-Depth | ISO/IEC 27001:2022, NIST SP 800-39 §2.3 |
| Fail-Secure | IEC 61508-1:2010, NIST SP 800-160 Vol 1 |
| Least Privilege | ISO/IEC 27001:2022 §8.2, NIST SP 800-53 AC-6 |
| Hardware Root of Trust (HRoT) | NIST SP 800-193, TCG Architecture Specification |
| Post-Quantum Cryptography (PQC) | NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) |
| CNSA 2.0 | NSA Commercial National Security Algorithm Suite 2.0 |
| Mandatory Access Control (MAC) | ISO/IEC 27001:2022 §8.3, NIST SP 800-53 AC-3 |
| Software Bill of Materials (SBOM) | ISO/IEC 5962:2021 (SPDX), NIST SP 800-161 |
| ICT Supply Chain Risk Management | ISO/IEC 27001:2022 A.5.21, NIST SP 800-161 |
| Idempotency | ISO/IEC 25010:2011 (Reliability sub-characteristic), IaC industry standard |
| Configuration Baseline | ISO/IEC 27001:2022 §8.9, NIST SP 800-53 CM-2 |
| Digital Forensic Readiness | ISO/IEC 27037:2012, ISO/IEC 27042:2015 |

---

## ISO 9001 Document Classification Codes

Role categories in `meta/main.yml` use ISO 9001 Quality Management System document type
prefixes. These are standard ISO 9001 classifications, not DSU inventions.

| Code | ISO 9001 Document Type | DSU Usage |
|---|---|---|
| `POL-SEC` | Policy | Security policy enforcement roles (e.g., `security/sshd`) |
| `SOP-OPS` | Standard Operating Procedure | Operational roles (e.g., `ops/monitoring`) |
| `WI-CONT` | Work Instruction | Container configuration roles (e.g., `containers/runtime`) |
| `STD-CORE` | Standard | Core infrastructure roles (e.g., `core/logging`) |
