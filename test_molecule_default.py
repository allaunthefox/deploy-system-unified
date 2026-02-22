#!/usr/bin/env python3
"""
Tests for Molecule default scenario configuration.

This test module validates that the default scenario is properly configured
with Ansible-Native format and all required files exist.

Args:
    None

Returns:
    int: 0 on success, 1 on failure

Example:
    python test_molecule_default.py
"""

import os
import yaml
import pytest


# Base path for molecule default scenario
MOLECULE_DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__),
    "deploy-system-unified",
    "molecule",
    "default"
)


def test_molecule_default_directory_exists():
    """Test that the default scenario directory exists."""
    assert os.path.isdir(MOLECULE_DEFAULT_PATH), \
        f"Molecule default directory should exist at {MOLECULE_DEFAULT_PATH}"


def test_molecule_yml_exists():
    """Test that molecule.yml exists."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    assert os.path.isfile(molecule_yml), \
        f"molecule.yml should exist at {molecule_yml}"


def test_molecule_yml_is_valid_yaml():
    """Test that molecule.yml is valid YAML."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    with open(molecule_yml, 'r') as f:
        config = yaml.safe_load(f)
    assert config is not None, "molecule.yml should be valid YAML"


def test_molecule_yml_has_ansible_section():
    """Test that molecule.yml has ansible section (Ansible-Native format)."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    with open(molecule_yml, 'r') as f:
        config = yaml.safe_load(f)
    assert 'ansible' in config, \
        "molecule.yml should have 'ansible' section for Ansible-Native format"


def test_molecule_yml_has_executor():
    """Test that molecule.yml has executor defined."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    with open(molecule_yml, 'r') as f:
        config = yaml.safe_load(f)
    assert 'executor' in config['ansible'], \
        "ansible.executor should be defined"
    assert 'backend' in config['ansible']['executor'], \
        "ansible.executor.backend should be defined"


def test_molecule_yml_has_test_sequence():
    """Test that molecule.yml has scenario.test_sequence defined."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    with open(molecule_yml, 'r') as f:
        config = yaml.safe_load(f)
    assert 'scenario' in config, \
        "molecule.yml should have 'scenario' section"
    assert 'test_sequence' in config['scenario'], \
        "scenario.test_sequence should be defined"


def test_molecule_yml_has_verifier():
    """Test that molecule.yml has verifier defined."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    with open(molecule_yml, 'r') as f:
        config = yaml.safe_load(f)
    assert 'verifier' in config, \
        "molecule.yml should have 'verifier' section"


def test_create_yml_exists():
    """Test that create.yml exists."""
    create_yml = os.path.join(MOLECULE_DEFAULT_PATH, "create.yml")
    assert os.path.isfile(create_yml), \
        f"create.yml should exist at {create_yml}"


def test_destroy_yml_exists():
    """Test that destroy.yml exists."""
    destroy_yml = os.path.join(MOLECULE_DEFAULT_PATH, "destroy.yml")
    assert os.path.isfile(destroy_yml), \
        f"destroy.yml should exist at {destroy_yml}"


def test_converge_yml_exists():
    """Test that converge.yml exists."""
    converge_yml = os.path.join(MOLECULE_DEFAULT_PATH, "converge.yml")
    assert os.path.isfile(converge_yml), \
        f"converge.yml should exist at {converge_yml}"


def test_prepare_yml_exists():
    """Test that prepare.yml exists."""
    prepare_yml = os.path.join(MOLECULE_DEFAULT_PATH, "prepare.yml")
    assert os.path.isfile(prepare_yml), \
        f"prepare.yml should exist at {prepare_yml}"


def test_verify_yml_exists():
    """Test that verify.yml exists."""
    verify_yml = os.path.join(MOLECULE_DEFAULT_PATH, "verify.yml")
    assert os.path.isfile(verify_yml), \
        f"verify.yml should exist at {verify_yml}"


def test_inventory_directory_exists():
    """Test that inventory directory exists."""
    inventory_dir = os.path.join(MOLECULE_DEFAULT_PATH, "inventory")
    assert os.path.isdir(inventory_dir), \
        f"inventory directory should exist at {inventory_dir}"


def test_inventory_hosts_yml_exists():
    """Test that inventory/hosts.yml exists."""
    hosts_yml = os.path.join(MOLECULE_DEFAULT_PATH, "inventory", "hosts.yml")
    assert os.path.isfile(hosts_yml), \
        f"inventory/hosts.yml should exist at {hosts_yml}"


def test_create_yml_has_podman_container_task():
    """Test that create.yml uses podman_container module."""
    create_yml = os.path.join(MOLECULE_DEFAULT_PATH, "create.yml")
    with open(create_yml, 'r') as f:
        content = f.read()
    assert 'containers.podman.podman_container' in content, \
        "create.yml should use containers.podman.podman_container module"


def test_destroy_yml_has_podman_container_task():
    """Test that destroy.yml uses podman_container module."""
    destroy_yml = os.path.join(MOLECULE_DEFAULT_PATH, "destroy.yml")
    with open(destroy_yml, 'r') as f:
        content = f.read()
    assert 'containers.podman.podman_container' in content, \
        "destroy.yml should use containers.podman.podman_container module"


def test_molecule_yml_no_driver_section():
    """Test that molecule.yml does NOT have driver section (Ansible-Native)."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    with open(molecule_yml, 'r') as f:
        config = yaml.safe_load(f)
    assert 'driver' not in config, \
        "Ansible-Native format should NOT have 'driver' section"


def test_molecule_yml_no_platforms_section():
    """Test that molecule.yml does NOT have platforms section (Ansible-Native)."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    with open(molecule_yml, 'r') as f:
        config = yaml.safe_load(f)
    assert 'platforms' not in config, \
        "Ansible-Native format should NOT have 'platforms' section"


def test_molecule_yml_no_provisioner_section():
    """Test that molecule.yml does NOT have provisioner section (Ansible-Native)."""
    molecule_yml = os.path.join(MOLECULE_DEFAULT_PATH, "molecule.yml")
    with open(molecule_yml, 'r') as f:
        config = yaml.safe_load(f)
    assert 'provisioner' not in config, \
        "Ansible-Native format should NOT have 'provisioner' section"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
