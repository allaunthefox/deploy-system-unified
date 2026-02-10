# OS Configuration Controls

The `os_settings.yml` file serves as the **Single Source of Truth (SSOT)** for fleet-wide operating system configurations.

**File Location:** `inventory/group_vars/all/os_settings.yml`

## Purpose

In a distributed microservice architecture, "where do we set the timezone?" or "what describes the base package list?" are common questions. This configuration file answers them by determining the baseline state for **every** managed node, regardless of its role (GPU Worker, Web Server, or Container Host).

### 1. System Identity

Controls the non-functional requirements of the server—how it identifies itself to the world and its administrators.

* **Timezone**: Ensures consistent logging timestamps across the fleet (Default: `UTC`).
* **Locale/Keyboard**: Ensures consistent character encoding and terminal behavior.

### 2. Administrative Access

Defines the "Break-Glass" and standard entry mechanisms.

* **Admin User**: The standard username created on all nodes.
* **Endlessh Integration**: If `system_enable_endlessh` is true, port 22 is trapped, and real SSH moves to 2222.
* **SSH Port**: The listening port for SSHD. (Dynamic based on Endlessh status).
* **Effective SSH Port**: `ssh_effective_port` is the single source of truth used by roles. When port randomization is enabled, the randomized port takes precedence.
* **Root Login**: Global security toggle to allow/deny direct root access.

## SSH Idempotence Guardrails

This project enforces a single effective SSH port and a single owner of `sshd_config` to prevent drift and duplicate directives.

- `ssh_effective_port` is the only port used by SSHD, firewall rules, Fail2Ban, and connection info. This removes conflicting settings between roles.
- If `ssh_randomize_port` is enabled, the randomized port **always** overrides `system_ssh_port`. This prevents toggling between ports across runs.
- Port 22 is only opened automatically when Endlessh is enabled, so the honeytrap cannot accidentally stay exposed.
- `roles/security/sshd` validates that `sshd_config` contains exactly one global `Port` directive and no duplicate global SSH directives, so misconfigurations fail fast.

See `docs/deployment/SSH_IDEMPOTENCE_GUARDRAILS.md` for the full rationale and operational guidance.

### 3. Base Software (Bootstrap)

Defines the "Minimum Viable Product" for a server.

* **Common Packages**: Installed on *all* distributions (e.g., `sudo`, `curl`).
* **Distro-Specifics**: Maps the common intents to specific package names (e.g., `apache2` vs `httpd` is handled in mappings, but here we define *what* we want).

### 4. Hardware & Kernel Profiles

Global overrides for the physical layer.

* **Kernel Profile**: Selects between `generic` (virtualization-safe) and `bare_metal` (hardware-optimized) tuning.
* **IOMMU/DMA**: Toggles low-level hardware isolation features.

## Example Configuration

```yaml
# inventory/group_vars/all/os_settings.yml

system_timezone: "America/New_York"
system_admin_user: "ops_team"
system_ssh_port: 2022
system_base_packages:
  common:
    - htop
    - tmux
    - git
```

## How Roles Use These Variables

* **`roles/core/bootstrap`**: Consumes `system_base_packages` to install software.
* **`roles/security/sshd`**: Consumes `ssh_effective_port` (via `system_ssh_port` and runtime overrides).
* **`roles/networking/firewall` / `roles/security/ips` / `roles/ops/connection_info`**: Use `ssh_effective_port` for consistency.

## Transfer Defaults (Least Privilege)

This project defaults to **explicit allow** for transfer protocols:

- **SSH transfer**: OpenSSH + `piped` transfer (no SFTP/SCP dependency).
- **NFS**: Disabled unless explicitly enabled in a profile.
- **Rsync**: SSH-based only, and disabled unless explicitly enabled.

Reference: `docs/deployment/SSH_TRANSFER_PROFILE.md`

### Example Profile Configuration (Explicit Allow)

```yaml
# Enable NFS explicitly (example)
storage_nfs_enable: true
storage_nfs_allow_broad_exports: false
storage_nfs_exports:
  - path: /srv/media/default
    clients:
      - "10.0.0.0/24(rw,sync,no_subtree_check)"
storage_nfs_mounts:
  - src: "10.0.0.10:/srv/media/default"
    path: /mnt/media
    opts: "rw,noatime"

# Enable SSH-based rsync explicitly (example)
ops_rsync_enable: true
ops_rsync_allowlist:
  - src: /srv/containers
    dest: "backup@10.0.0.20:/backups/containers"
    ssh_key: "/home/prod/.ssh/backup_key"
```

### Ephemeral Profiles (Extra Guard)

For `deployment_profile: "ephemeral"`, you must explicitly opt in:

```yaml
storage_nfs_ephemeral_allow: true
ops_rsync_ephemeral_allow: true
```
* **`roles/security/kernel`**: Consumes `kernel_profile` to decide whether to apply Sysctl hardening.
