# Shared Role

This role contains reusable tasks that can be included in other roles to reduce code duplication.

## Available Tasks

### assertions.yml

Common validation tasks:
- Check required variables are defined
- Verify OS is supported
- Check network connectivity
- Verify package manager availability

Usage:
```yaml
- name: Include shared assertions
  ansible.builtin.include_tasks: roles/shared/tasks/assertions.yml
```

### packages.yml

Cross-platform package installation:
- Debian (apt)
- RedHat (yum/dnf)
- Alpine (apk)
- Arch Linux (pacman)

Usage:
```yaml
- name: Install common packages
  ansible.builtin.include_tasks: roles/shared/tasks/packages.yml
  vars:
    package_name: curl
```

### backup_security.yml

Hash verification and timestamping for all backups:
- Chrony time synchronization check
- SHA256, SHA512, BLAKE3 hash computation
- Hash manifest creation

Usage:
```yaml
- name: Apply backup security
  ansible.builtin.include_tasks: roles/shared/tasks/backup_security.yml
  vars:
    backup_name: "restic-backup"
    backup_source_path: "/path/to/backup"
    backup_security_dir: "/var/backups/security"
```

## Adding Shared Tasks

To add new shared tasks:
1. Create a new file in `tasks/`
2. Document the required variables
3. Add usage examples to this README
