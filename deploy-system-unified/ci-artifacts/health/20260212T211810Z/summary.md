# summary

Health Check Evidence (T3)

- **Run ID:** `20260212T211810Z`
- **Mode:** Local smoke execution (`localhost`, `health_check_fail_on_mandatory=false`)
- **Artifact:** `ci-artifacts/health/20260212T211810Z/localhost.json`
- **Schema:** `deploy-system-unified/health-check/v1`

## Result Snapshot

- Total checks: `9`
- Passed: `4`
- Failed: `5`
- Warnings: `2`
- Mandatory failures: `3`

## Mandatory Failures Observed

- `podman` (service not running)
- `caddy` (unit not present)
- `caddy-http-local` (endpoint unreachable)

## Notes

This evidence confirms JSON summary emission and mandatory-failure classification logic.
The run was executed on a non-production localhost context, so mandatory gate enforcement was disabled for artifact capture.
