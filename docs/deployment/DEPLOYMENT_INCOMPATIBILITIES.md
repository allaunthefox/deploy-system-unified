# Deployment Incompatibility Matrix
# =============================================================================
# Combinations that should NOT be deployed due to conflicts, issues, or risks
# Last Updated: 2026-02-28
# =============================================================================

## Critical Incompatibilities (DO NOT DEPLOY)

### ❌ INC-001: Multiple Ingress Controllers

**Conflicting Stacks:** proxy-stack (Caddy) + External Ingress Controller

**Issue:** Running multiple ingress controllers on the same cluster without proper configuration causes:
- Port conflicts (80/443 already in use)
- Routing conflicts
- Certificate management issues
- Unpredictable traffic routing

**Symptoms:**
```
Error: listen tcp :80: bind: address already in use
Error: listen tcp :443: bind: address already in use
```

**Resolution:**
- Use ONLY ONE ingress controller per cluster
- If multiple needed, configure different ports or node selectors
- Use ingress class annotations to route traffic

**Valid Configuration:**
```yaml
# Choose ONE:
proxy-stack:
  enabled: true  # Caddy

# OR external (not in this project):
# - NGINX Ingress
# - Traefik
# - HAProxy
```

---

### ❌ INC-002: Duplicate DNS Servers

**Conflicting Stacks:** network-stack (Pi-hole) + CoreDNS on Same Port

**Issue:** Pi-hole configured to use hostNetwork with default DNS settings conflicts with CoreDNS:
- Port 53 conflicts
- DNS resolution loops
- Cluster DNS breaks

**Symptoms:**
```
Failed to list *v1.Pod: Get "https://172.17.0.1:443/api/v1/pods": dial tcp 172.17.0.1:443: connect: connection refused
```

**Resolution:**
```yaml
# Option 1: Don't use hostNetwork for Pi-hole
network-stack:
  pihole:
    hostNetwork: false  # Default
    service:
      type: LoadBalancer  # Expose via LB instead

# Option 2: Use different DNS port
network-stack:
  pihole:
    dnsPort: 5353  # Non-standard port
```

---

### ❌ INC-003: Multiple Database Instances on Same Node

**Conflicting Stacks:** database-stack + auth-stack (Authentik PostgreSQL) + ops-stack (Vaultwarden SQLite)

**Issue:** Running multiple database instances without resource isolation causes:
- I/O contention
- Memory pressure
- Performance degradation
- Potential data corruption

**Symptoms:**
```
WARNING: too many open files
ERROR: could not fork new process for connection: Resource temporarily unavailable
```

**Resolution:**
```yaml
# Option 1: Use external database for auth-stack
auth-stack:
  authentik:
    postgresql:
      enabled: false  # Use external
    externalPostgresql:
      host: database-stack-database-stack-postgresql.database.svc
      port: 5432

# Option 2: Use node affinity to separate databases
database-stack:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: workload-type
                operator: In
                values:
                  - database

auth-stack:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: workload-type
                operator: In
                values:
                  - auth
```

---

### ❌ INC-004: Insufficient Resources for Selected Profile

**Invalid Configuration:** Production profile on minimal hardware

**Issue:** Deploying production settings on minimal resources causes:
- OOMKilled pods
- Pending pods (unschedulable)
- Node instability
- Cluster crash

**Minimum Requirements by Profile:**

| Profile | MIN CPU | MIN Memory | MIN Storage | Result if Undersized |
|---------|---------|------------|-------------|---------------------|
| Minimal | 2 cores | 4Gi | 10Gi | Works |
| Standard | 4 cores | 8Gi | 20Gi | Works |
| Production | 16 cores | 64Gi | 800Gi | **CRASH if undersized** |
| Monitoring | 4 cores | 16Gi | 200Gi | Works |
| Media | 8 cores | 16Gi | 1Ti | Works |
| Security | 8 cores | 32Gi | 430Gi | Works |

**Validation:**
```bash
# Check node resources before deployment
kubectl top nodes
kubectl describe nodes | grep -A5 "Allocated resources"

# Validate before deploy
ansible-playbook playbooks/preflight_validate.yml -i inventory/production.ini
```

---

### ❌ INC-005: GPU Without Device Plugin

**Invalid Configuration:** media-stack with GPU enabled but no device plugin

**Issue:** Enabling GPU without device plugin causes:
- Pods stuck in Pending state
- Resource not found errors
- Wasted resources

**Symptoms:**
```
0/3 nodes are available: 3 Insufficient gpu.intel.com/i915
```

**Resolution:**
```yaml
# Option 1: Install GPU device plugin first
# Intel GPU:
kubectl apply -f https://github.com/intel/intel-device-plugins-for-kubernetes/releases/download/v0.27.0/deployment-schemas/intel-device-plugin-operator.yaml

# NVIDIA GPU:
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/main/deployments/static/nvidia-device-plugin.yml

# Option 2: Disable GPU
media-stack:
  hardware:
    gpu:
      enabled: false  # Default
```

---

## High-Risk Combinations (NOT RECOMMENDED)

### ⚠️ RISK-001: All Stacks on Single Node

**Configuration:** All 10 stacks on single-node cluster

**Issues:**
- Resource contention
- No high availability
- Single point of failure
- Performance degradation
- Storage bottlenecks

**Minimum for All Stacks:**
- 3 master nodes (HA)
- 3+ worker nodes
- External storage

**If You Must:**
```yaml
# Resource limits are CRITICAL
global:
  resourceLimits:
    enabled: true
    strict: true

# Disable non-essential stacks
ops-stack:
  enabled: false
security-stack:
  enabled: false
network-stack:
  wireguard:
    enabled: false
```

---

### ⚠️ RISK-002: emptyDir in Production

**Configuration:** Production profile with persistence_enabled=false

**Issues:**
- Data loss on pod restart
- No backup capability
- Configuration loss
- Database corruption risk

**Symptoms:**
- Lost user data after updates
- Reset configurations
- Database reinitialization required

**Resolution:**
```yaml
# NEVER use in production:
production:
  persistence_enabled: false  # ❌ WRONG

# ALWAYS use in production:
production:
  persistence_enabled: true  # ✅ CORRECT
  storage_class: nfs-client  # or ceph-rbd, gp3, etc.
```

---

### ⚠️ RISK-003: Default Passwords in Production

**Configuration:** Production deployment with default/empty passwords

**Issues:**
- Security vulnerability
- Unauthorized access
- Data breach risk
- Compliance violation

**Critical Passwords to Change:**
```yaml
# MUST be set via secrets in production:
grafana.adminPassword: ""  # ❌ Default
authentik.adminPassword: ""  # ❌ Default
postgresql.password: ""  # ❌ Default
redis.password: ""  # ❌ Default
pihole.password: ""  # ❌ Default
```

**Resolution:**
```bash
# Generate and set via secrets
export GRAFANA_PASSWORD=$(openssl rand -base64 32)
kubectl create secret generic grafana-secrets \
  -n monitoring \
  --from-literal=admin-password="$GRAFANA_PASSWORD"
```

---

### ⚠️ RISK-004: Monitoring Without Alerting

**Configuration:** monitoring-stack enabled but alertmanager disabled

**Issues:**
- No visibility into issues
- Silent failures
- delayed incident response
- SLA violations

**Resolution:**
```yaml
# ALWAYS enable alerting in production:
monitoring-stack:
  alertmanager:
    enabled: true  # ✅ Required
  alerting:
    enabled: true
    receivers:
      - name: default
        email_configs:
          - to: alerts@example.com
```

---

### ⚠️ RISK-005: Backup Without Testing

**Configuration:** backup-stack enabled but never tested

**Issues:**
- False sense of security
- Backup corruption undetected
- Recovery failure during incident
- Data loss despite "backups"

**Resolution:**
```yaml
# Configure backup testing:
backup-stack:
  testRestore:
    enabled: true
    schedule: "0 3 * * 0"  # Weekly test
  alertOnFailure: true
```

**Test Backup/Restore:**
```bash
# Manual test
kubectl create job --from=cronjob/backup-stack-restic test-backup -n backup
kubectl logs -n backup -l job-name=test-backup

# Verify backup exists
kubectl exec -n backup backup-stack-restic-xxxx -- restic snapshots
```

---

### ⚠️ RISK-006: Logging Without Retention Policy

**Configuration:** logging-stack with infinite retention

**Issues:**
- Storage exhaustion
- Performance degradation
- Increased costs
- Cluster instability

**Symptoms:**
```
PersistentVolumeClaim "loki-data-0" is pending
Node pressure: DiskPressure
```

**Resolution:**
```yaml
# ALWAYS set retention:
logging-stack:
  loki:
    retention:
      enabled: true
      period: "30d"  # Maximum retention
      maxSize: "100GB"  # Maximum size
  promtail:
    scrapeConfigs:
      - job_name: kubernetes-pods
        enabled: true
        # Drop high-volume logs
        relabelConfigs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            action: drop
            regex: "noisy-app"
```

---

### ⚠️ RISK-007: Auth Without Database HA

**Configuration:** auth-stack with single database instance

**Issues:**
- SSO single point of failure
- Authentication outage if DB fails
- User lockout
- Compliance violation

**Resolution:**
```yaml
# Use external HA database:
auth-stack:
  authentik:
    postgresql:
      enabled: false  # Disable bundled
    externalPostgresql:
      host: postgres-ha.database.svc
      port: 5432
      sslMode: require
  redis:
    enabled: false  # Disable bundled
    externalRedis:
      host: redis-ha.database.svc
      port: 6379
      passwordSecret:
        name: redis-secret
        key: password
```

---

## Moderate-Risk Combinations (USE WITH CAUTION)

### ⚡ CAUTION-001: Media Transcoding on Shared Node

**Configuration:** Jellyfin transcoding on node with other workloads

**Issues:**
- CPU spikes affect other pods
- Thermal throttling
- Unpredictable performance

**Mitigation:**
```yaml
media-stack:
  jellyfin:
    resources:
      requests:
        cpu: "2000m"  # Reserve cores
        memory: "4Gi"
      limits:
        cpu: "4000m"
        memory: "8Gi"
    nodeSelector:
      workload-type: media
    affinity:
      podAntiAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
                - key: app
                  operator: In
                  values:
                    - database
                    - monitoring
            topologyKey: kubernetes.io/hostname
```

---

### ⚡ CAUTION-002: High-Volume Logging with Limited Storage

**Configuration:** logging-stack with < 50Gi storage in production

**Issues:**
- Frequent log rotation
- Lost historical data
- Insufficient for debugging

**Minimum Storage:**
| Environment | Minimum Storage | Recommended |
|-------------|----------------|-------------|
| Development | 10Gi | 20Gi |
| Staging | 50Gi | 100Gi |
| Production | 100Gi | 200Gi+ |

---

### ⚡ CAUTION-003: Prometheus Without Downsampling

**Configuration:** Prometheus with high scrape rate and long retention

**Issues:**
- High cardinality
- Memory exhaustion
- Slow queries

**Resolution:**
```yaml
monitoring-stack:
  prometheus:
    scrapeInterval: "30s"  # Not 15s for large clusters
    retention:
      time: "15d"  # Not 30d+ without downsampling
    resources:
      limits:
        memory: "8Gi"  # Cap memory usage
```

---

## Validation Script

```bash
#!/bin/bash
# Validate deployment combination for known issues

set -euo pipefail

echo "=== Deployment Compatibility Check ==="
echo ""

# Check 1: Multiple ingress controllers
INGRESS_COUNT=$(kubectl get daemonsets,deployments -A -l app.kubernetes.io/component=ingress 2>/dev/null | wc -l || echo "0")
if [ "$INGRESS_COUNT" -gt 1 ]; then
    echo "❌ FAIL: Multiple ingress controllers detected"
    exit 1
fi
echo "✅ PASS: Single ingress controller"

# Check 2: GPU device plugin (if GPU enabled)
if grep -q "gpu.enabled: true" charts/*/values*.yaml 2>/dev/null; then
    GPU_PLUGIN=$(kubectl get daemonsets -n kube-system -l app=device-plugin 2>/dev/null | wc -l || echo "0")
    if [ "$GPU_PLUGIN" -eq 0 ]; then
        echo "⚠️  WARNING: GPU enabled but no device plugin found"
    else
        echo "✅ PASS: GPU device plugin present"
    fi
fi

# Check 3: Resource validation
TOTAL_CPU=$(kubectl top nodes 2>/dev/null | awk '{sum+=$2} END {print sum}' || echo "0")
TOTAL_MEM=$(kubectl top nodes 2>/dev/null | awk '{sum+=$4} END {print sum}' || echo "0")

if [ "$TOTAL_CPU" -lt 16000 ] && grep -q "production" inventory/*.ini 2>/dev/null; then
    echo "⚠️  WARNING: Production profile on < 16 cores"
fi

if [ "$TOTAL_MEM" -lt 64000 ] && grep -q "production" inventory/*.ini 2>/dev/null; then
    echo "⚠️  WARNING: Production profile on < 64Gi RAM"
fi

echo ""
echo "=== Validation Complete ==="
```

---

## Pre-Deployment Checklist

Before deploying any combination, verify:

```
☐ Resource Requirements Met
  ☐ CPU: Sufficient for selected profile
  ☐ Memory: Sufficient for selected profile
  ☐ Storage: Sufficient for selected profile

☐ Dependencies Satisfied
  ☐ Required stacks enabled
  ☐ Device plugins installed (if needed)
  ☐ Storage class available

☐ Security Configuration
  ☐ Passwords changed from defaults
  ☐ TLS certificates configured
  ☐ Network policies enabled

☐ Operational Readiness
  ☐ Backup strategy defined
  ☐ Alerting configured
  ☐ Runbook available
```

---

## Document Control

- **Version:** 1.0
- **Last Updated:** 2026-02-28
- **Maintained By:** Infrastructure Team
- **Review Frequency:** Monthly
- **Related:** DEPLOYMENT_MATRIX.md, PRODUCTION_RUNBOOK.md
