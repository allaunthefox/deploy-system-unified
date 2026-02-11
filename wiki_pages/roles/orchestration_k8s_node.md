# orchestration/k8s_node

**Role Path**: `roles/orchestration/k8s_node`

## Description
Tasks for orchestration/k8s_node - Kubernetes Node Readiness

## Key Tasks
- Disable SWAP (Mandatory for K8s)
- Remove SWAP from fstab
- Load Kubernetes required kernel modules
- Configure sysctl for Kubernetes networking
- Create directory for Kubernetes manifests
- Deploy GPU device plugins

---
*This page was automatically generated from role source code.*