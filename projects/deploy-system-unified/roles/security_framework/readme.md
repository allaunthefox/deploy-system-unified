security_framework role

This role contains tasks related to secure temporary files and other security hardening.

Secrets & Vault

- **Do not** commit plaintext secrets to the repository.
- This role expects secret variables to be supplied by an encrypted file (Ansible Vault) or external secret manager.

Recommended variables (place in `group_vars/all/vault.yml` or another encrypted file):

```yaml
# Example: group_vars/all/vault.yml (encrypted with ansible-vault)
database_password: "<your-database-password>"
api_token: "<your-api-token>"
ssh_private_key: "<your-ssh-private-key>"
```

Usage

- Create an encrypted file and add it to your playbook or group vars.
- Do not store actual values in the repo; commit only example files or placeholders.

If you want, I can add a safety check to CI that fails if any role file contains an unencrypted secret in a future PR.