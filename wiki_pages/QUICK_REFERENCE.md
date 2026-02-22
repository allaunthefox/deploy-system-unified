# Quick Reference Guide

Quick commands and common tasks for Deploy-System-Unified.

## Running Deployments

```bash
# Full production deployment
ansible-playbook -i inventory/production production_deploy.yml

# Dry run (check mode)
ansible-playbook -i inventory/production production_deploy.yml --check

# Deploy specific stack
ansible-playbook -i inventory/production run_anubis_only.yml

# Local development
ansible-playbook -i inventory/local configure_local_ssh.yml
```

## Testing

```bash
# Run Molecule tests
molecule test -s <scenario_name>

# Run specific scenario
molecule converge -s gpu_slicing
molecule verify -s gpu_slicing

# Precheck Podman access
make molecule-precheck

# Idempotency check
./scripts/verify_idempotence.sh
```

## Common Options

```bash
# Tags
--tags=security      # Run only security roles
--tags=containers    # Run only container roles
--tags=hardware      # Run only hardware roles

# Skip tags
--skip-tags=firewall # Skip firewall configuration

# Limit hosts
--limit=server1      # Run only on specific host
```

## Inventory

```bash
# View inventory
ansible-inventory -i inventory/production --list

# Group hosts
ansible -i inventory/production --list-hosts all
ansible -i inventory/production --list-hosts production
```

## Variables

```bash
# Extra variables
-e "gpu_stack_enable=true"
-e "containers_enable_gpu_support=true"

# Override defaults
-e "@secrets.yml"
```

## Troubleshooting

```bash
# Verbose output
ansible-playbook ... -v       # Verbose
ansible-playbook ... -vv      # More verbose
ansible-playbook ... -vvv    # Debug mode

# Start at specific task
ansible-playbook ... --start-at-task="Setup Docker"

# List tags
ansible-playbook --list-tags
```

## Make Commands

```bash
make help              # Show available targets
make molecule-test     # Run all Molecule tests
make lint              # Run linting
make validate          # Validate YAML files
```

## GPU Commands

```bash
# Discover GPUs
python3 roles/hardware/gpu/files/gpu_discovery.py --json

# Check vendor
python3 roles/hardware/gpu/files/gpu_discovery.py -c nvidia

# Check eGPU
python3 roles/hardware/gpu/files/gpu_discovery.py --egpu-check

# Check RDMA
python3 roles/hardware/gpu/files/gpu_discovery.py --rdma
```

## Container Management

```bash
# List containers
podman ps -a

# View logs
podman logs <container_name>

# Restart service
systemctl restart podman
```

## Links

- [Deployment Guide](UNIVERSAL_DEPLOYMENT_GUIDE)
- [Variable Reference](Variable_Reference)
- [Role Reference](Role_Reference)
