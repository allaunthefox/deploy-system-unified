# containers/ops

**Role Path**: `roles/containers/ops`

## Description
**Ops Container Role**

This role deploys operational dashboard and utility tools alongside the media stack.

## Key Tasks
- Run ops secret verifications
- Pull Ops Images
- Validate Vaultwarden admin token is set
- Create Ops Network Quadlet
- Create Ops Directories
- Create Ops Pod Quadlet
- Set Ops proxy hosts
- Deploy Ops Caddy Configuration
- Create Homarr Container Quadlet
- Create Vaultwarden Secrets File
- Create Vaultwarden Container Quadlet
- Create Wiki.js Container Quadlet
- Create Wastebin Container Quadlet
- Create Filebrowser Container Quadlet

## Default Variables
- `containers_ops_enable`
- `containers_ops_pod_name`
- `containers_ops_pod_network`
- `containers_ops_root_dir`
- `containers_ops_config_dir`
- `ops_enable`
- `ops_pod_name`
- `ops_pod_network`
- `ops_root_dir`
- `ops_config_dir`
- `containers_homarr_enable`
- `containers_homarr_image`
- `containers_homarr_port`
- `homarr_enable`
- `homarr_image`
- `homarr_port`
- `containers_vaultwarden_enable`
- `containers_vaultwarden_image`
- `containers_vaultwarden_port`
- `containers_vaultwarden_signups_allowed`
- `containers_vaultwarden_admin_token`
- `containers_vaultwarden_fail_secure`
- `vaultwarden_fail_secure`
- `vaultwarden_enable`
- `vaultwarden_image`
- `vaultwarden_port`
- `vaultwarden_signups_allowed`
- `vaultwarden_admin_token`
- `containers_wiki_enable`
- `containers_wiki_image`
- `containers_wiki_port`
- `containers_wiki_db_secret`
- `wiki_enable`
- `wiki_image`
- `wiki_port`
- `wiki_db_secret`
- `containers_wastebin_enable`
- `containers_wastebin_image`
- `containers_wastebin_port`
- `wastebin_enable`
- `wastebin_image`
- `wastebin_port`
- `containers_ops_domain`
- `ops_domain`
- `containers_filebrowser_enable`
- `containers_filebrowser_image`
- `containers_filebrowser_port`
- `filebrowser_enable`
- `filebrowser_image`
- `filebrowser_port`

---
*This page was automatically generated from role source code.*