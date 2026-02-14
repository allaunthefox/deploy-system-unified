# Rclone Role

This role installs and configures **Rclone**, enabling cloud storage connectivity for backups (specifically Restic).

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `rclone_enable` | `true` | Enable/Disable role. |
| `rclone_conf_file` | `/etc/rclone/rclone.conf` | Path to the config file (root-only). |
| `rclone_config_content` | `""` | **REQUIRED**. The raw content of the rclone config file (INI format). Must be provided via encrypted variables. |

## Usage with SOPS/Vault

This role expects the **entire** file content to be passed as a variable string. This allows complex multi-remote configurations without complex Ansible variable mapping.

1. Generate your config locally: `rclone config`
2. Copy the content of `~/.config/rclone/rclone.conf`.
3. Add it to your encrypted inventory:

```yaml
# group_vars/all/secrets.yml
rclone_config_content: |
  [gdrive]
  type = drive
  client_id = ...
  client_secret = ...
  token = ...

  [backblaze]
  type = b2
  account = ...
  key = ...
```
