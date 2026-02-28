#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-TST-1000104
# File Type: Python Test Script
# Test Type: Molecule Configuration Validation
# Description: Tests for Molecule default scenario configuration
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
"""
Tests for Molecule default scenario configuration.

This test module validates that the default scenario is properly configured
with Ansible-Native format and all required files exist.
"""

import unittest
import yaml
from pathlib import Path


# Base path for molecule default scenario (project root relative to tests/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MOLECULE_DEFAULT_PATH = PROJECT_ROOT / "molecule" / "default"


class TestMoleculeDefault(unittest.TestCase):
    """Test Molecule default scenario configuration."""

    def test_molecule_default_directory_exists(self):
        """Test that the default scenario directory exists."""
        self.assertTrue(MOLECULE_DEFAULT_PATH.is_dir(),
                        f"Molecule default directory should exist at {MOLECULE_DEFAULT_PATH}")

    def test_molecule_yml_exists(self):
        """Test that molecule.yml exists."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        self.assertTrue(molecule_yml.is_file(),
                        f"molecule.yml should exist at {molecule_yml}")

    def test_molecule_yml_is_valid_yaml(self):
        """Test that molecule.yml is valid YAML."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        if not molecule_yml.is_file():
            self.skipTest("molecule.yml not found")
        with open(molecule_yml, 'r') as f:
            config = yaml.safe_load(f)
        self.assertIsNotNone(config, "molecule.yml should be valid YAML")

    def test_molecule_yml_has_ansible_section(self):
        """Test that molecule.yml has ansible section (Ansible-Native format)."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        if not molecule_yml.is_file():
            self.skipTest("molecule.yml not found")
        with open(molecule_yml, 'r') as f:
            config = yaml.safe_load(f)
        self.assertIn('ansible', config,
                      "molecule.yml should have 'ansible' section for Ansible-Native format")

    def test_molecule_yml_has_executor(self):
        """Test that molecule.yml has executor defined."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        if not molecule_yml.is_file():
            self.skipTest("molecule.yml not found")
        with open(molecule_yml, 'r') as f:
            config = yaml.safe_load(f)
        self.assertIn('executor', config.get('ansible', {}),
                      "ansible.executor should be defined")
        self.assertIn('backend', config.get('ansible', {}).get('executor', {}),
                      "ansible.executor.backend should be defined")

    def test_molecule_yml_has_test_sequence(self):
        """Test that molecule.yml has scenario.test_sequence defined."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        if not molecule_yml.is_file():
            self.skipTest("molecule.yml not found")
        with open(molecule_yml, 'r') as f:
            config = yaml.safe_load(f)
        self.assertIn('scenario', config,
                      "molecule.yml should have 'scenario' section")
        self.assertIn('test_sequence', config.get('scenario', {}),
                      "scenario.test_sequence should be defined")

    def test_molecule_yml_has_verifier(self):
        """Test that molecule.yml has verifier defined."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        if not molecule_yml.is_file():
            self.skipTest("molecule.yml not found")
        with open(molecule_yml, 'r') as f:
            config = yaml.safe_load(f)
        self.assertIn('verifier', config,
                      "molecule.yml should have 'verifier' section")

    def test_create_yml_exists(self):
        """Test that create.yml exists."""
        create_yml = MOLECULE_DEFAULT_PATH / "create.yml"
        self.assertTrue(create_yml.is_file(),
                        f"create.yml should exist at {create_yml}")

    def test_destroy_yml_exists(self):
        """Test that destroy.yml exists."""
        destroy_yml = MOLECULE_DEFAULT_PATH / "destroy.yml"
        self.assertTrue(destroy_yml.is_file(),
                        f"destroy.yml should exist at {destroy_yml}")

    def test_converge_yml_exists(self):
        """Test that converge.yml exists."""
        converge_yml = MOLECULE_DEFAULT_PATH / "converge.yml"
        self.assertTrue(converge_yml.is_file(),
                        f"converge.yml should exist at {converge_yml}")

    def test_prepare_yml_exists(self):
        """Test that prepare.yml exists."""
        prepare_yml = MOLECULE_DEFAULT_PATH / "prepare.yml"
        self.assertTrue(prepare_yml.is_file(),
                        f"prepare.yml should exist at {prepare_yml}")

    def test_verify_yml_exists(self):
        """Test that verify.yml exists."""
        verify_yml = MOLECULE_DEFAULT_PATH / "verify.yml"
        self.assertTrue(verify_yml.is_file(),
                        f"verify.yml should exist at {verify_yml}")

    def test_inventory_directory_exists(self):
        """Test that inventory directory exists."""
        inventory_dir = MOLECULE_DEFAULT_PATH / "inventory"
        self.assertTrue(inventory_dir.is_dir(),
                        f"inventory directory should exist at {inventory_dir}")

    def test_inventory_hosts_yml_exists(self):
        """Test that inventory/hosts.yml or inventory/hosts exists."""
        inventory_dir = MOLECULE_DEFAULT_PATH / "inventory"
        if not inventory_dir.is_dir():
            self.skipTest("inventory directory not found")
        hosts_yml = inventory_dir / "hosts.yml"
        hosts = inventory_dir / "hosts"
        self.assertTrue(hosts_yml.is_file() or hosts.is_file(),
                        "hosts.yml or hosts should exist in inventory")

    def test_create_yml_has_podman_container_task(self):
        """Test that create.yml uses podman_container module."""
        create_yml = MOLECULE_DEFAULT_PATH / "create.yml"
        if not create_yml.is_file():
            self.skipTest("create.yml not found")
        with open(create_yml, 'r') as f:
            content = f.read()
        self.assertIn('podman_container', content,
                      "create.yml should use podman_container module")

    def test_destroy_yml_has_podman_container_task(self):
        """Test that destroy.yml uses podman_container module."""
        destroy_yml = MOLECULE_DEFAULT_PATH / "destroy.yml"
        if not destroy_yml.is_file():
            self.skipTest("destroy.yml not found")
        with open(destroy_yml, 'r') as f:
            content = f.read()
        self.assertIn('podman_container', content,
                      "destroy.yml should use podman_container module")

    def test_molecule_yml_no_driver_section(self):
        """Test that molecule.yml does NOT have driver section (Ansible-Native)."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        if not molecule_yml.is_file():
            self.skipTest("molecule.yml not found")
        with open(molecule_yml, 'r') as f:
            config = yaml.safe_load(f)
        self.assertNotIn('driver', config,
                         "molecule.yml should NOT have 'driver' section (Ansible-Native)")

    def test_molecule_yml_no_platforms_section(self):
        """Test that molecule.yml does NOT have platforms section (Ansible-Native)."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        if not molecule_yml.is_file():
            self.skipTest("molecule.yml not found")
        with open(molecule_yml, 'r') as f:
            config = yaml.safe_load(f)
        self.assertNotIn('platforms', config,
                         "molecule.yml should NOT have 'platforms' section (Ansible-Native)")

    def test_molecule_yml_no_provisioner_section(self):
        """Test that molecule.yml does NOT have provisioner section (Ansible-Native)."""
        molecule_yml = MOLECULE_DEFAULT_PATH / "molecule.yml"
        if not molecule_yml.is_file():
            self.skipTest("molecule.yml not found")
        with open(molecule_yml, 'r') as f:
            config = yaml.safe_load(f)
        self.assertNotIn('provisioner', config,
                         "molecule.yml should NOT have 'provisioner' section (Ansible-Native)")


if __name__ == '__main__':
    unittest.main()
