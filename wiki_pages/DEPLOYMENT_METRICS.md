# Deployment Metrics & Monitoring Guide

This guide covers metrics collection and monitoring for Deploy-System-Unified deployments.

## Overview

The system supports multiple levels of metrics collection:
- Deployment success/failure tracking
- Performance metrics
- System health indicators
- Container runtime metrics

## Deployment Metrics

### Success Rate Tracking

Track deployment success rates using the deployment summary:

```yaml
# After deployment, check the result
- name: Record deployment status
  ansible.builtin.set_fact:
    deployment_success: "{{ ansible_playbook_results.results | map(attribute='changed') | list }}"
```

### Key Metrics

| Metric | Description | Collection Method |
|--------|-------------|------------------|
| Deployment Time | Total time for playbook runs | Ansible timer |
| Task Changes | Number of changed tasks | Ansible callback |
| Failures | Failed tasks count | Ansible result |
| Idempotency | Repeat run changes | verify_idempotence.sh |

## Container Metrics

### Podman Stats

```bash
# Collect container resource usage
podman stats --no-stream --format json

# Monitor specific container
podman stats --name jellyfin --no-stream
```

### Key Metrics

- CPU usage percentage
- Memory usage (RSS, cache)
- Network I/O
- Block I/O

## Kubernetes Metrics

### kubectl top

```bash
# Pod resource usage
kubectl top pods

# Node resource usage
kubectl top nodes
```

### Metrics Collection

```bash
# Export to Prometheus format
kubectl top pods --no-headers | awk '{print "pod_"$1"_cpu"$2" " $3}'
```

## Health Checks

### System Health

```bash
# Check systemd services
systemctl list-units --failed

# Check containers
podman ps --format json | jq '.[].State'

# Check mounts
df -h | grep -E '/dev|/mnt'
```

### Custom Health Script

```yaml
# playbooks/health_check.yml
- name: Check all services
  hosts: all
  tasks:
    - name: Verify podman socket
      ansible.builtin.systemd:
        name: podman.socket
        state: started

    - name: Check container health
      ansible.builtin.command: podman ps --format json
      register: containers

    - name: Report status
      ansible.builtin.debug:
        msg: "Running containers: {{ containers.stdout }}"
```

## Integration with Monitoring Stack

### Prometheus Integration

Add metrics endpoint to Prometheus:

```yaml
# prometheus.yml
- job_name: 'deploy-system'
  static_configs:
    - targets: ['localhost:9100']
```

### Grafana Dashboards

Import the deployment dashboard for visualization.

## Alerting

### Success Rate Alerts

```yaml
# alerts.yml
- alert: DeploymentFailure
  expr: ansible_playbook_failures > 0
  for: 5m
  labels:
    severity: critical
```

## Logging

### Centralized Logging

```bash
# Ship logs to central location
journalctl -u podman -f | logshipper &
```

## Metrics Collection Scripts

### Example: Daily Metrics

```bash
#!/bin/bash
# scripts/metrics/daily.sh

DATE=$(date +%Y%m%d)
METRICS_DIR="/var/lib/deploy-system/metrics"

# Deployment success
echo "$(date): Checking deployments" >> $METRICS_DIR/deployment_$DATE.log

# Container stats
podman stats --no-stream --format json > $METRICS_DIR/containers_$DATE.json

# System load
uptime > $METRICS_DIR/load_$DATE.log
```

Add to crontab:
```bash
0 * * * * /home/prod/scripts/metrics/daily.sh
```

## Related Documentation

- [Monitoring Stack](docs/deployment/MONITORING.md)
- [Grafana Dashboards](docs/deployment/GRAFANA.md)
- [Alert Manager](docs/deployment/ALERTING.md)
