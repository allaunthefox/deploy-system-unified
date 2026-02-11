# TOOLING

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

Located in the `projects/deploy-system-unified/scripts/` directory, these tools are used for pre-deployment verification and CI gates.

- **`verify_idempotence.sh`**: Runs a playbook twice and asserts that the second run produces `changed=0`.
- **`smoke_test_production.sh`**: Performs a syntax check and a dry-run (`--check`) of the production deployment using the validation inventory.

## 🛠 Operational & Utility Scripts

Additional scripts for specialized tasks:

- **`run_deployment_session.sh`**: Ensures deployments run within a persistent `tmux` session to prevent interruption.
- **`setup_crowdsec.py`**: Automates the initialization and configuration of the CrowdSec security engine.
- **`porkbun_dns.py`**: Manages DNS records via the Porkbun API for automated certificate challenges.
- **`stage_migration_assets.sh`**: Prepares legacy data and assets for migration into the new system structure.
- **`ensure_podman_access.sh` / `ensure_docker_access.sh`**: Preflight checks to verify container engine accessibility for the current user.

## 🧹 Maintenance & Generation

Scripts used to maintain the documentation and project health:

- **`generate_role_pages.py`**: Automatically generates wiki detail pages from Ansible role source code.
- **`wiki_wiki_lint.py`**: High-performance linter for maintaining wiki consistency and integrity.
- **`wiki_check_fix.py`**: Utility for repairing common wiki structural issues.


## 🏗️ Core Configuration

The project is optimized for performance and security via `ansible.cfg`:

- **SOPS Integration**: Native support for SOPS-encrypted variables via `community.sops.sops`.
- **SSH Optimization**: Uses `pipelining` and `piped` transfer methods for speed; includes aggressive retry logic and connection persistence (`ControlPersist=60s`) to bridge network gaps.
- **Forensic Readiness**: Every run is logged to `./ansible.log` with timing information enabled (`profile_tasks`).

## ⚙️ Makefile

The `Makefile` provides standardized entry points for local development and CI:

- `make lint`: Runs `ansible-lint` against the entire project.
- `make molecule-precheck`: Verifies Podman access before running integration tests.
- `make test-x86` / `make test-arm64`: Executes architecture-specific GPU slicing tests via Molecule.

## 🧪 Molecule

Scenario-based testing for idempotency and multi-platform support.

- Use `molecule test` to run the full sequence (Destroy -> Create -> Converge -> **Idempotence** -> Verify).
