# STYLE_GUIDE

To maintain consistency and ensure clean linting across the Deploy-System-Unified project, all contributions must adhere to the following style requirements. These standards are enforced via the `make lint` suite.

## 🛠 General Standards

* **Extensions**: Use `.yml` for all YAML files, not `.yaml`.
* **EOF Newlines**: Every file (YAML, Markdown, Jinja2, etc.) must end with exactly one newline character.
* **Trailing Whitespace**: No lines should have trailing spaces or tabs.
* **Indentation**: Use spaces for indentation, never tabs.

## 📄 YAML Standards

* **Indentation**: Use 2 spaces for indentation.
* **Booleans**: Always use `true` or `false` (lowercase). Avoid `yes`, `no`, `on`, `off`.
* **Line Length**: Aim for a maximum of 160 characters per line.
* **Comments**: Use a single space after the `#` character (e.g., `# This is a comment`).
* **Lists**: Use a single space after the `-` character for list items.
* **FQCN**: Always use Fully Qualified Collection Names (e.g., `ansible.builtin.copy` instead of `copy`) for better reliability and clarity.
* **Braces Spacing**: Always include exactly one space inside Jinja2 delimiters: `{{ var }}` instead of `{{var}}` or `{{  var  }}`.
* **Argument Style**: Prefer YAML dictionary style for module arguments over inline `key=value` strings.

    ```yaml
    # GOOD
    ansible.builtin.file:
      path: /tmp/file
      state: touch

    # BAD
    ansible.builtin.file: path=/tmp/file state=touch
    ```

* **Checkpoint and Resume Pattern**: Implement clear conditional logic for checkpoint creation and resume operations

    ```yaml
    # GOOD - Conditional checkpoint and resume pattern
    - name: Check for existing deployment checkpoint
      ansible.builtin.stat:
        path: /var/lib/deploy-system/checkpoints/deployment_checkpoint.json
      register: checkpoint_file

    - name: Set deployment mode based on checkpoint existence
      ansible.builtin.set_fact:
        deployment_mode: "{{ 'resume' if checkpoint_file.stat.exists else 'fresh' }}"
    - name: Read checkpoint data if resuming from existing checkpoint
      ansible.builtin.slurp:
        src: /var/lib/deploy-system/checkpoints/deployment_checkpoint.json
      register: checkpoint_data
      when: deployment_mode == "resume"

    - name: Parse checkpoint data if resuming from existing checkpoint
      ansible.builtin.set_fact:
        resume_from_task: "{{ (checkpoint_data.content | b64decode | from_json).next_task }}"
        completed_roles: "{{ (checkpoint_data.content | b64decode | from_json).completed_roles }}"
      when: deployment_mode == "resume"
    - name: Run deployment with conditional resume capability
      block:
        - name: Run bootstrap role if not already completed
          ansible.builtin.import_role:
            name: bootstrap
          when: deployment_mode == "fresh" or "bootstrap" not in (completed_roles | default([]))

        - name: Run users role if not already completed
          ansible.builtin.import_role:
            name: users
          when: deployment_mode == "fresh" or "users" not in (completed_roles | default([]))
        # ... other roles ...

        - name: Update checkpoint after major phase completion
          ansible.builtin.copy:
            content: |
              {
                "timestamp": "{{ ansible_date_time.iso8601 }}",
                "last_completed_task": "current role completed",
                "next_task": "next role",
                "deployment_phase": "current phase",
                "completed_roles": {{ completed_roles | default([]) + ["bootstrap", "users"] | to_json }},
                "system_state": "partially_deployed"
              }
            dest: /var/lib/deploy-system/checkpoints/deployment_checkpoint.json
            mode: '0644'
            owner: root
            group: root
      rescue:
        - name: Handle deployment failure and create checkpoint
          block:
            - name: Create failure checkpoint when deployment fails
              ansible.builtin.copy:
                content: |
                  {
                    "timestamp": "{{ ansible_date_time.iso8601 }}",
                    "last_completed_task": "{{ ansible_failed_task.name if ansible_failed_task is defined else 'unknown' }}",
                    "next_task": "{{ ansible_failed_task.name if ansible_failed_task is defined else 'unknown' }}",
                    "deployment_phase": "failed",
                    "completed_roles": {{ completed_roles | default([]) | to_json }},
                    "failed_tasks": ["{{ ansible_failed_task.name if ansible_failed_task is defined else 'unknown' }}"],
                    "system_state": "failed"
                  }
                dest: /var/lib/deploy-system/checkpoints/deployment_failure_checkpoint.json
                mode: '0644'
                owner: root
                group: root
    ```

## 📝 Markdown Standards

* **Code Blocks**: Every fenced code block (represented by three backticks) MUST have a language specified (e.g., `yaml`, `bash`).
* **Headings**:
    * No trailing punctuation (like colons `:`) at the end of heading lines.
    * Ensure heading levels increment logically (don't skip from `##` to `####`).
    * Use a single space after the `#` symbols (e.g., `## My Heading`).
* **Links**: Ensure all internal link fragments (`#anchor`) are valid and match existing headers.

## 🤖 Ansible & Jinja2 Standards

### Role Metadata

* **meta/main.yml**: Every role MUST have a valid metadata file containing:
    * `author`, `description`, `license` (prefer MIT), and `min_ansible_version` (at least 2.15).
    * Target `platforms` supported by the role.
* **Complete Galaxy Info**: The `meta/main.yml` file should include a complete `galaxy_info` section with:
    * `role_name`: Short, lowercase name with underscores if needed
    * `author`: Author or organization name (typically "deploy-system-unified")
    * `description`: Clear, concise description of the role's purpose
    * `license`: License type (prefer "MIT")
    * `min_ansible_version`: Minimum required Ansible version (at least "2.15")
    * `platforms`: List of supported platforms with versions
    * `galaxy_tags`: Relevant tags for role discovery (lowercase letters and digits only, no hyphens)
* **Platform Specification**: Platforms should be listed with specific OS names and version ranges:

    ```yaml
    platforms:
      - name: Archlinux
        versions: [all]
      - name: Ubuntu
        versions: [all]
      - name: Debian
        versions: [all]
      - name: CentOS
        versions: [all]
      - name: Fedora
        versions: [all]
      - name: Alpine
        versions: [all]
    ```

* **Tag Standards**: Galaxy tags should be:
    * Lowercase letters and digits only
    * No hyphens or special characters
    * Concise and descriptive
    * Related to the role's functionality
* **Dependencies Section**: Include an empty `dependencies: []` section even if no dependencies exist.
* **Runtime Requirements**: For collections (which this project emulates with roles), add `meta/runtime.yml` to specify ansible-core version requirements:

    ```yaml
    ---
    requires_ansible: ">=2.15.0"
    ```

* **Runtime File Standards**: The `meta/runtime.yml` file should:
    * Be placed in the `meta/` directory of each role
    * Specify compatible ansible-core version ranges using semantic versioning
    * Use the format `requires_ansible: ">=MIN_VERSION,<MAX_VERSION"`
    * Follow the same version requirements as specified in the role's `meta/main.yml` min_ansible_version
    * Include a YAML document header (`---`) for consistency

### Galaxy Setup and Distribution

* **Galaxy Integration**: Roles should be designed for potential publication to Ansible Galaxy
* **Namespace Standards**: Use consistent namespace naming (e.g., `deploy-system-unified.role_name`)
* **Version Tags**: Use semantic versioning tags (e.g., `v1.0.0`) for Galaxy releases
* **Requirements Management**: Maintain `requirements.yml` for Galaxy role dependencies:

    ```yaml
    # For Galaxy roles
    roles:
      - name: username.role_name
        version: v1.2.3
        src: https://galaxy.ansible.com
    # For GitHub repositories
    roles:
      - name: username.role_name
        src: https://github.com/username/role_name
        version: v1.2.3
    ```

* **Publishing Readiness**: Ensure roles meet Galaxy publishing standards:
    * Complete and accurate metadata in `meta/main.yml`
    * Proper README documentation with usage examples
    * Functional test scenarios (preferably with Molecule)
    * Valid licensing information
    * Well-structured role layout following Ansible best practices
* **Collection Conversion**: When converting roles to collections:
    * Maintain the same metadata standards in `galaxy.yml`
    * Use proper collection namespace and name
    * Include collection-level requirements in `requirements.yml`
    * Update all internal role references to use FQCN format
* **Testing for Galaxy**: Before publishing to Galaxy:
    * Test role installation with `ansible-galaxy role install`
    * Verify all dependencies are properly declared
    * Confirm role functionality in isolated environments
    * Validate metadata completeness and accuracy

### Task Naming

* **Descriptive Names**: Every task and handler MUST have a `name` key that clearly describes its purpose.
* **Uniqueness**: Ensure task names are unique within a role to facilitate debugging and logging.

### Loops

* **loop over with_***: Use the `loop` keyword for simple lists. Use `with_fileglob`, `with_dict`, or other `with_` keywords only when a specific lookup plugin is required that is not easily handled by `loop` + `lookup()`.
* **Include vs Import**: Use `import_tasks` for static inclusion (parsed at playbook loading) and `include_tasks` for dynamic inclusion (evaluated at runtime). Similarly, use `import_role` for static role inclusion and `include_role` for dynamic role inclusion.
* **Static Inclusion**: Use `import_tasks` and `import_role` when:
    * The included content is always needed
    * You need to use variables in the `when` condition of the imported tasks
    * You want the tasks to be parsed during playbook parsing time
    * The included file path is static (doesn't change based on variables)
* **Dynamic Inclusion**: Use `include_tasks` and `include_role` when:
    * The inclusion is conditional based on runtime variables
    * You need to pass variables to the included content
    * The included file path changes based on variables
    * You want the tasks to be evaluated during execution time
* **Performance Considerations**: Static inclusion (`import_*`) happens at parse time and is more efficient for content that's always needed. Dynamic inclusion (`include_*`) happens at runtime and is more flexible for conditional content.

### Conditionals and Flow Control

* **Blocks**: Use blocks with rescue and always sections for error handling:

    ```yaml
    - block:
        - name: Task that might fail
          ansible.builtin.command: risky_command
      rescue:
        - name: Handle failure
          ansible.builtin.debug:
            msg: "Original task failed, executing recovery"
      always:
        - name: Cleanup tasks
          ansible.builtin.debug:
            msg: "Always executed"
    ```

* **Conditional Best Practices**: Use complex conditionals with parentheses for clarity:

    ```yaml
    when:
      - (condition1 or condition2)
      - not condition3
    ```

### Privilege Escalation

* **Explicit Become**: Specify `become: true` only where needed. Use `become_user` or `become_method` if it deviates from the default root escalation.
* **Scope**: Apply `become` at the task level rather than the block level unless all tasks in the block require escalation.

### Module Selection

* **Specialized over Generic**: Always prefer specialized modules over `command` or `shell`.
    * Use `ansible.builtin.file` for creating directories or deleting files.
    * Use `ansible.builtin.systemd` or `ansible.builtin.service` for managing services.
    * Use `ansible.builtin.get_url` instead of `curl` via shell.
    * Use `ansible.builtin.wait_for` for waiting on ports/services instead of polling with `uri` or `shell`.
    * Use `ansible.builtin.async_status` for checking async task status.
* **Command usage**: Use `command` only when no module exists. If pipes, redirects, or environment variables are needed, use `shell`.
* **Async Tasks**: For long-running operations, use async and poll:

    ```yaml
    - name: Long running task
      ansible.builtin.command: long_running_command
      async: 300  # 5 minutes
      poll: 0     # Don't wait for completion
    ```

### Package Management Pattern

* To support multiple distributions consistently, use the following pattern:

    ```yaml
    - name: Install packages (APT)
      ansible.builtin.apt:
        name: "{{ role_name_packages }}"
        state: present
        update_cache: true
      when: ansible_facts['pkg_mgr'] | default('') == 'apt'
    - name: Install packages (DNF)
      ansible.builtin.dnf:
        name: "{{ role_name_packages }}"
        state: present
      when: ansible_facts['pkg_mgr'] | default('') == 'dnf'

    - name: Install packages (Pacman)
      community.general.pacman:
        name: "{{ role_name_packages }}"
        state: present
      when: ansible_facts['pkg_mgr'] | default('') == 'pacman'
    ```

* **Best Practices**:
    * Always use `ansible_facts['pkg_mgr'] | default('')` to prevent errors when facts aren't gathered
    * Use `update_cache: true` for APT when installing packages
    * Use appropriate collection modules (e.g., `community.general.pacman`)
    * Use the generic `ansible.builtin.package` module when no distribution-specific configuration is required
    * For packages that only exist on specific distributions, use the distribution-specific module directly

### Logic & Facts

* **Jinja2 Delimiters**: Never use `{{ ...  }}` inside a `when` statement.
* **Complex Logic**: Use `ansible.builtin.set_fact` to break down complex expressions into readable variables before using them in tasks.

### File Permissions

* **Explicit Mode**: Always specify `mode` for `file`, `copy`, and `template` tasks.
* **String Format**: Use symbolic (e.g., `u=rw,g=r,o=r`) or 4-digit octal (e.g., `'0644'`) strings for modes. Always wrap octal modes in quotes to avoid YAML interpreting them as base-8 integers.

### Shell Tasks

* **Pipefail**: Any shell command using pipes (`|`) must have pipefail enabled. Use the Ansible-native `pipefail: true` argument where supported. If the linter continues to flag a task, include `set -o pipefail` at the beginning of the shell script and ensure `executable: /bin/bash` is set.

    ```yaml
    - name: Example task
      ansible.builtin.shell: |
        set -o pipefail
        command1 | command2
      args:
        executable: /bin/bash
    ```

* **Idempotency**: Always provide a `changed_when` condition for `shell` or `command` modules unless the task is inherently read-only.

### Error Handling

* **Avoid `ignore_errors: true`**: Use `failed_when` or `check_mode` instead. If a task is expected to fail under certain conditions, handle it explicitly.
* **Rescue Blocks**: Use `block` and `rescue` for complex multi-task error recovery.

### Security & Sensitive Data

* **Masking**: Always use `no_log: true` for any task handling passwords, tokens, API keys, or private keys.
* **Variables**: Never put secrets in `defaults/` or `vars/` files. Use `vault.yml` or environment variables.
* **Certificate Validation**: Always explicitly set `validate_certs: true` for uri/web requests unless there's a specific reason not to, and document why if disabled:

    ```yaml
    # GOOD - Explicitly validates certificates
    ansible.builtin.uri:
      url: https://api.example.com
      validate_certs: true  # Always validate certificates for security

    # AVOID - Using variables for certificate validation (security scanner flag)
    ansible.builtin.uri:
      url: https://api.example.com
      validate_certs: "{{ variable | default(true) }}"
    ```

* **Secure Defaults**: When using variables for security-sensitive settings, ensure they default to secure values:

    ```yaml
    # GOOD - Secure default
    validate_certs: "{{ api_validate_certs | default(true) }}"
    # AVOID - Insecure default
    validate_certs: "{{ api_validate_certs | default(false) }}"
    ```

### Linting & Suppressions

* **noqa**: Use `# noqa <rule>` to suppress specific `ansible-lint` warnings only when necessary and justified by a comment.

    ```yaml
    - name: Use latest package
      ansible.builtin.package:
        name: my-pkg
        state: latest # noqa package-latest
    ```

* **DSU003 (no_direct_placeholder_compare)**: This rule flags direct comparisons to placeholder values (e.g., `CHANGE_ME`, `CHANGE_ME_IN_VAULT`). Some files intentionally list placeholder defaults for validation (for example a central `preflight` guard). Prefer one of the following approaches to avoid false positives:

    1. Avoid literal placeholder defaults by using an empty default and a `bad_values` list (recommended):

    ```yaml
    - name: Define placeholder guard
      value: "{{ some_secret | default('') }}"
      bad_values: ["CHANGE_ME", ""]
    ```

    2. If a literal placeholder is required for policy/documentation, annotate the offending line with `# noqa DSU003` and, when appropriate, add the file to `.ansible-lint.yml` via `exclude_paths:` to scope the suppression (preferred over global rule disable):

    ```yaml
    # roles/ops/preflight/tasks/main.yml
    - name: "restic_password"
      value: "{{ restic_password | default('CHANGE_ME_IN_VAULT') }}" # noqa DSU003
      bad_values: ["CHANGE_ME_IN_VAULT", ""]
    ```

    ```yaml
    # .ansible-lint.yml
    rulesdir:
      - ansiblelint/rules
    exclude_paths:
      - roles/ops/preflight/tasks/main.yml
    ```

    Also add the file to `dev_tools/tools/style-guide-enforcement/.styleignore` when the style enforcement tool should ignore it entirely.

### Error Handling & Block Patterns

* **Block Error Handling**: Always include `rescue` and `always` sections when using `block` for critical operations:

    ```yaml
    # GOOD - Complete error handling pattern
    - name: Perform critical operation
      block:
        - name: Task that might fail
          ansible.builtin.command: critical_operation
      rescue:
        - name: Handle failure
          ansible.builtin.debug:
            msg: "Critical operation failed, handling gracefully"
      always:
        - name: Cleanup or status reporting
          ansible.builtin.debug:
            msg: "Operation completed or handled"
    ```

* **Conditional Block Handling**: When blocks are conditional, ensure error handling respects the same conditions:

    ```yaml
    # GOOD - Conditional block with appropriate error handling
    - name: Conditional operation with error handling
      when: feature_enabled | bool
      block:
        - name: Conditional task
          ansible.builtin.command: conditional_command
      rescue:
        - name: Handle conditional failure
          ansible.builtin.debug:
            msg: "Conditional operation failed"
          when: feature_enabled | default(false)
      always:
        - name: Report conditional operation status
          ansible.builtin.debug:
            msg: "Conditional operation completed or handled"
    ```

## 🐚 Shell Script Standards (*.sh)

* **Header**: Every script must start with a proper shebang and strict error handling:

    ```bash
    #!/bin/bash
    set -euo pipefail
    ```

    * `set -e`: Exit immediately if a command exits with a non-zero status
    * `set -u`: Exit immediately if an undefined variable is used
    * `set -o pipefail`: Exit immediately if any command in a pipeline fails
* **Quoting**: Quote all variable expansions to prevent word splitting: `"$MY_VAR"` instead of `$MY_VAR`.
    * Always quote variables in comparisons: `[[ "$VAR" == "value" ]]` instead of `[[ $VAR == "value" ]]`
    * Quote command substitutions: `result="$(command)"` instead of `result=$(command)`
* **Local Variables**: Use `local` for variables inside functions.

    ```bash
    function my_function() {
        local temp_var
        temp_var="temporary value"
        echo "$temp_var"
    }
    ```

* **Portability**: Stick to Bash features if using `#!/bin/bash`, or POSIX features if using `#!/bin/sh`.
* **Error Handling**: Use proper error handling in scripts:

    ```bash
    # Use trap for cleanup
    trap 'rm -f /tmp/tempfile.$$' EXIT

    # Check command success
    if ! command_that_might_fail; then
        echo "Error: command failed" >&2
        exit 1
    fi
    ```

* **Functions**: Use functions for code organization:

    ```bash
    #!/bin/bash
    # Function definitions at top
    log_message() {
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
    }

    # Main script execution
    main() {
        log_message "Starting script..."
        # script logic here
    }
    main "$@"
    ```

## 📁 Variable Naming

* **Prefixing**: Role-specific variables should be prefixed with the role name (e.g., `bootstrap_hostname` instead of just `hostname`).
* **Casing**: Use `snake_case` for all variable names.
* **Variable Scope and Naming Conventions**:
    * **Role Variables**: Use `role_name_variable_name` format (e.g., `users_ssh_keys`, `bootstrap_hostname`)
    * **Global Variables**: Use descriptive names that indicate their scope (e.g., `system_global_setting`, `deployment_environment`)
    * **Loop Variables**: Use descriptive names in `with_` loops (e.g., `item`, `host`, `service` rather than generic `i` or `x`)
    * **Internal Variables**: Use `role_name_internal_var` for variables used internally within a role
    * **Public Interface Variables**: Use `role_name_public_var` for variables that are meant to be overridden by users
* **Variable Types**:
    * **Lists**: Use plural names (e.g., `users_groups`, `packages_list`, `firewall_ports`)
    * **Dictionaries**: Use singular names (e.g., `user_config`, `service_definition`, `network_settings`)
    * **Boolean Flags**: Use `is_`, `has_`, `enable_`, or `disable_` prefixes (e.g., `is_production`, `has_gpu`, `enable_ssl`)
    * **Counters/Numbers**: Use descriptive names (e.g., `max_connections`, `timeout_seconds`, `retry_count`)
* **Avoid Reserved Words**: Don't use Ansible or Jinja2 reserved words as variable names (e.g., `host`, `item`, `result`, `delegate_to`)

### Jinja2 Templates

* **Escaping**: When using character sequences that Jinja2 might interpret (like `${#` or `{{`) in shell scripts or other templates, use escaping to render them literally:
    * `${#VAR}` becomes `${{ '{' }}#VAR}`.
    * `{{ VAR  }}` becomes `{{ "{{ "   }} VAR {{ " }}" }}`.
    * `{% statement %}` becomes `{% raw %}{% statement %}{% endraw %}` or `{{ "{{ "   }}% statement {{ "% "   }}}`.
* **Indentation**: Match the indentation of the surrounding file structure for Jinja2 control tags (`{% if ... %}`).
* **Variable Escaping in Templates**: When templates generate content that will be processed by Jinja2 again, use proper escaping:

    ```jinja2
    # In a Jinja2 template that generates shell script content
    echo "{{ "{{ "   }} variable_name {{ " }}" }}"
    # This renders as: echo "{{ variable_name }}" in the generated script
    ```

### Podman Quadlets

* **Structure**: Quadlet files (`.container`, `.network`, etc.) must follow standard systemd unit formatting.
* **Headers**: Do NOT include shell headers like `set -o pipefail` at the top of Quadlet templates; these are unit files, not scripts.
* **Resource Limits**: Place `MemoryMax` and `CPUQuota` in the `[Service]` section, not the `[Container]` section.
* **Template Placeholders**: When using Jinja2 templates for Quadlet files, use fully qualified image names for validation purposes:
    * Use `docker.io/library/ubuntu:latest` instead of `DUMMY_VALUE`
    * Use `docker.io/library/ubuntu:latest` for generic image placeholders
    * Use `test-container` for generic container name placeholders
    * This ensures proper validation while maintaining template functionality

## 🔍 Validation

Before submitting any changes, always run the full linting suite from the project root:

```bash
make lint
```

If your changes involve documentation only, you can run:

```bash
make lint-markdown
```

## 🐍 Python Code Standards

* **Shebang**: Python scripts should start with `#!/usr/bin/env python3` when intended to be executable.
* **Encoding**: Include `# -*- coding: utf-8 -*-` at the top of Python files.
* **Copyright Headers**: Include appropriate copyright headers with license information.
* **Imports**: Use proper import organization with `from __future__ import` statements first, followed by standard library imports, third-party imports, and local imports.
* **Docstrings**: Include docstrings for modules, classes, and functions following the Google or Sphinx style.
* **PEP 8 Compliance**: Follow PEP 8 style guidelines for naming, spacing, and formatting.
* **Ansible Plugin Standards**: For Ansible plugins (modules, callbacks, filters), follow Ansible's plugin development standards including proper class structure and documentation.

## ⚙️ Configuration Files Standards

* **INI Files**: Use `.ini` extension for INI-style configuration files. Maintain consistent section headers with `[section_name]` format.
* **JSON Files**: Use proper indentation (2 spaces) and ensure valid JSON syntax. Include trailing commas where appropriate for maintainability.
* **System Configuration Files**: When creating system configuration files in `files/` directories, follow the target system's conventions and include appropriate comments explaining settings.

## 🐳 Container Standards

* **Dockerfiles**:
    * Use specific base image tags (e.g., `ubuntu:24.04`) rather than `latest`.
    * Minimize layers by combining related RUN commands with `&&`.
    * Use `--no-install-recommends` with package managers when possible.
    * Set `DEBIAN_FRONTEND=noninteractive` for Debian-based images to avoid prompts.
* **Quadlet Files**: Follow systemd unit file format for Podman quadlet files. Place resource limits in `[Service]` section, not `[Container]` section.

## 📁 Directory Structure Standards

* **Roles Organization**: Organize roles with standard Ansible role structure (tasks, handlers, templates, files, vars, defaults, meta).
* **File Placement**:
    * Template files (`.j2`) go in `templates/` directory
    * Static files go in `files/` directory
    * Task files go in `tasks/` directory
    * Variable files go in `vars/` or `defaults/` directories
* **Inventory Structure**: Place inventory files in the `inventory/` directory with appropriate group and host variable organization.

## 🧪 Molecule Testing Standards

* **Scenario Structure**: Organize Molecule tests with clear scenario names that reflect the test purpose:
    * `default` - Basic functionality test
    * `integration` - Multi-component integration test
    * `convergence` - Idempotency test
    * `side_effect` - State change validation test
* **Molecule Configuration**:
    * Use `molecule.yml` for scenario-specific configuration
    * Include proper dependency management with `requirements.yml` for roles and `collections.yml` for collections
    * Configure appropriate platforms for testing different OS variants
    * Enable shared state when testing inter-dependent scenarios:

      ```yaml
      shared_state: true
      ```

* **Driver Selection**:
    * Use `podman` driver when available for container-based testing
    * Use `docker` driver as fallback when podman is not available
    * Use `delegated` driver for existing infrastructure testing
* **Playbook Integration**:
    * Use `converge.yml` for role/application deployment
    * Use `prepare.yml` for infrastructure preparation
    * Use `verify.yml` for post-deployment validation
    * Use `side_effect.yml` for testing state changes and recovery scenarios

* **Testing Sequence**:
    * Always test idempotency with `molecule idempotence`
    * Use `molecule test` for complete test cycle (create, converge, idempotency, verify, destroy)
    * Implement proper cleanup in `cleanup.yml` for external resource management
* **Verification**:
    * Use `testinfra` for host-based validation
    * Use `goss` for declarative system state validation
    * Include both positive and negative test cases
    * Test edge cases and error conditions

## 🧩 Placeholder Values Standards

When using placeholder values in templates, configuration files, or for validation purposes, use appropriate realistic values that maintain validation integrity:

### Template Placeholders

* **Jinja2 Variables**: Use meaningful placeholder values that reflect the expected data type:
    * String placeholders: `example-value`, `placeholder-name`, `test-value`
    * Numeric placeholders: `123`, `42`, `999`
    * Boolean placeholders: `true`/`false`
    * List placeholders: `["item1", "item2"]`
    * Dictionary placeholders: `{"key": "value"}`

### Configuration File Placeholders

* **IP Addresses**: Use standard reserved addresses:
    * IPv4: `192.0.2.1`, `198.51.100.1`, `203.0.113.1` (TEST-NET-1, TEST-NET-2, TEST-NET-3)
    * IPv6: `2001:db8::1` (documentation prefix)
* **Hostnames**: Use reserved domains:
    * `example.com`, `example.org`, `example.net`
    * `test.local`, `dev.local`
* **URLs**: Use reserved domains:
    * `https://example.com`, `https://api.example.com`
    * `http://localhost:8080`

### Validation Placeholders

* **File Paths**: Use standard test paths:
    * `/tmp/test-file`, `/var/tmp/test-data`
    * `/opt/test-app`, `/usr/local/test-bin`
* **User/Group Names**: Use standard test names:
    * `testuser`, `testgroup`, `devuser`
    * `appuser`, `serviceaccount`
* **Ports**: Use reserved test ports:
    * `1024-65535` range for non-privileged ports
    * Avoid well-known ports (0-1023)

### Container/Service Placeholders

* **Service Names**: Use descriptive test names:
    * `test-service`, `demo-app`, `validation-container`
* **Database Names**: Use standard test names:
    * `test_db`, `validation_db`, `example_db`
* **Credentials**: Use standard test values:
    * Username: `testuser`, `admin`, `service`
    * Password: `testpassword`, `changeme`, `password123` (never in production!)

## 🧰 Common Patterns & Conventions

### Default Values in Jinja2

* **Safe Defaults**: Always provide safe defaults for undefined variables:
    * Use `variable | default('safe_value')` pattern
    * For booleans: `variable | default(false)`
    * For lists: `variable | default([])`
    * For dictionaries: `variable | default({})`
* **Conditional Assignment**: Use proper conditional assignment:

    ```yaml
    # GOOD
    my_variable: "{{ some_condition | ternary('value_if_true', 'value_if_false') }}"

    # AVOID
    my_variable: "{{ 'value_if_true' if some_condition else 'value_if_false' }}"
    ```

### Error Handling Patterns

* **Try-Catch Equivalents**: Use proper Ansible error handling:
    * Use `block`/`rescue`/`always` for complex error handling
    * Use `failed_when` for custom failure conditions
    * Use `ignore_errors: false` (explicitly set to false, don't rely on defaults)
* **Idempotency Checks**: Always verify idempotency:
    * Use `check_mode: true` for dry-run validation
    * Use `changed_when` to properly detect changes
    * Use `register` and `when` for conditional execution

### Security Patterns

* **Vault Integration**: Proper vault variable handling:
    * Store sensitive data in `group_vars/all/vault.yml`
    * Use `no_log: true` for tasks handling sensitive data
    * Use `!vault` tag for encrypted values
* **Permissions**: Always specify file/directory permissions:
    * Use quoted octal notation: `'0644'`, `'0755'`, `'0600'`
    * Use symbolic notation when appropriate: `u=rw,g=r,o=r`
    * Set proper ownership: `owner: user`, `group: group`

### Performance Patterns

* **Efficiency**: Optimize for performance:
    * Use `delegate_to: localhost` for local tasks
    * Use `async`/`poll` for long-running operations
    * Use `run_once: true` for tasks that only need to run once
* **Caching**: Leverage Ansible's caching mechanisms:
    * Use `gather_facts: true` when facts are needed
    * Use `set_fact` for computed values
    * Cache expensive operations with `set_fact`

### Testing Patterns

* **Idempotency Testing**: Always test idempotency:
    * Run tasks twice to ensure idempotency
    * Use `changed_when` to properly detect changes
    * Verify state consistency
* **Molecule Testing**: Follow Molecule best practices:
    * Use `default` scenario for basic functionality
    * Use `integration` scenario for multi-component testing
    * Use `convergence` scenario for idempotency testing

## 📝 Git & Version Control Standards

### Commit Messages

* **Format**: Use conventional commit format: `type(scope): description`
* **Types**:
    * `feat`: New feature for the user
    * `fix`: Bug fix for the user
    * `docs`: Documentation changes
    * `style`: Code style changes (white-space, formatting, missing semi-colons)
    * `refactor`: Code changes that neither fix a bug nor add a feature
    * `perf`: Performance improvements
    * `test`: Adding missing tests or correcting existing tests
    * `chore`: Other changes that don't modify src or test files
* **Scope**: Optional parenthetical scope after type (e.g., `feat(users)`, `fix(sshd)`, `docs(style-guide)`)
* **Description**: Imperative, lower case, no period at the end
* **Length**: Keep first line under 72 characters
* **Body**: Optional longer description separated by blank line from subject
* **Footer**: Optional footer with breaking changes or issue references
* **Issues**: Reference issues with `fixes #123`, `closes #123`, or `relates to #456`
* **Examples**:

    ```bash
    # GOOD
    feat(users): add SSH key generation capability
    Adds automated SSH key generation for new users with proper permissions
    and configuration for secure access.

    fixes #123
    # GOOD
    fix(sshd): resolve authentication bypass vulnerability

    Corrects SSH configuration that allowed authentication bypass in certain
    edge cases with specific client configurations.
    closes #456

    # GOOD
    docs(style-guide): add Git standards section
    Adds comprehensive Git and version control standards to the style guide
    to ensure consistent collaboration practices.

    # AVOID
    "Fixed bug" or "Updated docs" or "Bug fix" or "Made changes"
    ```

### Branch Naming

* **Feature branches**: `feature/descriptive-name` (e.g., `feature/add-gpu-support`)
* **Bug fixes**: `fix/issue-description` (e.g., `fix/ssh-authentication-bypass`)
* **Documentation**: `docs/topic-name` (e.g., `docs/security-best-practices`)
* **Hotfixes**: `hotfix/critical-issue` (e.g., `hotfix/security-patch`)
* **Release**: `release/version` (e.g., `release/v1.2.0`)

### Pull Request/Merge Request Requirements

* **Title**: Follow same format as commit messages
* **Description**: Include problem statement, solution approach, and testing verification
* **Review**: Require at least one approval before merging
* **CI**: All CI checks must pass before merging
* **Changelog**: Update CHANGELOG.md if user-facing changes are included

### Version Tagging

* **Format**: Use semantic versioning (MAJOR.MINOR.PATCH)
* **Prefix**: Use `v` prefix (e.g., `v1.2.0`)
* **Annotations**: Use annotated tags with release notes

    ```bash
    git tag -a v1.2.0 -m "Release v1.2.0: Security enhancements and performance improvements"
    ```

## 📦 Dependency Management Standards

### Ansible Collection Dependencies

* **Requirements File**: Use `collections.yml` for collection dependencies
* **Version Pinning**: Pin to specific versions for production stability

    ```yaml
    # Production (specific versions)
    collections:
      - name: ansible.posix
        version: "1.5.0"
        source: https://galaxy.ansible.com
      - name: community.general
        version: "8.0.0"
        source: https://galaxy.ansible.com
      - name: containers.podman
        version: "1.18.1"
        source: https://galaxy.ansible.com
    ```

* **Development Versions**: Use ranges for development to allow updates while maintaining compatibility

    ```yaml
    # For development (compatible versions)
    collections:
      - name: ansible.posix
        version: ">=1.5.0,<2.0.0"
        source: https://galaxy.ansible.com
      - name: community.general
        version: ">=8.0.0,<9.0.0"
        source: https://galaxy.ansible.com
    ```

* **Installation**: Use `ansible-galaxy collection install -r collections.yml` for installation
* **Updates**: Regularly update collections following semantic versioning principles
* **Verification**: Verify collection integrity after installation with checksums
* **Local Development**: For local development, use `ansible_collections_path` to reference local collections

### Role Dependencies

* **Requirements File**: Use `requirements.yml` for role dependencies
* **Source Control**: Prefer Git repositories with specific tags/branches for stability

    ```yaml
    # Production (specific version)
    roles:
      - src: https://github.com/organization/role-repo.git
        version: v1.2.3
        name: organization.role_name
    ```

* **Local Dependencies**: Use relative paths for tightly coupled roles within the same project

    ```yaml
    # For local development
    roles:
      - name: local_role
        src: ./roles/local_role
        version: main
    ```

* **Galaxy Roles**: When using Galaxy roles, always specify version for reproducibility
* **Installation**: Use `ansible-galaxy role install -r requirements.yml` for installation
* **Verification**: Test role compatibility after dependency updates

### System Dependencies

* **Detection**: Check for required system packages before installation

    ```yaml
    - name: Check if package is installed
      ansible.builtin.command: command -v package_name
      register: package_check
      failed_when: false
      changed_when: false
    ```

* **Installation**: Use appropriate package managers per distribution

    ```yaml
    - name: Install package (APT)
      ansible.builtin.apt:
        name: "{{ system_dependency_package_name }}"
        state: present
      when: ansible_facts['pkg_mgr'] == 'apt'
    ```

* **Validation**: Verify dependencies are functional after installation

    ```yaml
    - name: Verify dependency functionality
      ansible.builtin.command: package_name --version
      register: dependency_version
      changed_when: false
    ```

* **Version Requirements**: Specify minimum required versions for system dependencies
* **Conflict Resolution**: Handle dependency conflicts gracefully with proper error messages
* **Cleanup**: Remove unnecessary dependencies after installation if they're only needed for setup

## 🔍 Logging & Debugging Standards

### Debug Tasks

* **Verbosity Control**: Use `verbosity` parameter to control when debug tasks appear:

    ```yaml
    - name: Debug variable content
      ansible.builtin.debug:
        var: my_variable
        verbosity: 2  # Only shows with -vv or higher
    ```

* **Validation**: Use `ansible.builtin.assert` for validation:

    ```yaml
    - name: Validate required variables
      ansible.builtin.assert:
        that:
          - required_var is defined
          - required_var | length > 0
        fail_msg: "required_var must be defined and non-empty"
    ```

* **Multiple Variables**: Use `msg` parameter to display multiple variables:

    ```yaml
    - name: Debug multiple variables
      ansible.builtin.debug:
        msg: |
          Variable 1: {{ var1 }}
          Variable 2: {{ var2 }}
          Variable 3: {{ var3 }}
        verbosity: 3
    ```

* **Conditional Debugging**: Use when conditions to enable/disable debugging based on variables:

    ```yaml
    - name: Verbose debugging output
      ansible.builtin.debug:
        var: complex_data_structure
        verbosity: 2
      when: debug_mode | default(false)
    ```

### Logging Output

* **Consistent Format**: Use consistent message formatting across all roles with proper prefixes:

    ```yaml
    - name: Report service status
      ansible.builtin.debug:
        msg: "[{{ role_name }}] Service {{ service_name }} is {{ service_status }}"
    ```

* **Information Density**: Provide sufficient context without overwhelming detail
* **Security Considerations**: Never log sensitive information without proper masking
* **Progress Indicators**: For long-running tasks, provide progress updates:

    ```yaml
    - name: Report progress during long operation
      ansible.builtin.debug:
        msg: "Processing item {{ item.name }} ({{ loop_index }} of {{ total_items }})"
      vars:
        loop_index: "{{ (play_hosts.index(inventory_hostname) + 1) if inventory_hostname in play_hosts else 1 }}"
      when: ansible_verbosity >= 1
    ```

* **Structured Logging**: Use structured logging for better parsing:

    ```yaml
    - name: Structured status report
      ansible.builtin.debug:
        msg:
          - "status: {{ operation_status }}"
          - "duration: {{ operation_duration }}s"
          - "result: {{ operation_result }}"
    ```

### Debugging Conventions

* **Task Naming**: Use descriptive names that indicate debugging purpose (e.g., "Debug: variable_name content")
* **Conditional Debugging**: Use when conditions to enable/disable debugging
* **Cleanup**: Remove or disable debug tasks in production playbooks
* **Performance Impact**: Minimize performance impact of debug tasks by using `changed_when: false`

## 🚀 Preflight Setup Standards

### Preflight Checks

* **Purpose**: Preflight checks validate system readiness before running critical operations
* **Placement**: Place preflight checks in `.ci/preflight_*.sh` scripts or `roles/ops/preflight/tasks/main.yml`
* **Scope**: Validate:
    * System requirements (kernel version, available memory, disk space)
    * Prerequisites (required packages, services, permissions)
    * Configuration (network connectivity, firewall rules, security settings)
    * Risk acknowledgment (safety confirmations for destructive operations)

### System Requirements Validation

* **Kernel Version**: Check minimum kernel version requirements:

    ```bash
    # Check kernel version
    KERNEL_VERSION=$(uname -r | cut -d'-' -f1)
    MIN_KERNEL="5.10.0"
    if [[ "$(printf '%s\n' "$MIN_KERNEL" "$KERNEL_VERSION" | sort -V | head -n1)" == "$MIN_KERNEL" ]]; then
        echo "Kernel version $KERNEL_VERSION meets minimum requirement of $MIN_KERNEL"
    else
        echo "ERROR: Kernel version $KERNEL_VERSION is below minimum requirement of $MIN_KERNEL"
        exit 1
    fi
    ```

* **Memory Availability**: Validate sufficient memory for operations:

    ```bash
    # Check available memory (in MB)
    AVAILABLE_MEM=$(free -m | awk 'NR==2{print $7}')
    REQUIRED_MEM=2048  # 2GB minimum
    if [ "$AVAILABLE_MEM" -lt "$REQUIRED_MEM" ]; then
        echo "ERROR: Insufficient memory. Available: ${AVAILABLE_MEM}MB, Required: ${REQUIRED_MEM}MB"
        exit 1
    fi
    ```

* **Disk Space**: Validate sufficient disk space:

    ```bash
    # Check available disk space (in GB)
    AVAILABLE_DISK=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
    REQUIRED_DISK=10  # 10GB minimum
    if [ "$AVAILABLE_DISK" -lt "$REQUIRED_DISK" ]; then
        echo "ERROR: Insufficient disk space. Available: ${AVAILABLE_DISK}GB, Required: ${REQUIRED_DISK}GB"
        exit 1
    fi
    ```

### Prerequisite Validation

* **Package Managers**: Verify required package managers are available:

    ```bash
    # Check for required package managers
    if ! command -v apt >/dev/null 2>&1 && ! command -v dnf >/dev/null 2>&1 && ! command -v pacman >/dev/null 2>&1; then
        echo "ERROR: No supported package manager found (apt, dnf, pacman)"
        exit 1
    fi
    ```

* **Services**: Verify required services are running:

    ```bash
    # Check if systemd is available and running
    if ! systemctl is-system-running >/dev/null 2>&1; then
        echo "ERROR: Systemd is not available or not running"
        exit 1
    fi
    ```

* **Permissions**: Validate required permissions:

    ```bash
    # Check if running with sufficient privileges
    if [ "$EUID" -ne 0 ]; then
        echo "ERROR: This script must be run as root"
        exit 1
    fi
    ```

### Risk Acknowledgment

* **Safety Variables**: Use safety acknowledgment variables for potentially destructive operations:

    ```yaml
    - name: Validate safety acknowledgment for network changes
      ansible.builtin.fail:
        msg: "ABORTING: This role modifies network configuration and may sever connections. Set 'network_acknowledge_risk: true' to proceed."
      when: not network_acknowledge_risk | default(false)
    ```

* **Configuration Changes**: Warn about configuration changes that may require restarts:

    ```yaml
    - name: Warn about system restart requirement
      ansible.builtin.debug:
        msg: "WARNING: System restart required after these changes. Set 'system_restart_allowed: true' to proceed automatically."
      when: system_restart_required | default(false) and not system_restart_allowed | default(false)
    ```

### Preflight Script Standards

* **Header**: Use proper shebang and error handling:

    ```bash
    #!/bin/bash
    set -euo pipefail
    ```

* **Naming Convention**: Use `preflight_*.sh` naming pattern
* **Exit Codes**: Use appropriate exit codes (0 for success, 1+ for failures)
* **Output Format**: Use consistent output format with INFO/WARN/ERROR prefixes:

    ```bash
    echo "[INFO] Preflight check passed: $CHECK_NAME"
    echo "[WARN] Potential issue detected: $WARNING_MESSAGE" >&2
    echo "[ERROR] Critical failure: $ERROR_MESSAGE" >&2
    ```

### Integration with Ansible

* **Role Integration**: Create a dedicated preflight role that can be included early in playbooks:

    ```yaml
    - hosts: all
      pre_tasks:
        - name: Include preflight checks
          ansible.builtin.import_role:
            name: preflight
    ```

* **Conditional Execution**: Allow skipping preflight checks with environment variable:

    ```bash
    if [ "${SKIP_PREFLIGHT:-false}" = "true" ]; then
        echo "[INFO] SKIP_PREFLIGHT=true; skipping preflight checks"
        exit 0
    fi
    ```

## 🔄 CI/CD Integration Standards

### Pipeline Structure

* **Stages**: Organize pipelines into clear stages (build, test, deploy, verify)
* **Parallelization**: Run independent tests in parallel to reduce execution time
* **Artifacts**: Preserve important outputs for debugging and verification

### Automated Testing

* **Trigger Conditions**: Run tests on all PRs, specific branches, and schedule
* **Test Coverage**: Ensure all roles have Molecule tests
* **Integration Tests**: Include multi-role integration testing
* **Performance Tests**: Include performance regression testing

### Deployment Strategies

* **Blue-Green**: Use for zero-downtime deployments where possible
* **Rolling**: Use for distributed systems with multiple nodes
* **Canary**: Use for gradual rollout of changes to subset of nodes

### Rollback Procedures

* **Automatic Rollback**: Implement automatic rollback on test failures
* **Manual Rollback**: Document manual rollback procedures
* **State Preservation**: Preserve system state during rollback operations

## 📚 Documentation Standards

### README.md Structure

Every role must include a README.md with:

1. **Description**: Brief purpose statement
2. **Requirements**: Ansible version, dependencies, system requirements
3. **Role Variables**: All variables with defaults, types, and descriptions
4. **Dependencies**: Required roles/collections
5. **Example Playbook**: Minimal working example
6. **License**: License type (prefer MIT)
7. **Author Information**: Contact or organization details

### Example Variable Documentation

```yaml
# defaults/main.yml
---
# User account configuration
bootstrap_username: deploy  # Primary deployment user account
bootstrap_uid: 1000          # User ID (integer, 1000-65535)
bootstrap_create_home: true  # Create home directory (boolean)
```

### CHANGELOG Format

* **Semantic Versioning**: Follow semantic versioning in changelog
* **Categories**: Group changes under `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
* **Dates**: Include release dates in ISO format (YYYY-MM-DD)
* **Links**: Link to relevant issues and PRs

### Architecture Decision Records (ADRs)

* **Format**: Use consistent ADR template
* **Location**: Store in `docs/adrs/` directory
* **Numbering**: Sequential numbering with descriptive filenames
* **Status**: Track decision status (proposed, accepted, superseded, deprecated)

## ⚡ Performance & Optimization Guidelines

### Task Execution Optimization

* **Fact Gathering**: Use `gather_facts: false` when facts aren't needed
* **Conditional Execution**: Use `when` clauses to skip unnecessary tasks
* **Idempotency**: Design tasks to be idempotent to avoid unnecessary changes

### Parallelization Guidelines

* **Strategy Selection**: Use `strategy: free` for independent tasks, `strategy: linear` for dependent tasks
* **Fork Control**: Adjust `--forks` based on target system capacity
* **Serial Execution**: Use `serial` for rolling updates to avoid service disruption

### Resource Consumption

* **Memory Usage**: Monitor and optimize memory consumption during execution
* **Disk Space**: Consider disk space requirements for temporary files
* **Network Bandwidth**: Minimize network transfers where possible

## 🌐 Cross-Platform Compatibility

### Path Handling

* **Separators**: Use `ansible.builtin.path_join` for cross-platform path construction
* **Normalization**: Use `ansible.builtin.abs` and `ansible.builtin.dirname` for path manipulation
* **Variables**: Use `ansible_facts` for platform-specific paths (e.g., `ansible_facts.python.executable`)

### Line Ending Considerations

* **Templates**: Use appropriate line endings for target platform
* **Scripts**: Ensure shell scripts have proper line endings (Unix-style LF)
* **Text Files**: Maintain consistent line endings across platforms

### Case Sensitivity

* **Variable Names**: Use lowercase with underscores (snake_case) to avoid case issues
* **File Names**: Use lowercase with underscores for consistency
* **Paths**: Be aware of case sensitivity differences between platforms

## 🔐 Secret Management Beyond Vault

### External Secret Managers

* **Integration**: Support integration with HashiCorp Vault, AWS Secrets Manager, Azure Key Vault
* **Fallback**: Implement Vault file fallback when external managers unavailable
* **Caching**: Implement secure caching for external secret retrieval

### Secret Rotation

* **Strategies**: Implement automated secret rotation where possible
* **Notification**: Notify stakeholders of upcoming secret rotations
* **Validation**: Validate new secrets before retiring old ones

### Temporary Credentials

* **Lifespan**: Limit lifespan of temporary credentials
* **Cleanup**: Automatically clean up expired temporary credentials
* **Access**: Restrict access to temporary credentials to necessary processes only

## 📊 Monitoring & Observability

### Execution Metrics

* **Timing**: Use `profile_tasks` callback to monitor task execution time
* **Metrics**: Collect and report execution metrics for performance analysis
* **Baseline**: Establish performance baselines for regression detection

### Callback Plugins

* **Selection**: Use appropriate callback plugins for different monitoring needs
* **Configuration**: Configure callbacks for both development and production
* **Output**: Format output for integration with monitoring systems

### Integration Points

* **Prometheus**: Export metrics in Prometheus format when possible
* **Logging Systems**: Integrate with centralized logging systems (ELK, Graylog)
* **Alerting**: Implement alerting for critical failures and performance degradation

## 🚨 Assume Nothing Philosophy

Following Ansible's core design principle, all automation must operate under the "assume nothing" philosophy:

### Explicit Configuration Requirements

* **Never assume defaults**: Always explicitly configure values rather than relying on implicit defaults
* **Validate prerequisites**: Check for required resources, permissions, and dependencies before proceeding
* **Fail fast**: Use `ansible.builtin.assert` to validate assumptions early in task execution
* **Environment awareness**: Always check environment conditions before making changes
* **Ansible configuration awareness**: Understand and explicitly set Ansible's default behaviors (e.g., `error_on_undefined_vars: true`, `host_key_checking: true`) to ensure predictable behavior

### Example Implementation

```yaml
# GOOD - Explicit validation and conditional decision making
- name: Validate required variables are set
  ansible.builtin.assert:
    that:
      - target_directory is defined
      - target_directory | length > 0
      - target_directory is string
    fail_msg: "target_directory must be defined as a non-empty string"
- name: Validate directory exists and is accessible
  ansible.builtin.stat:
    path: "{{ target_directory }}"
  register: dir_stat
  failed_when: not dir_stat.stat.exists or not dir_stat.stat.isdir

# BAD - Assuming directory exists
- name: Copy files to target directory
  ansible.builtin.copy:
    src: files/config.conf
    dest: "{{ target_directory }}/config.conf"
```

### Connection and Authentication

* **Connection validation**: Always verify connectivity before executing tasks
* **Authentication verification**: Confirm authentication methods work before proceeding
* **Privilege escalation**: Explicitly define and validate become requirements
* **Facts validation**: Always verify that required facts are available before using them; use `| default()` filters safely

## 🔒 Security-First Defaults

All configurations must default to the most secure settings:

### Certificate Validation

* **Always validate**: Default `validate_certs: true` for all SSL/TLS connections
* **Explicit exceptions**: Only disable certificate validation with proper justification and documentation
* **Secure protocols**: Default to latest secure protocol versions

### Network Security

* **Restrictive firewalls**: Default to deny-all rules with explicit allowances
* **Service exposure**: Minimize service exposure by default
* **Port security**: Close unused ports by default

### Permission Security

* **Least privilege**: Default to minimal required permissions
* **Explicit escalation**: Only escalate privileges when explicitly required
* **Audit trail**: Maintain audit trails for all privileged operations

## ✅ Strict Validation Patterns

### Pre-flight Validation

* **System readiness**: Validate system state before making changes
* **Dependency checks**: Verify all dependencies are available and functional
* **Resource availability**: Confirm sufficient resources (memory, disk, CPU) are available
* **Permission validation**: Verify required permissions before executing tasks
* **Configuration validation**: Validate configuration parameters before applying them
* **Connectivity verification**: Test connectivity to required services and endpoints

### Runtime Validation

* **Input sanitization**: Sanitize and validate all inputs before processing
* **State verification**: Verify system state after each operation
* **Idempotency checks**: Confirm operations are idempotent before execution
* **Progress validation**: Validate that long-running operations are progressing as expected
* **Intermediate state checks**: Verify intermediate states during complex operations

### Post-execution Validation

* **Result verification**: Validate that operations produced expected results
* **Side-effect checks**: Verify no unintended side effects occurred
* **Clean-up verification**: Confirm all temporary resources were cleaned up
* **Service health checks**: Verify that services are running correctly after changes
* **Functional validation**: Test that affected systems function as expected after changes

## ❗ Robust Error Handling

### Fail-Safe Defaults

* **Safe failure modes**: Design systems to fail in a safe state
* **Graceful degradation**: Implement graceful degradation when components fail
* **Recovery procedures**: Provide clear recovery procedures for common failure scenarios

### Comprehensive Error Detection

* **Multi-layer validation**: Implement validation at multiple layers (input, processing, output)
* **Early detection**: Detect and report errors as early as possible
* **Detailed diagnostics**: Provide detailed diagnostic information for troubleshooting

### Edge Case Handling

* **Undefined variables**: Always provide safe defaults for undefined variables using `| default()` filter
* **Missing facts**: Handle cases where expected facts are not available using `| default()` with safe fallbacks
* **Network timeouts**: Implement appropriate retry mechanisms and timeouts for network operations
* **Resource contention**: Handle cases where resources are temporarily unavailable
* **Partial failures**: Design operations to handle partial failures gracefully without leaving systems in inconsistent states
* **Unexpected responses**: Validate API responses and command outputs before processing them
* **Deployment interruptions**: Implement checkpoint and resume functionality to handle deployment interruptions

## 🛡 Disaster Recovery & Backup Standards

### Configuration Backup

* **Automation**: Automate backup of critical configuration files
* **Retention**: Implement appropriate retention policies for backups
* **Verification**: Regularly verify backup integrity and restoration procedures

### State Recovery

* **Idempotency**: Ensure playbooks can recover to desired state from any intermediate state
* **Rollback Playbooks**: Maintain dedicated rollback playbooks for emergency situations
* **Recovery Procedures**: Document manual recovery procedures for automation failures
* **Checkpoint Creation**: Implement checkpoint creation at logical deployment boundaries to enable resumable operations
* **Resume Capability**: Design playbooks with resume capability from checkpoints after interruption

### Checkpoint and Resume Standards

* **Checkpoint Location**: Store checkpoints in `/var/lib/deploy-system/checkpoints/` with appropriate permissions (mode `0600`)
* **Checkpoint Format**: Use JSON format for checkpoints with standardized fields:
    * `deployment_id`: Unique identifier for the deployment session
    * `status`: Current status (e.g., `running`, `not running`, `completed`, `not completed`, `failed`, `not failed`)
    * `last_successful_task`: Name of the last successfully completed task
    * `next_task_to_resume`: Name of the task to resume from
    * `completed_phases`: Array of completed deployment phases
    * `current_phase`: Current deployment phase being executed
    * `start_time`: ISO 8601 timestamp of deployment start
    * `last_updated`: ISO 8601 timestamp of last checkpoint update
    * `resume_attempts`: Number of resume attempts made
    * `deployment_variables`: Snapshot of deployment variables at checkpoint time
    * `system_context`: System information relevant to deployment
* **Resume Logic**: Implement conditional logic to detect existing checkpoints and resume from appropriate task if found
* **Progress Tracking**: Update checkpoints after each major phase completion
* **Failure Handling**: Create checkpoints when failures occur to enable recovery
* **Log Integration**: Update deployment logs when checkpoints are created or resumed from

### Testing Procedures

* **Regular Testing**: Regularly test disaster recovery procedures
* **Simulation**: Simulate various failure scenarios for comprehensive testing
* **Resume Testing**: Test resume functionality from various checkpoint states
* **Documentation**: Document recovery time objectives (RTO) and recovery point objectives (RPO)

## 🤖 LLM Guidance

This section is for AI assistants helping with this repository.

1. **Read First**: Before modifying any file, read its existing content and this style guide. Adhere strictly to the established patterns.
2. **Linting is Mandatory**: After any modification, you MUST run `make lint` (or the specific sub-linter) to verify your changes. Do not consider a task complete until linters pass.
3. **Atomic Changes**: Prefer multiple small `replace` calls over one massive change. This makes validation easier and reduces the risk of breakage.
4. **No Explanatory Comments**: Do not add comments describing *what* your code does. Only add comments explaining *why* a specific complex logic was chosen if it's not obvious.
5. **Security Guardrails**:
    * Never remove `no_log: true` from tasks that have it.
    * Never introduce hardcoded credentials.
    * Ensure all shell tasks use `set -o pipefail`.
6. **Jinja2 Escaping**: Be extremely careful with character sequences like `${#` and `{{` in templates. Use the escaping patterns defined in the "Ansible & Jinja2 Standards" section.
7. **Deduplication**: If you notice massive duplication in documentation (like in `usage.md`), proactively deduplicate it using Python scripts or surgical edits.

### Conflict Resolution Hierarchy

When multiple standards appear to conflict, apply this hierarchy:

1. **Security** > All other considerations
2. **Idempotency** > Portability, Performance, Convenience
3. **Portability** > Performance, Convenience
4. **Performance** > Convenience
5. **Convenience** (lowest priority)

### Fail Closed Principles

When uncertain about implementation choices, default to the most secure and conservative option:

* **Unknown Variables**: Default to secure values (e.g., `false`, `disabled`, `deny`)
* **Module Choice**: Choose specialized modules over generic `shell` or `command`
* **Inclusion Strategy**: Choose `import_*` over `include_*` when uncertain
* **Permission Defaults**: Choose restrictive permissions over permissive
* **Network Access**: Choose deny-all over allow-all when uncertain
* **Service Exposure**: Choose minimal exposure over maximum functionality

### LLM Operating Mode

Follow these strict operating principles:

* **No Invented Files**: Do not create files that were not explicitly requested
* **No Rule Relaxation**: Do not relax rules for brevity or convenience
* **No Omitted Metadata**: Do not silently omit required metadata or configuration elements
* **No Assumption Making**: Do not make assumptions about missing information; ask for clarification
* **No Creative Interpretation**: Do not interpret requirements creatively; follow them exactly as specified
* **No Scope Expansion**: Do not expand the scope of requested changes beyond what was specified

### LLM Priority Guidelines

When working with LLMs on this codebase, prioritize these elements with clear intent and goals:

* **Clear Intent Communication**: Use explicit, unambiguous language when describing the purpose of code changes
* **Goal-Oriented Changes**: Every modification should have a clearly stated goal that aligns with project objectives
* **Precision Over Creativity**: Prioritize exact specification fulfillment over creative interpretation
* **Explicit Context Provision**: Provide sufficient context for each change to ensure proper understanding
* **Direct Problem Solving**: Address the specific problem stated without adding unrelated functionality
* **Transparent Decision Making**: Clearly document the reasoning behind each technical decision
* **Focused Scope Management**: Stay within the bounds of the requested task while achieving the intended outcome
* **Verifiable Outcomes**: Ensure all changes produce measurable, verifiable results that meet the stated goals

### Strict Upgrade Policies

When implementing upgrades, follow these strict policies that prioritize security and system integrity over backward compatibility:

* **Zero-Downtime Upgrades**: Always implement rolling updates that maintain service availability
* **Immutable Infrastructure**: Treat systems as immutable after deployment; redeploy rather than modify in-place
* **Version Pinning**: Pin all dependencies to specific versions to prevent unexpected updates
* **Automated Rollbacks**: Implement automatic rollback mechanisms for failed upgrades
* **Comprehensive Testing**: Test all upgrades in staging environments before production deployment
* **Breaking Changes Acceptance**: Accept breaking changes as necessary for security improvements
* **Hard Deprecation**: Remove deprecated features aggressively rather than maintaining compatibility
* **Security-First Updates**: Prioritize security patches over feature additions
* **State Management**: Ensure state is preserved or properly migrated during upgrades
* **Configuration Validation**: Validate all configurations after upgrades to ensure correctness

### LLM Application of "Assume Nothing" Philosophy

When implementing the "assume nothing" philosophy, LLMs should follow these specific directives:

* **Validate Before Action**: Always verify prerequisites exist before performing operations
* **Explicit Configuration**: Never rely on implicit defaults; always specify configuration values explicitly
* **Comprehensive Checking**: Verify system state, permissions, dependencies, and connectivity before proceeding
* **Safe Defaults**: When defaults must be used, ensure they are the most secure and conservative options
* **Error Anticipation**: Plan for and handle potential failures at every step of execution
* **State Verification**: Confirm system state before and after operations to ensure expected outcomes
* **Requirement Validation**: Explicitly check that all requirements are met before beginning any process
