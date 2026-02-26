# Forensic Documentation Standard (DSU-6767)

**Standard**: DSU-6767-F  
**Scope**: All Ansible Roles & Playbooks  
**Compliance**: ISO 27001 §12.4, ISO 27037

---

## 📖 Overview

This document defines the mandatory forensic metadata required for every critical task in the **Deploy-System-Unified** project. Adherence to this standard ensures that all infrastructure changes generate a high-fidelity auditable trace in our **Loki/Grafana** dashboards.

---

## 🧩 The Naming Pattern

All critical tasks MUST follow this exact string format:

`[Standard] | [Audit Event Identifier] | [Task Name]`

### 1. Standard (The Why)
The compliance control that justifies the action.
- Examples: `ISO 27001 §10.1`, `NIST IA-2`, `CIS 1.1.1`

### 2. Audit Event Identifier (The What)
A unique 6-digit code from the `DSU_AUDIT_EVENT_IDENTIFIERS.md` catalog.
- `3xxxxx`: System Lifecycle
- `4xxxxx`: Security Operations
- `5xxxxx`: IDENTITY / App Ops
- `6xxxxx`: Deployment / Idempotency
- `7xxxxx`: Containers
- `8xxxxx`: Hardware / Platform
- `9xxxxx`: Backup / Recovery

### 3. Task Name (The Description)
A concise, human-readable description of the action.

---

## 🛠️ Implementation Example

**Incorrect:**
```yaml
- name: Install auditd
  ansible.builtin.package:
    name: auditd
```

**Correct (DSU Standard):**
```yaml
- name: "ISO 27001 §12.4 | 840040 | Ensure auditd package is installed"
  ansible.builtin.package:
    name: auditd
```

---

## 🔍 Validation

The **Forensic Naming Enforcer** (GitHub Action) automatically scans all PRs for this pattern. Tasks that lack a valid code or standard will fail the build.

### How to choose a code:
1. Open `DSU_AUDIT_EVENT_IDENTIFIERS.md`.
2. Search for your task's intent (e.g., "firewall", "user create").
3. Copy the corresponding code and ISO section.

---

*Verified by: DSU Security Auditor*
*Last Updated: February 2026*
