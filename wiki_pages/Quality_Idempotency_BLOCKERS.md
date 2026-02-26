# Idempotency Blockers

**Audit date:** 2026-02-03  
**Scope:** `deploy-system-unified` (all roles + branch templates)  
**Method:** Static analysis (repo scan + YAML parse). No playbooks executed.

This document lists **hard blockers** (things that can make a run fail or silently do the wrong thing) and **idempotency breakers** (things that always change, always restart, or drift every run), with **concrete fixes**.

---

## Fix Patterns (Use These Everywhere)

1. **Prefer Ansible modules** over `shell`/`command` whenever possible.
2. **Only use `ansible.builtin.command`** for real executables.
   - `command -v ...` is a shell builtin, not an executable.
   - Redirects like `> /dev/null` and operators like `|` / `&&` require `shell`, not `command`.
3. **If you use `set -o pipefail`**, force bash:
   - Add `args: { executable: /bin/bash }`
   - Or remove `pipefail` and structure the command so failure is explicit.
4. **For "check" commands**, set `changed_when: false`.
5. **For "do" commands**, gate them with `creates:`/`removes:` or a prior check + conditional.

---

## Critical Blockers

### POSIX Syntax Issues {#posix-syntax-issues}

**Problem:** Shell commands using POSIX syntax that fails under `/bin/sh`.

**Common patterns:**
```yaml
# WRONG - pipefail requires bash
- name: Check something
  command: set -o pipefail && some_command | grep pattern
  
# CORRECT - specify bash explicitly
- name: Check something
  command: set -o pipefail && some_command | grep pattern
  args:
    executable: /bin/bash
```

**Fix:** Always use `args: { executable: /bin/bash }` when using bash-specific features.

---

### Shell Command Issues {#shell-command-issues}

**Problem:** Using `command` module for shell builtins or complex pipelines.

**Common patterns:**
```yaml
# WRONG - command -v is a shell builtin
- name: Check if binary exists
  command: command -v binary_name
  
# CORRECT - use shell module
- name: Check if binary exists
  shell: command -v binary_name
  changed_when: false
  
# WRONG - pipe requires shell
- name: Count processes
  command: ps aux | grep myapp | wc -l
  
# CORRECT - use shell
- name: Count processes
  shell: ps aux | grep myapp | wc -l
  changed_when: false
```

**Fix:** Use `shell` module for builtins, pipes, and redirects.

---

### Ansible Module Issues {#ansible-module-issues}

**Problem:** Using wrong module for the task or missing idempotency guards.

**Common patterns:**
```yaml
# WRONG - template always reports changed
- name: Deploy config
  template:
    src: config.j2
    dest: /etc/app/config
    
# CORRECT - add proper ownership and mode
- name: Deploy config
  template:
    src: config.j2
    dest: /etc/app/config
    mode: '0644'
    owner: root
    group: root
```

**Fix:** Use appropriate modules with full parameter specification.

---

## Idempotency Breakers

### Timestamp Issues {#timestamp-issues}

**Problem:** Tasks that embed timestamps or dates always report changed.

**Common patterns:**
```yaml
# WRONG - timestamp in content
- name: Write config
  copy:
    content: "Generated at {{ ansible_date_time.iso8601 }}"
    dest: /etc/app/config

# CORRECT - static content only
- name: Write config
  copy:
    content: "Static configuration"
    dest: /etc/app/config
```

**Fix:** Never include dynamic values in file content unless required.

---

### Randomization Issues {#randomization-issues}

**Problem:** Tasks generating random values always report changed.

**Common patterns:**
```yaml
# WRONG - random password every run
- name: Generate password
  set_fact:
    password: "{{ lookup('password', '/dev/null') }}"

# CORRECT - store and reuse
- name: Read existing password
  slurp:
    src: /etc/app/.password
  register: existing_password
  failed_when: false
  
- name: Generate password if missing
  set_fact:
    password: "{{ lookup('password', '/dev/null') }}"
  when: existing_password is not defined
```

**Fix:** Persist random values and reuse on subsequent runs.

---

### Service Restart Issues {#service-restart-issues}

**Problem:** Handlers triggered unnecessarily or services restarted every run.

**Common patterns:**
```yaml
# WRONG - restart every run
- name: Restart service
  systemd:
    name: myapp
    state: restarted
    
# CORRECT - only restart on config change
- name: Deploy config
  template:
    src: config.j2
    dest: /etc/myapp/config
  notify: restart_myapp
  
handlers:
  - name: restart_myapp
    systemd:
      name: myapp
      state: restarted
```

**Fix:** Use handlers triggered only by actual changes.

---

## Remediation Steps

### Automated Fixes {#automated-fixes}

The following issues can be fixed automatically via linting:

1. **DSU003 violations** - Replace `CHANGE_ME` comparisons with defensive patterns
2. **Missing `changed_when: false`** - Add to check commands
3. **Deprecated `with_items`** - Replace with `loop`

Run `make lint-fix` to apply automated fixes.

---

### Manual Fixes {#manual-fixes}

The following issues require manual review:

1. **Timestamp in content** - Review and remove dynamic values
2. **Random value generation** - Implement persistence pattern
3. **Service restart logic** - Convert to handler pattern
4. **Shell vs command** - Review and use appropriate module

Review each task flagged by `ansible-lint` and apply the fix patterns above.

---

## Related Documents

- **[TERMINOLOGY](TERMINOLOGY)** — Formal definitions including "Configuration Drift"
- **[Quality_Idempotency_BLOCKERS](Quality_Idempotency_BLOCKERS)** — This document
- **[DSU_ACTION_CODES_COMPLETE](DSU_ACTION_CODES_COMPLETE)** — Audit Event Identifier 600151 (Idempotency check)
