# SSH Transfer Profile

## 1. Purpose

This profile defines how the deployment system handles file transfer over SSH when SFTP/SCP is restricted or unavailable on a target host.

The project default is to **defer to standard OpenSSH** with **pipelined transfers**, which aligns with the rest of the deployment model (SSH + systemd + Podman).

## 2. Default Behavior (Recommended)

- **Transport**: OpenSSH
- **Transfer Method**: `piped`
- **Rationale**:
  - Avoids hard dependency on `sftp-server` or `scp` on minimal hosts.
  - Keeps all traffic within the SSH channel.
  - Matches existing `pipelining = True` optimization in `ansible.cfg`.

## 3. Implementation (Controller)

Set in `ansible.cfg`:

```ini
[ssh_connection]
pipelining = True
transfer_method = piped
```

## 4. Troubleshooting

If a host explicitly **requires SFTP/SCP**, override by setting:

```ini
[ssh_connection]
transfer_method = sftp
```

or per-host in inventory using:

```ini
[host_group]
host ansible_ssh_common_args="-o PreferredAuthentications=publickey"
```

(Use only if the host mandates a specific SSH policy.)

## 5. Related Defaults

### NFS

Default: **explicit allow only** (disabled unless enabled).  
The project expects explicit enablement plus explicit export/mount configuration to avoid accidental exposure. This enforces least‑privilege by requiring opt‑in at the profile level.

Recommendation:
- Enable only in profiles that explicitly require shared storage.
- Prefer read-only mounts where possible.
- Declare explicit allow variables and allowed endpoints/paths in the profile.
- Broad exports (e.g., `0.0.0.0/0`, `::/0`, `*`) are blocked unless explicitly allowed.

### Rsync

Default: **explicit allow only** with **SSH-based rsync** (no rsync daemon).  
Rationale: keeps all transfers within the existing SSH trust model and avoids opening additional services; requires explicit enablement to prevent accidental data exfil paths.

Recommendation:
- Use `rsync` over SSH with key-based auth.
- Avoid `rsyncd` unless a dedicated, locked-down transfer node is required.
- Keep an explicit allowlist of endpoints/paths in the profile (least privilege).

## 6. Example Profile Configuration

Use these variables in a profile or inventory group to explicitly allow NFS and/or rsync.

```yaml
# Explicit allow: NFS (example)
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

# Explicit allow: Rsync over SSH (example)
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

## 7. Scope

This is a **controller-side** profile. No changes are required on managed hosts.
