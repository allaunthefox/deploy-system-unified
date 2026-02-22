# SSH_INCIDENT_POSTMORTEM

## Summary
This document describes an SSH connectivity incident that occurred during the deployment of the `deploy-system-unified` project.

## Incident Overview
- **Date**: February 5, 2026
- **Issue**: SSH daemon was misconfigured and not running on the expected port (2222)
- **Impact**: VS Code Remote SSH connections were failing with "Connection refused" errors
- **Affected Systems**: Contabo VPS with IP 38.242.222.130

## Root Causes

### 1. SSH Configuration Issues
- SSH daemon configuration file (`/etc/ssh/sshd_config`) contained duplicate entries
- Multiple conflicting `Port`, `LogLevel`, `X11Forwarding`, and other directives
- Ansible playbook modifications created configuration conflicts

### 2. Undefined Environment Variable
- The `PLATFORM` variable was undefined in shell environments
- Caused warnings during SSH connection establishment
- Affected VS Code Remote SSH extension functionality

### 3. Service Management Problems
- SSH service was not starting properly through systemd
- Manual SSH processes were running alongside systemd service
- Inconsistent service states led to connection failures

## Resolution Steps Taken

### 1. SSH Configuration Cleanup
- Backed up the original configuration file
- Created a clean, de-duplicated SSH configuration
- Ensured Port 2222 was properly configured
- Maintained all security hardening settings

### 2. Environment Variable Fix
- Added `PLATFORM` variable definition to user's `.bashrc`
- Added `PLATFORM` variable to system-wide `/etc/environment`
- Added `PLATFORM` variable to system-wide `/etc/profile` and `/etc/bash.bashrc`

### 3. SSH Host Configuration
- Updated `/home/prod/.ssh/config` with proper host entry for "GrowinBoi"
- Configured correct IP address (38.242.222.130)
- Set proper port (2222) and user (prod)
- Specified appropriate SSH key for authentication

### 4. Service Restart
- Started SSH daemon with cleaned configuration
- Verified SSH was listening on port 2222
- Enabled SSH service for automatic startup

## Prevention and Guardrails

See `docs/deployment/SSH_IDEMPOTENCE_GUARDRAILS.md` for the current guardrails, rationale, and operational guidance that prevent a repeat of this incident.

## Conclusion
This incident highlighted the importance of proper SSH configuration management and environment variable handling in automated deployment systems. By implementing the prevention measures outlined above, similar incidents can be avoided in the future.

The key lessons learned include:
- Always validate configuration files before applying changes
- Prevent duplicate entries in configuration files
- Ensure all required environment variables are defined
- Implement proper monitoring and validation for critical services
- Maintain clear documentation for troubleshooting procedures
