# Container Monitoring Role

This role utilizes Podman Quadlets to deploy a monitoring stack consisting of **Prometheus** and **Grafana**.

## Architecture

* **Prometheus**: Time-series database. Scrapes metrics from:
    * `node_exporter` (Host)
    * `cadvisor` (Containers - *Optional/Planned*)
* **Grafana**: Visualization dashboard.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `monitoring_enable` | `true` | Enable the stack. |
| `monitoring_pod_name` | `mon_pod` | Name of the pod. |
| `monitoring_prometheus_image` | `prom/prometheus:latest` | Prometheus Image. |
| `monitoring_grafana_image` | `grafana/grafana:latest` | Grafana Image. |
| `monitoring_grafana_admin_password` | `CHANGE_ME` | **Secure this via Vault!** |

## Network

The monitoring stack runs on the `deploy-net` network (or configured `monitoring_network`) to reach other containers.

## Persistence

Data is stored in `{{ monitoring_root_dir }}` (Default: `/srv/monitoring`).
