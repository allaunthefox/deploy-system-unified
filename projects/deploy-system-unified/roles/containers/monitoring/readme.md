# Container Monitoring Role

This role uses Podman Quadlets to deploy a monitoring stack consisting of Prometheus and Grafana.

## Architecture

- Prometheus: Time-series database and metrics scraper for `node_exporter` (host).
- Prometheus can optionally scrape `cadvisor` for container metrics (planned).
- Grafana: Visualization dashboard.

## Defaults (Key Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `monitoring_enable` | `true` | Enable the stack. |
| `monitoring_instance` | `default` | Instance name for multi-tenant separation. |
| `monitoring_root_dir` | `/srv/monitoring/{{ monitoring_instance }}` | Data directory for Prometheus and Grafana. |
| `monitoring_config_dir` | `/srv/containers/monitoring_config/{{ monitoring_instance }}` | Config directory (Prometheus config). |
| `monitoring_network` | `host` | Pod network for rootless mode. Rootful mode uses host networking. |
| `monitoring_pod_name` | `mon-pod-{{ monitoring_instance }}` | Name of the pod. |
| `monitoring_prometheus_image` | `docker.io/prom/prometheus:v3.9.1` | Prometheus image. |
| `monitoring_grafana_image` | `docker.io/grafana/grafana:12.3.2` | Grafana image. |
| `monitoring_grafana_admin_user` | `admin` | Grafana admin user. |
| `monitoring_grafana_admin_password` | `CHANGE_ME_IN_VAULT` | Secure this via Vault/SOPS. |

## Network

- Rootful mode always uses host networking.
- Rootless mode uses `monitoring_network`. If it is not `host`, ports `9090` (Prometheus) and `3000` (Grafana) are published to the host.
- Ensure your firewall allows the ports you expose, or front Grafana/Prometheus with a reverse proxy.

## Persistence

Data is stored in `{{ monitoring_root_dir }}`. Prometheus config lives in `{{ monitoring_config_dir }}/prometheus`.
