# Production Deployment Runbook
# =============================================================================
# Audit Event Identifier: DSU-RUN-200001
# Document Type: Production Runbook
# Compliance: ISO 27001 §12.4, ISO 27040 §10.2
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Step-by-step guide for deploying to production
# =============================================================================

## Prerequisites

### 1. Infrastructure Requirements

- [ ] Kubernetes cluster (K3s v1.31.4+) with 3+ master nodes and 3+ worker nodes
- [ ] Storage class configured (NFS, Ceph, or cloud provider)
- [ ] Ingress controller installed (Caddy, NGINX, or Traefik)
- [ ] cert-manager installed for TLS certificates
- [ ] SOPS and Age installed for secrets management

### 2. DNS Configuration

Configure DNS records for:
```
monitoring.example.com    -> Load Balancer IP
jellyfin.example.com      -> Load Balancer IP
radarr.example.com        -> Load Balancer IP
sonarr.example.com        -> Load Balancer IP
```

### 3. Secrets Generation

Generate production secrets:

```bash
# Generate SOPS age key
mkdir -p ~/.config/sops/age
age-keygen -o ~/.config/sops/age/keys.txt

# Get the public key
cat ~/.config/sops/age/keys.txt | grep "# public key"

# Update .sops.yaml with the public key
# Edit secrets.sops.template.yaml with production values

# Encrypt secrets
sops -e inventory/group_vars/all/secrets.sops.template.yaml > inventory/group_vars/all/secrets.sops.yml
```

### 4. Generate Production Passwords

```bash
# Grafana Admin Password
export GRAFANA_PASSWORD=$(openssl rand -base64 32)

# PostgreSQL Password
export POSTGRES_PASSWORD=$(openssl rand -base64 32)

# Redis Password
export REDIS_PASSWORD=$(openssl rand -base64 32)

# Authentik Secret Key
export AUTHENTIK_SECRET_KEY=$(openssl rand -base64 64)

# Authentik Admin Password
export AUTHENTIK_PASSWORD=$(openssl rand -base64 32)

# Restic Password
export RESTIC_PASSWORD=$(openssl rand -base64 32)
```

---

## Deployment Steps

### Step 1: Validate Inventory

```bash
cd /home/prod/Workspaces/repos/github/deploy-system-unified

# Validate inventory syntax
ansible-inventory -i inventory/production.ini --list

# Validate connectivity
ansible -i inventory/production.ini all -m ping
```

### Step 2: Validate Secrets

```bash
# Decrypt and validate secrets
sops -d inventory/group_vars/all/secrets.sops.yml | yq eval

# Verify all required secrets are present
sops -d inventory/group_vars/all/secrets.sops.yml | grep -E "password|secret|key" | wc -l
```

### Step 3: Run Preflight Checks

```bash
# Run preflight assertions
ansible-playbook playbooks/preflight_gate.yml -i inventory/production.ini

# Run preflight validation
ansible-playbook playbooks/preflight_gate.yml -i inventory/production.ini
```

### Step 4: Deploy Base Hardening

```bash
# Deploy base hardened infrastructure
ansible-playbook base_hardened.yml -i inventory/production.ini

# Verify deployment
ansible-playbook base_hardened.yml -i inventory/production.ini --tags validate
```

### Step 5: Deploy Kubernetes

```bash
# Deploy Kubernetes infrastructure
ansible-playbook playbooks/deploy_kubernetes.yml -i inventory/production.ini

# Verify cluster
kubectl get nodes
kubectl get pods -A
```

### Step 6: Deploy Helm Charts

```bash
# Deploy all stacks with production values
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini \
  -e persistence_enabled=true \
  -e monitoring_persistence_enabled=true \
  -e media_persistence_enabled=true

# Or deploy individual stacks:
helm install monitoring charts/monitoring-stack -n monitoring \
  -f charts/monitoring-stack/values.production.yaml \
  --set grafana.adminPassword="$GRAFANA_PASSWORD"

helm install media charts/media-stack -n media \
  -f charts/media-stack/values.production.yaml

helm install logging charts/logging-stack -n logging \
  -f charts/logging-stack/values.production.yaml

helm install database charts/database-stack -n database \
  -f charts/database-stack/values.production.yaml \
  --set postgresql.password="$POSTGRES_PASSWORD" \
  --set redis.password="$REDIS_PASSWORD"
```

### Step 7: Deploy Secrets

```bash
# Apply encrypted secrets
sops -d inventory/group_vars/all/secrets.sops.yml | kubectl apply -f -

# Verify secrets
kubectl get secrets -A
```

### Step 8: Validate Deployment

```bash
# Check all pods are running
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

# Check all deployments
kubectl get deployments -A

# Run validation playbook
ansible-playbook deploy_all_stacks.yml -i inventory/production.ini --tags validate
```

### Step 9: Configure TLS

```bash
# If using cert-manager, verify certificates
kubectl get certificates -A

# Check certificate status
kubectl describe certificate monitoring-tls -n monitoring
```

### Step 10: Configure Backup

```bash
# Deploy backup stack
helm install backup charts/backup-stack -n backup \
  -f charts/backup-stack/values.production.yaml \
  --set restic.repository="$RESTIC_REPOSITORY" \
  --set restic.password="$RESTIC_PASSWORD"

# Verify backup cronjob
kubectl get cronjobs -n backup

# Test backup
kubectl create job --from=cronjob/backup-stack-restic manual-backup -n backup
```

---

## Post-Deployment Tasks

### 1. Update DNS Records

Update DNS to point to the load balancer:
```
monitoring.example.com    -> <LOAD_BALANCER_IP>
jellyfin.example.com      -> <LOAD_BALANCER_IP>
radarr.example.com        -> <LOAD_BALANCER_IP>
sonarr.example.com        -> <LOAD_BALANCER_IP>
```

### 2. Configure Alerting

Edit Alertmanager configuration:
```bash
kubectl edit configmap monitoring-monitoring-stack-alertmanager -n monitoring
```

Add notification channels:
- Email
- Slack
- PagerDuty

### 3. Import Grafana Dashboards

Access Grafana at https://monitoring.example.com
- Username: admin
- Password: $GRAFANA_PASSWORD

Import dashboards:
- Kubernetes Cluster Monitoring (ID: 6417)
- Prometheus Overview (ID: 2)
- Node Exporter Full (ID: 1860)

### 4. Configure Jellyfin

Access Jellyfin at https://jellyfin.example.com
- Complete initial setup wizard
- Configure media libraries
- Enable hardware acceleration if available

### 5. Configure Radarr/Sonarr

Access Radarr at https://radarr.example.com
Access Sonarr at https://sonarr.example.com
- Complete initial setup
- Configure download clients
- Configure indexers

---

## Rollback Procedure

### If Deployment Fails

1. **Stop the deployment:**
   ```bash
   # Cancel ansible playbook (Ctrl+C)
   ```

2. **Check what failed:**
   ```bash
   kubectl get events -A --sort-by='.lastTimestamp' | tail -50
   ```

3. **Rollback Helm release:**
   ```bash
   helm rollback <release-name> -n <namespace>
   ```

4. **Delete failed deployment:**
   ```bash
   helm uninstall <release-name> -n <namespace>
   ```

5. **Fix the issue and redeploy**

### Full Cluster Rollback

```bash
# Uninstall all Helm charts
for ns in monitoring media logging database backup auth network proxy ops security; do
  helm list -n $ns -q | xargs -L1 helm uninstall -n $ns
done

# Verify cleanup
kubectl get all -A
```

---

## Monitoring and Maintenance

### Daily Checks

```bash
# Check pod status
kubectl get pods -A

# Check for crashlooping pods
kubectl get pods -A --field-selector=status.phase=Failed

# Check PVC usage
kubectl get pvc -A

# Check node resources
kubectl top nodes
kubectl top pods -A
```

### Weekly Tasks

- [ ] Review backup logs
- [ ] Check certificate expiration
- [ ] Review security alerts
- [ ] Update Grafana dashboards if needed

### Monthly Tasks

- [ ] Review resource usage and adjust limits
- [ ] Update Helm charts to latest versions
- [ ] Review and rotate secrets
- [ ] Test disaster recovery procedure

---

## Troubleshooting

### Common Issues

**Pods stuck in Pending:**
```bash
# Check PVC status
kubectl get pvc -A

# Check storage class
kubectl get storageclass

# Check node resources
kubectl describe node <node-name>
```

**Pods in CrashLoopBackOff:**
```bash
# Check logs
kubectl logs <pod-name> -n <namespace> --tail=100

# Check previous logs
kubectl logs <pod-name> -n <namespace> --previous

# Describe pod for events
kubectl describe pod <pod-name> -n <namespace>
```

**TLS Certificate Issues:**
```bash
# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager

# Check certificate status
kubectl describe certificate <cert-name> -n <namespace>
```

---

## Support Contacts

- **On-call:** oncall@example.com
- **Security Team:** security@example.com
- **Infrastructure Team:** infra@example.com

---

## Document Control

- **Version:** 1.0
- **Last Updated:** 2026-02-28
- **Maintained By:** Infrastructure Team
- **Review Frequency:** Quarterly
