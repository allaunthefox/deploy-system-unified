# Advanced Security Hardening Role

This role provides optional advanced security hardening features that can be enabled in profile branches. These features are designed to be optional additions to the standard security configuration and should not affect the main branch functionality.

## Features

### SSH Port Randomization

- Randomizes the SSH port to a value between 10000-65535
- Stores connection information in an encrypted file
- Optionally syncs the encrypted file to a specified destination

### SSH Key Rotation

- Enables automatic rotation of SSH host keys
- Configures rotation interval (default: 90 days)
- Creates backup of old keys before rotation

### TMUX Session Management

- Ensures a persistent TMUX session is available during deployment
- Helps prevent connection loss during configuration changes

## Variables

- `advanced_security_hardening_enabled`: Enable the advanced security hardening features (default: false)
- `ssh_randomize_port`: Enable SSH port randomization (default: false)
- `ssh_random_port_range_start`: Starting port for randomization (default: 10000)
- `ssh_random_port_range_end`: Ending port for randomization (default: 65535)
- `ssh_rsync_destination`: Destination to sync encrypted connection info (optional)
- `ssh_key_rotation_enabled`: Enable SSH key rotation (default: false)
- `ssh_key_rotation_interval_days`: Interval for key rotation in days (default: 90)
- `tmux_session_for_deployment`: Enable TMUX session management (default: true)
- `tmux_session_name`: Name of the TMUX session (default: "deployment-session")
- `encryption_method`: Method to encrypt connection info ('sops' or 'vault', default: 'sops')

## Use Cases

### 1. Ephemeral Docker Containers (Security-First Approach)

**When to use**: Temporary environments where security is paramount but persistence isn't needed
**Examples**: CI/CD runners, security testing environments, temporary compute resources

```yaml
- role: advanced_security_hardening
  vars:
    ssh_randomize_port: true
    ssh_rsync_destination: ""  # No need to save for ephemeral containers
    ssh_key_rotation_enabled: false  # Less critical for short-lived containers
```

### 2. Production Servers (Balanced Approach)

**When to use**: Production environments where both security and stability are critical
**Examples**: Web servers, database servers, application servers

```yaml
- role: advanced_security_hardening
  vars:
    ssh_randomize_port: false  # Avoids complicating monitoring and access
    ssh_key_rotation_enabled: true
    ssh_key_rotation_interval_days: 90
    ssh_rsync_destination: "/secure/storage/location/"
```

### 3. Development Environments (Flexibility Approach)

**When to use**: Development environments where convenience is balanced with basic security
**Examples**: Developer workstations, testing environments, staging systems

```yaml
- role: advanced_security_hardening
  vars:
    advanced_security_hardening_enabled: false  # Skip advanced hardening for convenience
    ssh_randomize_port: false
    ssh_key_rotation_enabled: false
```

## Usage

This role is intended to be used in profile branches as an optional addition to the standard security configuration. To use it, include it in your profile's playbook with the desired variable settings.

## Security Notes

While SSH port randomization adds a layer of obscurity, it does not significantly improve security against determined attackers. The primary security comes from the existing SSH hardening (key-only auth, post-quantum crypto, etc.) which should remain the focus of security efforts.
