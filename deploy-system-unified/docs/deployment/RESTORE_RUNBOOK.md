# Restore Runbook

**Status:** Draft
**Last Updated:** February 13, 2026

This runbook details the procedures for recovering the system from various failure scenarios.

## Scenarios

### 1. Configuration Loss (GitOps Recovery)
**Symptom:** Server configuraton is drifted or corrupted, but data is intact.
**Resolution:** Re-run Ansible.

```bash
# From Controller
ansible-playbook -i inventory/production.ini production_deploy.yml
```

### 2. Data Loss (Volume Restoration)
**Symptom:** Application data in `/var/lib/docker/volumes` is deleted or corrupted.
**Resolution:** Restore from Restic snapshot.

**Prerequisites:**
- Restic password (from Vault/SOPS).
- Repository access.

**Procedure:**
1. Stop services to unlock files:
   ```bash
   systemctl stop docker
   ```
2. List snapshots:
   ```bash
   restic -r /srv/backups/restic snapshots
   ```
3. Restore specific path:
   ```bash
   restic -r /srv/backups/restic restore latest --target / --include /var/lib/docker/volumes/my-volume
   ```
4. Restart services:
   ```bash
   systemctl start docker
   ```

### 3. Total System Loss (Bare Metal Recovery)
**Symptom:** Server hardware failure or OS corruption requiring wipe.
**Resolution:** Provision new host -> Apply Ansible -> Restore Data.

**Procedure:**
1. **Provision:** Install base OS (Debian/Ubuntu) on new hardware.
2. **Bootstrap:** Configure SSH access.
3. **Deploy Config:** Run Ansible `production_deploy.yml` (This installs Docker, Restic, etc.).
4. **Restore Data:**
   - Stop Docker: `systemctl stop docker`
   - Run Restore Script: `/usr/local/bin/restore_data.sh` (or manual restic restore)
   - Start Docker: `systemctl start docker`

## Verification
After restore, verify:
1. Docker containers are running (`docker ps`).
2. volume data exists (`ls -la /var/lib/docker/volumes`).
3. Application health checks pass.
