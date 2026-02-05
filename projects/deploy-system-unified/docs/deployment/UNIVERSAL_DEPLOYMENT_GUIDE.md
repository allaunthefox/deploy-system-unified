# Universal Deployment Guide

This guide outlines the standard operating procedure (SOP) for deploying the **Deploy-System-Unified** stack to any new target system. It isolates the replicable steps required to bring a server from "Fresh OS" to "Production Ready".

## 1. Prerequisites

### Controller Machine (Where you run Ansible)

- **Ansible**: Core 2.14+
- **Python**: 3.10+
- **SSH Access**: Root or Sudo user access to the target.

### Target System

- **OS**: Arch Linux (rolling) is the primary target.
    - *Note: RHEL/Debian support is experimental.*
- **Network**: Public Internet access.
- **Root Partition**: At least 50GB (if using Media roles).
- **Users**: A root user with SSH key access.

## 2. Infrastructure Profile Selection

The system uses a "Template" architecture. Do not edit `site.yml` directly. Instead, select a **Branch Template** that matches your hardware/use-case.

**Available Templates (`branch_templates/`)**:

- `base_hardened.yml`: Minimal security baseline.
- `contabo_cloud_vps_30_ssd.yml`: Contabo VPS optimized (Media Stack).
- `bare_metal_hardened.yml`: Physical server defaults.
- `gpu_slicing_*.yml`: Specialized GPU profiles.

**Action**:
Copy the chosen template to the project root:

```bash
cp branch_templates/contabo_cloud_vps_30_ssd.yml my_deployment.yml
```

## 3. Configuration & Customization

Edit your local `my_deployment.yml` to define environment-specific variables.

### Key Variables to Override

| Variable | Description | Example |
|:---|:---|:---|
| `media_domain` | The base domain for Caddy proxying | `media.example.com` |
| `caddy_acme_email` | Email for Let's Encrypt | `admin@example.com` |
| `porkbun_api_key` | (If using DNS-01 challenge) | `pk1_...` |
| `media_instance_name` | Unique Identifier for this stack | `default`, `node2` |
| `crowdsec_enable` | Toggle security stack | `true` |

*Security Tip: Use `ansible-vault` for API keys in production.*

## 4. Deployment Execution

Run the playbook against your inventory.

```bash
# Validate Syntax
ansible-playbook my_deployment.yml --syntax-check

# Run Deployment
ansible-playbook -i inventory/hosts my_deployment.yml
```

## 5. Transfer & Least-Privilege Defaults

This project enforces **explicit allow** and **least‑privilege** defaults for transfer protocols.

**Default behavior**:
- **SSH transfer**: OpenSSH + `piped` transfer (no SFTP/SCP dependency).
- **NFS**: Disabled unless explicitly enabled in a profile.
- **Rsync**: SSH-based only, and **disabled unless explicitly enabled** in a profile.

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

**Expected Outcome**:

- System is hardened (SSH ports changed, Firewall active).
- Storage is formatted (Btrfs subvolumes created/mounted).
- Podman Quadlets are generated in `/etc/containers/systemd/`.
- Systemd services are active.

### Podman Default Capabilities

During container runtime configuration, the project sets a default capability set in `containers.conf` for GPU and container runtime compatibility. This is the canonical default used by the roles:

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

**Important**: `gpu` is **not** a Linux capability and must **not** appear in `default_capabilities` or `Capabilities=` lists. GPU access should be granted via device nodes and mounts (e.g., `/dev/nvidia*` or `/dev/dri/*`) and optional vendor-specific environment variables (e.g., `NVIDIA_DRIVER_CAPABILITIES`).
See the GPU Enablement Recipe in `docs/deployment/CONTAINER_RUNTIME.md` for safe defaults and examples.

## 6. Post-Deployment: The "Hybrid Security" Hook

**Critical Step**: The CrowdSec "Hybrid" architecture (Container Agent + Host Binary Bouncer) requires a one-time cryptographic handshake that cannot be fully automated inside the playbook due to circular dependencies between the API readiness and the Host Service.

**Action**:
Run the included setup script **on the target server**.

1. **SSH into Target**:

   ```bash
   ssh -p 2222 root@target-ip
   ```

2. **Execute Setup Script**:

   ```bash
   # Ensure you are root
   sudo python3 /path/to/repo/scripts/setup_crowdsec.py
   ```

**What this script does**:

1. Checks if CrowdSec Agent container is healthy.
2. Checks if Host Firewall Bouncer service is installed.
3. Generates an API Key inside the container (`cscli bouncers add`).
4. Injects the key into the host config `/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml`.
5. Restarts the Host Firewall Bouncer.

**Verification**:

```bash
sudo podman exec crowdsec cscli bouncers list
# Should show "firewall-bouncer-host" with Status: valid
```

## 7. Verification Checklist

To confirm the replication was successful, verify these core subsystems:

### A. Web Ingress (Caddy)

```bash
curl -I https://<your_domain>
# Expect: 200 OK or 401 Unauthorized (if auth enabled)
# Check Logs: tail -f /var/log/caddy/access.log
```

### B. Security (CrowdSec)

```bash
# Internal Metrics
sudo podman exec crowdsec cscli metrics
# Ensure 'crowdsecurity/caddy-logs' parser has hits.

# Firewall Rules (Host)
sudo ipset list
# Expect: Sets named 'crowdsec-blacklists' are populated.
```

### C. Media Services (If deployed)

Navigate to `https://jellyfin.<your_domain>` and ensure the setup wizard appears.

---

## 8. Troubleshooting

- **"Unable to find ipset"**: Run `pacman -S ipset` (Fixed in v2.1 roles, but check legacy deploys).
- **"Lines parsed: 0"**: Verify `acquis.yaml` in `/srv/containers/caddy/crowdsec/config/` has `type: caddy` label.
- **Service Failures**: Use `journalctl -xeu <service>` to debug systemd Quadlet issues.
