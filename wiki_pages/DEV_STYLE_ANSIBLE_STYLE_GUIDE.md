# Ansible_Style_Guide

To maintain consistency and ensure clean linting for Ansible content in the Deploy-System-Unified project, all contributions must adhere to the following style requirements.

## Ansible-Specific Standards

* **Task Naming**: All tasks must have descriptive names that clearly indicate their purpose.
* **Idempotency**: All tasks must be idempotent - running them multiple times should have the same effect as running them once.
* **Handlers**: Use handlers for services that should only restart when configuration changes.
* **Includes vs Imports**: Use `include_tasks` for dynamic inclusion and `import_tasks` for static inclusion.
* **Roles Structure**: Follow the standard Ansible role directory structure with proper separation of concerns.
* **Variables**: Use descriptive variable names and define defaults in `defaults/main.yml`.
* **Conditionals**: Use `when` clauses appropriately to conditionally execute tasks.
* **Loops**: Use `loop` instead of `with_items` and other deprecated loop constructs.

## Best Practices

* **Error Handling**: Implement proper error handling and validation.
* **Security**: Never hardcode secrets in playbooks; use vault or other secure methods.
* **Documentation**: Document all roles and complex tasks with clear explanations.
* **Testing**: Include tests for all roles to ensure functionality and idempotency.

## Linting

These standards are enforced via the `make lint` suite. All Ansible files must pass linting checks before acceptance.