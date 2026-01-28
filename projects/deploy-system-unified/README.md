# Deploy-System-Unified

Set up production-ready container infrastructure with one command. No Kubernetes complexity, no manual systemd configuration, no security guesswork.

## Features

- Secure SSH configuration with non-standard port and key-only authentication
- Podman + Quadlet container management
- Caddy reverse proxy with automatic HTTPS
- SELinux/AppArmor security policies
- Automatic weekly security updates

## Usage

```bash
ansible-playbook -i inventory/your-server.ini site.yml
```

## Branch Templates

This repository includes specialized templates in the `branch_templates/` directory for different use cases:
- `ephemeral_containers.yml` - For temporary, security-focused environments
- `production_servers.yml` - For stable production environments  
- `development_servers.yml` - For development and testing environments

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the GPL-3.0 License - see the `LICENSE` file for details.