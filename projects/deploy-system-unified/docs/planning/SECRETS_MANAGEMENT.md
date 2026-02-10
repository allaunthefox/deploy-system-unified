# SECRETS_MANAGEMENT

**Status:** Planned. Ansible Vault is currently active for deployments.

This project adopts **SOPS** (Secrets OPerationS) with **Age** encryption for managing sensitive credentials. This approach allows us to keep encrypted secrets in the Git repository while maintaining granular control and diff-ability.

## Why SOPS?

* **Encrypted Values, Visible Keys**: Unlike Ansible Vault (which encrypts the full file), SOPS only encrypts the *values*. This allows us to see variable names in Git diffs.
* **No Shared Passwords**: Uses Age public/private key pairs instead of a shared symmetric password.
* **Ansible Integration**: Using `community.sops`, encrypted files are decrypted on-the-fly during playbook execution.

## Prerequisites

1. **Install Tools**:

    ```bash
    # Install SOPS
    curl -LO https://github.com/getsops/sops/releases/download/v3.9.0/sops-v3.9.0.linux.amd64
    sudo mv sops-v3.9.0.linux.amd64 /usr/local/bin/sops
    sudo chmod +x /usr/local/bin/sops

    # Install Age
    sudo apt-get install age
    ```

2. **Install Ansible Collection**:

    ```bash
    ansible-galaxy collection install community.sops
    ```

3. **Generate Keys** (One-time setup per Admin):

    ```bash
    mkdir -p ~/.config/sops/age
    age-keygen -o ~/.config/sops/age/keys.txt
    ```

    * **Keep `keys.txt` SAFE.** This is the master key to decrypt everything.
    * **Note the Public Key** (`age1...`). You will need this for the configuration.

## Project Configuration

### 1. `.sops.yaml`

Root configuration file defining which keys govern which files.

```yaml
creation_rules:
  # Encrypt all secret group_vars
  - path_regex: group_vars/.*\.sops\.ya?ml$
    key_groups:
      - age:
          - "age1..." # REPLACEME with Recipient Public Keys
```

### 2. `ansible.cfg`

Enable the plugin to autoload `.sops.yml` files.

```ini
[defaults]
vars_plugins_enabled = host_group_vars, community.sops.sops
```

## Workflow

### Creating a Secret

Do not edit secret files directly with `nano` or `vim`. Use `sops`.

```bash
# Creates (or edits) an encrypted file
sops group_vars/all/secrets.sops.yml
```

Content should look like standard YAML:

```yaml
db_password: "my_super_secret_password"
api_token: "xxyyzz"
```

### Usage in Playbooks

Simply reference the variable as normal.

```yaml
- name: Print Secret
  debug:
    msg: "The password is {{ db_password }}"
```

## Migration Checklist

* [ ] Install SOPS and Age binaries.
* [ ] Generate project Age keys.
* [ ] Create `.sops.yaml`.
* [ ] Enable `community.sops.sops` in `ansible.cfg`.
* [ ] Migrate `authentik_secret_key`, `postgres_password`, `transmission_pass`, `vaultwarden_admin_token` to `group_vars/all/secrets.sops.yml`.
* [ ] Add `access_admin_password_hash` to `group_vars/all/secrets.sops.yml` (hashed password for admin user).
* [ ] Remove hardcoded secrets from `defaults/main.yml` files.
