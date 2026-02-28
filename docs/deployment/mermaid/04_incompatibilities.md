---
title: Deployment Incompatibilities
description: Critical and high-risk combinations that should NOT be deployed
lastUpdated: 2026-02-28
auditEventIdentifier: DSU-MMD-130001
mermaidVersion: 1.2
rendererSupport:
  - github
  - gitlab
  - mermaid-live
---

```mermaid
graph TB
    subgraph "❌ CRITICAL - NEVER DEPLOY"
        INC001["INC-001: Multiple Ingress Controllers<br/>Issue: Port 80/443 conflicts<br/>Fix: Use ONE ingress controller<br/>⚠️ Affects: All Profiles"]
        INC002["INC-002: Duplicate DNS Servers<br/>Issue: Port 53 conflicts<br/>Fix: No hostNetwork for Pi-hole<br/>⚠️ Affects: Profiles B, E, F"]
        INC003["INC-003: Multiple DBs Same Node<br/>Issue: I/O contention<br/>Fix: Use node affinity<br/>⚠️ Affects: Profiles C, F"]
        INC004["INC-004: Insufficient Resources<br/>Issue: OOMKilled, crash<br/>Fix: Match profile to hardware<br/>⚠️ Affects: All Profiles"]
        INC005["INC-005: GPU Without Plugin<br/>Issue: Pods stuck pending<br/>Fix: Install plugin or disable<br/>⚠️ Affects: Profile E (Media)"]
    end

    subgraph "⚠️ HIGH RISK - NOT RECOMMENDED"
        RISK001["RISK-001: All Stacks Single Node<br/>Issue: No HA, contention<br/>Fix: Use 3+ nodes<br/>⚠️ Affects: Profile C"]
        RISK002["RISK-002: emptyDir in Production<br/>Issue: Data loss<br/>Fix: Use persistence<br/>⚠️ Affects: Profile C"]
        RISK003["RISK-003: Default Passwords<br/>Issue: Security risk<br/>Fix: Generate strong passwords<br/>⚠️ Affects: All Profiles"]
        RISK004["RISK-004: Monitoring Without Alerting<br/>Issue: Silent failures<br/>Fix: Enable alertmanager<br/>⚠️ Affects: Profiles A, B, D"]
        RISK005["RISK-005: Backup Without Testing<br/>Issue: False security<br/>Fix: Test restores<br/>⚠️ Affects: Profiles C, D, E, F"]
        RISK006["RISK-006: Logging Without Retention<br/>Issue: Storage exhaustion<br/>Fix: Set retention period<br/>⚠️ Affects: Profiles B, C, D, F"]
        RISK007["RISK-007: Auth Without DB HA<br/>Issue: SSO single point of failure<br/>Fix: Use external HA DB<br/>⚠️ Affects: Profiles B, C, F"]
    end

    subgraph "⚡ MODERATE RISK - USE WITH CAUTION"
        CAUTION001["CAUTION-001: Media Transcoding Shared Node<br/>Issue: CPU spikes affect others<br/>Fix: Use node selector<br/>⚠️ Affects: Profiles B, C, E"]
        CAUTION002["CAUTION-002: High-Volume Logging + Limited Storage<br/>Issue: Frequent rotation<br/>Fix: Increase storage<br/>⚠️ Affects: Profiles A, B, D"]
        CAUTION003["CAUTION-003: Prometheus Without Downsampling<br/>Issue: Memory exhaustion<br/>Fix: Set scrape interval<br/>⚠️ Affects: Profiles A, B, C, D"]
    end

    subgraph "Profiles"
        PA["Profile A<br/>MINIMAL"]
        PB["Profile B<br/>STANDARD"]
        PC["Profile C<br/>PRODUCTION"]
        PD["Profile D<br/>MONITORING"]
        PE["Profile E<br/>MEDIA"]
        PF["Profile F<br/>SECURITY"]
    end

    classDef critical fill:#ffebee,stroke:#c62828,stroke-width:3px
    classDef high fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef moderate fill:#fff9c4,stroke:#f9a825,stroke-width:2px
    classDef profile fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px

    class INC001,INC002,INC003,INC004,INC005 critical
    class RISK001,RISK002,RISK003,RISK004,RISK005,RISK006,RISK007 high
    class CAUTION001,CAUTION002,CAUTION003 moderate
    class PA,PB,PC,PD,PE,PF profile
```

---

## 📋 Affected Profiles Matrix

| Issue | A | B | C | D | E | F |
|-------|:-:|:-:|:-:|:-:|:-:|:-:|
| **INC-001** Multiple Ingress | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **INC-002** Duplicate DNS | ❌ | ⚠️ | ❌ | ❌ | ⚠️ | ⚠️ |
| **INC-003** Multiple DBs | ❌ | ❌ | ⚠️ | ❌ | ❌ | ⚠️ |
| **INC-004** Insufficient Resources | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **INC-005** GPU Without Plugin | ❌ | ❌ | ❌ | ❌ | ⚠️ | ❌ |
| **RISK-001** All Stacks Single Node | ❌ | ❌ | ⚠️ | ❌ | ❌ | ❌ |
| **RISK-002** emptyDir Production | ❌ | ❌ | ⚠️ | ❌ | ❌ | ❌ |
| **RISK-003** Default Passwords | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **RISK-004** Monitoring No Alerting | ⚠️ | ⚠️ | ❌ | ⚠️ | ❌ | ❌ |
| **RISK-005** Backup Without Testing | ❌ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| **RISK-006** Logging No Retention | ❌ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ |
| **RISK-007** Auth Without DB HA | ❌ | ⚠️ | ❌ | ❌ | ❌ | ⚠️ |
| **CAUTION-001** Transcoding Shared | ❌ | ⚠️ | ⚠️ | ❌ | ⚠️ | ❌ |
| **CAUTION-002** High-Volume Logging | ⚠️ | ⚠️ | ❌ | ⚠️ | ❌ | ❌ |
| **CAUTION-003** Prometheus No Downsample | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ |

**Legend:** ✅ = Critical | ⚠️ = Applies | ❌ = Not applicable

---

## 🔧 Mitigation Checklist

### Before Deployment
- [ ] Verify hardware meets profile requirements (see [Resource Requirements](./05_resource_requirements.md))
- [ ] Generate strong passwords using `openssl rand -base64 32`
- [ ] Review network topology for port conflicts
- [ ] Confirm single ingress controller configuration

### During Deployment
- [ ] Monitor resource usage via `kubectl top nodes`
- [ ] Verify PVC binding and storage class
- [ ] Check pod scheduling and affinity rules

### After Deployment
- [ ] Test backup restoration procedure
- [ ] Configure alertmanager routing
- [ ] Set log retention policies
- [ ] Validate HA database connections

---

## See Also

- [Deployment Profiles](./02_deployment_profiles.md) - Profile stack compositions
- [Decision Tree](./06_decision_tree.md) - Choosing the right profile
- [Security Architecture](./07_security_architecture.md) - Security controls overview
