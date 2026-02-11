# ops/pre_connection

**Role Path**: `roles/ops/pre_connection`

## Description
Tasks for ops/pre_connection role

## Key Tasks
- Check for existing custom SSH port on target (idempotent)
- Compute SSH port range bounds (idempotent)
- Generate random SSH port if enabled (idempotent)
- Set final SSH port fact (idempotent)
- Set effective SSH port fact (idempotent)
- Warn when randomization overrides Endlessh port conventions
- Check connectivity to target SSH port
- Inform operator if SSH port is closed (Anticipating Knocking)

---
*This page was automatically generated from role source code.*