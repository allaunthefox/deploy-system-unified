# ops_session

**Role Path**: `roles/ops/session`

## Description
**Deployment Session**
Ensures deployments run within persistent sessions (Tmux) to prevent interruption.

## Key Tasks
- Ensure TMUX session is available for deployment (idempotent)
- Set TMUX session validity fact (idempotent)
- Validate TMUX session creation (idempotent)

## Default Variables
- `tmux_session_for_deployment`
- `tmux_session_name`

---
*This page was automatically generated from role source code.*