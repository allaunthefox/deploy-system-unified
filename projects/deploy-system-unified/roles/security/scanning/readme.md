security/scanning role

This role provides a comprehensive security framework for the Deploy-System-Unified project, including system validation, secure time synchronization, security tool configuration (trivy, aide, lynis, etc.), and secure handling of temporary files and SSH information.

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
