# core_logging

**Role Path**: `roles/core/logging`

## Description
**Forensic Logging Readiness**
Ensures mandatory forensic readiness by configuring systemd-journal-remote and log aggregation tools.

## Key Tasks
- Install systemd-journal-remote for log aggregation readiness
- Ensure journald directory exists for persistence
- Configure journald for forensic integrity and rate limiting
- Ensure rsyslog is installed (Alpine)
- Ensure rsyslog configuration directory exists (Generic)
- Configure rsyslog for centralized log shipping (Generic)
- Ensure rsyslog is running and enabled (Generic)
- Determine log reload command
- Create logrotate configuration for application logs
- Validate journald configuration
- Warn about journald verification issues

## Default Variables
- `logging_journal_remote_packages`

---
*This page was automatically generated from role source code.*