# Deployment Example

This guide shows how to create a deployment using the Deploy-System-Unified templates.

## Step 1: Clone or Access the Repository

First, you need access to the Deploy-System-Unified repository:

```bash
# If cloning:
git clone https://github.com/your-org/deploy-system-unified.git
cd deploy-system-unified
REPO_PATH=$(pwd)
cd ..

# Or if you already have access to the repository:
REPO_PATH="/path/to/deploy-system-unified"
```

## Step 2: Create Your Own Deployment Directory

Create a separate directory for your specific deployment:

```bash
mkdir my-webserver-deployment
cd my-webserver-deployment
```

## Step 3: Copy a Template

Copy the appropriate template for your use case:

```bash
# For a production web server
cp "$REPO_PATH/branch_templates/production_servers.yml" site.yml

# For a development environment
# cp "$REPO_PATH/branch_templates/development_servers.yml" site.yml

# For an ephemeral container environment
# cp "$REPO_PATH/branch_templates/ephemeral_containers.yml" site.yml
```

## Step 4: Customize the Template

Edit the `site.yml` file to customize it for your specific needs:

```bash
# Edit the file to adjust variables, add/remove roles, etc.
vim site.yml
```

For example, you might want to add specific container configurations or modify security settings.

## Step 5: Set Up Inventory

Create your inventory file for the target systems:

```bash
# Create an inventory file
cat > inventory.ini << EOF
[webservers]
your-server.example.com ansible_user=your-user

[webservers:vars]
ansible_python_interpreter=/usr/bin/python3
EOF
```

## Step 6: Run the Deployment

Execute the deployment with access to the roles from the main repository:

```bash
ansible-playbook -i inventory.ini site.yml --extra-vars "ansible_roles_path=$REPO_PATH/roles"
```

Or alternatively, you can set the ANSIBLE_ROLES_PATH environment variable:

```bash
ANSIBLE_ROLES_PATH="$REPO_PATH/roles" ansible-playbook -i inventory.ini site.yml
```

## Important Notes

- The main repository acts as a base layer with common roles and functionality
- Your deployment directory contains only your specific configuration
- This separation ensures clean, modular deployments
- You can have multiple deployment directories for different purposes
- Always test in a safe environment before deploying to production