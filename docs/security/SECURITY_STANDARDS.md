# Deploy-System-Unified Security Standards

**Audit Event Identifier:** DSU-SEC-220001  
**Document Type:** Security Standard  
**Version:** 1.0  
**Date:** 2026-02-28  
**Status:** ✅ ENFORCED  
**Compliance:** ISO 27001 §8.20, NIST SP 800-53, CIS Benchmark  
**Review Status:** Bi-annual  
**Next Review:** 2026-08-28  

---

## Overview

This document defines the mandatory security standards for all Helm charts in the Deploy-System-Unified project. All charts MUST comply with these standards before deployment to production.

---

## 1. RBAC Standards

### 1.1 ServiceAccount (REQUIRED)

Every chart MUST create a dedicated ServiceAccount:

```yaml
# templates/rbac.yaml
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "chart.serviceAccountName" . }}
  labels:
    app.kubernetes.io/name: {{ include "chart.name" . }}
    app.kubernetes.io/instance: {{ .Release.Name }}
    app.kubernetes.io/component: {{ .Chart.Name }}
  {{- with .Values.serviceAccount.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Requirements:**
- ✅ ServiceAccount MUST be created by default (`create: true`)
- ✅ Name SHOULD be auto-generated from chart fullname
- ✅ Annotations MUST be configurable (for IRSA, workload identity, etc.)
- ❌ MUST NOT use `default` ServiceAccount

**Configuration (values.yaml):**
```yaml
serviceAccount:
  create: true
  name: ""  # Auto-generated if empty
  annotations: {}
  # Example for EKS IRSA:
  # eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT:role/ROLE
```

---

### 1.2 Role/ClusterRole (REQUIRED)

Every chart MUST define minimal RBAC permissions:

```yaml
# Use Role for namespace-scoped resources
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {{ include "chart.fullname" . }}
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list", "watch"]
```

**OR**

```yaml
# Use ClusterRole for cluster-wide resources (e.g., nodes, pods/log)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: {{ include "chart.fullname" . }}
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get"]
```

**Requirements:**
- ✅ Role MUST follow least privilege principle
- ✅ ClusterRole SHOULD be used only when namespace scope is insufficient
- ✅ Verbs MUST be explicitly listed (no `*` wildcards)
- ✅ Resources MUST be explicitly listed (no `*` wildcards)

---

### 1.3 RoleBinding/ClusterRoleBinding (REQUIRED)

Every chart MUST bind ServiceAccount to Role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: {{ include "chart.fullname" . }}
subjects:
  - kind: ServiceAccount
    name: {{ include "chart.serviceAccountName" . }}
    namespace: {{ .Release.Namespace }}
roleRef:
  kind: Role
  name: {{ include "chart.fullname" . }}
  apiGroup: rbac.authorization.k8s.io
```

**Requirements:**
- ✅ Binding MUST reference the chart's ServiceAccount
- ✅ Binding MUST be in the same namespace as the workload
- ✅ roleRef MUST match the Role/ClusterRole name

---

## 2. Pod Security Standards

### 2.1 Pod-Level SecurityContext (REQUIRED)

Every Deployment/DaemonSet/StatefulSet MUST define pod security context:

```yaml
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: <app-specific-uid>
        runAsGroup: <app-specific-gid>
        fsGroup: <app-specific-gid>
        fsGroupChangePolicy: "OnRootMismatch"
        seccompProfile:
          type: RuntimeDefault
```

**Requirements:**
- ✅ `runAsNonRoot: true` - MUST be set
- ✅ `runAsUser` - MUST be non-zero (use app-specific UID)
- ✅ `runAsGroup` - MUST match runAsUser or app GID
- ✅ `fsGroup` - MUST be set for volume permissions
- ✅ `seccompProfile.type` - MUST be `RuntimeDefault` or `Localhost`

**Recommended UIDs:**
| Application | UID | GID | Notes |
|-------------|-----|-----|-------|
| Grafana | 472 | 472 | Official grafana user |
| Prometheus | 65534 | 65534 | nobody user |
| Loki | 10001 | 10001 | loki user |
| Generic apps | 1000 | 1000 | Standard non-root |

---

### 2.2 Container-Level SecurityContext (REQUIRED)

Every container MUST define security context:

```yaml
containers:
  - name: <container-name>
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: false  # true if app doesn't write
      capabilities:
        drop:
          - ALL
        # add: []  # Only if absolutely required
```

**Requirements:**
- ✅ `allowPrivilegeEscalation: false` - MUST be set
- ✅ `readOnlyRootFilesystem` - SHOULD be true (false only if app needs writes)
- ✅ `capabilities.drop: ["ALL"]` - MUST drop all capabilities
- ❌ `capabilities.add` - MUST NOT add unless documented exception

**Documented Exceptions:**
| Application | Capability | Reason |
|-------------|-----------|--------|
| Pi-hole | NET_ADMIN | DHCP server functionality |
| Promtail | DAC_READ_SEARCH | Read host logs |
| Jellyfin (GPU) | NET_BIND_SERVICE | GPU access |

---

## 3. Network Security

### 3.1 Service Configuration (REQUIRED)

Every Service MUST explicitly define type:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "chart.fullname" . }}
spec:
  type: ClusterIP  # Default, explicit
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
  selector:
    app: {{ include "chart.name" . }}
```

**Requirements:**
- ✅ `type: ClusterIP` - SHOULD be default (use LoadBalancer/NodePort only when needed)
- ✅ Ports MUST be explicitly named
- ✅ Selector MUST reference pod labels

---

### 3.2 Ingress Configuration (OPTIONAL)

If Ingress is provided:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "chart.fullname" . }}
  annotations:
    # MUST NOT use deprecated annotations
    # kubernetes.io/ingress.class: nginx  # DEPRECATED
spec:
  ingressClassName: nginx  # USE THIS INSTEAD
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ include "chart.fullname" . }}
                port:
                  number: 80
```

**Requirements:**
- ✅ MUST use `spec.ingressClassName` (not annotation)
- ✅ MUST use `pathType: Prefix` or `Exact` (not `ImplementationSpecific`)
- ✅ TLS SHOULD be configured for production

---

## 4. Image Security

### 4.1 Image Specification (REQUIRED)

Every container MUST specify image with tag:

```yaml
containers:
  - name: <container-name>
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
    imagePullPolicy: IfNotPresent  # or Always for :latest
```

**Requirements:**
- ✅ Image MUST include explicit tag (no `:latest` in production)
- ✅ `imagePullPolicy` MUST be set
- ✅ Repository and tag MUST be configurable via values.yaml

**Configuration (values.yaml):**
```yaml
image:
  repository: grafana/grafana
  tag: "11.5"  # Pin specific version
  pullPolicy: IfNotPresent
```

---

### 4.2 Image Digest (RECOMMENDED)

For production, use image digest:

```yaml
image:
  repository: grafana/grafana
  tag: "11.5@sha256:abc123..."  # Pin digest
```

---

## 5. Resource Management

### 5.1 Resource Requests/Limits (REQUIRED)

Every container MUST define resources:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

**Requirements:**
- ✅ `requests.memory` - MUST be set
- ✅ `requests.cpu` - MUST be set
- ✅ `limits.memory` - MUST be set
- ✅ `limits.cpu` - SHOULD be set (optional for burstable workloads)

**Guidelines:**
| Workload Type | Memory Request | Memory Limit | CPU Request | CPU Limit |
|---------------|---------------|--------------|-------------|-----------|
| Small app | 128Mi | 256Mi | 50m | 100m |
| Medium app | 256Mi | 512Mi | 100m | 500m |
| Large app | 512Mi | 1Gi | 250m | 1000m |
| Database | 1Gi | 2Gi | 500m | 2000m |

---

## 6. Health Checks

### 6.1 Liveness Probe (REQUIRED)

Every container MUST define liveness probe:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

**Requirements:**
- ✅ `initialDelaySeconds` - MUST be set (give app time to start)
- ✅ `periodSeconds` - MUST be set
- ✅ `timeoutSeconds` - MUST be set
- ✅ `failureThreshold` - MUST be set

---

### 6.2 Readiness Probe (REQUIRED)

Every container MUST define readiness probe:

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

**Requirements:**
- ✅ MUST be set for all containers
- ✅ `initialDelaySeconds` SHOULD be less than liveness probe

---

### 6.3 Startup Probe (RECOMMENDED)

For slow-starting applications:

```yaml
startupProbe:
  httpGet:
    path: /health
    port: http
  failureThreshold: 30
  periodSeconds: 5
```

---

## 7. Secrets Management

### 7.1 Secret References (REQUIRED)

Secrets MUST be referenced via environment variables:

```yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: {{ include "chart.fullname" . }}-secrets
        key: db-password
```

**Requirements:**
- ✅ Secrets MUST NOT be hardcoded in templates
- ✅ MUST use `secretKeyRef` for sensitive data
- ✅ Secret names SHOULD be generated from chart fullname

---

### 7.2 Secret Generation (RECOMMENDED)

Charts SHOULD auto-generate secrets for testing:

```yaml
# templates/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "chart.fullname" . }}-secrets
type: Opaque
stringData:
  db-password: {{ .Values.db.password | default (randAlphaNum 32) | quote }}
```

**Requirements:**
- ✅ Auto-generated secrets MUST use `randAlphaNum` with length ≥ 32
- ✅ Production MUST override with external secrets (SOPS, Vault, etc.)

---

## 8. Validation Checklist

Before merging a chart, verify:

### RBAC
- [ ] ServiceAccount created
- [ ] Role/ClusterRole defined with minimal permissions
- [ ] RoleBinding/ClusterRoleBinding created
- [ ] Deployment references ServiceAccount

### Pod Security
- [ ] Pod securityContext defined
- [ ] runAsNonRoot: true
- [ ] runAsUser/runAsGroup set (non-zero)
- [ ] seccompProfile set

### Container Security
- [ ] Container securityContext defined
- [ ] allowPrivilegeEscalation: false
- [ ] capabilities.drop: ALL
- [ ] No privileged containers

### Resources
- [ ] Memory requests/limits set
- [ ] CPU requests/limits set
- [ ] Values are appropriate for workload

### Health
- [ ] Liveness probe defined
- [ ] Readiness probe defined
- [ ] Probes have appropriate thresholds

### Images
- [ ] Image tag pinned (no :latest)
- [ ] imagePullPolicy set
- [ ] Repository configurable via values

### Secrets
- [ ] No hardcoded secrets
- [ ] Secrets referenced via secretKeyRef
- [ ] Secret names follow convention

---

## 9. Compliance Mapping

| Standard | Control | Implementation |
|----------|---------|----------------|
| CIS Kubernetes Benchmark 5.2.1 | Run as non-root | securityContext.runAsNonRoot |
| CIS Kubernetes Benchmark 5.2.2 | Drop capabilities | securityContext.capabilities.drop |
| CIS Kubernetes Benchmark 5.2.3 | Read-only root FS | securityContext.readOnlyRootFilesystem |
| CIS Kubernetes Benchmark 5.2.4 | Privilege escalation | securityContext.allowPrivilegeEscalation |
| NIST SP 800-190 | Least privilege | RBAC Role with minimal verbs |
| NIST SP 800-190 | Service accounts | Dedicated ServiceAccount per app |
| ISO 27001 §8.20 | Access control | RBAC + securityContext |
| Pod Security Standards | Restricted | All controls above |

---

## 10. Exceptions Process

If a chart cannot comply with a standard:

1. **Document the exception** in the chart's values.yaml:
   ```yaml
   # SECURITY EXCEPTION: NET_ADMIN capability required for DHCP
   # See: docs/security/exceptions.md#pi-hole-net-admin
   ```

2. **Create exception documentation** in `docs/security/exceptions.md`:
   ```markdown
   ### Pi-hole NET_ADMIN Capability
   
   **Chart:** network-stack (Pi-hole)
   **Capability:** NET_ADMIN
   **Reason:** Required for DHCP server functionality
   **Risk:** Container can modify network configuration
   **Mitigation:** Pod runs as non-root, limited to specific network namespace
   ```

3. **Get security team approval** before merging

---

## 11. Enforcement

### Pre-commit Hooks
```bash
# Run security validation
./scripts/validate-chart-security.sh charts/<chart-name>
```

### CI/CD Checks
- [ ] Helm lint passes
- [ ] Security validation script passes
- [ ] No hardcoded secrets detected
- [ ] All required fields present

### Runtime Enforcement
- [ ] Pod Security Admission set to `restricted`
- [ ] OPA Gatekeeper policies enforced
- [ ] Falco rules monitor for violations

---

## 12. References

- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST SP 800-190](https://csrc.nist.gov/publications/detail/sp/800-190/final)
- [ISO 27001 Controls](https://www.iso.org/standard/27001)

---

**All charts MUST comply with these standards. Non-compliant charts will be rejected in CI/CD.**
