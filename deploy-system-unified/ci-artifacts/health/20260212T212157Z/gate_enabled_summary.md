# gate_enabled_summary

- **Run ID:** `20260212T212157Z`
- **Playbook Exit Code:** `2`
- **Inventory:** `localhost,`
- **Gate Setting:** `health_check_fail_on_mandatory=true`
- **JSON Artifact:** `ci-artifacts/health/20260212T212157Z/localhost.json`

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

Mandatory gate enforcement is functioning: playbook failed when required checks failed.
