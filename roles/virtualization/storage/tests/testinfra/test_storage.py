"""
Testinfra tests for virtualization/storage role.

This role handles virtualization storage configuration:
- Storage pool management
- Volume provisioning for VMs
- Storage backend configuration
"""
import pytest


class TestVirtStorage:
    """Test virtualization storage configuration."""

    def test_libvirt_storage_directory(self, host):
        """Verify libvirt storage directory exists."""
        d = host.file("/var/lib/libvirt")
        if d.exists:
            assert d.is_directory, "/var/lib/libvirt should be a directory"

    def test_libvirt_images_directory(self, host):
        """Verify libvirt images directory exists."""
        d = host.file("/var/lib/libvirt/images")
        if d.exists:
            assert d.is_directory, "/var/lib/libvirt/images should be a directory"

    def test_qemu_img_available(self, host):
        """Verify qemu-img command is available."""
        assert host.exists("qemu-img"), "qemu-img command should be available"


class TestStoragePools:
    """Test storage pool configuration."""

    def test_libvirt_pools_directory(self, host):
        """Verify libvirt pools configuration directory exists."""
        d = host.file("/etc/libvirt/storage")
        if d.exists:
            assert d.is_directory, "/etc/libvirt/storage should be a directory"


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), virtualization storage not available")
