# Potential Problems When Deploying Profile Combinations

This document identifies potential issues that may arise when deploying combinations of profiles in Deploy-System-Unified and provides recommendations for mitigating them.

## 1. GPU Vendor Mismatch

**Problem**: When using a GPU slicing profile, if the configured `containers_gpu_vendor` does not match the actual GPU vendor detected, deployment will fail or produce unexpected results.

**Example**:

- Using `gpu_slicing_bare_metal.yml` (configured for NVIDIA) on a system with AMD GPU
- MIG (Multi-Instance GPU) enabled for non-NVIDIA GPUs

**Solution**:

- Ensure `containers_gpu_vendor` matches the actual GPU hardware
- Use `containers_gpu_slicing.strategy: "auto"` to automatically detect and configure GPU slicing
- Verify GPU vendor before deployment using `lspci` command

## 2. Role Duplication and Overlapping Functionality

**Problem**: Some roles are imported by multiple branch templates, potentially leading to duplication.

**Example**:

- `base_hardened.yml` and `base_ephemeral.yml` both import many core roles
- GPU-related roles may be included in multiple GPU profiles

**Solution**:

- The project's design ensures idempotent execution - roles should handle duplication correctly
- Use tags to limit role execution if necessary
- Always run the latest version of the style guide enforcement tool to ensure consistency

## 3. Kubernetes Cluster State

**Problem**: Deploying Kubernetes GPU profiles without a properly configured Kubernetes cluster can fail.

**Example**:

- `k8s_gpu_node.yml` or `k8s_gpu_workload.yml` without a running Kubernetes control plane
- Mismatched Kubernetes versions between the control plane and worker nodes

**Solution**:

- Ensure Kubernetes cluster is properly configured before deploying GPU-specific profiles
- Verify kubectl connectivity before running GPU-related playbooks
- Check Kubernetes API server and kubelet status

## 4. GPU Slicing Strategy Incompatibility

**Problem**: Some GPU slicing strategies are not compatible with all GPU types or virtualization environments.

**Example**:

- MIG (Multi-Instance GPU) is only supported on certain NVIDIA GPUs (A100, A30, H100)
- SR-IOV (Single Root I/O Virtualization) requires specific hardware and BIOS support
- Time-slicing may not work correctly with older GPU drivers

**Solution**:

- Refer to the GPU Slicing Planning Document (`Offline_Research/LLM_RESEARCH/planning/GPU_Slicing_Planning_Document.md`)
- Use `auto` strategy to automatically select compatible slicing method
- Verify GPU capabilities before configuring slicing

## 5. Container Runtime Conflicts

**Problem**: Deploying container-related profiles with incompatible runtime configurations.

**Example**:

- Using both Docker and Podman profiles
- Mismatched container runtime versions
- GPU support not properly configured for container runtime

**Solution**:

- The project prioritizes Podman as the default container runtime
- Ensure container runtime is properly installed and configured
- Check that container runtime version matches requirements for GPU support

## 6. Security Hardening Overlaps

**Problem**: Some security roles may have overlapping functionality, potentially leading to conflicts.

**Example**:

- `networking/firewall` and `networking/container_networks` both configure iptables rules
- `security/hardening` and `security/resource_protection` may set overlapping kernel parameters

**Solution**:

- Roles are designed to complement each other, not conflict
- The style guide enforcement tool ensures consistency
- Review `security_audit_report.md` for detailed security configuration

## 7. Ephemeral vs. Persistent Storage

**Problem**: Deploying ephemeral and persistent storage profiles together can cause conflicts.

**Example**:

- `base_ephemeral.yml` creates RAM-backed secrets storage that conflicts with persistent storage profiles
- Secrets stored in RAM-disk will be lost on reboot

**Solution**:

- Avoid combining ephemeral and persistent storage profiles
- If using ephemeral storage, ensure secrets management is properly configured
- Test ephemeral profiles in a controlled environment

## 8. Network Configuration Conflicts

**Problem**: Network-related profiles may set conflicting configuration.

**Example**:

- `networking/virtual` and `networking/container_networks` both configure network interfaces
- `system_ssh_port` variable may be set differently in multiple profiles

**Solution**:

- Define network configuration variables in `group_vars` or `host_vars`
- Avoid setting conflicting variables in multiple branch templates
- Use the `--diff` flag with ansible-playbook to preview changes

## 9. Hardware Compatibility

**Problem**: Some profiles require specific hardware or virtualization capabilities.

**Example**:

- `gpu_slicing_virtual_host.yml` requires VT-d or AMD-Vi for GPU passthrough
- `virtual_hypervisor.yml` requires nested virtualization support

**Solution**:

- Verify hardware requirements before deploying
- Use `preflight` role to check system capabilities
- Refer to the hardware requirements documentation

## 10. Idempotence Issues

**Problem**: Some tasks may not be completely idempotent, leading to unexpected changes on subsequent runs.

**Example**:

- GPU discovery and configuration tasks
- Container runtime setup
- Hardware-specific configuration

**Solution**:

- The project uses idempotent patterns wherever possible
- Test changes in a controlled environment before production deployment
- Use `ansible-playbook --check` to preview changes

## Best Practices for Profile Combinations

1. **Start with base profiles**: Always deploy `base_hardened.yml` or `base_ephemeral.yml` first
2. **Use specific profiles**: Choose the most specific profile for your use case
3. **Test in isolation**: Deploy profiles one at a time in a test environment
4. **Verify compatibility**: Check that selected profiles are compatible with each other
5. **Document changes**: Keep track of profile combinations and their configurations
6. **Run style guide enforcement**: Ensure consistency with `enforce_style_guide.sh`
7. **Check preflight conditions**: Run `preflight` role to verify system capabilities

## Recommended Profile Combinations

1. **Production Container Host**: `base_hardened.yml` + `production_servers.yml`
2. **Development Environment**: `base_hardened.yml` + `development_servers.yml`
3. **GPU Workstation**: `base_hardened.yml` + `gpu_workstations.yml`
4. **Kubernetes GPU Node**: `base_hardened.yml` + `k8s_secure_node.yml` + `k8s_gpu_node.yml`
5. **Ephemeral Sandbox**: `base_ephemeral.yml` + `ephemeral_containers.yml`

Always test profile combinations in a controlled environment before deploying to production.
