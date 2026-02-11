# YAML_Style_Guide

To maintain consistency and ensure clean linting for YAML files in the Deploy-System-Unified project, all contributions must adhere to the following style requirements.

## General Standards

* **Extensions**: Use `.yml` for all YAML files, not `.yaml`.
* **EOF Newlines**: Every file (YAML, Markdown, Jinja2, etc.) must end with exactly one newline character.
* **Trailing Whitespace**: No lines should have trailing spaces or tabs.
* **Indentation**: Use spaces for indentation, never tabs.

## YAML-Specific Standards

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
    ```

## Linting

These standards are enforced via the `make lint` suite. All YAML files must pass linting checks before acceptance.