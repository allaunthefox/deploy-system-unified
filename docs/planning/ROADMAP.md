# Roadmap

Our detailed planning and execution documents are maintained in the `docs/planning/` directory.

---

## 📋 Planning Overview

This roadmap provides a high-level view of project direction. For detailed execution plans, see the linked documents.

> **Current Status:** [Base Layer Implementation Status (95% Complete)](../development/BASE_LAYER_IMPLEMENTATION_STATUS.md)

### Planning Horizons

| Horizon | Timeframe | Focus |
|---------|-----------|-------|
| **Current** | Q1 2026 (Jan-Mar) | Stability, idempotence, GPU orchestration |
| **Near-Term** | Q2 2026 (Apr-Jun) | Security enhancements, compliance framework |
| **Mid-Term** | Q3-Q4 2026 (Jul-Dec) | Enterprise features, community growth |
| **Long-Term** | 2027+ | Advanced features, ecosystem expansion |

---

## 🎯 Active Plans (Q1 2026)

| Plan | Status | Focus | Completion |
|------|--------|-------|------------|
| **[Phase 3: Secrets & K8s Plan](PHASE3_SECRETS_K8S_PLAN.md)** | 🟢 Active | SOPS migration, Kubernetes scaling | Mar 2026 |
| **[Stability Execution Plan](STABILITY_EXECUTION_PLAN_2026.md)** | ✅ Complete | Idempotence, GPU orchestration | Feb 2026 |
| **[Phased Execution Plan](PHASED_EXECUTION_PLAN.md)** | 📚 Reference | Task breakdown | Reference |

---

## 🔒 Proposed Plans (Q2 2026)

| Plan | Status | Focus | Timeline |
|------|--------|-------|----------|
| **[Security Enhancement Plan](SECURITY_ENHANCEMENT_PLAN_2026.md)** | 🟡 Proposed | CIS/STIG compliance, continuous monitoring, enterprise secrets | Q2-Q4 2026 |

### Security Enhancement Highlights

**Objective:** Elevate security posture from **Good (80/100)** to **Excellent (92/100)**

**Key Initiatives:**
1. **Compliance Framework Integration**
   - CIS Benchmark mapping (Level 1 & 2)
   - DISA STIG integration
   - NIST 800-53/800-171 mapping

2. **Continuous Security Monitoring**
   - Goss-based validation
   - Drift detection and remediation
   - Security dashboard (Grafana)

3. **Enterprise Secrets Management**
   - HashiCorp Vault integration
   - Cloud secret managers (AWS/Azure/GCP)
   - Automated secret rotation

4. **Enhanced Container Security**
   - Image signing (Sigstore/Cosign)
   - Runtime security (Falco)
   - Network policy enforcement

5. **Security Testing & Validation**
   - Automated vulnerability scanning
   - Penetration testing framework
   - Red team automation (MITRE ATT&CK)

**Competitive Position:** Will make Deploy-System-Unified the **highest-rated** Ansible security hardening project (92/100 vs. ansible-lockdown's 86/100).

**Activation:** Requires Security Review Board approval and resource allocation.

**See:** [SECURITY_ENHANCEMENT_PLAN_2026.md](SECURITY_ENHANCEMENT_PLAN_2026.md) for full details.

---

## 🔮 Future Plans

### Completed Plans

| Plan | Status | Completion Date | Notes |
|------|--------|-----------------|-------|
| **[Restructuring Plan](RESTRUCTURING_PLAN_2026.md)** | ✅ Complete | Feb 2026 | Architecture-based restructuring (x86/ARM/RISC-V) |
| **[Community Enhancement Plan](COMMUNITY_ENHANCEMENT_PLAN.md)** | ✅ Complete | Feb 2026 | CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md |

### Backlog Plans

| Plan | Priority | Focus | Activation Criteria |
|------|----------|-------|---------------------|
| **[GPU Enhanced Plan](GPU_ENHANCED_PLAN.md)** | Medium | Advanced GPU orchestration (Vulkan, eGPU, Thunderbolt) | After Phase 3 completion |
| **[Media Stack v2](MEDIA_STACK_V2.md)** | Low | Next-gen media stack architecture | Community demand |
| **[Migration Plan](MIGRATION_PLAN.md)** | Low | Migration strategies and tooling | User requests |
| **[Determinism Roadmap](DETERMINISM_ROADMAP.md)** | Medium | Full deployment determinism | After security enhancements |

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

### Q2 2026: Forensic Intelligence & Archival Excellence ✅

**Theme:** Compliance, monitoring, and autonomic recovery

**Goals:**
- ✅ ISO 27040 Autonomic Restore Testing active
- ✅ Loki/Grafana Forensic Dashboards operational
- ✅ SBOM Supply Chain Audit implemented (CycloneDX)
- ✅ PQC Secret Archival Readiness (Age 1.3+)
- ✅ 100% Metadata coverage (81/81 roles)
- ✅ 100/100 Compliance Score achieved

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
- 🔵 Full CIS/STIG compliance
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
| **Security Score** | 80/100 | 85/100 | 92/100 |
| **Role Implementation Score** | 73/100 | 90/100 | 95/100 |
| **CIS Compliance** | 0% | 80% (Level 1) | 95% (Level 1+2) |
| **STIG Compliance** | 0% | 70% | 90% |
| **Test Coverage** | ~60% | 75% | 90% |
| **Molecule Platforms/Role** | 1 | 3+ | 5+ |
| **Documentation Coverage** | ~70% | 85% | 95% |

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
| [Stability Execution Plan](STABILITY_EXECUTION_PLAN_2026.md) | Current execution board |
| [Security Enhancement Plan](SECURITY_ENHANCEMENT_PLAN_2026.md) | Security roadmap (proposed) |
| [GPU Enhanced Plan](GPU_ENHANCED_PLAN.md) | GPU feature backlog |
| [Community Enhancement Plan](COMMUNITY_ENHANCEMENT_PLAN.md) | Community growth strategy |
| [Restructuring Plan](RESTRUCTURING_PLAN_2026.md) | Completed architecture work |

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
