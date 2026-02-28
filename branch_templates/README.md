# Branch Templates Directory

This directory contains reference Ansible playbooks for different deployment scenarios. Each file represents a use case and can be used as a template when you create a separate deployment directory. For production deployments from this repository, use `PRODUCTION_DEPLOY.YML` in the repo root and treat `branch_templates/` as reference-only to avoid drift and preserve determinism.

## Available Templates

1. **ephemeral_containers.yml** - For temporary, security-focused environments
   - Use case: CI/CD runners, security testing, temporary compute
   - Features: SSH port randomization, enhanced security logging, Podman/Quadlet container management, Caddy reverse proxy

2. **production_servers.yml** - For stable production environments
   - Use case: Web servers, databases, application servers
   - Features: SSH key rotation, standard security measures, Podman/Quadlet container management, Caddy reverse proxy

3. **development_servers.yml** - For development and testing environments
   - Use case: Developer workstations, testing, staging
   - Features: Basic security with convenience prioritized, Podman/Quadlet container management, Caddy reverse proxy

4. **gpu_workstations.yml** - For GPU-accelerated environments
   - Use case: AI/ML, data processing, visualization, GPU computing
   - Features: GPU driver installation, container GPU support, CUDA toolkit, optimized system settings, NVIDIA/AMD/Intel GPU profiles
   - Supported GPUs: NVIDIA (CUDA), AMD (ROCm), Intel (OpenCL)

## Usage

If you are deploying directly from this repository, run `PRODUCTION_DEPLOY.YML` instead of copying a template. Use the templates below only when creating a custom deployment directory.

Guidelines:

- `PRODUCTION_DEPLOY.YML` is the canonical entrypoint for real deployments.
- Templates may diverge (tags, optional role ordering) and are not guaranteed to stay in lockstep.
- When you copy a template out-of-tree, treat it as a fork and document your deltas.

To use any of these templates in a separate deployment directory:

1. Create your own deployment directory
2. Copy the appropriate template to your deployment directory
3. Customize the variables as needed for your specific requirements
4. Ensure you have access to the roles from the main repository (set ANSIBLE_ROLES_PATH or use --extra-vars)
5. Test thoroughly before deploying to production
Example (reference-only):

```bash
# Create your own deployment directory (separate from the main repo)
mkdir my-production-deployment && cd my-production-deployment

# Copy the template to your deployment directory
cp /path/to/deploy-system-unified/branch_templates/production_servers.yml SITE.YML
# Customize SITE.YML for your specific needs

# Run the deployment with access to the roles from the main repository
ansible-playbook -i inventory/your-server.ini SITE.YML --extra-vars "ansible_roles_path=/path/to/deploy-system-unified/roles"
```

Each template includes:

- **Quantum-Ready (PQC Hybrid)**: Native support for quantum-resistant key exchange (ML-KEM, sntrup761).
- **ISO 27001 §9.2/10.1 Compliance**: Fully mapped access control and cryptographic tasks.
- Core system setup
- Security hardening appropriate for the use case
- Container runtime setup (Podman)
- Container configuration (Quadlet)
- Caddy reverse proxy with automatic HTTPS
- SSH and access configuration
- Additional security measures as appropriate for the use case
