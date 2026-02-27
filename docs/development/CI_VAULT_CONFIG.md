# CI/CD Vault Configuration

## Overview

This project uses Ansible Vault for encrypting sensitive data. The vault configuration supports both production deployments and CI/lint workflows.

## Configuration

### Production Deployments

For production deployments, the vault password is read from `.vault_pass` file:

```ini
# ansible.cfg
vault_password_file = .vault_pass
```

### CI/Lint Workflows (No Vault)

For CI/lint workflows that don't need vault decryption, override via environment variable:

```bash
# Disable vault for lint-only workflows
export ANSIBLE_VAULT_PASSWORD_FILE=/dev/null

# Run lint/validation
ansible-lint
yamllint .
```

**Why use `/dev/null`?**
- Allows playbook syntax validation without vault secrets
- Enables linting in public CI pipelines
- Prevents accidental secret exposure in logs

## Environment Variable Priority

Ansible vault password file resolution follows this order:

1. `ANSIBLE_VAULT_PASSWORD_FILE` environment variable (highest priority)
2. `vault_password_file` in ansible.cfg
3. `--vault-password-file` command-line argument (highest when specified)

## CI/CD Examples

### GitHub Actions

```yaml
- name: Run Ansible lint (no vault)
  run: ansible-lint
  env:
    ANSIBLE_VAULT_PASSWORD_FILE: /dev/null

- name: Deploy with vault
  run: ansible-playbook site.yml
  env:
    ANSIBLE_VAULT_PASSWORD_FILE: ${{ secrets.VAULT_PASSWORD }}
```

### Local Development

```bash
# Lint without vault (safe for public CI)
export ANSIBLE_VAULT_PASSWORD_FILE=/dev/null
ansible-lint

# Deploy with vault
export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass
ansible-playbook site.yml
```

## Security Considerations

1. **Never commit `.vault_pass`** - It's in `.gitignore` by default
2. **Use environment variables in CI** - Don't hardcode vault passwords
3. **Separate lint/deploy workflows** - Lint doesn't need vault access
4. **Audit vault usage** - Check `ansible.log` for vault operations

## Troubleshooting

### ERROR: Vault password required

```bash
# Solution 1: Set vault password file
export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass

# Solution 2: Use command-line argument
ansible-playbook site.yml --vault-password-file .vault_pass

# Solution 3: For lint-only, disable vault
export ANSIBLE_VAULT_PASSWORD_FILE=/dev/null
```

### ERROR: Vault decryption failed

```bash
# Check vault password file permissions
chmod 600 .vault_pass

# Verify vault password is correct
ansible-vault view secrets.yml --vault-password-file .vault_pass
```

## Related Documentation

- [Ansible Vault Best Practices](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
- [SOPS Integration](./docs/development/SOPS_INTEGRATION.md)
- [Secret Management](./docs/security/SECRET_MANAGEMENT.md)
