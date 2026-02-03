# Molecule Getting Started

## Overview

Molecule is a tool that aids in the development and testing of Ansible roles. It automates the process of testing roles across multiple instances, operating systems, and distributions.

## Installation

Install Molecule using pip:

```bash
pip install molecule
```

## Basic Commands

- `molecule init`: Initialize a new role or scenario
- `molecule create`: Create instances
- `molecule converge`: Configure instances
- `molecule idempotence`: Test idempotence
- `molecule verify`: Verify instances
- `molecule test`: Run full test sequence
- `molecule destroy`: Destroy instances

## Basic Workflow

1. Create a new role with Molecule: `molecule init role my_role`
2. Write your Ansible tasks in the role
3. Configure molecule.yml for your testing needs
4. Run `molecule test` to execute the full test sequence

## Test Sequence

Molecule executes the following sequence:

1. **Dependency**: Install dependencies
2. **Create**: Create instances
3. **Prepare**: Prepare instances
4. **Converge**: Apply Ansible playbooks
5. **Idempotence**: Test idempotence
6. **Side Effect**: Test side effects
7. **Verify**: Verify the system
8. **Cleanup**: Cleanup instances
9. **Destroy**: Destroy instances

## Configuration

Molecule configuration is stored in `molecule.yml` files. This file defines:

- Driver (platform to test on)
- Platforms (operating systems to test)
- Provisioner (Ansible)
- Verifier (testing framework)
- Scenarios (different test configurations)
