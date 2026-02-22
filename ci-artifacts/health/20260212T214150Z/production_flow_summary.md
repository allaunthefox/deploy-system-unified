# production_flow_summary

- **Run ID:** `20260212T214150Z`
- **Playbook:** `production_deploy.yml`
- **Inventory:** `inventory/local.ini`
- **Mode:** Full entrypoint execution with role checkpoints pre-seeded to validate flow wiring and post-task health gate
- **Playbook Exit Code:** `2`
- **JSON Artifact:** `ci-artifacts/health/20260212T214150Z/localhost.json`

## Counts

- total: `9`
- passed: `4`
- failed: `5`
- warnings: `2`
- mandatory_failures: `3`

## Mandatory Failures

- `podman`
- `caddy`
- `caddy-http-local`

## Result

Health gate enforcement triggered in production entrypoint context.
