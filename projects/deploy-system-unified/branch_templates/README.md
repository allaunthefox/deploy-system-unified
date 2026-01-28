# Branch Templates Directory

This directory contains ready-to-use Ansible playbooks for different deployment scenarios. Each file represents a different use case and can be used as a template for creating profile branches.

## Available Templates

1. **ephemeral_containers.yml** - For temporary, security-focused environments
   - Use case: CI/CD runners, security testing, temporary compute
   - Features: SSH port randomization, enhanced security logging

2. **production_servers.yml** - For stable production environments
   - Use case: Web servers, databases, application servers
   - Features: SSH key rotation, standard security measures

3. **development_servers.yml** - For development and testing environments
   - Use case: Developer workstations, testing, staging
   - Features: Basic security with convenience prioritized

## Usage

To use any of these templates in a profile branch:

1. Copy the appropriate template to your profile branch
2. Customize the variables as needed for your specific requirements
3. Add any additional roles or tasks specific to your profile
4. Test thoroughly before deploying to production

Example:
```bash
# In your profile branch
cp /path/to/branch_templates/production_servers.yml site.yml
# Then customize site.yml for your specific needs
```