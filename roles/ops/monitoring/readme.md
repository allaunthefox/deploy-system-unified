# Monitoring Role (`ops/monitoring`)

## Description

This role deploys standard system monitoring agents and tools. It focuses on OS-level observability, providing metrics and health checks.

## Features

- **Node Exporter**: Prometheus exporter for hardware and OS metrics.
- **Smartmon**: S.M.A.R.T. disk monitoring daemon.
- **NVMe CLI**: Tools for NVMe device management and monitoring.

## Requirements

- Ansible 2.15+
- Supported OS: Ubuntu (Focal/Jammy), RHEL 9, Arch Linux.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `monitoring_enable_node_exporter` | `true` | Enable installation of Prometheus Node Exporter. |
| `monitoring_enable_smartmon` | `true` | Enable Smartd for disk health monitoring. |

## Usage

```yaml
- role: ops/monitoring
  vars:
    monitoring_enable_node_exporter: true
```
