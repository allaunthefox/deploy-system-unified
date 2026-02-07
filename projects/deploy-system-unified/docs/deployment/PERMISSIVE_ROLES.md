# Permissive Roles

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
1. Run the diagnostic playbook (non‑failing): `ansible-playbook playbooks/preflight_diagnose.yml` to get a JSON report (`ci-artifacts/preflight_diagnose_<host>.json`).
2. Fix placeholders and secret files, or set the per-role fail_secure flag to `false` if you accept risk:
   - Global override: `core_security_fail_secure: false`
   - Per-role alias: `containers_fail_secure: false` or service override `vaultwarden_fail_secure: false`
3. After remediation, enable hard enforcement by adding asserts and enforcement tasks guarded by `core_security_fail_secure`.

See docs/deployment/PERMISSIVE_ROLES.md in the repo for the canonical list and migration guidance.
