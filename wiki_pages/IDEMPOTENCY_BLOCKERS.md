# IDEMPOTENCY_BLOCKERS

Audit date: 2026-02-03  
Scope: `deploy-system-unified` (all roles + branch templates)  
Method: static analysis (repo scan + YAML parse). No playbooks executed.

This document lists **hard blockers** (things that can make a run fail or silently do the wrong thing) and **idempotency breakers** (things that always change, always restart, or drift every run), with **concrete fixes**.

## Fix Patterns (Use These Everywhere)

1. Prefer Ansible modules over `shell`/`command` whenever possible.
2. Only use `ansible.builtin.command` for real executables.
   - `command -v ...` is a shell builtin, not an executable.
   - Redirects like `> /dev/null` and operators like `|` / `&&` require `shell`, not `command`.
3. If you use `set -o pipefail`, force bash:
   - Add `args: { executable: /bin/bash }`
   - Or remove `pipefail` and structure the command so failure is explicit.
4. For “check” commands, set `changed_when: false`.
5. For “do” commands, gate them with `creates:`/`removes:` or a prior check + conditional.

## Critical Blockers

### 1. Broken POSIX test syntax (`[ ... ]`) in multiple shell scripts

**Problem:** Several tasks use invalid test syntax like `if [-n "$X"]; then` or `if ["$X" != "Y"]; then`. The `[` command requires spaces around `[` and `]`.

**Impact:** These tasks either **never run their “then” branch** (silent no-op) or behave unpredictably. In a few cases, it can cause **non-idempotent behavior** (e.g., re-randomizing SSH ports).

**Files (examples):**

1. `roles/ops/pre_connection/tasks/main.yml`  
   - `if ["$CURRENT_PORT" != "22"] && [-n "$CURRENT_PORT"]; then`
2. `roles/hardware/virtual_guest/tasks/providers/generic_cloud.yml`  
   - `if [-n "$PRIMARY_IF"]; then`
3. `roles/hardware/virtual_guest/tasks/providers/contabo.yml`  
   - `if [-n "$PRIMARY_IF"]; then`
4. `roles/hardware/sas/tasks/main.yml`  
   - `if [-e "$dev/device/queue_depth"]; then`  
   - `if ["$target" -gt "$max"]; then`  
   - `if ["$current" -lt "$target"]; then`
5. `roles/core/memory/tasks/main.yml`  
   - `elif ["$(lspci ...)" -eq 1] && ...; then`
6. `roles/core/secrets/tasks/main.yml`  
   - `if [-f "$encrypted_file"] && [-s "$encrypted_file"]; then`
7. `roles/security/sandboxing/tasks/main.yml`  
   - `dmesg | grep -i landlock || [-c /dev/landlock]`

**How to fix:** Replace with POSIX-correct tests:

```sh
# Bad
if [-n "$PRIMARY_IF"]; then

# Good (POSIX sh)
if [ -n "$PRIMARY_IF" ]; then
```

```sh
# Bad
if ["$CURRENT_PORT" != "22"] && [-n "$CURRENT_PORT"]; then

# Good
if [ "$CURRENT_PORT" != "22" ] && [ -n "$CURRENT_PORT" ]; then
```

### 2. Misuse of `ansible.builtin.command` for shell builtins and redirection

**Problem:** `ansible.builtin.command` does not run a shell. It cannot evaluate:

1. Shell builtins like `command -v`
2. Redirects like `> /dev/null 2>&1`
3. Pipelines like `| grep ...`
4. Operators like `&&`

**Impact:** False negatives, broken validations, or tasks that silently don’t do what they claim. This can halt deployments (assertions) or skip security/encryption steps.

**Files (high impact):**

1. `roles/ops/preflight/tasks/main.yml`  
   - Required binaries check uses: `cmd: "command -v {{ item }}"`
2. `roles/security/secrets/tasks/main.yml`  
   - Builtin checks: `cmd: command -v sops`, `cmd: command -v ansible-vault`  
   - Redirect checks: `cmd: sops -d ... > /dev/null 2>&1`, `cmd: ansible-vault view ... > /dev/null 2>&1`
3. `roles/hardware/gpu/handlers/main.yml`  
   - `ansible.builtin.command: udevadm control --reload-rules && udevadm trigger` (uses `&&`)
4. `roles/containers/lxc/tasks/vendor/amd_sriov.yml`  
   - `cmd: lspci ... | grep ... | grep ...`
5. Branch templates (these are runnable playbooks too):  
   - `branch_templates/k8s_gpu_node.yml` / `branch_templates/k8s_gpu_worker.yml` / `branch_templates/k8s_gpu_workload.yml`  
   - `branch_templates/gpu_slicing_virtual_host.yml` / `branch_templates/gpu_slicing_virtual_guest.yml`

**How to fix:**

Option A (preferred): Use `shell` when you truly need shell features.

```yaml
- name: Check if sops exists
  ansible.builtin.shell: "command -v sops"
  register: sops_check
  changed_when: false
  failed_when: false
```

Option B: Remove redirects/pipes and run real executables with `command`, using `no_log: true` for secrets:

```yaml
- name: Validate SOPS file (no stdout printing)
  ansible.builtin.command:
    cmd: sops -d "{{ item.path }}"
  register: sops_validation
  changed_when: false
  failed_when: false
  no_log: true
```

Option C: Split `&&` into separate `command` steps (or use `shell`).

## Bash-Only Features Used Under `/bin/sh`

### 3. `set -o pipefail` used without forcing bash

**Problem:** `ansible.builtin.shell` uses `/bin/sh` by default; on many distros `/bin/sh` is `dash` (no `pipefail`).

**Impact:** The shell snippet fails immediately, and downstream asserts can halt a run.

**Files:**

1. `roles/security/scanning/tasks/main.yml`
2. `roles/security/audit_integrity/tasks/main.yml`
3. `roles/security/sandboxing/tasks/main.yml`

**How to fix:**

Option A: Force bash.

```yaml
ansible.builtin.shell: |
  set -o pipefail
  ...
args:
  executable: /bin/bash
```

Option B: Remove `pipefail` and avoid relying on pipeline exit codes.

## High-Risk Idempotency Breakers

### 4. SSH port “idempotent” detection can re-randomize ports

**File:** `roles/ops/pre_connection/tasks/main.yml`

**Problem:** The “existing port” detection is broken (see invalid test syntax). If it always returns empty, the subsequent logic can generate a new random port on every controller run.

**How to fix:**

1. Fix test syntax.
2. Prefer reading the effective port via `sshd -T` if available:

```sh
CURRENT_PORT="$(sshd -T 2>/dev/null | awk '/^port /{print $2; exit}')"
```

3. If randomization is enabled, persist the chosen port to a controller-side checkpoint and reuse it.

### 5. LXC GPU passthrough apply always “changes” and can restart every run

**File:** `roles/containers/lxc/tasks/main.yml`

**Problems:**

1. `lxc config set ...` is constructed in a way that’s unlikely to be valid (multiple entries joined by `;`).
2. `changed_when: true` + `failed_when: false` marks success even on failure.
3. Restart step is conditioned on `.changed` which is forced true → restarts each run.

**How to fix:**

1. Build a single `raw.lxc` value and set it once.
2. Compare existing config to desired before applying.
3. Use `changed_when` based on actual drift.

### 6. Btrfs subvolume creation condition is incorrect

**File:** `roles/storage/filesystems/btrfs/tasks/subvolumes.yml`

**Problem:** `item.item.path is not directory` is not a reliable remote-state test here.

**How to fix:** `stat` the path (remote) and create only when absent, or query `btrfs subvolume list` for existence.

## Noisy “Always Changed” Tasks (Not Always Dangerous, But Break Molecule Idempotency)

### 7. Always-changed commands

**Files:**

1. `roles/containers/config/tasks/main.yml`  
   - `loginctl enable-linger ...` has `changed_when: true`
2. `roles/security/hardening/tasks/main.yml`  
   - sticky-bit find/chmod uses `changed_when: sticky_result.rc == 0` (always “changed” on success)

**How to fix:**

1. Check current state first (e.g., `loginctl show-user USER -p Linger`), apply only on drift.
2. For “bulk chmod” tasks, set `changed_when: false` or emit a count of changed paths and use that.

### 8. Intentional drift: checkpoint timestamps

**Files:**

1. `tasks/SAVE_CHECKPOINT.YML`
2. `roles/containers/quadlets/tasks/main.yml`

**Problem:** Timestamp fields guarantee file content changes every run.

**How to address (choose one):**

1. Accept the drift (document it; don’t run idempotency tests with checkpoints enabled).
2. Set `changed_when: false` on checkpoint writes.
3. Only update `timestamp` when the payload actually changed (compare old vs new).

## Known Logic Bugs That Cause Silent No-Ops

### 9. Networking “jumbo frames” condition references the wrong fact

**File:** `roles/networking/physical/tasks/main.yml`

**Problem:** Condition uses `item.value.speed`, but the parsed fact is `speed_mbps`. This makes the jumbo-frame branch unreliable.

**How to fix:** Use `item.value.speed_mbps` consistently and validate `port_type` parsing (current regex only captures the first word).

## Recommended Next Steps

1. Fix the **Critical Blockers** first (broken `[ ... ]` tests, `command` vs `shell`, `pipefail` portability).
2. Add a Molecule scenario (or a basic CI job) that runs the core roles in `--check` mode and a second run for idempotency.
3. Add a lint rule to prevent reintroducing these:
   - Reject `ansible.builtin.command` tasks whose `cmd` contains `|`, `>`, `&&`, `$(`.
   - Reject shell scripts containing `if [-` / `if ["` patterns.

---

# Red Team Findings (Security Risks That Need Addressing)

This section focuses on **security posture**, not just idempotency. Items here are likely to be flagged in a red‑team assessment.

## 1. Secrets embedded in world‑readable unit files

**Problem:** Several Quadlet/systemd container definitions embed secrets directly in `Environment=` lines, and those files are written with `mode: '0644'`. This makes secrets readable by any local user.

**Examples:**

- `roles/containers/monitoring/templates/grafana.container.j2`  
  - `Environment=GF_SECURITY_ADMIN_PASSWORD={{ monitoring_grafana_admin_password }}`
- `roles/containers/authentik/tasks/main.yml`  
  - `Environment=AUTHENTIK_SECRET_KEY={{ authentik_secret_key }}`
  - `Environment=AUTHENTIK_EMAIL__PASSWORD={{ authentik_email_password }}`
  - `Environment=POSTGRES_PASSWORD={{ authentik_pg_pass }}`
- `roles/containers/caddy/tasks/main.yml`  
  - `Environment=PORKBUN_API_KEY={{ porkbun_api_key }}`
  - `Environment=PORKBUN_SECRET_API_KEY={{ porkbun_secret_api_key }}`

**Impact:** Any local user can read secrets from `/etc/containers/systemd/*.container`.

**Fix:**

- Move secrets into `EnvironmentFile` with `0600` permissions.
- Or use Podman secrets / systemd credentials (`LoadCredential`).
- Change Quadlet file mode to `0640` or `0600` if secrets must remain inline.

## 2. Placeholder/weak secrets are not enforced

**Problem:** Defaults include placeholder values that are not validated or rejected.

**Examples:**

- `roles/containers/authentik/defaults/main.yml`:  
  - `authentik_secret_key: "generate_me_with_openssl_rand_base64_60"`
- `roles/containers/caddy/templates/firewall-bouncer.yaml.j2`:  
  - `api_key: {{ crowdsec_firewall_bouncer_key | default('CHANGE_ME') }}`

**Impact:** Deployments can run with predictable/unsafe secrets.

**Fix:**

- Add `assert` tasks that fail if placeholders are detected.
- Or auto‑generate secrets on first run and store them in encrypted secrets storage.

## 3. Supply‑chain risk: unverified downloads and source builds

**Problem:** Several tasks fetch or build critical binaries without checksum/GPG verification or version pinning.

**Examples:**

- `roles/containers/caddy/tasks/main.yml`  
  - Downloads `crowdsec-firewall-bouncer` tarball from GitHub without checksum verification.
- `roles/containers/runtime/tasks/slicing/oneapi.yml`  
  - `curl ... | apt-key add -` + adds repo, no key verification, no pinning.
- `roles/containers/lxc/tasks/vendor/intel_oneapi.yml`  
  - Same pattern as above.
- `roles/networking/services/endlessh/tasks/main.yml`  
  - Clones `master` and builds as root, no commit pin.

**Impact:** Remote code execution via compromised upstream or MITM.

**Fix:**

- Pin versions and verify checksums/GPG signatures.
- Avoid `curl | apt-key add -`; use a signed keyring with `signed-by=` in the source list.
- Prefer distro packages when available.

## 4. Secrets tooling detection can fail silently

**Problem:** Use of `command -v` with `ansible.builtin.command` (a shell builtin) can incorrectly report missing tools.

**Files:**

- `roles/ops/preflight/tasks/main.yml`
- `roles/security/secrets/tasks/main.yml`
- `roles/security/scanning/tasks/enhanced_security_with_required_tools.yml`

**Impact:** Security tooling is skipped even when installed; encryption method selection is wrong.

**Fix:**

- Switch to `ansible.builtin.shell` or check binaries by absolute path.
- Example: `ansible.builtin.shell: "command -v sops"` with `changed_when: false`.

## 5. Controller‑side secrets handling (temp files)

**Problem:** Some roles create temp files with sensitive data on the controller (delegate_to localhost).

**Examples:**

- `roles/ops/connection_info/tasks/main.yml`
- `roles/security/audit_integrity/tasks/main.yml`

**Impact:** Leaked secrets if controller is shared or if temp files persist.

**Fix:**

- Ensure temp files are created with `0600`, stored outside `/tmp` when possible, and removed immediately after encryption.
- For multi‑host runs, avoid `run_once` for per‑host secrets unless you intentionally want only a single host’s output.

## 6. Network exposure by design (Host networking + no port gating)

**Problem:** Many services run with `Network=host`, meaning any exposed service binds directly to the host interface.

**Impact:** If firewall rules are absent or misconfigured, services are exposed to the public Internet.

**Fix:**

- Enforce firewall rules for each service.
- Or use bridge networking with explicit publishes and a dedicated reverse proxy network.

---

If you want, I can convert these into specific patch sets (e.g., “Secrets Hardening”, “Supply‑Chain Hardening”) and apply them.  
