# PRE_COMMIT

This document explains how to install and use the repository's local pre-commit hook and run the style enforcement script locally.

## Why
Running the enforcement locally prevents style violations (YAML, Ansible, FQCN, ShellCheck, etc.) from reaching CI and keeps the `main` branch green.

## Requirements
- Python 3.8+ (for `pre-commit` and optional tools)
- `pre-commit` (install via `pip` or `pipx`)
- System packages used by the enforcement script: `ripgrep` (`rg`), `fd-find` (`fd`), `shellcheck`

## Install `pre-commit`

Recommended (pipx):

- pipx: `pipx install pre-commit`

Or with pip in a virtualenv:

- python -m pip install --user pre-commit

## Install the hooks for this repo

From the repository root:

- pre-commit install
- pre-commit install --hook-type pre-push  # optional: ensure check runs on push

## Run the style enforcement locally

To run the enforcement manually (fast, single check):

- bash dev_tools/tools/style-guide-enforcement/run_and_fail_on_violations.sh --report

This will produce a report file under `dev_tools/tools/style-guide-enforcement/` named like `compliance_report_YYYYMMDD_HHMMSS.md`. The script exits non-zero if violations are found.

### Run Style Tooling Unit Tests
If you modify the enforcement script or patterns, verify the changes by running the unit test suite:
```bash
pytest -q dev_tools/tools/style-guide-enforcement/tests
```

To run all configured pre-commit hooks on all files (useful before pushing):

- pre-commit run --all-files

## Troubleshooting
- If `fd` is not available as `fd` on Debian/Ubuntu, the CI wrapper links `fdfind` to `fd` when installing dependencies.
- If the enforcement script reports missing tools, install `ripgrep` (`rg`), `fd-find` (`fd`), and `shellcheck`.

## Notes
- The pre-commit hook is intentionally conservative and uses the same enforcement script that CI runs, keeping local and CI behavior aligned.
- If you need to skip the hook for a quick commit, use: `git commit --no-verify` (but avoid doing so routinely).
