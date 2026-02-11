# containers/authentik

**Role Path**: `roles/containers/authentik`

## Description
**Identity Provider (Authentik)**
Deploys Authentik for identity management, featuring comprehensive secret validation and negative testing.

## Key Tasks
- Verify Authentik secrets when fail-secure is enabled
- Create Authentik Directories
- Create Authentik secrets file
- Create Authentik Postgres Quadlet
- Create Authentik Redis Quadlet
- Create Authentik Server Quadlet
- Create Authentik Worker Quadlet
- Deploy Caddy Authentik Configuration

## Default Variables
- `authentik_enable`
- `authentik_image`
- `authentik_redis_image`
- `authentik_postgres_image`
- `authentik_base_dir`
- `authentik_data_dir`
- `authentik_config_dir`
- `authentik_port_http`
- `authentik_port_https`
- `authentik_pg_user`
- `authentik_pg_db`
- `authentik_pg_pass`
- `authentik_secret_key`
- `containers_authentik_fail_secure`
- `authentik_email_host`
- `authentik_email_port`
- `authentik_email_username`
- `authentik_email_password`
- `authentik_email_from`
- `authentik_email_use_tls`
- `authentik_network_name`

---
*This page was automatically generated from role source code.*