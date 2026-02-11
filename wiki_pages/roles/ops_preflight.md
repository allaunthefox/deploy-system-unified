# ops/preflight

**Role Path**: `roles/ops/preflight`

## Description
Preflight role - Validation and readiness checks ONLY

## Key Tasks
- Gather minimum facts for preflight checks
- Determine virtualization profile (preflight)
- Validate distribution is supported
- Validate systemd is available
- Check for minimum memory
- Check for required binaries
- Validate required binaries exist
- Check network connectivity
- Validate network connectivity
- Install KVM checker (Bare Metal only)
- Validate KVM Hardware Acceleration (Bare Metal only)
- Assert KVM is functional
- Set preflight completion facts
- Define default secret guards
- Run preflight diagnose (non-failing)
- Define deployment profile for transfer policy
- Validate deployment profile is supported
- Enforce NFS explicit-allow policy (least privilege)
- Enforce NFS export scope (no broad exports by default)
- Enforce NFS ephemeral opt-in (strict profiles)
- Enforce rsync explicit-allow policy (least privilege)
- Enforce rsync ephemeral opt-in (strict profiles)
- Validate required secrets are not default placeholders
- Scan inventory for placeholder test_key usage (controller)
- Fail if placeholder test_key is present in inventory

## Default Variables
- `preflight_require_systemd`
- `preflight_check_memory`
- `preflight_min_memory_mb`
- `preflight_check_network`
- `preflight_connectivity_check_url`
- `preflight_required_binaries`

---
*This page was automatically generated from role source code.*