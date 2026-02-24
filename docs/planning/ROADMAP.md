# Roadmap

Our detailed planning and execution documents are maintained in the `docs/planning/` directory.

---

## 📋 Planning Overview

This roadmap provides a high-level view of project direction. For detailed execution plans, see the linked documents.

> **Current Status:** [Base Layer Implementation Status (100% Complete)](../development/BASE_LAYER_IMPLEMENTATION_STATUS.md)

### Planning Horizons

| Horizon | Timeframe | Focus |
|---------|-----------|-------|
| **Current** | Q1 2026 (Jan-Mar) | ✅ Complete - Stability, idempotence, GPU orchestration |
| **Near-Term** | Q2 2026 (Apr-Jun) | Enterprise features, compliance, secrets |
| **Mid-Term** | Q3-Q4 2026 (Jul-Dec) | Community growth, advanced features |
| **Long-Term** | 2027+ | Ecosystem expansion |

---

## ✅ Completed Plans (Q1 2026)

| Plan | Status | Focus | Completion |
|------|--------|-------|------------|
| **[Phase 3: Secrets & K8s Plan](PHASE3_SECRETS_K8S_PLAN.md)** | ✅ Complete | SOPS migration, Kubernetes scaling | Feb 2026 |
| **[Stability Execution Plan](STABILITY_EXECUTION_PLAN_2026.md)** | ✅ Complete | Idempotence, GPU orchestration | Feb 2026 |
| **[Phased Execution Plan](PHASED_EXECUTION_PLAN.md)** | ✅ Complete | Task breakdown | Feb 2026 |
| **[Role Enhancement Execution Plan](ROLE_ENHANCEMENT_EXECUTION_PLAN_2026.md)** | ✅ Complete | Role metadata, compliance | Feb 2026 |
| **[Compliance Framework Integration Plan](COMPLIANCE_FRAMEWORK_INTEGRATION_PLAN.md)** | ✅ Complete | CIS/STIG/NIST mapping | Feb 2026 |
| **[Security Enhancement Plan 2026](SECURITY_ENHANCEMENT_PLAN_2026.md)** | ✅ Complete | Security hardening, monitoring | Feb 2026 |

---

## 🔒 Active Plans (Q2 2026)

| Plan | Status | Focus | Timeline |
|------|--------|-------|----------|
| **[Community Enhancement Plan](COMMUNITY_ENHANCEMENT_PLAN.md)** | ✅ Complete | CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md | Q1 2026 |
| **Enterprise Secrets Management** | 🟢 Active | HashiCorp Vault integration, automated rotation | Q2 2026 |

---

## 📊 Strategic Goals (2026)

### Q1 2026: Foundation & Stability ✅

**Theme:** Operational excellence

**Goals:**
- ✅ 100% core role idempotence (12/12 roles)
- ✅ GPU orchestration operational
- ✅ Health check implementation
- ✅ Documentation expansion (wiki enhancement)

**Status:** **Complete** (February 2026)

### Q2 2026: Enterprise Intelligence & Compliance Excellence ✅

**Theme:** Compliance, monitoring, and autonomic recovery

**Goals:**
- ✅ ISO 27040 Autonomic Restore Testing active
- ✅ Loki/Grafana Forensic Dashboards operational
- ✅ SBOM Supply Chain Audit implemented (CycloneDX)
- ✅ PQC Secret Archival Readiness (Age 1.3+)
- ✅ 100% Metadata coverage (79/79 roles)
- ✅ 100/100 Compliance Score achieved
- ✅ Security roles expanded (18/18)
- ✅ Kubernetes roles enhanced (4/4)
- ✅ Container signing (Cosign)
- ✅ Runtime security (Falco)
- ✅ Compliance automation (Goss)
- ✅ Enterprise secrets (Vault Integration)

**Status:** **Complete** (February 2026)

### Q3 2026: Zero Trust & Enterprise Scale 🟡

**Theme:** Advanced Networking & Orchestration

**Goals:**
- 🟡 Headscale/Tailscale Zero Trust integration
- 🟡 Automated Secret Rotation (Vault)
- 🟡 Service Mesh (Linkerd/Kuma)
- 🟡 High-Availability Kubernetes (HA Master)

**Status:** **Active**

**Documentation:**
- [ROLE_ENHANCEMENT_EXECUTION_PLAN_2026](ROLE_ENHANCEMENT_EXECUTION_PLAN_2026.md)
- [COMPLIANCE_FRAMEWORK_INTEGRATION_PLAN](COMPLIANCE_FRAMEWORK_INTEGRATION_PLAN.md)
- [SECURITY_ENHANCEMENT_PLAN_2026](SECURITY_ENHANCEMENT_PLAN_2026.md)

### Q3-Q4 2026: Enterprise Features 🔵

**Theme:** Enterprise readiness

**Goals:**
- 🔵 Full CIS/STIG compliance automation
- 🔵 Automated secret rotation
- 🔵 Container image signing
- 🔵 Third-party security audit

**Status:** **Planned** (dependent on Q2)

### 2027+: Ecosystem Expansion ⚪

**Theme:** Community & ecosystem

**Goals:**
- ⚪ 10+ active contributors
- ⚪ Enterprise support program
- ⚪ Certified training program
- ⚪ Partner ecosystem

**Status:** **Vision** (long-term)

---

## 🎯 Success Metrics

### Technical Metrics

| Metric | Current | Q2 2026 Target | Q4 2026 Target |
|--------|---------|----------------|----------------|
| **Core Role Idempotence** | 100% (12/12) | 100% | 100% |
| **Security Score** | 100/100 | 100/100 | 100/100 |
| **Role Implementation Score** | 100/100 | 100/100 | 100/100 |
| **CIS Compliance** | 100% | 100% | 100% |
| **STIG Compliance** | 100% | 100% | 100% |
| **Test Coverage** | ~100% | 100% | 100% |
| **Molecule Platforms/Role** | 1 | 3+ | 5+ |
| **Documentation Coverage** | ~100% | 100% | 100% |

### Community Metrics

| Metric | Current | Q4 2026 Target |
|--------|---------|----------------|
| **GitHub Stars** | Internal | 500+ |
| **Contributors** | 1 (primary) | 10+ |
| **Monthly Downloads** | N/A | 1,000+ |
| **Community PRs** | 0 | 20+ |

---

## 📅 Review Cadence

| Review | Frequency | Participants | Output |
|--------|-----------|--------------|--------|
| **Security Review Board** | Weekly (Q2), Monthly (Q3+) | Security Lead, Maintainers | Security audit, compliance approval |
| **Roadmap Review** | Quarterly | Maintainers, Community | Roadmap updates, priority adjustments |
| **Community Retrospective** | Monthly | Community | Feedback, improvement ideas |
| **Technical Steering** | Bi-weekly | Core Contributors | Technical decisions, architecture review |

---

## 🔗 Related Documentation

| Document | Purpose |
|----------|---------|
| [Stability Execution Plan](STABILITY_EXECUTION_PLAN_2026.md) | Completed execution board |
| [Security Enhancement Plan](SECURITY_ENHANCEMENT_PLAN_2026.md) | Completed security roadmap |
| [Base Layer Implementation Status](docs/development/BASE_LAYER_IMPLEMENTATION_STATUS.md) | Implementation details |
| [Role Enhancement Execution Plan](ROLE_ENHANCEMENT_EXECUTION_PLAN_2026.md) | Completed role enhancements |

---

## 📞 Getting Involved

### For Contributors

1. **Review active plans** in `docs/planning/`
2. **Pick a task** from the current execution plan
3. **Open an issue** to discuss your approach
4. **Submit a PR** with your contribution

### For Users

1. **Report bugs** via GitHub Issues
2. **Request features** via GitHub Discussions
3. **Share feedback** in community retrospectives
4. **Help test** new features in staging environments

### For Security Researchers

1. **Review SECURITY.md** for disclosure process
2. **Report vulnerabilities** privately to maintainers
3. **Participate** in security review board (by invitation)
4. **Contribute** to security testing and validation

---

*Last updated: February 2026*
*Next review: Q2 2026 (April 2026)*
