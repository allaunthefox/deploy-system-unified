# Wiki Index - Complete Documentation Map
# =============================================================================
# Central index for all Deploy-System-Unified documentation
# Last Updated: 2026-02-28
# =============================================================================

## 📚 Documentation Categories

### 1. Getting Started

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](../README.md) | Project overview | All users |
| [docs/INDEX.md](INDEX.md) | Documentation hub | All users |
| [docs/deployment/DEPLOYMENT_QUICK_REFERENCE.md](deployment/DEPLOYMENT_QUICK_REFERENCE.md) | One-page quick ref | Operators |
| [docs/deployment/PRODUCTION_RUNBOOK.md](deployment/PRODUCTION_RUNBOOK.md) | Step-by-step deploy | Operators |

---

### 2. Architecture & Design

| Document | Purpose | Audience |
|----------|---------|----------|
| [docs/architecture/README.md](architecture/README.md) | Core philosophy | Architects |
| [docs/architecture/VIRTUAL_NETWORKING.md](architecture/VIRTUAL_NETWORKING.md) | VLAN/VXLAN design | Network engineers |
| [docs/architecture/SECURITY_LAYERS.md](architecture/SECURITY_LAYERS.md) | 5-layer defense | Security team |
| [docs/architecture/MODULAR_LAYERS.md](architecture/MODULAR_LAYERS.md) | Layered architecture | Architects |

---

### 3. Deployment Guides

| Document | Purpose | Stacks Covered |
|----------|---------|----------------|
| [docs/deployment/DEPLOYMENT_MATRIX.md](deployment/DEPLOYMENT_MATRIX.md) | All valid combinations | All 11 stacks |
| [docs/deployment/DEPLOYMENT_INCOMPATIBILITIES.md](deployment/DEPLOYMENT_INCOMPATIBILITIES.md) | Invalid combinations | All 11 stacks |
| [docs/deployment/ANUBIS_DEPLOYMENT.md](deployment/ANUBIS_DEPLOYMENT.md) | Anubis AI Firewall | Anubis only |
| [docs/deployment/PRODUCTION_RUNBOOK.md](deployment/PRODUCTION_RUNBOOK.md) | Production deployment | All stacks |

#### Deployment Profiles

| Profile | Use Case | Stacks | Resources |
|---------|----------|--------|-----------|
| **A) MINIMAL** | Dev/Testing | 2 | 2 CPU, 4Gi, 10Gi |
| **B) STANDARD** | Development | 8 | 4 CPU, 8Gi, 20Gi |
| **C) PRODUCTION** | Full Production | 11 | 16+ CPU, 64Gi+, 800Gi+ |
| **D) MONITORING** | Observability | 4 | 4 CPU, 16Gi, 200Gi |
| **E) MEDIA** | Media Server | 4 | 8+ CPU, 16Gi, 1Ti+ |
| **F) SECURITY** | Compliance | 6 | 8 CPU, 32Gi, 430Gi |

---

### 4. Security & Compliance

| Document | Purpose | Standards |
|----------|---------|-----------|
| [docs/security/SECURITY_STANDARDS.md](security/SECURITY_STANDARDS.md) | Security requirements | CIS, NIST, ISO 27001 |
| [DSU_AUDIT_EVENT_IDENTIFIERS.md](../DSU_AUDIT_EVENT_IDENTIFIERS.md) | Audit code catalog | ISO 27001, ISO 27040 |
| [docs/security/THREAT_MODEL.md](security/THREAT_MODEL.md) | STRIDE analysis | ISO 27001 |
| [docs/compliance/COMPLIANCE_REPORT.md](compliance/COMPLIANCE_REPORT.md) | Compliance status | CIS, NIST, ISO |

#### Audit Event Identifiers (New)

| Section | Codes | Purpose |
|---------|-------|---------|
| §3 Container Operations | 700010-700021 | Helm, Anubis |
| §4 Network Operations | 810310-810320 | TLS, Network Policy |
| §9 Monitoring & Logging | 840040-840051 | Monitoring, Loki |
| §10 Compliance & Audit | 400040-400060 | Security, RBAC |
| §11 Deployment & Config | 900010-900030 | Helm, Validation |
| §12 Idempotency & Drift | 600015-600016 | Drift correction |
| §13 AI Infrastructure | 480010-480012 | Anubis AI Firewall |
| §24 Kubernetes Operations | 820010-820060 | K8s, Helm, PVC |
| §25 Application Stacks | 850000-850100 | All 11 stacks |

---

### 5. Stack Documentation

#### Kubernetes Helm Charts (10 stacks)

| Stack | Namespace | Documentation | Production Ready |
|-------|-----------|---------------|-----------------|
| monitoring-stack | monitoring | charts/monitoring-stack/README.md | ✅ |
| media-stack | media | charts/media-stack/README.md | ✅ |
| logging-stack | logging | charts/logging-stack/README.md | ✅ |
| database-stack | database | charts/database-stack/README.md | ✅ |
| auth-stack | auth | charts/auth-stack/README.md | ✅ |
| backup-stack | backup | charts/backup-stack/README.md | ✅ |
| network-stack | network | charts/network-stack/README.md | ✅ |
| proxy-stack | proxy | charts/proxy-stack/README.md | ✅ |
| ops-stack | ops | charts/ops-stack/README.md | ✅ |
| security-stack | security | charts/security-stack/README.md | ✅ |

#### Podman Containers (1 stack)

| Stack | Type | Documentation | Production Ready |
|-------|------|---------------|-----------------|
| **anubis** | Container (Podman) | [docs/deployment/ANUBIS_DEPLOYMENT.md](deployment/ANUBIS_DEPLOYMENT.md) | ✅ |

---

### 6. Development & Testing

| Document | Purpose | Tools |
|----------|---------|-------|
| [docs/development/CONTRIBUTING.md](development/CONTRIBUTING.md) | Contributing guide | Git, Ansible |
| [docs/development/STYLE_GUIDE.md](development/STYLE_GUIDE.md) | Code style | yamllint, ansible-lint |
| [docs/development/MOLECULE_TESTING.md](development/MOLECULE_TESTING.md) | Molecule tests | Molecule, Docker |
| [scripts/validate-chart-security.sh](../scripts/validate-chart-security.sh) | Chart validation | Bash, grep |
| [scripts/validate-deployment-compatibility.sh](../scripts/validate-deployment-compatibility.sh) | Compatibility check | Bash, kubectl |

---

### 7. Operations & Maintenance

| Document | Purpose | Frequency |
|----------|---------|-----------|
| [docs/RESTORE_RUNBOOK.md](RESTORE_RUNBOOK.md) | Disaster recovery | As needed |
| [docs/deployment/PRODUCTION_RUNBOOK.md](deployment/PRODUCTION_RUNBOOK.md) | Daily operations | Daily |
| [docs/benchmarks/](benchmarks/) | Performance baselines | Monthly |
| [docs/planning/ROADMAP.md](planning/ROADMAP.md) | Future planning | Quarterly |

---

### 8. Charts Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| [charts/README.md](../charts/README.md) | Chart deployment guide | charts/ |
| [charts/_templates/_security-helpers.tpl](../charts/_templates/_security-helpers.tpl) | Security templates | charts/ |
| [charts/*/values.production.yaml](../charts/) | Production values | charts/*/ |

---

## 🔧 Quick Links by Task

### I want to...

| Task | Document | Command |
|------|----------|---------|
| **Deploy everything** | PRODUCTION_RUNBOOK.md | `ansible-playbook deploy_all_stacks.yml -i inventory/production.ini` |
| **Deploy monitoring only** | DEPLOYMENT_MATRIX.md | `helm install monitoring charts/monitoring-stack -n monitoring` |
| **Deploy Anubis** | ANUBIS_DEPLOYMENT.md | `ansible-playbook run_anubis_only.yml -i inventory/production.ini` |
| **Validate charts** | SECURITY_STANDARDS.md | `./scripts/validate-chart-security.sh charts/monitoring-stack` |
| **Check compatibility** | DEPLOYMENT_INCOMPATIBILITIES.md | `./scripts/validate-deployment-compatibility.sh` |
| **Find audit code** | DSU_AUDIT_EVENT_IDENTIFIERS.md | Search by code or standard |
| **Troubleshoot** | PRODUCTION_RUNBOOK.md | See Troubleshooting section |

---

## 📊 Stack Status Matrix

| Stack | Type | Security Hardened | RBAC | Production Values | Audit Codes |
|-------|------|-------------------|------|-------------------|-------------|
| monitoring-stack | Helm | ✅ | ✅ | ✅ | 850000-850009 |
| media-stack | Helm | ✅ | ✅ | ✅ | 850010-850019 |
| logging-stack | Helm | ✅ | ✅ | ✅ | 850020-850029 |
| database-stack | Helm | ✅ | ✅ | ✅ | 850030-850039 |
| auth-stack | Helm | ✅ | ✅ | ✅ | 850040-850049 |
| backup-stack | Helm | ✅ | ✅ | ✅ | 850050-850059 |
| network-stack | Helm | ✅ | ✅ | ✅ | 850060-850069 |
| proxy-stack | Helm | ✅ | ✅ | ✅ | 850070-850079 |
| ops-stack | Helm | ✅ | ✅ | ✅ | 850080-850089 |
| security-stack | Helm | ✅ | ✅ | ✅ | 850090-850099 |
| anubis | Podman | ✅ | N/A | ✅ | 850100-850109 |

---

## 🎯 Documentation Quality

| Document | Last Updated | Reviewed By | Next Review |
|----------|--------------|-------------|-------------|
| DEPLOYMENT_MATRIX.md | 2026-02-28 | Infrastructure Team | 2026-03-28 |
| DEPLOYMENT_INCOMPATIBILITIES.md | 2026-02-28 | Security Team | 2026-03-28 |
| SECURITY_STANDARDS.md | 2026-02-28 | Security Team | 2026-03-28 |
| ANUBIS_DEPLOYMENT.md | 2026-02-28 | Infrastructure Team | 2026-03-28 |
| DSU_AUDIT_EVENT_IDENTIFIERS.md | 2026-02-28 | Compliance Team | 2026-03-28 |
| PRODUCTION_RUNBOOK.md | 2026-02-28 | Operations Team | 2026-03-28 |

---

## 📖 Document Control

**Version:** 1.0  
**Last Updated:** 2026-02-28  
**Maintained By:** Infrastructure Team  
**Review Frequency:** Monthly  

**Related Documents:**
- [README.md](../README.md)
- [docs/INDEX.md](INDEX.md)
- [DSU_AUDIT_EVENT_IDENTIFIERS.md](../DSU_AUDIT_EVENT_IDENTIFIERS.md)

---

**End of Wiki Index**
