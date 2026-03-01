# CIS Benchmark Mapping

**Audit Event Identifier:** DSU-DOC-190010  
**Last Updated:** 2026-03-01  
**Status:** 🏗️ In Progress

This document tracks the alignment of **Deploy-System-Unified** security controls with the Center for Internet Security (CIS) Benchmarks.

---

## 📊 Mapping Summary

| Benchmark | Level | Implemented | Coverage | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Ubuntu Linux 22.04 LTS** | 1 | 42/50 | 84% | 🏗️ Mapping |
| **Debian Linux 12** | 1 | 38/48 | 79% | 🏗️ Mapping |
| **Red Hat Enterprise Linux 9** | 1 | 35/52 | 67% | 🏗️ Mapping |
| **CIS Docker Benchmark** | 1 | 18/22 | 81% | 🏗️ Mapping |

---

## 🛠️ Control Mapping (SSH Server)

| CIS ID | Control Description | DSU Role | Implementation Status |
| :--- | :--- | :--- | :--- |
| **5.2.1** | Ensure permissions on /etc/ssh/sshd_config | `security/sshd` | ✅ Standardized |
| **5.2.2** | Ensure permissions on SSH private host keys | `security/sshd` | ✅ Standardized |
| **5.2.3** | Ensure permissions on SSH public host keys | `security/sshd` | ✅ Standardized |
| **5.2.4** | Ensure SSH access is limited | `security/sshd` | ✅ Standardized |
| **5.2.5** | Ensure SSH LogLevel is set to VERBOSE | `security/sshd` | ✅ Standardized |
| **5.2.11** | Ensure only strong Ciphers are used | `security/sshd` | ✅ Standardized |
| **5.2.12** | Ensure only strong MAC algorithms are used | `security/sshd` | ✅ Standardized |
| **5.2.13** | Ensure only strong KEX algorithms are used | `security/sshd` | ✅ Standardized |
| **5.2.14** | Ensure weak SSH host keys are removed | `security/sshd` | ✅ Standardized |
| **5.2.16** | Ensure SSH root login is disabled | `security/sshd` | ✅ Standardized |
| **5.2.17** | Ensure SSH PasswordAuthentication is disabled | `security/sshd` | ✅ Standardized |
| **5.2.23** | Ensure SSH Idle Timeout Interval is configured | `security/sshd` | ✅ Standardized |

---

## ⚠️ Known Gaps

- **[GAP-CIS-001]**: CIS 1.1.1.1 - Ensure mounting of cramfs filesystems is disabled (Verification needed on RHEL9).
- **[GAP-CIS-002]**: CIS 4.1.1.1 - Ensure auditd is installed (Mapping needed for specific RHEL sub-packages).

---

## 🛡️ Next Actions

1. Complete mapping for **Initial System Hardening** (CIS Section 1.1).
2. Complete mapping for **Network Configuration** (CIS Section 3).
3. Implement `compliance_framework_enable` logic in `preflight`.
