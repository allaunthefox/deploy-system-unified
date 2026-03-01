# Deployment Quick Reference Card
# =============================================================================
# Audit Event Identifier: DSU-GUI-240002
# Document Type: Quick Reference Guide
# Last Updated: 2026-02-28
# Version: 1.0
# Profiles: A-F | Stacks: 11 | Runtimes: Kubernetes, Podman
# =============================================================================

## Stack Quick Reference

| Stack | Namespace | Components | Production Ready |
|-------|-----------|------------|-----------------|
| 📊 monitoring | monitoring | Prometheus, Grafana, Alertmanager | ✅ |
| 🎬 media | media | Jellyfin, Radarr, Sonarr | ✅ |
| 📝 logging | logging | Loki, Promtail | ✅ |
| 🗄️ database | database | PostgreSQL, Redis | ✅ |
| 🔐 auth | auth | Authentik | ✅ |
| 💾 backup | backup | Restic, Rclone | ✅ |
| 🌐 network | network | Pi-hole, WireGuard | ✅ |
| 🔀 proxy | proxy | Caddy | ✅ |
| ⚙️ ops | ops | Homarr, Vaultwarden | ✅ |
| 🛡️ security | security | CrowdSec, Trivy | ✅ |
| 🤖 **anubis** | **container (Podman)** | **Anubis AI Firewall** | **✅** |

---

## Profile Quick Select

```
┌─────────────────────────────────────────────────────────────────┐
│ SELECT YOUR DEPLOYMENT PROFILE                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  A) MINIMAL (Dev/Test)                                          │
│     Stacks: monitoring, media                                   │
│     Resources: 2 CPU, 4Gi RAM, 10Gi storage                     │
│     Command: -e persistence_enabled=false                       │
│                                                                 │
│  B) STANDARD (Development)                                      │
│     Stacks: All except backup, security                         │
│     Resources: 4 CPU, 8Gi RAM, 20Gi storage                     │
│     Command: -e persistence_enabled=false                       │
│                                                                 │
│  C) PRODUCTION (Full Stack)                                     │
│     Stacks: All 10 stacks                                       │
│     Resources: 16+ CPU, 64Gi+ RAM, 800Gi+ storage               │
│     Command: -e persistence_enabled=true                        │
│                                                                 │
│  D) MONITORING ONLY                                             │
│     Stacks: monitoring, logging, backup                         │
│     Resources: 4 CPU, 16Gi RAM, 200Gi storage                   │
│     Command: -e media_stack_enabled=false                       │
│                                                                 │
│  E) MEDIA SERVER                                                │
│     Stacks: media, monitoring, backup                           │
│     Resources: 8+ CPU, 16Gi RAM, 1Ti+ storage                   │
│     Command: -e media_gpu_enabled=true                          │
│                                                                 │
│  F) SECURITY & COMPLIANCE                                       │
│     Stacks: monitoring, logging, security, auth, backup         │
│     Resources: 8 CPU, 32Gi RAM, 430Gi storage                   │
│     Command: -e media_stack_enabled=false                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## One-Line Deployments

```bash
# Minimal testing
ansible-playbook deploy_all_stacks.yml -i inventory/local_test.ini -e persistence_enabled=false

# Standard development
ansible-playbook deploy_all_stacks.yml -i inventory/local_test.ini

# Production full stack
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini -e persistence_enabled=true

# Monitoring only
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini -e media_stack_enabled=false -e database_stack_enabled=false

# Media server with GPU
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini -e media_gpu_enabled=true -e logging_stack_enabled=false

# Security stack only
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini -e media_stack_enabled=false -e ops_stack_enabled=false
```

---

## Resource Requirements

| Profile | CPU | Memory | Storage | Network |
|---------|-----|--------|---------|---------|
| Minimal | 2 cores | 4Gi | 10Gi | 1Gbps |
| Standard | 4 cores | 8Gi | 20Gi | 1Gbps |
| Production | 16+ cores | 64Gi+ | 800Gi+ | 10Gbps |
| Monitoring | 4 cores | 16Gi | 200Gi | 1Gbps |
| Media | 8+ cores | 16Gi | 1Ti+ | 1Gbps |
| Security | 8 cores | 32Gi | 430Gi | 1Gbps |

---

## Security Checklist

```
Production Deployment:
  ☐ RBAC enabled (serviceAccount.create=true)
  ☐ Pod security context (runAsNonRoot=true)
  ☐ Resource limits defined
  ☐ Network policies enabled
  ☐ TLS certificates configured
  ☐ Secrets encrypted with SOPS
  ☐ Backup strategy defined
  ☐ Monitoring alerts configured
```

---

## Validation Commands

```bash
# Validate all charts
for chart in charts/*/; do
  ./scripts/validate-chart-security.sh "$chart"
done

# Check deployment status
kubectl get pods -A --field-selector=status.phase!=Running

# Check resource usage
kubectl top nodes && kubectl top pods -A

# Check PVC status
kubectl get pvc -A

# Check security context
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.securityContext.runAsNonRoot}{"\n"}{end}'
```

---

## Troubleshooting Quick Fix

```bash
# Pod stuck in Pending
kubectl describe pod <pod-name> -n <namespace>
kubectl get pvc -n <namespace>

# Pod in CrashLoopBackOff
kubectl logs <pod-name> -n <namespace> --tail=100
kubectl logs <pod-name> -n <namespace> --previous

# DNS issues
kubectl run dns-test --image=busybox --rm -it -- nslookup google.com

# Certificate issues
kubectl get certificates -A
kubectl describe certificate <cert-name> -n <namespace>

# Rollback deployment
helm rollback <release-name> -n <namespace>
```

---

## Contact & Support

| Issue Type | Priority | Contact | Response Time |
|------------|----------|---------|---------------|
| Production Down | P0 | oncall@example.com | 15 minutes |
| Security Incident | P0 | security@example.com | 15 minutes |
| Performance Issue | P1 | infra@example.com | 4 hours |
| Feature Request | P3 | github-issues | 1 week |

---

## Document Info

- **Version:** 1.0
- **Last Updated:** 2026-02-28
- **Full Documentation:** docs/deployment/PRODUCTION_RUNBOOK.md
- **Deployment Matrix:** docs/deployment/DEPLOYMENT_MATRIX.md
- **Security Standards:** docs/security/SECURITY_STANDARDS.md
