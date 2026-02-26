# Role: containers/monitoring

WI-CONT | Forensic Intelligence Stack (Prometheus, Grafana, Loki).

## Forensic Intelligence (ISO 27001 §12.4)
- **Loki**: Log aggregation for forensic audit trails.
- **Promtail**: Action-Code aware log collector.
- **Grafana**: Real-time Forensic Dashboard.
- **Audit Event Identifier**: 840040 (Loki Init)
- **Audit Event Identifier**: 840041 (Grafana Forensic Dashboard)

## Key Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `monitoring_loki_enable` | `true` | Enable Loki aggregation |
| `monitoring_forensic_dashboard_enabled` | `true` | Provision DSU Forensic Dashboard |

## Summary
Deploys a full observability suite with specialized forensic dashboards that filter by Audit Event Identifier for real-time compliance auditing.
