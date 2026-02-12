Security tooling and guidance
This directory contains guidance and helper scripts related to detecting and handling secrets.

Detect-secrets CI

- We run `detect-secrets` in CI via `.github/workflows/detect-secrets.yml` to detect accidental commits of secrets.
- To run locally:

  python -m pip install detect-secrets
  detect-secrets scan --all-files --json > .secrets_scan.json
- If the scan finds results, review the listed files and remove/rotate secrets; prefer Ansible Vault or an external secret manager.

Ansible Vault guidance

- Never commit plaintext secrets to the repository.
- Use `ansible-vault` to encrypt sensitive variables and reference them in roles.
- Example workflow:
  1. Create an encrypted file: `ansible-vault encrypt group_vars/all/vault.yml`
  2. Add variables (e.g., `database_password: !vault | ENC[...]`)
  3. In your playbooks/roles, reference `vars_files: - group_vars/all/vault.yml`

If you'd like, I can add a sample playbook and CI checks to validate vault usage.
