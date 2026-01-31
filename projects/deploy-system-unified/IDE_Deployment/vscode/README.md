# VS Code Profile for Deploy-System-Unified
## Overview

This VS Code profile is specifically designed for working on the Deploy-System-Unified project, an Ansible-based infrastructure as code (IaC) system for managing secure, hardened VPS environments.
## Configuration Files

### 1. settings.json
Contains project-specific VS Code settings:
- **Editor Configuration**: 2-space indentation, format on save, UTF-8 encoding
- **File Exclusions**: Ignores .git, node_modules, dist, build, and venv directories
- **Language-Specific Settings**:
  - YAML: Uses Red Hat YAML extension, 2-space indentation
  - Ansible: Uses Red Hat Ansible extension, 2-space indentation
  - Python: Uses ms-python extension, 2-space indentation, Black formatter
  - Markdown: Uses markdownlint extension
- **Ansible Configuration**: Points to system ansible installation
- **Python Configuration**: Enables pylint, Black formatter, isort
- **Git Integration**: Auto-stash, smart commit, GitLens code lens
- **Copilot Configuration**: Enables GitHub Copilot for all relevant languages
- **Color Theme**: Shades of Purple (installed on server)
### 2. extensions.json
Recommends essential extensions for working on this project:
- Red Hat Ansible Language Server
- Red Hat YAML Language Server
- Microsoft Python Extensions
- Markdown Lint
- GitLens
- GitHub Copilot
- GitHub Actions
- Docker Containers
- GitLab Workflow

### 3. launch.json
Provides debugging configurations:
- **Debug Ansible Playbook**: Debugs any Ansible playbook
- **Debug Ansible Lint**: Runs ansible-lint on a selected file
- **Debug Python Script**: Debugs Python scripts
- **Debug Molecule Test**: Runs Molecule tests for security role
- **Run Playbook: Test Security Role**: Runs the test_security_role.yml
- **Run Playbook: Test SSH Forwarding**: Runs the test_sshd_forwarding.yml
## Key Features

### Ansible Development
- **Language Support**: Syntax highlighting, autocompletion, and validation for Ansible files
- **Linting**: ansible-lint integration with project-specific rules
- **Debugging**: Step-through debugging of Ansible playbooks
- **Playbook Execution**: Quick launch configurations for testing
### Python Development
- **Language Support**: Full Python language support with Pylance
- **Linting**: pylint with custom configuration
- **Formatting**: Black formatter with 160-character line length
- **Imports**: isort integration for import sorting

### Git Integration
- **GitLens**: Enhanced Git capabilities with code lens and current line blame
- **Auto-stash**: Automatically stashes changes when pulling
- **Smart Commit**: Commits all changes with a single message
### Security
- **GitHub Copilot**: AI-assisted code completion (configured for Ansible and Python)
- **YAML Schema Validation**: Validates Ansible files against ansible-lint schemas
- **Vault Support**: Recognizes Ansible Vault (!vault) tags in YAML files

## Usage
1. **Open the Project**: In VS Code, File > Open Folder > select the project directory
2. **Install Recommended Extensions**: VS Code will prompt you to install recommended extensions
3. **Debug Playbooks**: Use the Run and Debug panel to execute debugging configurations
4. **Format on Save**: Changes are automatically formatted on save
5. **Lint on Demand**: Use Command Palette to run ansible-lint or pylint

## System Requirements
- VS Code 1.108.2 or later (installed on server)
- Python 3.14 or later
- Ansible 2.15 or later
- Required extensions (listed in extensions.json)

## Contributing
When making changes to this VS Code profile:
1. Ensure all settings follow the project's style guide
2. Test configurations before committing
3. Update this README if adding new features

## License

MIT
