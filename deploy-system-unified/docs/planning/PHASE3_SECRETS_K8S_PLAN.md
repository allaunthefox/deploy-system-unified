# PHASE3_SECRETS_K8S_PLAN

**Created:** February 13, 2026  
**Status:** In Progress  
**Scope:** SOPS Secrets Migration, Kubernetes Cluster Integration, and Scalability Benchmarking.

## Purpose

This document outlines the execution plan for Phase 3 of the 2026 Stability and Enhancement Roadmap. The primary goals are to transition from Ansible Vault to SOPS for secret management and to establish a foundational Kubernetes footprint for scalable workloads.

## Current Target Window (Next 2-4 Weeks)

### Target Board

| ID | Target | Status | Required Output | Evidence Path |
| :--- | :--- | :--- | :--- | :--- |
| T1 | SOPS Migration Execution | Pending | Fully migrated `secrets.sops.yml` with Age encryption; Preflight gates updated | `inventory/group_vars/all/secrets.sops.yml` + `playbooks/preflight_assertions.yml` |
| T2 | Kubernetes Prototype Cluster | Pending | Functional K3s/K8s cluster deployed via Ansible; Nodes joined and ready | `roles/kubernetes/master` + `roles/kubernetes/node` |
| T3 | Helm Chart Standardization | Pending | Base Helm charts for core services (Media/Ops) adapting existing Quadlet logic | `charts/media-stack/` + `charts/ops-stack/` |
| T4 | Scalability Benchmark | Pending | Resource utilization metrics for K8s vs. Podman on identical hardware | `docs/benchmarks/k8s_vs_podman_resource_usage.md` |

## In Scope (This Window)

1.  **Secrets Management**:
    *   Execution of the `SOPS_MIGRATION_GUIDE` (Phases 1-6).
    *   Integration of SOPS with Ansible (lookup plugins, vars plugins).
    *   Rotation of initial key material.

2.  **Kubernetes Foundation**:
    *   Development of `kubernetes/master` and `kubernetes/node` roles.
    *   Deployment of a lightweight distribution (k3s or rke2) suited for the edge/hybrid targets.
    *   Basic Ingress controller setup (Traefik or Nginx).

3.  **Workload Portability**:
    *   Translation of selected Quadlet definitions (Media Stack) to Kubernetes Manifests/Helm Charts.

## Out of Scope (This Window)

1.  Full migration of *all* services to Kubernetes (Hybrid state will persist).
2.  Complex Service Mesh implementations (Istio/Linkerd) - focus on basic Ingress first.
3.  Changes to the legacy `deploy-system` repo (focus remains on `deploy-system-unified`).

## Success Criteria (Phase 3)

1.  ✅ Production secrets are managed via SOPS/Age with no unencrypted fallback in the active path.
2.  ✅ A reproducible Ansible playbook exists to deploy a multi-node Kubernetes cluster.
3.  ✅ At least one core stack (e.g., Media or Ops) is successfully running on the K8s cluster.
4.  ✅ Benchmarks provide data-driven guidance on the overhead of K8s for this environment.

## Dependencies and Risks

1.  **Learning Curve**: Operational complexity of K8s vs. Systemd Quadlets.
2.  **Resource Overhead**: K8s control plane usage on smaller nodes.
3.  **Migration Downtime**: Potential service interruption during Secrets cutover.
