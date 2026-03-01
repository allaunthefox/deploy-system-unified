# Monitoring Role

**Audit Event Identifier:** DSU-PLY-100107  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role deploys a comprehensive observability stack, including Prometheus for metrics, Grafana for visualization, and Loki for forensic log aggregation.

## Architecture

```mermaid
graph TD
    subgraph Data Sources
        NODE[Node Exporter] --> PROM(Prometheus)
        CAD[cAdvisor] --> PROM
        LOKI_plugin[Docker/Podman] --> LOKI(Loki)
        LOGS[System Logs] --> PROMTAIL[Promtail]
    end
    
    subgraph Aggregation
        PROMTAIL --> LOKI
        PROM --> GRAF[Grafana]
        LOKI --> GRAF
    end
    
    subgraph Visualization
        GRAF --> DASH[Forensic Dashboard]
        GRAF --> ALERT[Alert Manager]
    end
    
    classDef source fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef agg fill:#fff3e0,stroke:#ff6f00,stroke-width:2px;
    classDef viz fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    
    class NODE,CAD,LOKI_plugin,LOGS,PROMTAIL source;
    class PROM,LOKI,GRAF agg;
    class DASH,ALERT viz;
```

## Features
- **Prometheus**: Time-series database for metrics.
- **Grafana**: Operational and forensic dashboards.
- **Loki**: Log aggregation system (like Prometheus, but for logs).
- **Forensic Ready**: Pre-configured dashboards for audit event tracking.
- **Gatus**: Automated health checking and status page.

## Usage

```yaml
- name: Deploy Monitoring Stack
  hosts: container_nodes
  roles:
    - containers/monitoring
```
