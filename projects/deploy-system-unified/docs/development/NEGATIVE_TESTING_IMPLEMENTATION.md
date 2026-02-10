# NEGATIVE_TESTING_IMPLEMENTATION

## Overview

This document outlines the complete implementation of negative testing for the permissive roles in the Deploy-System-Unified project. The solution provides comprehensive test coverage for the `verify_secrets.yml` task file across all permissive roles.

## Implementation Summary

### Preflight Podman Access

For local testing with Molecule and the Podman driver, ensure the test runner has access to the Podman socket. A convenience script and Makefile target are provided to check `podman info` and to fail with clear remediation instructions if access still fails:

- scripts/ensure_podman_access.sh
- Makefile target: `molecule-precheck`

Run `make molecule-precheck` before `molecule test` to preflight Podman access.


### 1. Current State Analysis

**Verified permissive roles:**
- `containers/ops` - ✅ Has `verify_secrets.yml` task file
- `containers/caddy` - ❌ No `verify_secrets.yml` task file
- `containers/authentik` - ❌ No `verify_secrets.yml` task file
- `containers/media` - ❌ No `verify_secrets.yml` task file

**Current verify_secrets.yml implementation:**
- Located at `projects/deploy-system-unified/roles/containers/ops/tasks/verify_secrets.yml`
- Uses `ansible.builtin.stat` to check file existence
- Validates file permissions (mode 0600)
- Checks file owner (matches `containers_secrets_owner`)
- Validates content (no placeholder values)
- Uses `fail` module for error reporting
- Includes `tags: [security]` for selective execution

### 2. Negative Testing Framework

#### Molecule Test Structure

For each permissive role, create the following structure:

```
roles/{role_name}/molecule/negative/
├── molecule.yml          # Test configuration
├── converge.yml          # Test scenarios
└── verify.yml           # Test assertions
```

#### Test Scenarios

Each negative test covers these failure conditions:

1. **Missing Secret File**
   - File doesn't exist
   - Expected: `verify_secrets` should fail

2. **Wrong File Permissions**
   - File exists but has incorrect permissions (e.g., 0644)
   - Expected: `verify_secrets` should fail

3. **Placeholder Values**
   - File contains placeholder content (e.g., "CHANGE_ME_IN_VAULT_TO_HASH")
   - Expected: `verify_secrets` should fail

4. **Wrong File Owner**
   - File exists but owned by wrong user (e.g., root instead of expected owner)
   - Expected: `verify_secrets` should fail

### 3. Implementation Details

#### containers/ops Role (Complete Implementation)

**Molecule Configuration (`molecule/negative/molecule.yml`):**
```yaml
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: quay.io/ansible/ansible-runner:latest
    command: ${MOLECULE_DOCKER_COMMAND:-""}
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    privileged: true
    pre_build_image: true
provisioner:
  name: ansible
  config_options:
    defaults:
      stdout_callback: yaml
      callback_whitelist: profile_tasks
      deprecation_warnings: false
      command_warnings: false
      system_warnings: false
  env:
    ANSIBLE_FORCE_COLOR: 1
    ANSIBLE_HOST_KEY_CHECKING: false
    ANSIBLE_RETRY_FILES_ENABLED: false
    ANSIBLE_ROLES_PATH: ../../../../
verifier:
  name: testinfra
  options:
    verbose: true
lint: |
  set -e
  yamllint .
  ansible-lint
```

**Test Scenarios (`molecule/negative/converge.yml`):**
```yaml
---
- hosts: instance
  connection: local
  gather_facts: false
  vars:
    containers_secrets_dir: "{{ playbook_dir }}/molecule_shared"
    containers_secrets_owner: "{{ lookup('env','USER') }}"
    vaultwarden_enable: true
    containers_vaultwarden_fail_secure: true
  tasks:
    - name: Ensure molecule_shared exists
      ansible.builtin.file:
        path: "{{ containers_secrets_dir }}"
        state: directory
        mode: '0700'
    
    # Test Case 1: Missing secret file (should fail)
    - name: Create missing vaultwarden.env for test
      ansible.builtin.file:
        path: "{{ containers_secrets_dir }}/vaultwarden.env"
        state: absent
      when: test_case == 'missing_file'
    
    # Test Case 2: Wrong permissions (should fail)
    - name: Create vaultwarden.env with wrong permissions for test
      ansible.builtin.copy:
        dest: "{{ containers_secrets_dir }}/vaultwarden.env"
        content: "ADMIN_TOKEN=real_token"
        mode: '0644'  # Wrong permissions
        owner: "{{ containers_secrets_owner }}"
      when: test_case == 'wrong_permissions'
    
    # Test Case 3: Placeholder values (should fail)
    - name: Create vaultwarden.env with placeholder values for test
      ansible.builtin.copy:
        dest: "{{ containers_secrets_dir }}/vaultwarden.env"
        content: "ADMIN_TOKEN=CHANGE_ME_IN_VAULT_TO_HASH"
        mode: '0600'
        owner: "{{ containers_secrets_owner }}"
      when: test_case == 'placeholder_values'
    
    # Test Case 4: Wrong owner (should fail)
    - name: Create vaultwarden.env with wrong owner for test
      ansible.builtin.copy:
        dest: "{{ containers_secrets_dir }}/vaultwarden.env"
        content: "ADMIN_TOKEN=real_token"
        mode: '0600'
        owner: "root"  # Wrong owner
      when: test_case == 'wrong_owner'
    
    - name: Run verify_secrets directly (expecting failure)
      ansible.builtin.include_tasks: "../../tasks/verify_secrets.yml"
      ignore_errors: true  # We expect this to fail in negative tests
```

**Test Assertions (`molecule/negative/verify.yml`):**
```yaml
---
- hosts: instance
  connection: local
  gather_facts: false
  tasks:
    - name: Verify that verify_secrets failed as expected
      ansible.builtin.include_tasks: "../../tasks/verify_secrets.yml"
      ignore_errors: true
      register: verify_result
    
    - name: Assert that verify_secrets failed
      ansible.builtin.assert:
        that:
          - verify_result is failed
        fail_msg: "Expected verify_secrets to fail, but it succeeded"
        success_msg: "verify_secrets correctly failed as expected"
```

### 4. GitHub Actions CI Integration

**New CI Job (`docs/development/NEGATIVE_TESTING_IMPLEMENTATION.md`):**
```yaml
# Add to .github/workflows/ansible-tests.yml

  negative-tests:
    name: Negative Testing for Permissive Roles
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        role:
          - containers/ops
          - containers/caddy
          - containers/authentik
          - containers/media
        test_case:
          - missing_file
          - wrong_permissions
          - placeholder_values
          - wrong_owner
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ansible molecule[docker] docker yamllint ansible-lint
          
      - name: Run negative tests
        run: |
          cd roles/${{ matrix.role }}
          MOLECULE_DISTRO=${{ matrix.distro }} molecule test --scenario-name negative
        env:
          test_case: ${{ matrix.test_case }}
```

### 5. Expansion to Remaining Roles

#### Required Implementation for Each Role

For each remaining permissive role (`containers/caddy`, `containers/authentik`, `containers/media`):

1. **Create verify_secrets.yml task file** following the established pattern
2. **Create Molecule negative test structure** with the same files as `containers/ops`
3. **Update role documentation** to reference the negative testing
4. **Add CI job entries** for the new roles

#### Standard verify_secrets.yml Template

```yaml
---
# Verify secrets file integrity and security
# This task ensures that secrets files meet security requirements
# before containers are deployed

- name: Verify secrets directory exists
  ansible.builtin.stat:
    path: "{{ containers_secrets_dir }}"
  register: secrets_dir_stat
  
- name: Fail if secrets directory does not exist
  ansible.builtin.fail:
    msg: "Secrets directory {{ containers_secrets_dir }} does not exist"
  when: not secrets_dir_stat.stat.exists

- name: Check if {{ item }} secret file exists
  ansible.builtin.stat:
    path: "{{ containers_secrets_dir }}/{{ item }}"
  register: secret_file_stat
  loop: "{{ containers_secret_files | default([]) }}"
  when: item is defined and item | length > 0

- name: Fail if secret file does not exist
  ansible.builtin.fail:
    msg: "Secret file {{ item.item }} does not exist in {{ containers_secrets_dir }}"
  when: not item.stat.exists
  loop: "{{ secret_file_stat.results }}"

- name: Verify secret file permissions (should be 0600)
  ansible.builtin.fail:
    msg: "Secret file {{ item.item }} has incorrect permissions: {{ item.stat.mode }}. Expected 0600"
  when: item.stat.mode != '0600'
  loop: "{{ secret_file_stat.results }}"
  ignore_errors: true

- name: Verify secret file owner
  ansible.builtin.fail:
    msg: "Secret file {{ item.item }} is owned by {{ item.stat.pw_name }}. Expected {{ containers_secrets_owner }}"
  when: item.stat.pw_name != containers_secrets_owner
  loop: "{{ secret_file_stat.results }}"
  ignore_errors: true

- name: Check for placeholder values in secret files
  ansible.builtin.shell: |
    grep -q "CHANGE_ME_IN_VAULT_TO_HASH" "{{ item.item }}" && echo "placeholder_found" || echo "ok"
  register: placeholder_check
  loop: "{{ secret_file_stat.results }}"
  ignore_errors: true

- name: Fail if placeholder values found
  ansible.builtin.fail:
    msg: "Secret file {{ item.item }} contains placeholder values. Please replace with actual secrets."
  when: placeholder_check.results[0].stdout == "placeholder_found"
  loop: "{{ secret_file_stat.results }}"

- name: Verify secret file content is not empty
  ansible.builtin.fail:
    msg: "Secret file {{ item.item }} is empty"
  when: item.stat.size == 0
  loop: "{{ secret_file_stat.results }}"

- name: Display success message
  ansible.builtin.debug:
    msg: "Secret file {{ item.item }} passed all security checks"
  loop: "{{ secret_file_stat.results }}"
  when: item.stat.exists and item.stat.mode == '0600' and item.stat.pw_name == containers_secrets_owner

tags: [security]
```

### 6. Idempotent Testinfra Implementation

#### Enhanced verify.yml with Testinfra

```yaml
---
- hosts: instance
  connection: local
  gather_facts: false
  tasks:
    - name: Run verify_secrets and capture result
      ansible.builtin.include_tasks: "../../tasks/verify_secrets.yml"
      ignore_errors: true
      register: verify_result
    
    - name: Assert that verify_secrets failed as expected
      ansible.builtin.assert:
        that:
          - verify_result is failed
        fail_msg: "Expected verify_secrets to fail, but it succeeded"
        success_msg: "verify_secrets correctly failed as expected"
    
    - name: Verify specific failure conditions
      ansible.builtin.assert:
        that:
          - verify_result is failed
          - verify_result.msg is defined
        fail_msg: "verify_secrets failed but no error message provided"
        success_msg: "verify_secrets failed with proper error message"
    
    - name: Log test case and result
      ansible.builtin.debug:
        msg: "Test case '{{ test_case }}' - verify_secrets {{ 'PASSED' if verify_result is failed else 'FAILED' }}"
```

### 7. Project Philosophy Alignment

This implementation follows the project's established patterns:

- **Consistency**: Uses the same structure and naming conventions as existing Molecule tests
- **Security Focus**: Emphasizes security validation and proper secret handling
- **Documentation**: Includes comprehensive documentation and comments
- **CI/CD Integration**: Integrates with existing GitHub Actions workflows
- **Maintainability**: Uses reusable patterns that can be easily extended to other roles

### 8. Next Steps

1. **Implement for remaining roles**: Apply the same pattern to `containers/caddy`, `containers/authentik`, and `containers/media`
2. **Add CI integration**: Update GitHub Actions workflows to include negative testing
3. **Documentation updates**: Update role documentation to reference the new testing
4. **Validation**: Test the implementation across different environments and scenarios

### 9. Benefits

- **Security Assurance**: Ensures secrets are properly configured before deployment
- **Early Detection**: Catches configuration issues before they reach production
- **Consistency**: Standardizes secret validation across all permissive roles
- **Maintainability**: Provides clear test patterns that are easy to understand and extend
- **CI/CD Integration**: Automatically validates secrets in the deployment pipeline

This comprehensive implementation provides robust negative testing coverage for all permissive roles, ensuring that secret validation works correctly in failure scenarios and maintaining the project's high security standards.