# Branch Templates Directory

This directory contains ready-to-use Ansible playbooks for different deployment scenarios. Each file represents a different use case and can be used as a template for creating profile branches. All templates build upon the base functionality provided in the main project.

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

## Usage

To use any of these templates, copy the appropriate template to your own deployment directory (separate from this repository):

1. Create your own deployment directory
2. Copy the appropriate template to your deployment directory
3. Customize the variables as needed for your specific requirements
4. Ensure you have access to the roles from the main repository (set ANSIBLE_ROLES_PATH or use --extra-vars)
5. Test thoroughly before deploying to production

Example:
```bash
# Create your own deployment directory (separate from the main repo)
mkdir my-production-deployment && cd my-production-deployment

# Copy the template to your deployment directory
cp /path/to/deploy-system-unified/branch_templates/production_servers.yml site.yml

# Customize site.yml for your specific needs

# Run the deployment with access to the roles from the main repository
ansible-playbook -i inventory/your-server.ini site.yml --extra-vars "ansible_roles_path=/path/to/deploy-system-unified/roles"
```

Each template includes:
- Core system setup
- Security hardening appropriate for the use case
- Container runtime setup (Podman)
- Container configuration (Quadlet)
- Caddy reverse proxy with automatic HTTPS
- SSH and access configuration
- Additional security measures as appropriate for the use case