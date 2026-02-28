# PERMISSIVE_ROLES

This document lists roles that currently *assume permissive defaults* (placeholder secrets, host networking, or files written world-readable). Use these guidelines when hardening.

Why this matters
- Defaulting to permissive behaviour increases the risk of accidental exposure in untrusted environments.
- We provide diagnostics and per-role opt-outs so operators can remediate before enforcement.

Initial role list (audit and mitigation planned):
- `roles/containers/ops` — Vaultwarden, Homarr, Filebrowser, Wiki, etc.
- `roles/containers/media` — Jellyfin, qBittorrent, Radarr, Sonarr, etc.
- `roles/containers/monitoring` — Grafana default passwords, Prometheus.
- `roles/containers/caddy` — CrowdSec keys, proxy assumptions.
- `roles/containers/authentik` — Authentik secret key and DB password.
- `roles/storage/backup/restic` — `restic_password` placeholder default.

How to proceed
1. Run the diagnostic playbook (non‑failing): `ansible-playbook playbooks/PREFLIGHT_DIAGNOSE.YML` to get a JSON report (`ci-artifacts/preflight_diagnose_<host>.json`).
2. Fix placeholders and secret files, or set the per-role fail_secure flag to `false` if you accept risk:
   - Global override: `core_security_fail_secure: false`
   - Per-role alias: `containers_fail_secure: false` or service override `vaultwarden_fail_secure: false`
3. After remediation, enable hard enforcement by adding asserts and enforcement tasks guarded by `core_security_fail_secure`.
Per-service hardening examples
- `containers_vaultwarden_fail_secure` / `vaultwarden_fail_secure` (default: inherit from `containers_fail_secure`) — when true the role will assert the presence of `{{ containers_secrets_dir }}/vaultwarden.env` with mode `0600` and correct owner, and assert it does not contain placeholder values.

Next steps (recommended): add Molecule/integration tests for each service to validate both failing (placeholder) and passing (real secret) behaviour before broad enforcement. (Added initial Molecule positive tests for: `containers/ops` (Vaultwarden), `storage/backup/restic`, `containers/monitoring`, `containers/caddy`, `containers/authentik`, and `containers/media`.)
See docs/deployment/PERMISSIVE_ROLES.md in the repo for the canonical list and migration guidance.
