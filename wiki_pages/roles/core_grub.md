# core_grub

**role**: `core/grub`

**Centralized Bootloader Management**
Aggregates and applies kernel parameters from various roles into a single GRUB configuration.

## Testing

Molecule scenario: `roles/core/grub/molecule/default`

Behavior:
- Uses the Molecule `default` driver (no container provisioning).
- Uses `/tmp/molecule-grub-default` as a disposable GRUB config file.
- Mocks GRUB handlers with `/tmp/grub-mock-bin` and logs to `/tmp/grub_handler.log`.
- `prepare.yml` clears prior artifacts.
- `side_effect.yml` is a no-op placeholder (no side effects are expected).
- `cleanup.yml` removes artifacts with `become: true` to avoid root-owned leftovers.

Run: `cd roles/core/grub && molecule test`

## Variables

### `core_grub_enabled`
- `core_grub_enabled`

### `core_grub_base_params`
- `core_grub_base_params`

### `core_grub_security_params`
- `core_grub_security_params`

### `core_grub_hardware_params`
- `core_grub_hardware_params`

### `core_grub_isolation_params`
- `core_grub_isolation_params`

### `core_grub_performance_params`
- `core_grub_performance_params`

### `core_grub_extra_params`
- `core_grub_extra_params`

### `core_grub_config_path`
- `core_grub_config_path`

### `core_grub_force_update`
- `core_grub_force_update`
