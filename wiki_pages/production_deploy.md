# production_deploy

The **production_deploy.yml** playbook is the main entry point for all site-wide production deployments. It orchestrates the entire deployment process, ensuring that security gates are passed and configurations are applied consistently across the fleet.

### Canonical Location
- `projects/deploy-system-unified/production_deploy.yml`

### Execution
To run a production deployment, use the following command from the repository root:

```bash
ansible-playbook production_deploy.yml -i inventory/<your_inventory>.ini
```

### Safety Gates
This playbook includes mandatory preflight assertions to verify Vault encryption, SOPS hygiene, and system readiness before any changes are applied.
