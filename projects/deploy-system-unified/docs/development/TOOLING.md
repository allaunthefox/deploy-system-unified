# TOOLING

The project uses a high-performance enforcement engine to maintain architectural integrity.

## ✅ Stable Local Tooling (Recommended)

To avoid collection version drift and lint warnings, run tooling from the project venv and use the project-local collections cache:

```bash
python -m venv .venv
./.venv/bin/pip install ansible-core==2.20.2 ansible-lint==26.1.1
./.venv/bin/ansible-galaxy collection install -r requirements.yml -p .collections
```

Notes:
- `ansible.cfg` pins `collections_path` to `.collections`, so no extra env vars are needed.
- `dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh` automatically prefers `.venv` when present.

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

- **FQCN Compliance**: Uses multiline PCRE patterns via `rg -U` to ensure all Ansible tasks use Fully Qualified Collection Names (e.g., `ansible.builtin.copy`).
- **Recursive Role Audit**: Recursively searches for nested roles and enforces a full standard directory structure (`vars/`, `handlers/`, etc.).
- **Embedded Shell Audit**: Uses **Shellcheck** to lint code inside `ansible.builtin.shell` blocks.
- **Security Audit**: Identifies unsafe permissions (`777`) and potential hardcoded secrets.

### Unit Testing the Tool
The enforcement logic is verified by a `pytest` suite located in `dev_tools/tools/style-guide-enforcement/tests/`. Run these before modifying the enforcement script:
```bash
python3 -m pytest dev_tools/tools/style-guide-enforcement/tests/
```

## 🛡️ Stability Gating Scripts

Located in the `scripts/` directory, these tools are used for pre-deployment verification and CI gates.

- **`verify_idempotence.sh`**: Runs a playbook twice and asserts that the second run produces `changed=0`.
- **`smoke_test_production.sh`**: Performs a syntax check and a dry-run (`--check`) of the production deployment using the validation inventory.

## 🧪 Molecule

Scenario-based testing for idempotency and multi-platform support.

- Always run Molecule from the project venv (or with the venv on `PATH`) so it uses the pinned `ansible-core` and the project `.collections`:
  `source .venv/bin/activate && molecule test -s <scenario>`
- Use `molecule test` to run the full sequence (Destroy -> Create -> Converge -> **Idempotence** -> Verify).
