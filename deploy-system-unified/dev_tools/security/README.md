Security tooling and guidance
This directory contains guidance and helper scripts related to detecting and handling secrets.

Detect-secrets CI

- We run `detect-secrets` in CI via `.github/workflows/detect-secrets.yml` to detect accidental commits of secrets.
- The CI now emits a `/.detect-secrets-findings.md` artifact and creates GitHub check annotations that include `file:line` references and nearby code snippets to make triage easier.
- To run locally and reproduce the CI artifact:

  python -m pip install detect-secrets jq
  detect-secrets scan --all-files --json > .secrets_scan.json
  # or use the provided local runner to produce the same CI artifacts:
  .ci-local/run-local-ci.sh detect-secrets

- If the scan finds results, review the listed files and remove/rotate secrets; prefer Ansible Vault or an external secret manager.

Ansible Vault guidance

- Never commit plaintext secrets to the repository.
- Use `ansible-vault` to encrypt sensitive variables and reference them in roles.
- Example workflow:
  1. Create an encrypted file: `ansible-vault encrypt group_vars/all/vault.yml`
  2. Add variables (e.g., `database_password: !vault | ENC[...]`)
  3. In your playbooks/roles, reference `vars_files: - group_vars/all/vault.yml`

If you'd like, I can add a sample playbook and CI checks to validate vault usage.
