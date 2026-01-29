# Deploy-System-Unified

Base layer for production-ready infrastructure with customizable deployments. No Kubernetes complexity, no manual systemd configuration, no security guesswork.

## Architecture

This project follows a modular architecture where the main repository serves as a base layer and specific deployments are created in separate directories. See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architectural information.

## Features

- Secure SSH configuration with non-standard port and key-only authentication
- SELinux/AppArmor security policies
- Automatic weekly security updates
- Base system validation and readiness checks
- Foundation for custom deployments via branch templates

## Usage

The main project serves as a base layer. For specific deployments, copy a branch template to your own deployment directory:

```bash
# Create your own deployment directory
mkdir my-deployment && cd my-deployment

# Copy a branch template to your deployment directory
cp /path/to/deploy-system-unified/branch_templates/production_servers.yml site.yml

# Customize as needed
ansible-playbook -i inventory/your-server.ini site.yml --extra-vars "ansible_roles_path=/path/to/deploy-system-unified/roles"

> **Note:** `projects/deploy-system-unified/main.yml` is a pristine base and must **not** contain a top-level `roles:` list. Use templates in `branch_templates/` and copy the desired template to your deployment's `site.yml`. CI enforces this and will reject PRs that add `roles:` to the base playbook.
```

## Branch Templates

This repository includes specialized templates in the `branch_templates/` directory for different use cases:
- `ephemeral_containers.yml` - For temporary, security-focused environments with Podman/Quadlet container management
- `production_servers.yml` - For stable production environments with Podman/Quadlet container management
- `development_servers.yml` - For development and testing environments with Podman/Quadlet container management

Each branch template includes:
- Container runtime setup (Podman)
- Container configuration (Quadlet)
- Caddy reverse proxy with automatic HTTPS
- Appropriate security hardening for the use case

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the GPL-3.0 License - see the `LICENSE` file for details.