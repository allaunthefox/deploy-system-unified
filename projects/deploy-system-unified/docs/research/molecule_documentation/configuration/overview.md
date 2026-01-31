# Molecule Configuration
## Molecule.yml Structure
The main configuration file for Molecule is `molecule.yml`. It defines how Molecule should test your Ansible roles.

## Main Configuration Sections
### Dependency
Configures dependency management for roles and collections:
```yaml
dependency:
  name: galaxy
  enabled: true
  options:
    role-file: requirements.yml
    requirements-file: requirements.yml
```

### Driver
Defines the platform where instances will be created:
```yaml
driver:
  name: docker
  # or podman, vagrant, ec2, gce, azure, etc.
```
### Platforms
Defines the operating systems to test on:
```yaml
platforms:
  - name: instance
    image: geerlingguy/docker-ubuntu2004-ansible
    pre_build_image: true
```

### Provisioner
Configures how Ansible will be used:
```yaml
provisioner:
  name: ansible
  config_options:
    defaults:
      stdout_callback: yaml
  playbooks:
    converge: ${MOLECULE_PLAYBOOK:-playbook.yml}
```
### Verifier
Configures how tests will be run:
```yaml
verifier:
  name: testinfra
  directory: ../tests
```

## Scenario Configuration
Different test scenarios can be configured in separate directories:
```
molecule/
├── default/
│   └── molecule.yml
├── centos/
│   └── molecule.yml
└── integration/
    └── molecule.yml
```
## Common Configuration Options

### Driver Options
- `name`: Platform driver (docker, podman, vagrant, etc.)
- `options`: Driver-specific options
- `volumes`: Volume mounts for containers
- `tmpfs`: Temporary file systems
### Platform Options
- `name`: Instance name
- `image`: Base image for container/vm
- `hostname`: Hostname for the instance
- `groups`: Groups to assign the instance to
- `children`: Child groups to assign

### Provisioner Options
- `name`: Provisioner name (usually ansible)
- `config_options`: Ansible configuration options
- `playbooks`: Custom playbook paths
- `inventory`: Custom inventory options
- `env`: Environment variables
### Verifier Options
- `name`: Verifier name (testinfra, goss, inspec, etc.)
- `options`: Verifier-specific options
- `directory`: Test directory location
- `additional_files_or_dirs`: Additional test files

## Environment Variables
Molecule supports environment variables in configuration:
- `${MOLECULE_EPHEMERAL_DIRECTORY}`
- `${MOLECULE_INSTANCE_NAME}`
- `${MOLECULE_SCENARIO_DIRECTORY}`
- `${MOLECULE_PLAYBOOK}`
