# ROLE_ENHANCEMENT_EXECUTION_PLAN_2026

**Status:** Proposed (Q2-Q3 2026)
**Priority:** Critical
**Objective:** Elevate role implementation from **73/100** to **95+/100** while maintaining usability

---

## 📋 Executive Summary

This plan provides a detailed, actionable roadmap for enhancing all Deploy-System-Unified roles to achieve near-perfect implementation standards while preserving the project's usability and innovation advantages.

**Current State:** 73/100 (Good)
**Target State:** 95/100 (Excellent, industry-leading)
**Timeline:** 12 weeks (Q2-Q3 2026)
**Estimated Effort:** 120-160 hours

### Score Improvement Trajectory

| Week | Target Score | Focus Area |
|------|--------------|------------|
| 0 (Baseline) | 73/100 | Current state |
| 4 | 81/100 | Metadata & documentation |
| 8 | 88/100 | Testing framework |
| 12 | 95/100 | Compliance integration |
| 16+ | 98/100 | Continuous improvement |

---

## 🎯 Enhancement Tracks

### Track 1: Metadata & Documentation (Weeks 1-4)

**Objective:** Enhance all role metadata to industry-leading standards

**Current Score:** 70/100 → **Target:** 95/100

#### Task 1.1: Enhance meta/main.yml (Week 1-2)

**Scope:** All 81 roles

**Template:**

```yaml
# roles/<category>/<role>/meta/main.yml
---
galaxy_info:
  role_name: <role_name>
  author: deploy-system-unified
  description: <Clear, concise description of role purpose>
  company: Deploy-System-Unified Project
  license: MIT
  min_ansible_version: "2.15"
  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
        - noble
    - name: Debian
      versions:
        - bullseye
        - bookworm
    - name: Fedora
      versions:
        - '39'
        - '40'
    - name: Archlinux
      versions:
        - all
    - name: Alpine
      versions:
        - '3.18'
        - '3.19'
    - name: RockyLinux
      versions:
        - '9'
    - name: AlmaLinux
      versions:
        - '9'
  galaxy_tags:
    - <primary_category>      # e.g., security, core, containers
    - <function>              # e.g., hardening, bootstrap, runtime
    - <compliance>            # e.g., cis, stig, compliance (if applicable)
    - <technology>            # e.g., ssh, firewall, podman
    - <platform>              # e.g., linux, multiarch
    - security                # All security roles
    - hardening               # All hardening roles
    - infrastructure          # All infrastructure roles
    - automation              # All roles
    - deploy-system-unified   # Project identifier

collections:
  - ansible.builtin
  - community.general
  - community.crypto

dependencies: []
# Or if dependencies exist:
# dependencies:
#   - role: core/bootstrap
#   - role: core/identity
```

**Role-Specific Examples:**

```yaml
# roles/security/hardening/meta/main.yml
galaxy_info:
  role_name: hardening
  description: Core system security hardening with CIS benchmark alignment
  galaxy_tags:
    - security
    - hardening
    - cis
    - stig
    - compliance
    - system
    - linux
    - multiarch
    - infrastructure
    - deploy-system-unified

# roles/core/bootstrap/meta/main.yml
galaxy_info:
  role_name: bootstrap
  description: System initialization and base configuration with virtualization awareness
  galaxy_tags:
    - core
    - bootstrap
    - system
    - initialization
    - linux
    - multiarch
    - virtualization
    - infrastructure
    - deploy-system-unified

# roles/security/sshd/meta/main.yml
galaxy_info:
  role_name: sshd
  description: SSH daemon hardening with strong cryptography and access control
  galaxy_tags:
    - security
    - ssh
    - sshd
    - hardening
    - access_control
    - cryptography
    - cis
    - linux
    - network
    - deploy-system-unified
```

**Action Items:**
- [ ] Create meta/main.yml template
- [ ] Update 12 core roles
- [ ] Update 15 security roles
- [ ] Update 12 container roles
- [ ] Update 8 networking roles
- [ ] Update 6 storage roles
- [ ] Update 10 hardware roles
- [ ] Update 5 virtualization roles
- [ ] Update 4 kubernetes roles
- [ ] Update 6 ops roles
- [ ] Update 3 shared roles

---

#### Task 1.2: Add Argument Specs (Week 2-3)

**Scope:** All 81 roles

**Template:**

```yaml
# roles/<category>/<role>/meta/argument_specs.yml
---
argument_specs:
  main:
    short_description: <One-line description>
    description:
      - <Multi-line detailed description>
      - <Include key features>
      - <Include use cases>
    version_added: '1.0.0'
    author:
      - '@allaunthefox'
      - 'Deploy-System-Unified Team'
    options:
      <variable_name>:
        type: <str|int|bool|list|dict>
        description: '<Clear description of what this variable does>'
        required: <true|false>
        default: <default_value>
        choices:
          - <choice1>
          - <choice2>
        elements: <str|int|bool>  # For list types
        aliases:
          - <alternative_name>
        deprecated_aliases:
          - name: <old_name>
            version: '2.0.0'
            why: '<Reason for deprecation>'
            alternatives:
              - '<new_variable_name>'
    
    requirements:
      - python >= 3.8
      - ansible-core >= 2.15
    
    seealso:
      - module: ansible.builtin.<related_module>
      - ref: <Documentation reference>
        description: '<What the reference covers>'
```

**Example (security/hardening):**

```yaml
# roles/security/hardening/meta/argument_specs.yml
---
argument_specs:
  main:
    short_description: Core system security hardening role
    description:
      - Implements comprehensive system security hardening
      - Configures file permissions, user accounts, and PAM
      - Aligns with CIS Level 1 benchmarks
      - Supports multi-distribution deployments
    version_added: '1.0.0'
    author:
      - '@allaunthefox'
      - 'Deploy-System-Unified Team'
    options:
      security_hardening_enabled:
        type: bool
        description: Enable or disable security hardening
        required: false
        default: true
      
      security_enable_ufw:
        type: bool
        description: Enable UFW firewall management
        required: false
        default: true
      
      security_enable_fail2ban:
        type: bool
        description: Enable Fail2Ban intrusion prevention
        required: false
        default: true
      
      security_enable_auto_updates:
        type: bool
        description: Enable automatic security updates
        required: false
        default: true
      
      security_kernel_hardening:
        type: bool
        description: Enable kernel-level hardening (sysctl, etc.)
        required: false
        default: true
    
    requirements:
      - python >= 3.8
      - ansible-core >= 2.15
    
    seealso:
      - module: ansible.builtin.user
      - module: ansible.builtin.file
      - ref: LAYERED_SECURITY
        description: Defense-in-depth security model
```

**Action Items:**
- [ ] Create argument_specs template
- [ ] Document all variables for each role
- [ ] Add deprecation notices for legacy variables
- [ ] Link to related documentation

---

#### Task 1.3: Populate Handlers (Week 3-4)

**Scope:** All roles with empty handlers

**Template:**

```yaml
# roles/security/hardening/handlers/main.yml
---
- name: restart_auditd
  ansible.builtin.systemd:
    name: auditd
    state: restarted
  become: true
  when:
    - ansible_facts['service_mgr'] == 'systemd'
    - not (is_virtualized | default(false))

- name: reload_sysctl
  ansible.builtin.command:
    cmd: sysctl --system
  become: true
  changed_when: false

- name: restart_sshd
  ansible.builtin.systemd:
    name: "{{ 'ssh' if ansible_facts['os_family'] == 'Debian' else 'sshd' }}"
    state: restarted
  become: true
  when: ansible_facts['service_mgr'] == 'systemd'
```

**Common Handlers by Category:**

```yaml
# Core roles handlers
- name: reload_systemd
  ansible.builtin.systemd:
    daemon_reload: true

- name: restart_chrony
  ansible.builtin.systemd:
    name: chronyd
    state: restarted

# Security roles handlers
- name: restart_fail2ban
  ansible.builtin.systemd:
    name: fail2ban
    state: restarted

- name: restart_ufw
  ansible.builtin.systemd:
    name: ufw
    state: restarted

# Container roles handlers
- name: restart_podman
  ansible.builtin.systemd:
    name: podman
    state: restarted

- name: restart_caddy
  ansible.builtin.systemd:
    name: caddy
    state: restarted
```

**Action Items:**
- [ ] Audit all roles for missing handlers
- [ ] Create handlers for each role category
- [ ] Test handler notifications
- [ ] Document handler usage

---

#### Task 1.4: Populate Vars (Week 3-4)

**Scope:** All roles with empty vars

**Template:**

```yaml
# roles/security/hardening/vars/main.yml
---
# Internal variables - DO NOT OVERRIDE
# These are computed values and role-internal state

_hardening_packages_debian:
  - libpam-tmpdir
  - auditd
  - fail2ban
  - ufw

_hardening_packages_redhat:
  - audit
  - fail2ban
  - firewalld

_hardening_packages_arch:
  - audit
  - fail2ban
  - ufw

_sensitive_file_permissions:
  - { path: '/etc/shadow', mode: '0600' }
  - { path: '/etc/passwd', mode: '0644' }
  - { path: '/etc/group', mode: '0644' }
  - { path: '/etc/sudoers', mode: '0440' }

_system_accounts_to_lock:
  - bin
  - daemon
  - adm
  - lp
  - sync
  - shutdown
  - halt
  - mail
```

**Action Items:**
- [ ] Identify internal variables for each role
- [ ] Move complex defaults to vars
- [ ] Document vars vs. defaults distinction
- [ ] Add comments explaining computed values

---

### Track 2: Testing Framework (Weeks 5-8)

**Objective:** Implement comprehensive testing for all roles

**Current Score:** 60/100 → **Target:** 95/100

#### Task 2.1: Expand Molecule Scenarios (Week 5-6)

**Scope:** All 81 roles

**Enhanced Molecule Configuration:**

```yaml
# roles/<category>/<role>/molecule/default/molecule.yml
---
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml

driver:
  name: podman  # or docker

platforms:
  - name: ubuntu2204-${INSTANCE_UUID}
    image: docker.io/geerlingguy/docker-ubuntu2204-ansible:latest
    pre_build_image: true
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    command: /lib/systemd/systemd
    tmpfs:
      - /run
      - /tmp
    groups:
      - all
      - debian
      - ubuntu

  - name: debian12-${INSTANCE_UUID}
    image: docker.io/geerlingguy/docker-debian12-ansible:latest
    pre_build_image: true
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    command: /lib/systemd/systemd
    tmpfs:
      - /run
      - /tmp
    groups:
      - all
      - debian

  - name: alpine319-${INSTANCE_UUID}
    image: alpine:3.19
    pre_build_image: true
    command: /sbin/init
    tmpfs:
      - /run
      - /tmp
    groups:
      - all
      - alpine
    privileged: true

provisioner:
  name: ansible
  env:
    ANSIBLE_ROLES_PATH: ../../../../../
    ANSIBLE_VERBOSITY: ${ANSIBLE_VERBOSITY:-0}
  config_options:
    defaults:
      interpreter_python: auto_silent
      callback_whitelist: profile_tasks, timer
  lint: |
    set -e
    ansible-lint
  playbooks:
    converge: ${MOLECULE_PLAYBOOK:-converge.yml}
    verify: verify.yml

verifier:
  name: testinfra
  lint: |
    set -e
    pylint tests/
  options:
    connection: podman
    verbose: true

scenario:
  name: default
  test_sequence:
    - lint
    - destroy
    - dependency
    - syntax
    - create
    - prepare
    - converge
    - idempotence
    - verify
    - cleanup
    - destroy
```

**Action Items:**
- [ ] Update molecule.yml for all roles
- [ ] Add multi-platform testing (3+ distros)
- [ ] Configure Testinfra verifier
- [ ] Add linting integration

---

#### Task 2.2: Create Testinfra Tests (Week 6-8)

**Scope:** All 81 roles

**Test Template:**

```python
# roles/<category>/<role>/molecule/default/tests/test_<role>.py
"""
Test suite for <role_name> role.

This test suite verifies:
1. Package installation
2. Service status
3. Configuration file content
4. File permissions
5. Security controls
"""

import os
import testinfra
import pytest


def test_security_packages_installed(host):
    """Verify security packages are installed"""
    packages = {
        'Debian': ['auditd', 'libpam-tmpdir'],
        'RedHat': ['audit'],
        'Archlinux': ['audit'],
        'Alpine': ['audit'],
    }
    
    os_family = host.system_info.distribution
    for package in packages.get(os_family, []):
        pkg = host.package(package)
        assert pkg.is_installed, f"Package {package} should be installed"


def test_auditd_service(host):
    """Verify auditd service is running and enabled"""
    # Skip in containers
    if host.backend.name == 'docker':
        pytest.skip("auditd not available in containers")
    
    auditd = host.service('auditd')
    assert auditd.is_running, "auditd service should be running"
    assert auditd.is_enabled, "auditd service should be enabled"


def test_sensitive_file_permissions(host):
    """Verify sensitive file permissions"""
    files = {
        '/etc/shadow': {'mode': '0600', 'owner': 'root', 'group': 'root'},
        '/etc/passwd': {'mode': '0644', 'owner': 'root', 'group': 'root'},
        '/etc/group': {'mode': '0644', 'owner': 'root', 'group': 'root'},
        '/etc/sudoers': {'mode': '0440', 'owner': 'root', 'group': 'root'},
    }
    
    for path, expected in files.items():
        f = host.file(path)
        assert f.exists, f"File {path} should exist"
        assert f.mode == expected['mode'], \
            f"File {path} should have mode {expected['mode']}, got {f.mode}"
        assert f.user == expected['owner'], \
            f"File {path} should be owned by {expected['owner']}"
        assert f.group == expected['group'], \
            f"File {path} should have group {expected['group']}"


def test_system_accounts_locked(host):
    """Verify system accounts are locked"""
    accounts = ['bin', 'daemon', 'adm', 'lp', 'sync', 'shutdown', 'halt', 'mail']
    
    for account in accounts:
        user = host.user(account)
        # Check if password is locked (starts with ! or *)
        assert user.password.startswith('!') or user.password.startswith('*'), \
            f"System account {account} should be locked"


def test_pam_configuration(host):
    """Verify PAM configuration"""
    if host.system_info.distribution not in ['debian', 'ubuntu']:
        pytest.skip("PAM test only for Debian-based systems")
    
    common_password = host.file('/etc/pam.d/common-password')
    assert common_password.exists
    assert common_password.contains('pam_unix.so.*sha512.*rounds=65536'), \
        "PAM should use SHA-512 with 65536 rounds"


def test_login_defs(host):
    """Verify login.defs configuration"""
    login_defs = host.file('/etc/login.defs')
    
    assert login_defs.contains('^PASS_MIN_DAYS\\s+7'), \
        "PASS_MIN_DAYS should be 7"
    assert login_defs.contains('^PASS_MAX_DAYS\\s+90'), \
        "PASS_MAX_DAYS should be 90"
    assert login_defs.contains('^PASS_WARN_AGE\\s+14'), \
        "PASS_WARN_AGE should be 14"
```

**SSH Role Tests Example:**

```python
# roles/security/sshd/molecule/default/tests/test_sshd.py
"""Test suite for security/sshd role"""

def test_sshd_config_permissions(host):
    """Verify sshd_config has correct permissions"""
    sshd_config = host.file('/etc/ssh/sshd_config')
    assert sshd_config.mode == '0644'
    assert sshd_config.user == 'root'
    assert sshd_config.group == 'root'


def test_sshd_hardening_settings(host):
    """Verify SSH hardening configuration"""
    sshd_config = host.file('/etc/ssh/sshd_config')
    
    assert sshd_config.contains('^PermitRootLogin no'), \
        "PermitRootLogin should be no"
    assert sshd_config.contains('^PasswordAuthentication no'), \
        "PasswordAuthentication should be no"
    assert sshd_config.contains('^PubkeyAuthentication yes'), \
        "PubkeyAuthentication should be yes"
    assert sshd_config.contains('^MaxAuthTries 3'), \
        "MaxAuthTries should be 3"
    assert sshd_config.contains('^ClientAliveInterval 300'), \
        "ClientAliveInterval should be 300"
    assert sshd_config.contains('^LoginGraceTime 60'), \
        "LoginGraceTime should be 60"


def test_sshd_strong_algorithms(host):
    """Verify SSH uses strong cryptographic algorithms"""
    sshd_config = host.file('/etc/ssh/sshd_config')
    
    assert sshd_config.contains('Ciphers.*chacha20-poly1305'), \
        "SSH should use ChaCha20-Poly1305 cipher"
    assert sshd_config.contains('MACs.*hmac-sha2-512-etm'), \
        "SSH should use SHA-512 ETM MAC"
    assert sshd_config.contains('KexAlgorithms.*curve25519'), \
        "SSH should use Curve25519 key exchange"


def test_sshd_host_keys(host):
    """Verify SSH host key configuration"""
    # Ed25519 key should exist
    ed25519_key = host.file('/etc/ssh/ssh_host_ed25519_key')
    assert ed25519_key.exists
    assert ed25519_key.mode == '0600'
    
    # RSA key should exist (4096-bit)
    rsa_key = host.file('/etc/ssh/ssh_host_rsa_key')
    assert rsa_key.exists
    assert rsa_key.mode == '0600'
    
    # DSA keys should NOT exist (weak)
    dsa_key = host.file('/etc/ssh/ssh_host_dsa_key')
    assert not dsa_key.exists, "DSA host keys should be removed"


def test_sshd_service(host):
    """Verify SSH service is running"""
    sshd = host.service('ssh') if host.system_info.distribution == 'debian' \
           else host.service('sshd')
    
    assert sshd.is_running, "SSH service should be running"
    assert sshd.is_enabled, "SSH service should be enabled"
```

**Action Items:**
- [ ] Create test templates for each role category
- [ ] Write tests for all 81 roles
- [ ] Add platform-specific test skips
- [ ] Configure CI to run tests
- [ ] Add test coverage reporting

---

#### Task 2.3: Add Goss Validation (Week 7-8)

**Scope:** Security-critical roles (priority), then all roles

**Goss Configuration Template:**

```yaml
# roles/<category>/<role>/molecule/default/tests/goss.yaml
---
# Goss configuration for <role_name>
# Run with: goss -g goss.yaml validate

file:
  /etc/shadow:
    exists: true
    mode: "0600"
    owner: root
    group: root
    filetype: file
  
  /etc/passwd:
    exists: true
    mode: "0644"
    owner: root
    group: root
    filetype: file
  
  /etc/sudoers:
    exists: true
    mode: "0440"
    owner: root
    group: root
    filetype: file

user:
  root:
    exists: true
    shell: /bin/bash
  
  bin:
    exists: true
    locked: true
  
  daemon:
    exists: true
    locked: true

service:
  auditd:
    enabled: true
    running: true
  
  sshd:
    enabled: true
    running: true

port:
  tcp:22:
    listening: true
    ip:
      - 0.0.0.0

process:
  auditd:
    running: true
  
  sshd:
    running: true

command:
  # Verify no duplicate SSH directives
  check_sshd_config:
    exit-status: 0
    exec: grep -E "^[^#]" /etc/ssh/sshd_config | awk '{print $1}' | sort | uniq -d | wc -l
    stdout:
      - "0"
  
  # Verify kernel parameters
  check_kernel_hardening:
    exit-status: 0
    exec: sysctl net.ipv4.tcp_syncookies | grep -c "= 1"
    stdout:
      - "1"
```

**Action Items:**
- [ ] Create goss.yaml for security roles
- [ ] Integrate Goss with Molecule
- [ ] Add Goss to CI pipeline
- [ ] Create Goss test templates

---

### Track 3: Compliance Integration (Weeks 9-12)

**Objective:** Map all security controls to compliance frameworks

**Current Score:** 40/100 → **Target:** 95/100

#### Task 3.1: CIS Benchmark Mapping (Week 9-10)

**Scope:** All security roles

**CIS Mapping Template:**

```yaml
# roles/security/hardening/tasks/main.yml
---
# CIS Ubuntu Linux 22.04 LTS Benchmark v2.0.0

- name: "1.1.1 | Ensure mounting of squashfs filesystems is disabled (Automated)"
  ansible.builtin.lineinfile:
    path: /etc/modprobe.d/squashfs.conf
    line: install squashfs /bin/true
    create: true
    mode: '0644'
  tags:
    - cis
    - cis_1.1.1
    - level_1
    - filesystem
    - medium_severity
  changed_when: false

- name: "1.4.1 | Ensure permissions on bootloader config are configured (Automated)"
  ansible.builtin.file:
    path: /boot/grub/grub.cfg
    owner: root
    group: root
    mode: '0600'
  tags:
    - cis
    - cis_1.4.1
    - level_1
    - bootloader
    - high_severity
  when: not (is_virtualized | default(false))

- name: "5.2.1 | Ensure permissions on /etc/ssh/sshd_config are configured (Automated)"
  ansible.builtin.file:
    path: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: '0600'
  tags:
    - cis
    - cis_5.2.1
    - level_1
    - ssh
    - medium_severity

- name: "5.2.2 | Ensure permissions on SSH private host key files are configured (Automated)"
  ansible.builtin.file:
    path: "{{ item }}"
    owner: root
    group: root
    mode: '0600'
  loop:
    - /etc/ssh/ssh_host_rsa_key
    - /etc/ssh/ssh_host_ed25519_key
    - /etc/ssh/ssh_host_ecdsa_key
  tags:
    - cis
    - cis_5.2.2
    - level_1
    - ssh
    - medium_severity

- name: "5.2.3 | Ensure permissions on SSH public host key files are configured (Automated)"
  ansible.builtin.file:
    path: "{{ item }}"
    owner: root
    group: root
    mode: '0644'
  loop:
    - /etc/ssh/ssh_host_rsa_key.pub
    - /etc/ssh/ssh_host_ed25519_key.pub
    - /etc/ssh/ssh_host_ecdsa_key.pub
  tags:
    - cis
    - cis_5.2.3
    - level_1
    - ssh
    - low_severity

- name: "5.2.4 | Ensure SSH access is limited (Automated)"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?AllowUsers'
    line: 'AllowUsers {{ ssh_allowed_users | join(" ") }}'
  tags:
    - cis
    - cis_5.2.4
    - level_2
    - ssh
    - high_severity
  when: ssh_allowed_users is defined
```

**CIS Level Mapping:**

| CIS Section | DSU Role | Coverage |
|-------------|----------|----------|
| 1.1 Filesystem | security/hardening | 85% |
| 1.4 Bootloader | core/grub | 90% |
| 2.1 Service Configuration | core/systemd | 80% |
| 3.1 Network Configuration | networking/firewall | 95% |
| 3.2 Network Hardening | security/kernel | 90% |
| 4.1 Auditd | security/audit_integrity | 95% |
| 5.1 SSH Server | security/sshd | 100% |
| 5.2 SSH Configuration | security/sshd | 100% |
| 5.3 PAM | security/hardening | 85% |
| 5.4 User Accounts | security/access | 90% |
| 5.5 Root Login | security/sshd | 100% |
| 5.6 User Environment | security/hardening | 80% |

**Action Items:**
- [ ] Map all security tasks to CIS controls
- [ ] Add CIS tags to all tasks
- [ ] Create CIS compliance report playbook
- [ ] Document CIS coverage gaps

---

#### Task 3.2: Task Naming with Compliance IDs (Week 10-11)

**Scope:** All security and core roles

**Naming Convention:**

```yaml
# Format: "[SEVERITY] | CIS X.X.X | Description"
# Or: "CIS X.X.X | STIG V-XXXXX | Description"

# Examples:
- name: "CIS 5.2.1 | Configure SSH config file permissions"
  ansible.builtin.file:
    path: /etc/ssh/sshd_config
    mode: '0600'
  tags:
    - cis_5_2_1
    - ssh
    - medium_severity

- name: "CIS 1.4.1 | STIG V-38583 | Configure bootloader permissions"
  ansible.builtin.file:
    path: /boot/grub/grub.cfg
    mode: '0600'
  tags:
    - cis_1_4_1
    - stig_v_38583
    - bootloader
    - high_severity

- name: "CIS 5.2.4 | Limit SSH access to authorized users"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?AllowUsers'
    line: 'AllowUsers {{ ssh_allowed_users | join(" ") }}'
  tags:
    - cis_5_2_4
    - ssh
    - access_control
    - high_severity
```

**Severity Classification:**

| Severity | Description | Remediation Timeline |
|----------|-------------|---------------------|
| `critical_severity` | Immediate exploitation risk | 24 hours |
| `high_severity` | Significant security impact | 7 days |
| `medium_severity` | Moderate security impact | 30 days |
| `low_severity` | Minor security improvement | 90 days |

**Action Items:**
- [ ] Update all task names with compliance IDs
- [ ] Add severity tags to all tasks
- [ ] Create severity-based playbooks
- [ ] Document severity classification

---

#### Task 3.3: STIG Mapping (Week 11-12)

**Scope:** Security roles (government/enterprise focus)

**STIG Mapping Template:**

```yaml
# roles/security/sshd/tasks/main.yml
---
# DISA STIG for SSH Server

- name: "MEDIUM | V-38583 | SSH daemon must set MaxAuthTries to 3 or less"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^(#)?MaxAuthTries'
    line: 'MaxAuthTries 3'
    validate: '/usr/sbin/sshd -t -f %s'
  tags:
    - stig
    - v_38583
    - srg_os_000480_gpos_00227
    - sshd_configuration
    - medium_severity
    - cis_8_1_3
  notify: restart_sshd

- name: "MEDIUM | V-38584 | SSH daemon must set MaxStartups to 10:30:60"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^(#)?MaxStartups'
    line: 'MaxStartups 10:30:60'
    validate: '/usr/sbin/sshd -t -f %s'
  tags:
    - stig
    - v_38584
    - srg_os_000480_gpos_00227
    - sshd_configuration
    - medium_severity
  notify: restart_sshd

- name: "MEDIUM | V-38585 | SSH daemon must set ClientAliveInterval to 300 or less"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^(#)?ClientAliveInterval'
    line: 'ClientAliveInterval 300'
    validate: '/usr/sbin/sshd -t -f %s'
  tags:
    - stig
    - v_38585
    - srg_os_000480_gpos_00227
    - sshd_configuration
    - medium_severity
  notify: restart_sshd

- name: "MEDIUM | V-38586 | SSH daemon must set ClientAliveCountMax to 2 or less"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^(#)?ClientAliveCountMax'
    line: 'ClientAliveCountMax 2'
    validate: '/usr/sbin/sshd -t -f %s'
  tags:
    - stig
    - v_38586
    - srg_os_000480_gpos_00227
    - sshd_configuration
    - medium_severity
  notify: restart_sshd

- name: "HIGH | V-38587 | SSH root login must be disabled"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^(#)?PermitRootLogin'
    line: 'PermitRootLogin no'
    validate: '/usr/sbin/sshd -t -f %s'
  tags:
    - stig
    - v_38587
    - srg_os_000480_gpos_00227
    - sshd_configuration
    - high_severity
    - cis_5_2_16
  notify: restart_sshd
```

**STIG SRG Mapping:**

```yaml
# Create a mapping file for SRG references
# roles/security/sshd/files/stig_srg_mapping.yml
---
stig_to_srg:
  V-38583: SRG-OS-000480-GPOS-00227
  V-38584: SRG-OS-000480-GPOS-00227
  V-38585: SRG-OS-000480-GPOS-00227
  V-38586: SRG-OS-000480-GPOS-00227
  V-38587: SRG-OS-000480-GPOS-00227
  V-38588: SRG-OS-000021-GPOS-00005
  V-38589: SRG-OS-000074-GPOS-00042
```

**Action Items:**
- [ ] Map security tasks to STIG controls
- [ ] Add STIG tags to all relevant tasks
- [ ] Create SRG mapping file
- [ ] Generate STIG compliance reports

---

### Track 4: Documentation & Usability (Weeks 1-12, ongoing)

**Objective:** Maintain usability while adding complexity

#### Task 4.1: Create Role README Templates

**Template:**

```markdown
# {{ role_name }}

**Category:** {{ category }}
**Status:** {{ status }}
**Compliance:** CIS Level {{ level }}, STIG {{ version }}

## Description

{{ role_description }}

## Requirements

- Ansible 2.15+
- Python 3.8+
- Root/sudo privileges
- Supported OS: Ubuntu 20.04+, Debian 11+, RHEL 9+, Arch Linux, Alpine 3.18+

## Role Variables

### Required Variables

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `{{ required_var }}` | str | Description | `value` |

### Optional Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `{{ optional_var }}` | bool | `true` | Description |

### Compliance Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `cis_level_1_enable` | bool | `true` | Enable CIS Level 1 controls |
| `cis_level_2_enable` | bool | `false` | Enable CIS Level 2 controls |
| `stig_enable` | bool | `false` | Enable DISA STIG controls |

## Dependencies

- `role: core/bootstrap`
- `role: core/identity`

## Example Playbook

### Basic Usage

```yaml
- hosts: all
  become: true
  roles:
    - role: {{ category }}/{{ role_name }}
```

### CIS Compliance Mode

```yaml
- hosts: all
  become: true
  vars:
    cis_level_1_enable: true
    cis_level_2_enable: false
  roles:
    - role: {{ category }}/{{ role_name }}
```

### STIG Compliance Mode

```yaml
- hosts: all
  become: true
  vars:
    stig_enable: true
    stig_profile: server
  roles:
    - role: {{ category }}/{{ role_name }}
```

## Tags

| Tag | Description |
|-----|-------------|
| `{{ role_name }}` | All tasks in this role |
| `cis` | CIS benchmark tasks |
| `stig` | STIG compliance tasks |
| `level_1` | CIS Level 1 tasks |
| `level_2` | CIS Level 2 tasks |

## Testing

### Molecule

```bash
cd roles/{{ category }}/{{ role_name }}
molecule test
```

### Manual Verification

```bash
# Verify CIS compliance
ansible-playbook verify_cis.yml --tags {{ role_name }}

# Verify STIG compliance
ansible-playbook verify_stig.yml --tags {{ role_name }}
```

## Compliance Coverage

### CIS Ubuntu 22.04 LTS Benchmark v2.0.0

| Control ID | Status | Notes |
|------------|--------|-------|
| 1.1.1 | ✅ Implemented | squashfs disabled |
| 1.4.1 | ✅ Implemented | Bootloader permissions |
| 5.2.1 | ✅ Implemented | SSH config permissions |

### DISA STIG

| STIG ID | SRG ID | Status |
|---------|--------|--------|
| V-38583 | SRG-OS-000480-GPOS-00227 | ✅ Implemented |
| V-38584 | SRG-OS-000480-GPOS-00227 | ✅ Implemented |

## Troubleshooting

### Common Issues

#### Issue: Service fails to start

**Solution:** Check logs with `journalctl -u service_name`

#### Issue: Compliance check fails

**Solution:** Run `ansible-playbook verify_cis.yml --tags {{ role_name }} -v`

## See Also

- [CIS Benchmark Documentation](https://www.cisecurity.org/benchmark/ubuntu_linux)
- [DISA STIG Documentation](https://public.cyber.mil/stigs/)
- [LAYERED_SECURITY](../../wiki_pages/LAYERED_SECURITY.md)

## License

MIT License - See LICENSE file for details

## Author Information

- Deploy-System-Unified Team
- https://github.com/allaunthefox/deploy-system-unified
```

**Action Items:**
- [ ] Create README template
- [ ] Update all role READMEs
- [ ] Add compliance sections
- [ ] Include testing instructions

---

#### Task 4.2: Create Quick Reference Guides

**Template:**

```markdown
# Role Quick Reference

## Security Roles

### security/hardening

```yaml
# Quick start
- role: security/hardening
  vars:
    security_hardening_enabled: true
    security_enable_ufw: true

# CIS Mode
- role: security/hardening
  vars:
    cis_level_1_enable: true
    cis_level_2_enable: false

# STIG Mode
- role: security/hardening
  vars:
    stig_enable: true
```

### security/sshd

```yaml
# Quick start
- role: security/sshd
  vars:
    sshd_permit_root_login: "no"
    sshd_password_authentication: "no"

# With trusted group exceptions
- role: security/sshd
  vars:
    sshd_enable_trusted_group_exceptions: true
    sshd_trusted_groups:
      - ssh-admins
      - ssh-developers
```

## Core Roles

### core/bootstrap

```yaml
# Quick start
- role: core/bootstrap
  vars:
    core_install_base_packages: true
```

## Testing

```bash
# Test single role
molecule test -s default

# Test with specific platform
MOLECULE_PLATFORM=ubuntu2204 molecule test

# Run idempotence check
molecule test --idempotence
```
```

**Action Items:**
- [ ] Create quick reference for all roles
- [ ] Add common use cases
- [ ] Include troubleshooting tips
- [ ] Link to full documentation

---

## 📊 Success Metrics

### Week 4 Checkpoint

| Metric | Target | Measurement |
|--------|--------|-------------|
| meta/main.yml updated | 81/81 roles | File count |
| galaxy_tags ≥ 8 | 81/81 roles | Tag count |
| collections declared | 81/81 roles | File audit |
| argument_specs added | 81/81 roles | File count |
| handlers populated | 50/81 roles | File audit |
| vars populated | 50/81 roles | File audit |

### Week 8 Checkpoint

| Metric | Target | Measurement |
|--------|--------|-------------|
| Molecule scenarios | 81/81 roles | File count |
| Multi-platform tests | 81/81 roles | Platform count ≥ 3 |
| Testinfra tests | 81/81 roles | Test file count |
| Goss validation | 20/81 roles | Goss file count |
| CI integration | 100% | Pipeline status |

### Week 12 Checkpoint

| Metric | Target | Measurement |
|--------|--------|-------------|
| CIS task mapping | 100% security tasks | Tag audit |
| STIG task mapping | 100% security tasks | Tag audit |
| Severity tags | 100% tasks | Tag audit |
| README updated | 81/81 roles | File audit |
| Quick reference | 81/81 roles | Documentation audit |

### Final Score Projection

| Category | Baseline | Week 4 | Week 8 | Week 12 |
|----------|----------|--------|--------|---------|
| Role Structure | 85/100 | 90/100 | 95/100 | 98/100 |
| Task Implementation | 90/100 | 90/100 | 92/100 | 95/100 |
| Metadata & Docs | 70/100 | 90/100 | 92/100 | 95/100 |
| Testing & Validation | 60/100 | 65/100 | 90/100 | 95/100 |
| Compliance Integration | 40/100 | 50/100 | 75/100 | 95/100 |
| Innovation | 95/100 | 95/100 | 95/100 | 98/100 |
| **TOTAL** | **73/100** | **80/100** | **90/100** | **96/100** |

---

## ⚠️ Risk Mitigation

### Risk 1: Complexity Overload

**Risk:** Adding compliance metadata makes roles harder to use

**Mitigation:**
- Keep defaults simple and sensible
- Use tags for optional complexity
- Create "simple mode" playbooks
- Document common use cases clearly

### Risk 2: Testing Overhead

**Risk:** Comprehensive testing slows development

**Mitigation:**
- Run full tests in CI only
- Provide quick test mode for development
- Cache test environments
- Parallelize test execution

### Risk 3: Compliance Drift

**Risk:** CIS/STIG benchmarks update, roles become outdated

**Mitigation:**
- Quarterly compliance review
- Automated benchmark change detection
- Version-locked compliance testing
- Clear deprecation path

### Risk 4: Maintenance Burden

**Risk:** Too many files to maintain

**Mitigation:**
- Use templates and generators
- Automate repetitive updates
- Document maintenance procedures
- Community contribution guidelines

---

## 🔗 Related Documentation

- [SECURITY_ENHANCEMENT_PLAN_2026](SECURITY_ENHANCEMENT_PLAN_2026.md) - Overall security roadmap
- [ROLE_IMPLEMENTATION_STANDARDS_REVIEW](../development/ROLE_IMPLEMENTATION_STANDARDS_REVIEW.md) - Current state analysis
- [ROADMAP](ROADMAP.md) - Project direction
- [STYLE_GUIDE](../../wiki_pages/STYLE_GUIDE.md) - Implementation standards

---

**Document Owner:** Development Lead
**Created:** February 23, 2026
**Next Review:** Week 4 checkpoint (March 2026)
**Approval Status:** ⏳ Pending
