# HARDENING_ENFORCEMENT_PLAN_2026 (STRICT MANDATE)

**Status:** **ACTIVE MANDATE**
**Principle:** "One Failure is Total Failure"
**Scope:** Absolute hardening of all production and hardened workloads.

---

## 📋 Guiding Principle: Zero-Tolerance Security

In a security-first infrastructure, a single misconfigured sysctl, an unverified binary, or a silent failure in a permission change is a total system failure. This plan mandates the transition from "Best Effort" hardening to "Strict Enforcement."

---

## 🎯 Track 1: Fail-Stop Hardening (Zero-Tolerance)

**Objective:** Eliminate silent failures in security tasks.

| Mandate | Implementation Rule | Status |
| :--- | :--- | :--- |
| **No Silent Failures** | Remove all `failed_when: false` and `ignore_errors` from `roles/security`. | 🚨 **ENFORCING** |
| **Post-Task Verification** | Every hardening task MUST be followed by an `assert` task verifying the state. | 🚨 **ENFORCING** |
| **LSM Enforcement** | Fail deployment if required LSMs (AppArmor, Landlock, Yama) are inactive. | 🚨 **ENFORCING** |

### 🛠️ Example: Strict Sysctl Enforcement
```yaml
- name: "STRICT | Apply kernel.kptr_restrict"
  ansible.posix.sysctl:
    name: "kernel.kptr_restrict"
    value: "2"
    state: present
    reload: true

- name: "VERIFY | kernel.kptr_restrict is enforced"
  ansible.builtin.shell: cat /proc/sys/kernel/kptr_restrict
  register: _kptr_val
  failed_when: _kptr_val.stdout != "2"
```

---

## 🛡️ Track 2: Supply Chain Integrity (Verified Provenance)

**Objective:** Prevent "Trust-on-First-Use" (TOFU) vulnerabilities.

### 2.1 Binary & Repository Integrity
- **Mandatory GPG**: No repository (Apt/Yum) may be added without `gpgkey` and `gpgcheck: yes`.
- **Digest Pinning**: All container images MUST use `sha256:` digests. Tags alone are insufficient.
- **Checksum Validation**: Every binary download (Vault, Falco, etc.) MUST have a hardcoded SHA256 checksum in `vars/main.yml`.

### 2.2 Image Signing
- **Cosign Enforcement**: Containers will not start unless `cosign verify` passes against the specific image digest.
- **SBOM Generation**: Fail deployment if `syft` or `trivy` cannot generate a signed SBOM for the current release.

---

## 🏗️ Track 3: Advanced Exploit Mitigation

**Objective:** Neutralize lateral movement and container escape.

### 3.1 Kernel Self-Protection
- **Lockdown Mode**: Mandatory `kernel.lockdown = confidentiality` for bare-metal hardened hosts.
- **Yama/Ptrace**: Strict `ptrace_scope = 1` or `2`. Any attempt to attach to a process by a non-parent will trigger a high-severity alert.
- **BPF Hardening**: `unprivileged_bpf_disabled = 1` and `bpf_jit_harden = 2` are mandatory.

### 3.2 Real-time Mitigation (Falco & Crowdsec)
- **Falco Blocking**: Transition Falco from "Monitor" to "Active Kill." Use `falco-sidekick` to terminate containers that attempt unauthorized syscalls or shell spawns.
- **Crowdsec Hybrid**: Enforce IP-blocklists at the XDP/ebpf layer before traffic reaches the application.

---

## 🔑 Track 4: Secrets Lifecycle & PQC

**Objective:** Eliminate long-lived secrets and quantum-vulnerability.

- **Dynamic Secrets**: Transition from static files to HashiCorp Vault dynamic engine (Short-lived 1hr TTL).
- **PQC-Everywhere**: Expand hybrid lattice cryptography (ML-KEM/ML-DSA) from SSH to internal TLS and VPN Mesh.
- **Memory Hardening**: Ensure `libpam-tmpdir` and `ramfs` are used for all decrypted secrets. Fail if secrets land on persistent storage.

---

## 🏗️ Track 5: Infrastructure-as-Code (IaC) Supply Chain

**Objective:** Secure the deployment toolchain itself.

- **Collection Pinning**: Mandatory `requirements.yml` with explicit versions for all community collections. Deployment MUST fail if an unpinned collection is detected.
- **Role Verification**: External roles (Galaxy) MUST be replaced with verified local copies or pinned to specific git commits with SHA256 verification.
- **Controller Hardening**: The Ansible controller (CI runner) is part of the TCB. It MUST be isolated, use ephemeral credentials, and undergo the same `lynis` audit as target hosts.

---

## 🧪 Track 6: Negative Testing (Chaos Security)

**Objective:** Prove that "Fail-Stop" actually stops the deployment.

- **Breaking Tests**: Implement automated tests that intentionally introduce misconfigurations (e.g., `PermitRootLogin yes`) and verify the deployment halts with an error.
- **Unauthorized Image Test**: Attempt to deploy an unsigned container image; verify that the Supply Chain Guard blocks the pull.
- **Rollback Verification**: Prove that a failed security check triggers a safe state (isolation or rollback) rather than leaving a "half-hardened" system.

---

## 🔍 Track 7: Forensic Metadata & Redaction

**Objective:** Ensure auditable deployments without leakage.

- **Deployment Provenance**: Every playbook run MUST generate a signed `provenance.json` containing: `operator_id`, `git_commit_sha`, `timestamp`, and `inventory_fingerprint`.
- **Zero-Leakage Logs**: Mandatory audit of all roles for `no_log: true` on tasks handling passwords, keys, or PII. Fail CI if a sensitive keyword is detected in a non-redacted task.
- **Immutable Trace**: Deployment logs MUST be streamed directly to Loki with a cryptographic seal, matching the system journal's integrity.

---

## 🔒 Track 8: Volatile Secret Infrastructure (RAM-only Env)

**Objective:** Eliminate plaintext secrets on persistent storage.

- **RAM-Disk Enforcement**: All decrypted `.env` files MUST reside on a `tmpfs` (RAM-disk) mount at `/run/secrets/dsu/`. 
- **Auto-Wipe**: Secrets MUST be automatically wiped on service stop or system reboot (inherent to `tmpfs`).
- **SOPS-to-RAM Pipeline**: Ansible MUST decrypt secrets from `secrets.sops.yml` and write them directly to the RAM-disk. Persistent `/var/lib/` or `/etc/` paths for plaintext secrets are FORBIDDEN in `hardened` profiles.
- **Zero-Footprint Audit**: VERIFY tasks MUST confirm that secret files do not exist on the underlying physical block device (SSD/HDD).

---

## 📊 Success Metrics (Total System)

- **Unpinned Dependency Count**: 0 (Collections, Roles, Images).
- **Negative Test Pass Rate**: 100% (The system reliably fails on insecurity).
- **Forensic Coverage**: 100% of deployment actions mapped to a verified operator and code version.

---

*This document serves as the absolute standard for all security-related PRs in 2026. Non-compliant code will be rejected.*
