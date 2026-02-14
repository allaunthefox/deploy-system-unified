# Ops Container Role

This role deploys operational dashboard and utility tools alongside the media stack.

## Storage Locations

Persistence is split between application configuration and potential data storage.

### Configuration Data

Base Path: `{{ ops_config_dir }}` (Default: `/srv/containers/ops_config`)

| Directory | Service | Description |
| :--- | :--- | :--- |
| `/homarr/configs` | Homarr | Dashboard JSON configurations |
| `/homarr/icons` | Homarr | Uploaded dashboard icons |
| `/homarr/data` | Homarr | Persistent app data |
| `/vaultwarden` | Vaultwarden | SQLite DB, RSA Keys, Attachments |
| `/wiki/data` | Wiki.js | SQLite DB (if used) or Local Git Repo |
| `/wastebin` | Wastebin | SQLite DB for pastes |

### Operational Data

Base Path: `{{ ops_root_dir }}` (Default: `/srv/ops`)

* *Reserved for future shared operational data dumps (logs, backups).*

## Network

* **Internal Network**: All services run on the `ops_pod` attached to `{{ ops_pod_network }}` (Default: `deploy-net`).
* **Ingress**: Caddy Reverse Proxy handles all traffic.
    * `dashboard.{{ ops_domain }}` -> Homarr
    * `vault.{{ ops_domain }}` -> Vaultwarden
    * `wiki.{{ ops_domain }}` -> Wiki.js
    * `paste.{{ ops_domain }}` -> Wastebin

## Key Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `ops_enable` | `true` | Main toggle. |
| `homarr_enable` | `true` | Deploy the dashboard. |
| `vaultwarden_enable` | `true` | Deploy password manager. |
| `wiki_enable` | `false` | Deploy Wiki.js. |
| `wastebin_enable` | `false` | Deploy Pastebin. |
