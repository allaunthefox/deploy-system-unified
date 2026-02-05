---
# Container Runtime Guide

This guide documents container runtime defaults and security-relevant settings.

## Podman Default Capabilities

The project sets a default capability set in `containers.conf` for GPU and container runtime compatibility. This is the canonical default used by the roles:

```yaml
default_capabilities = [
  "CAP_CHOWN",
  "CAP_DAC_OVERRIDE",
  "CAP_FSETID",
  "CAP_FOWNER",
  "CAP_MKNOD",
  "CAP_NET_RAW",
  "CAP_SETGID",
  "CAP_SETUID",
  "CAP_SETFCAP",
  "CAP_SETPCAP",
  "CAP_NET_BIND_SERVICE",
  "CAP_SYS_CHROOT",
  "CAP_KILL",
  "CAP_AUDIT_WRITE"
]
```

**Capability Definitions (Scope + Purpose)**:

- `CAP_CHOWN`: Allows changing file ownership (used when services need to set correct ownership inside mounts).
- `CAP_DAC_OVERRIDE`: Bypass discretionary access control checks for file read/write/execute (used for containerized services that must read protected paths).
- `CAP_FSETID`: Preserve setuid/setgid bits on file modifications (used when installing files that retain privilege bits).
- `CAP_FOWNER`: Override file ownership checks for operations like chmod (used by apps that manage their own file permissions).
- `CAP_MKNOD`: Create device nodes (used by apps that need to create or manage special files).
- `CAP_NET_RAW`: Use raw sockets (needed for tools like ping and some network diagnostics).
- `CAP_SETGID`: Change group IDs (used by services that drop privileges).
- `CAP_SETUID`: Change user IDs (used by services that drop privileges).
- `CAP_SETFCAP`: Set file capabilities on binaries (used when tools need to grant capability-based permissions).
- `CAP_SETPCAP`: Modify process capabilities (used by init scripts/tools that adjust capabilities).
- `CAP_NET_BIND_SERVICE`: Bind to privileged ports (<1024) (used for services like reverse proxies).
- `CAP_SYS_CHROOT`: Use `chroot` (used by legacy apps or sandbox setups).
- `CAP_KILL`: Send signals to processes owned by other users (used for coordinated service shutdown).
- `CAP_AUDIT_WRITE`: Write to the audit log (used by security/audit tooling).

**Important: `gpu` is not a Linux capability**:

The string `gpu` is **not** a valid Linux kernel capability and must **not** appear in `default_capabilities` or `Capabilities=` lists. Including it causes Podman/Quadlet validation errors. Keep `default_capabilities` restricted to `CAP_*` entries only.

### When GPU Access *Should* Be Enabled (Examples)

Use explicit device access and/or CDI to enable GPUs. Example Quadlet snippet:

```ini
[Container]
# NVIDIA
Device=/dev/nvidia0
Device=/dev/nvidiactl
Device=/dev/nvidia-uvm

# Intel/AMD
Device=/dev/dri/renderD128
Device=/dev/dri/card0
```

For runtime hints, prefer labels or variables (not `default_capabilities`):

```ini
[Container]
Label=requires=gpu
```

This keeps kernel capabilities clean while still declaring intent for GPU-enabled services.

If you need NVIDIA driver feature gating, use the vendor variable (not Linux capabilities):

```ini
[Container]
Environment=NVIDIA_DRIVER_CAPABILITIES=compute,video,utility
```

### GPU Enablement Recipe (Safe Default)

Use device access + mounts, and **do not** add non‑`CAP_*` values to capability lists.

```ini
[Container]
Device=/dev/nvidia0
Device=/dev/nvidiactl
Device=/dev/nvidia-uvm
Volume=/usr/bin/nvidia-smi:/usr/bin/nvidia-smi:ro
```

For Intel/AMD:

```ini
[Container]
Device=/dev/dri/card0
Device=/dev/dri/renderD128
Volume=/dev/dri:/dev/dri:rw
```

Optional (NVIDIA only):

```ini
[Container]
Environment=NVIDIA_DRIVER_CAPABILITIES=compute,video,utility
```
