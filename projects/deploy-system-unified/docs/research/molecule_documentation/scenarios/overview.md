# overview

## Overview

Scenarios in Molecule allow you to test your Ansible roles under different conditions, configurations, or environments. Each scenario represents a unique testing situation.

## Default Scenario

The default scenario is located at `molecule/default/` and contains:

- `molecule.yml`: Configuration for the scenario
- `converge.yml`: Playbook to apply during convergence
- `verify.yml`: Playbook to run during verification
- `destroy.yml`: Playbook to run during destruction (optional)
- `create.yml`: Playbook to run during creation (optional)
- `prepare.yml`: Playbook to run during preparation (optional)

## Creating Custom Scenarios

Custom scenarios can be created using:

```bash
molecule init scenario -r role_name scenario_name
```

## Common Scenario Types

### Platform Scenarios

Test on different operating systems:

- `molecule/ubuntu/`
- `molecule/centos/`
- `molecule/fedora/`
- `molecule/alpine/`

### Configuration Scenarios

Test different configurations:

- `molecule/minimal/`: Minimal configuration
- `molecule/full/`: Full configuration
- `molecule/ha/`: High availability configuration

### Integration Scenarios

Test integration with other services:

- `molecule/integration/`: Integration tests
- `molecule/dependency/`: Dependency testing
- `molecule/api/`: API integration tests

## Scenario Configuration

Each scenario has its own `molecule.yml` file that can override:

- Platforms to test on
- Driver configuration
- Provisioner settings
- Verifier configuration
- Test sequence options

## Running Specific Scenarios

Run a specific scenario with:

```bash
molecule test -s scenario_name
molecule converge -s scenario_name
molecule verify -s scenario_name
```

## Scenario Dependencies

Scenarios can depend on other scenarios:

```yaml
scenario:
  name: dependent_scenario
  parent: base_scenario
```

## Parallel Execution

Multiple scenarios can be run in parallel:

```bash
molecule test --parallel
```

## Scenario Best Practices

- Use descriptive names for scenarios
- Keep scenarios focused on specific testing goals
- Document scenario purposes
- Use consistent directory structure
- Test different configurations and platforms
- Include both positive and negative test cases
- Verify idempotence in each scenario
