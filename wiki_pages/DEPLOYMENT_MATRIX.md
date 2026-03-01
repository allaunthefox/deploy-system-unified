# Deployment Combinations Matrix
# =============================================================================
# Audit Event Identifier: DSU-GUI-240001
# Document Type: Deployment Guide
# Last Updated: 2026-02-28
# Version: 1.0
# Profiles: A (MINIMAL), B (STANDARD), C (PRODUCTION), D (MONITORING), E (MEDIA), F (SECURITY)
# =============================================================================

## Stack Overview

| ID | Stack | Namespace/Type | Components | Priority | Dependencies |
|----|-------|----------------|------------|----------|--------------|
| S01 | monitoring-stack | monitoring | Prometheus, Grafana, Alertmanager | P0 | None |
| S02 | media-stack | media | Jellyfin, Radarr, Sonarr | P1 | None |
| S03 | logging-stack | logging | Loki, Promtail | P0 | None |
| S04 | database-stack | database | PostgreSQL, Redis | P0 | None |
| S05 | auth-stack | auth | Authentik | P1 | database-stack |
| S06 | backup-stack | backup | Restic, Rclone | P2 | None |
| S07 | network-stack | network | Pi-hole, WireGuard | P1 | None |
| S08 | proxy-stack | proxy | Caddy | P0 | None |
| S09 | ops-stack | ops | Homarr, Vaultwarden | P2 | auth-stack (optional) |
| S10 | security-stack | security | CrowdSec, Trivy | P1 | logging-stack (optional) |
| **S11** | **anubis** | **container (Podman)** | **Anubis AI Firewall** | **P0** | **proxy-stack (Caddy)** |

---

## Deployment Profiles

### Profile A: Minimal (Development/Testing)

**Purpose:** Quick local testing, minimal resources

| Stack | Enabled | Persistence | Resources | Notes |
|-------|---------|-------------|-----------|-------|
| monitoring-stack | ✅ | ❌ emptyDir | Minimal | For basic monitoring |
| media-stack | ✅ | ❌ emptyDir | Minimal | No GPU |
| logging-stack | ❌ | - | - | Optional |
| database-stack | ❌ | - | - | Optional |
| auth-stack | ❌ | - | - | Not needed |
| backup-stack | ❌ | - | - | Not needed |
| network-stack | ❌ | - | - | Optional |
| proxy-stack | ❌ | - | - | Use port-forward |
| ops-stack | ❌ | - | - | Optional |
| security-stack | ❌ | - | - | Optional |
| **anubis** | **❌** | **-** | **-** | **Not needed for testing** |

**Resource Requirements:**
- CPU: 2 cores
- Memory: 4Gi
- Storage: 10Gi

**Deployment Command:**
```bash
ansible-playbook deploy_all_stacks.yml -i inventory/local_test.ini \
  -e persistence_enabled=false \
  -e logging_stack_enabled=false \
  -e database_stack_enabled=false \
  -e auth_stack_enabled=false
```

---

### Profile B: Standard (Development with Services)

**Purpose:** Full development environment with all core services

| Stack | Enabled | Persistence | Resources | Notes |
|-------|---------|-------------|-----------|-------|
| monitoring-stack | ✅ | ❌ emptyDir | Standard | Full monitoring |
| media-stack | ✅ | ❌ emptyDir | Standard | No GPU |
| logging-stack | ✅ | ❌ emptyDir | Standard | Full logging |
| database-stack | ✅ | ❌ emptyDir | Standard | For apps |
| auth-stack | ✅ | ❌ emptyDir | Standard | SSO for dev |
| backup-stack | ❌ | - | - | Optional |
| network-stack | ✅ | ❌ emptyDir | Minimal | Pi-hole only |
| proxy-stack | ✅ | ❌ emptyDir | Minimal | Local ingress |
| ops-stack | ✅ | ❌ emptyDir | Minimal | Homarr dashboard |
| security-stack | ❌ | - | - | Optional |

**Resource Requirements:**
- CPU: 4 cores
- Memory: 8Gi
- Storage: 20Gi

**Deployment Command:**
```bash
ansible-playbook deploy_all_stacks.yml -i inventory/local_test.ini \
  -e persistence_enabled=false \
  -e backup_stack_enabled=false \
  -e security_stack_enabled=false
```

---

### Profile C: Production (Full Stack)

**Purpose:** Complete production deployment

| Stack | Enabled | Persistence | Resources | Notes |
|-------|---------|-------------|-----------|-------|
| monitoring-stack | ✅ | ✅ 50Gi | Production | Full observability |
| media-stack | ✅ | ✅ 500Gi | Production | GPU optional |
| logging-stack | ✅ | ✅ 100Gi | Production | 30-day retention |
| database-stack | ✅ | ✅ 20Gi | Production | HA recommended |
| auth-stack | ✅ | ✅ 10Gi | Production | SSO for all |
| backup-stack | ✅ | ✅ 100Gi | Production | Daily backups |
| network-stack | ✅ | ✅ 5Gi | Production | Pi-hole + WireGuard |
| proxy-stack | ✅ | ✅ 5Gi | Production | TLS enabled |
| ops-stack | ✅ | ✅ 10Gi | Production | Full ops suite |
| security-stack | ✅ | ✅ 20Gi | Production | Full security |
| **anubis** | **✅** | **N/A** | **Minimal** | **AI Firewall (port 8080)** |

**Resource Requirements:**
- CPU: 16+ cores
- Memory: 64Gi+
- Storage: 800Gi+

**Deployment Command:**
```bash
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini \
  -e persistence_enabled=true \
  -e media_gpu_enabled=true
```

---

### Profile D: Monitoring & Logging Only

**Purpose:** Observability stack for existing applications

| Stack | Enabled | Persistence | Resources | Notes |
|-------|---------|-------------|-----------|-------|
| monitoring-stack | ✅ | ✅ 50Gi | Production | Full monitoring |
| media-stack | ❌ | - | - | Not needed |
| logging-stack | ✅ | ✅ 100Gi | Production | Full logging |
| database-stack | ❌ | - | - | Not needed |
| auth-stack | ❌ | - | - | Not needed |
| backup-stack | ✅ | ✅ 50Gi | Standard | Backup configs |
| network-stack | ❌ | - | - | Not needed |
| proxy-stack | ✅ | ❌ emptyDir | Minimal | Ingress only |
| ops-stack | ❌ | - | - | Not needed |
| security-stack | ✅ | ❌ emptyDir | Minimal | Trivy only |

**Resource Requirements:**
- CPU: 4 cores
- Memory: 16Gi
- Storage: 200Gi

**Deployment Command:**
```bash
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini \
  -e media_stack_enabled=false \
  -e database_stack_enabled=false \
  -e auth_stack_enabled=false \
  -e network_stack_enabled=false \
  -e ops_stack_enabled=false
```

---

### Profile E: Media Server Only

**Purpose:** Dedicated media streaming server

| Stack | Enabled | Persistence | Resources | Notes |
|-------|---------|-------------|-----------|-------|
| monitoring-stack | ✅ | ❌ 10Gi | Minimal | Basic monitoring |
| media-stack | ✅ | ✅ 1Ti | Production | GPU enabled |
| logging-stack | ❌ | - | - | Not needed |
| database-stack | ❌ | - | - | Not needed |
| auth-stack | ❌ | - | - | Not needed |
| backup-stack | ✅ | ✅ 100Gi | Standard | Media backups |
| network-stack | ✅ | ❌ emptyDir | Minimal | Pi-hole optional |
| proxy-stack | ✅ | ❌ emptyDir | Minimal | Ingress only |
| ops-stack | ❌ | - | - | Not needed |
| security-stack | ❌ | - | - | Not needed |

**Resource Requirements:**
- CPU: 8+ cores (with GPU)
- Memory: 16Gi
- Storage: 1Ti+

**Deployment Command:**
```bash
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini \
  -e logging_stack_enabled=false \
  -e database_stack_enabled=false \
  -e auth_stack_enabled=false \
  -e ops_stack_enabled=false \
  -e security_stack_enabled=false \
  -e media_gpu_enabled=true
```

---

### Profile F: Security & Compliance

**Purpose:** Security monitoring and compliance stack

| Stack | Enabled | Persistence | Resources | Notes |
|-------|---------|-------------|-----------|-------|
| monitoring-stack | ✅ | ✅ 50Gi | Production | Full monitoring |
| media-stack | ❌ | - | - | Not needed |
| logging-stack | ✅ | ✅ 200Gi | Production | Extended retention |
| database-stack | ✅ | ✅ 20Gi | Production | For security tools |
| auth-stack | ✅ | ✅ 10Gi | Production | SSO + audit |
| backup-stack | ✅ | ✅ 100Gi | Production | Compliance backups |
| network-stack | ✅ | ❌ emptyDir | Minimal | Pi-hole only |
| proxy-stack | ✅ | ❌ emptyDir | Minimal | TLS required |
| ops-stack | ❌ | - | - | Not needed |
| security-stack | ✅ | ✅ 50Gi | Production | Full security |
| **anubis** | **✅** | **N/A** | **Minimal** | **AI Firewall for web apps** |

**Resource Requirements:**
- CPU: 8 cores
- Memory: 32Gi
- Storage: 430Gi

**Deployment Command:**
```bash
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini \
  -e media_stack_enabled=false \
  -e ops_stack_enabled=false \
  -e logging_retention_days=90
```

---

## Configuration Matrix

### Persistence Options

| Option | Storage Class | Use Case | Pros | Cons |
|--------|--------------|----------|------|------|
| emptyDir | - | Testing | Fast, no setup | Data lost on restart |
| local-path | local-path | Dev/Local | Simple, no external deps | Node-bound |
| nfs-client | nfs-client | Production | Shared, persistent | Requires NFS server |
| ceph-rbd | ceph-rbd | Production HA | HA, shared | Complex setup |
| cloud-provider | gp3/standard | Cloud | Managed, HA | Vendor lock-in |

---

### Resource Tiers

| Tier | CPU Request | CPU Limit | Memory Request | Memory Limit | Use Case |
|------|-------------|-----------|----------------|--------------|----------|
| Minimal | 50m | 100m | 128Mi | 256Mi | Testing, dev |
| Standard | 250m | 500m | 512Mi | 1Gi | Development |
| Production | 500m | 2000m | 1Gi | 4Gi | Production |
| High-Perf | 1000m | 4000m | 2Gi | 8Gi | Media, databases |

---

### Security Profiles

| Profile | runAsNonRoot | readOnlyRootFilesystem | capabilities | seccomp | Use Case |
|---------|--------------|----------------------|--------------|---------|----------|
| Baseline | false | false | none | none | Legacy apps |
| Restricted | true | false | drop: ALL | RuntimeDefault | Most apps |
| Hardened | true | true | drop: ALL | RuntimeDefault | Security-critical |

---

## Deployment Scenarios

### Scenario 1: Single Node (Home Lab)

```yaml
# inventory/group_vars/home_lab.yml
kubernetes_flannel_backend: host-gw
persistence_enabled: false
media_gpu_enabled: true
monitoring_persistence_enabled: true
logging_persistence_enabled: false
```

**Stacks:** monitoring, media, logging (optional), network (Pi-hole)

---

### Scenario 2: Multi-Node Cluster (SMB)

```yaml
# inventory/group_vars/smb.yml
kubernetes_flannel_backend: wireguard
persistence_enabled: true
storage_class: nfs-client
ha_enabled: true
replica_count: 3
```

**Stacks:** All stacks enabled

---

### Scenario 3: Cloud-Native (EKS/GKE/AKS)

```yaml
# inventory/group_vars/cloud.yml
kubernetes_flannel_backend: vxlan
persistence_enabled: true
storage_class: gp3  # or premium-rbd/managed-premium
ingress_controller: nginx
tls_cert_manager_enabled: true
```

**Stacks:** All stacks with cloud integrations

---

### Scenario 4: Air-Gapped (Offline)

```yaml
# inventory/group_vars/airgap.yml
kubernetes_flannel_backend: host-gw
persistence_enabled: true
storage_class: local-path
offline_mode: true
airgap_registry: registry.local:5000
```

**Stacks:** Core stacks only (monitoring, logging, database)

---

## Compatibility Matrix

### Stack Dependencies

| Stack | Requires | Optional | Conflicts |
|-------|----------|----------|-----------|
| monitoring-stack | - | logging-stack | - |
| media-stack | - | backup-stack | - |
| logging-stack | - | - | - |
| database-stack | - | - | - |
| auth-stack | database-stack | - | - |
| backup-stack | - | monitoring-stack | - |
| network-stack | - | - | - |
| proxy-stack | - | - | - |
| ops-stack | - | auth-stack | - |
| security-stack | - | logging-stack | - |

---

### Version Compatibility

| Component | Min Version | Max Version | Tested Version |
|-----------|-------------|-------------|----------------|
| K3s | v1.28.0 | v1.32.x | v1.31.4+k3s1 |
| Helm | v3.15.0 | v4.x | v3.16.4 |
| Ansible | v2.16.0 | v2.20.x | v2.20.2 |
| Python | v3.8.0 | v3.14.x | v3.14.3 |

---

## Quick Reference

### Deployment Commands

```bash
# Minimal (testing)
ansible-playbook deploy_all_stacks.yml -i inventory/local_test.ini \
  -e persistence_enabled=false

# Standard (development)
ansible-playbook deploy_all_stacks.yml -i inventory/local_test.ini

# Production (full stack)
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini \
  -e persistence_enabled=true

# Individual stack
helm install monitoring charts/monitoring-stack -n monitoring \
  -f charts/monitoring-stack/values.production.yaml
```

### Validation Commands

```bash
# Validate chart security
./scripts/validate-chart-security.sh charts/monitoring-stack

# Check all pods
kubectl get pods -A --field-selector=status.phase!=Running

# Check resource usage
kubectl top nodes
kubectl top pods -A
```

---

## Decision Tree

```
Start
  │
  ├─ Need media streaming?
  │   ├─ Yes → Enable media-stack (+GPU?)
  │   └─ No → Skip
  │
  ├─ Need observability?
  │   ├─ Yes → Enable monitoring-stack + logging-stack
  │   └─ No → Skip
  │
  ├─ Need SSO?
  │   ├─ Yes → Enable auth-stack + database-stack
  │   └─ No → Skip
  │
  ├─ Production deployment?
  │   ├─ Yes → Enable persistence + backup-stack + security-stack
  │   └─ No → Use emptyDir
  │
  └─ Need network services?
      ├─ Yes → Enable network-stack + proxy-stack
      └─ No → Skip
```

---

## Support Matrix

| Profile | Support Level | SLA | Contact |
|---------|--------------|-----|---------|
| Minimal | Community | Best effort | GitHub Issues |
| Standard | Community | Best effort | GitHub Issues |
| Production | Enterprise | 99.9% | support@example.com |
| Custom | Enterprise | 99.99% | support@example.com |

---

## Document Control

- **Version:** 1.0
- **Last Updated:** 2026-02-28
- **Maintained By:** Infrastructure Team
- **Review Frequency:** Monthly
