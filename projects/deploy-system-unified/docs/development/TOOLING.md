# Development Tooling

The project uses a high-performance enforcement engine to maintain architectural integrity.

## 🛠 `enforce_style_guide.sh`

This script is the primary gatekeeper for the project's standards. It utilizes **ripgrep (rg)** and **fd** for near-instant auditing of the codebase.

### Command Switches

| Switch | Name | Risk Level | Description |
| :--- | :--- | :--- | :--- |
| (None) | **Audit Mode** | N/A | Runs all checks (YAML, Ansible, Shell, Security, Structure) and reports violations without changing any files. Returns exit code 1 if issues are found. |
| `-p`, `--low-risk-repair` | **Safe Repair** | **Zero** | **Recommended for automation.** Automatically fixes non-destructive issues: trailing spaces, missing EOF newlines, and missing YAML document starts (`---`). |
| `-f`, `--fix` | **Auto-Fix** | **Moderate** | Performs all Safe Repairs PLUS structural changes: renames files with spaces or uppercase letters to `snake_case`. **Warning:** This can break internal imports if not reviewed. |
| `-r`, `--report` | **Report Only** | N/A | Generates a Markdown compliance report but always exits with 0. Used primarily in CI/CD to upload artifacts even if checks fail. |
| `-q`, `--quiet` | **Quiet Mode** | N/A | Suppresses all output except for critical errors. |

### Advanced Audits

- **Recursive Role Audit**: Unlike standard linters, this tool recursively searches for nested roles (e.g., `roles/core/time`) and enforces a full directory structure (`vars/`, `handlers/`, etc.).
- **Embedded Shell Audit**: Uses **Shellcheck** to lint code inside `ansible.builtin.shell` blocks, preventing logic errors in embedded scripts.
- **Security Audit**: Uses targeted regex to find world-writable modes (`777`, `666`) and hardcoded secret patterns.

## 🧪 Molecule

Scenario-based testing for idempotency and multi-platform support.

- Use `molecule test` to run the full sequence (Destroy -> Create -> Converge -> **Idempotence** -> Verify).

## 🔍 Manual Syntax Checks

To verify the playbooks and role paths without standard inventory warnings, use the validation inventory:

```bash
export ANSIBLE_ROLES_PATH=./roles
ansible-playbook -i inventory/validation.ini --syntax-check branch_templates/*.yml
```
