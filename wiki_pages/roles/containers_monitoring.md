# containers/monitoring

**Role Path**: `roles/containers/monitoring`

## Description
**Container Monitoring Role**

This role uses Podman Quadlets to deploy a monitoring stack consisting of Prometheus and Grafana.

## Key Tasks
- Check Monitoring Enable
- Verify monitoring secrets when fail-secure is enabled
- Validate Grafana admin password is set
- Enforce CHANGE_ME policy for monitoring stack
- Create Monitoring Network Quadlet
- Create Monitoring Directories
- Create Grafana secrets file
- Deploy Prometheus Config
- Deploy Monitoring Pod Quadlet
- Deploy Prometheus Container Quadlet
- Deploy Grafana Container Quadlet
- Remove legacy generated systemd units (rootless)
- Reload rootless systemd to pick up quadlets
- Start monitoring pod and services (quadlet units)

## Default Variables
- `monitoring_enable`
- `monitoring_instance`
- `monitoring_root_dir`
- `monitoring_config_dir`
- `monitoring_network`
- `monitoring_pod_name`
- `monitoring_prometheus_image`
- `monitoring_grafana_image`
- `monitoring_grafana_admin_user`
- `monitoring_grafana_admin_password`
- `containers_monitoring_fail_secure`

---
*This page was automatically generated from role source code.*