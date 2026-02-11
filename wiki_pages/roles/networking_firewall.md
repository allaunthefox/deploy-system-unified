# networking/firewall

**Role Path**: `roles/networking/firewall`

## Description
**Multi-Distro Firewall**
Unified interface for managing rules via UFW (Debian/Arch) or Firewalld (RHEL/Fedora).

## Key Tasks
- Install UFW (Debian/Ubuntu/Arch)
- Install Firewalld (RedHat/CentOS)
- Build effective firewall TCP port list
- Set UFW Default Forward Policy
- Import UFW Rules
- Configure UFW defaults
- Import Firewalld Rules
- Enable UFW Final State
- Fail on unsupported OS Family

## Default Variables
- `firewall_enabled`
- `firewall_allowed_tcp_ports`
- `firewall_allow_endlessh`
- `firewall_endlessh_port`
- `firewall_allowed_udp_ports`
- `firewall_additional_rules`
- `firewall_forward_policy`

---
*This page was automatically generated from role source code.*