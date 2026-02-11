# ops/monitoring

**Role Path**: `roles/ops/monitoring`

## Description
Tasks for ops/monitoring

## Key Tasks
- Load platform-specific variables
- Install monitoring packages (Debian/Ubuntu)
- Install monitoring packages (RHEL/Rocky)
- Install monitoring packages (Arch Linux)
- Install monitoring packages (Alpine)
- Determine Node Exporter Service Name
- Enable and start Node Exporter
- Configure Smartd (Basic)
- Enable and start Smartd

## Default Variables
- `monitoring_enable_node_exporter`
- `monitoring_enable_smartmon`
- `monitoring_enable_nvme_cli`
- `monitoring_node_exporter_version`
- `monitoring_node_exporter_port`
- `monitoring_node_exporter_collectors`
- `monitoring_smartd_interval`

---
*This page was automatically generated from role source code.*