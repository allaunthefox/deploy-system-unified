# IDE_Deployment - IDE Configuration Profiles
## Overview

This directory contains IDE-specific configuration profiles for working with the Deploy-System-Unified project. Each IDE has its own subdirectory with all necessary settings, extensions, and launch configurations.
## Structure

```
IDE_Deployment/
├── vscode/                  # Visual Studio Code configuration
│   ├── settings.json        # Project-specific VS Code settings
│   ├── extensions.json      # Recommended VS Code extensions
│   ├── launch.json          # VS Code debugging configurations
│   └── README.md            # VS Code profile documentation
└── README.md                # This file - IDE_Deployment overview
```
## Supported IDEs

### 1. Visual Studio Code (vscode/)
The VS Code profile is specifically designed for working on the Deploy-System-Unified project, an Ansible-based infrastructure as code (IaC) system for managing secure, hardened VPS environments.

**Key Features:**
- Syntax highlighting and autocompletion for Ansible, YAML, and Python
- Integrated debugging for Ansible playbooks and Python scripts
- Project-specific linting and formatting configurations
- Recommended extensions for Ansible development
- Git integration with GitLens and GitHub Copilot
**To Use:**
1. Open VS Code
2. File > Open Folder > select the project directory
3. VS Code will automatically detect the configuration in IDE_Deployment/vscode/
4. Install recommended extensions when prompted

## Adding New IDE Profiles
To add a new IDE configuration:
1. Create a new subdirectory with the IDE name (e.g., `intellij/`, `sublime/`)
2. Add all necessary configuration files
3. Create a README.md in the subdirectory explaining how to use the profile
4. Update this overview file with information about the new IDE profile

## Contributing
When modifying IDE configurations:
1. Follow the project's style guide
2. Test configurations before committing
3. Keep configurations focused on project-specific needs
4. Update documentation with any changes

## License

MIT
