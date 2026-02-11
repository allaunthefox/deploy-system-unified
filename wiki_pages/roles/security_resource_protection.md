# security_resource_protection

**Role Path**: `roles/security/resource_protection`

## Description
**DoS Mitigation**
Implements resource limits (tasks, memory, descriptors) to mitigate denial-of-service and resource exhaustion.

## Key Tasks
- Validate minimum resource requirements
- Configure system-wide ulimits for process isolation
- Enforce Systemd global resource limits

## Default Variables
- `resource_min_ram_mb`
- `resource_default_tasks_max`
- `resource_default_memory_max`

---
*This page was automatically generated from role source code.*