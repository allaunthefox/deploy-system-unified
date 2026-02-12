# Recovery Objectives (RPO & RTO)

**Status:** Draft
**Date:** February 13, 2026

This document defines the recovery targets for the `deploy-system-unified` infrastructure.

## Definitions

*   **RPO (Recovery Point Objective):** The maximum acceptable amount of data loss measured in time.
*   **RTO (Recovery Time Objective):** The maximum acceptable time to restore service after a disaster.

## Objectives by Tier

### Tier 1: Core Critical Data
*   **Scope:** User data volumes (`/var/lib/docker/volumes`), Database dumps, Secrets.
*   **RPO:** 24 Hours (Daily Backups)
*   **RTO:** 4 Hours (Manual Restore)
*   **Strategy:** Restic snapshots to offsite storage.

### Tier 2: System Configuration
*   **Scope:** OS configuration, Package lists, User accounts.
*   **RPO:** N/A (Infrastructure as Code)
*   **RTO:** 2 Hours (Ansible Redeploy)
*   **Strategy:** Git repository is the source of truth.

### Tier 3: Logs & Ephemeral Data
*   **Scope:** `/var/log`, Temporary build artifacts.
*   **RPO:** Best Effort (No guarantee)
*   **RTO:** N/A
*   **Strategy:** Local retention only, no offsite backup.

## Backup Schedule

*   **Daily:** Full snapshot of Tier 1 data (Restic).
*   **Weekly:** Verification run (check integrity).
*   **Monthly:** Test restore of random subsets.
