# LOGGING_POLICY

**Status:** Draft
**Date:** February 13, 2026

This document defines the log retention and storage policies for the `deploy-system-unified` infrastructure.

## System Logs (Journald)

*   **Retention Period:** 30 Days (`MaxRetentionSec`)
*   **Rotation Frequency:** Daily (`MaxFileSec`)
*   **Storage Mechanism:** Persistent (`/var/log/journal`)
*   **Compression:** Enabled
*   **Sealing:** Enabled (Forward Secure Sealing)

## Application Logs (Logrotate)

*   **Target:** `/var/log/*.log` and `/var/log/*/*.log`
*   **Retention Period:** 30 Rotations
*   **Frequency:** Daily
*   **Compression:** Enabled (Delayed)

## Rate Limiting

*   **Burst:** 1000 messages
*   **Interval:** 30 seconds
*   **Action:** Drop messages exceeding limit (DoS protection)

## Compliance

*   All nodes MUST enforce `Storage=persistent`.
*   All nodes MUST enable FSS (Forward Secure Sealing).
