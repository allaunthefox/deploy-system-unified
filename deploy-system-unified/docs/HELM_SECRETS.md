# Helm Secrets Management

This document outlines the security practices for managing secrets in Helm charts.

## Overview

All Helm charts must handle sensitive data securely. The project follows these principles:

1. **Never commit secrets** to version control
2. **Use external secrets** management where possible
3. **Encrypt at rest** using SOPS or similar

## Password Placeholders

All charts use placeholder passwords that MUST be changed in production:

| Chart | Default Password | Location |
|-------|-----------------|----------|
| ops-stack | `CHANGEME` | `values.yaml` |
| database-stack | `CHANGEME` | `values.yaml` |
| monitoring-stack | `admin` | `values.yaml` |
| auth-stack | `admin` | `values.yaml` |
| network-stack | `admin` | `values.yaml` |
| backup-stack | N/A | Must be configured |

## Secure Deployment

### Option 1: External Secrets Operator

Use the External Secrets Operator to inject secrets from a secret manager:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: app-secrets
  data:
    - secretKey: postgres-password
      remoteRef:
        key: database/creds
        property: password
```

### Option 2: SOPS Encrypted Values

Encrypt sensitive values file:

```bash
# Install SOPS
brew installmozilla/sops/sops

# Create encrypted values file
sops -e values.yaml > values.encrypted.yaml

# Decrypt for deployment
sops -d values.encrypted.yaml > values.yaml
```

### Option 3: Kubernetes Secrets

Create secrets manually:

```bash
kubectl create secret generic app-secrets \
  --from-literal=postgres-password='your-secure-password' \
  --from-literal=redis-password='your-secure-password'
```

## Reference

- [SOPS Migration Guide](./deployment/SOPS_MIGRATION_GUIDE.md)
- [Security Audit Report](../wiki_pages/SECURITY_AUDIT_REPORT.md)
- [External Secrets Operator](https://external-secrets.io/)
