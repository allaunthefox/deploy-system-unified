# CIS Benchmark Mapping

**Audit Event Identifier:** DSU-DOC-190010  
**Last Updated:** 2026-03-01  
**Status:** 🏗️ In Progress

This document tracks the alignment of **Deploy-System-Unified** security controls with the Center for Internet Security (CIS) Benchmarks.

---

## 📊 Mapping Summary

| Benchmark | Level | Implemented | Coverage | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Ubuntu Linux 22.04 LTS** | 1 | 45/50 | 90% | 🏗️ Mapping |
| **Debian Linux 12** | 1 | 41/48 | 85% | 🏗️ Mapping |
| **Red Hat Enterprise Linux 9** | 1 | 38/52 | 73% | 🏗️ Mapping |
| **CIS Docker Benchmark** | 1 | 20/22 | 91% | 🏗️ Mapping |

---

## 🛠️ Control Mapping (System Hardening)

| CIS ID | Control Description | DSU Role | Implementation Status |
| :--- | :--- | :--- | :--- |
| **1.1.1** | Ensure security-related packages are installed | `security/hardening` | ✅ Standardized |
| **1.1.2** | Ensure mounting of unused filesystems is disabled | `security/hardening` | ✅ Standardized |
| **1.1.8** | Ensure system accounts are locked | `security/hardening` | ✅ Standardized |
| **4.1.1** | Ensure auditd service is enabled and started | `security/hardening` | ✅ Standardized |
| **5.3.6** | Ensure account lockout is configured (pam_faillock) | `security/hardening` | ✅ Standardized |
| **6.1.1** | Ensure PAM configuration is hardened | `security/hardening` | ✅ Standardized |
| **8.1.2** | Ensure wireless interfaces are disabled | `security/hardening` | ✅ Standardized |

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

## 🛠️ Control Mapping (Network Configuration)

| CIS ID | Control Description | DSU Role | Implementation Status |
| :--- | :--- | :--- | :--- |
| **4.4.1** | Ensure firewall software is installed | `networking/firewall` | ✅ Standardized |
| **4.4.2** | Ensure firewall port list is built | `networking/firewall` | ✅ Standardized |
| **4.4.3** | Ensure firewall configuration is supported | `networking/firewall` | ✅ Standardized |
| **4.4.1.1** | Ensure firewall default policies are configured | `networking/firewall` | ✅ Standardized |
| **4.4.1.2** | Ensure firewall default forward policy is set | `networking/firewall` | ✅ Standardized |
| **4.4.1.3** | Ensure firewall rules are imported | `networking/firewall` | ✅ Standardized |
| **4.4.1.4** | Ensure firewall is enabled | `networking/firewall` | ✅ Standardized |

---

## ⚠️ Known Gaps

- **[GAP-CIS-001]**: CIS 1.1.1.1 - Ensure mounting of cramfs filesystems is disabled (Verification needed on RHEL9).
- **[GAP-CIS-002]**: CIS 4.1.1.1 - Ensure auditd is installed (Mapping needed for specific RHEL sub-packages).

---

## 🛡️ Next Actions

1. Implement `compliance_framework_enable` logic in `preflight`.
2. Conduct Goss POC for automated verification of mapped controls.
3. Integrate HashiCorp Vault for centralized secret distribution.
