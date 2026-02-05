# Architecture and Vendor Profiles

This project favors explicit architecture and vendor selection to avoid accidental x86-only deployments. When a role supports architecture/vendor profiles, set the target explicitly in inventory or branch templates.

## Goals

- Make target CPU architecture explicit in deployments.
- Keep vendor selection explicit for GPU-specific roles.
- Ensure deployment profiles are discoverable and documented.

## GPU Stack (Universal Drivers)

- Profiles live under `roles/hardware/gpu/arch/<arch>/<vendor>/`.
- Set `gpu_stack_arch` to the target architecture (defaults to `ansible_architecture`).
- Set `gpu_stack_vendor` to the GPU vendor (nvidia, amd, intel, mali, adreno, img).

Example:

```yaml
gpu_stack_arch: "aarch64"
gpu_stack_vendor: "nvidia"
```

## GPU Slicing

- Intel model coverage is tracked in `roles/containers/runtime/vars/intel_gpu_models.yml`.
- Prefer explicit vendor selection in container runtime roles.
- Prefer explicit architecture selection when using GPU container roles:
    - `containers_arch_override` for `containers/runtime`
    - `quadlet_arch_override` for `containers/quadlets`

## Guidance

- If a role supports explicit architecture selection, prefer the explicit variable over inferred facts.
- Keep profile lists aligned with the role’s `arch/` structure and supported vendor lists.
