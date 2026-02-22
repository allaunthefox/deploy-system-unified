# inventory_local_blocker

- **Date (UTC):** 2026-02-12
- **Attempted Inventory:** `inventory/local.ini`
- **Result:** playbook failed before `ops/health_check` task execution.

## Error

`Could not process 'inventory/group_vars/all/secrets.generated.yml': failed to combine variables, expected dicts but got a 'dict' and a '_AnsibleTaggedStr'.`

## Impact

This blocks direct production-playbook-context validation via `inventory/local.ini` until the inventory variable merge issue is resolved.
