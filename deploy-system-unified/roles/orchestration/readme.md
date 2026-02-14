# Orchestration Role

This role manages higher-level orchestration platforms like Kubernetes.

## Sub-Components

* **k8s_node**: Kubernetes node bootstrapping and joining.

## Usage

```yaml
- name: Join K8s Cluster
  hosts: k8s_workers
  roles:
    - orchestration
```
