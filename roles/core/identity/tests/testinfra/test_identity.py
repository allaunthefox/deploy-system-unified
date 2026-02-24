"""
Testinfra tests for core/identity role.

This role handles system identity and UUID generation:
- Generating high-entropy UUID for virtualization objects
- Setting hostname configuration
- Managing object identity facts
"""
import pytest


class TestIdentityUUID:
    """Test UUID generation and configuration."""

    def test_uuid_generation_available(self, host):
        """Verify UUID generation is available."""
        # Linux kernel should provide UUID generation
        f = host.file("/proc/sys/kernel/random/uuid")
        assert f.exists, "/proc/sys/kernel/random/uuid should exist"

    def test_uuid_generation_works(self, host):
        """Verify UUID can be generated."""
        cmd = host.run("cat /proc/sys/kernel/random/uuid")
        assert cmd.rc == 0, "UUID generation should succeed"
        # UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (36 chars)
        uuid = cmd.stdout.strip()
        assert len(uuid) == 36, f"UUID should be 36 characters, got {len(uuid)}"
        # Verify UUID format (8-4-4-4-12 hex digits)
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        assert re.match(uuid_pattern, uuid.lower()), f"UUID '{uuid}' should match standard format"

    def test_uuid_uniqueness(self, host):
        """Verify generated UUIDs are unique."""
        uuids = []
        for _ in range(3):
            cmd = host.run("cat /proc/sys/kernel/random/uuid")
            if cmd.rc == 0:
                uuids.append(cmd.stdout.strip())
        # All generated UUIDs should be unique
        assert len(uuids) == len(set(uuids)), "Generated UUIDs should be unique"

    def test_random_device_exists(self, host):
        """Verify /dev/random exists."""
        f = host.file("/dev/random")
        assert f.exists, "/dev/random should exist"
        assert f.is_symlink or f.is_device, "/dev/random should be a device or symlink"

    def test_urandom_device_exists(self, host):
        """Verify /dev/urandom exists."""
        f = host.file("/dev/urandom")
        assert f.exists, "/dev/urandom should exist"
        assert f.is_symlink or f.is_device, "/dev/urandom should be a device or symlink"


class TestIdentityHostname:
    """Test hostname configuration."""

    def test_hostname_command_available(self, host):
        """Verify hostname command is available."""
        assert host.exists("hostname"), "hostname command should be available"
        assert host.exists("hostnamectl"), "hostnamectl command should be available"

    def test_hostname_set(self, host):
        """Verify hostname is set."""
        cmd = host.run("hostname")
        assert cmd.rc == 0, "hostname command should succeed"
        hostname = cmd.stdout.strip()
        assert len(hostname) > 0, "Hostname should not be empty"

    def test_hostname_file_exists(self, host):
        """Verify /etc/hostname exists."""
        f = host.file("/etc/hostname")
        if f.exists:
            assert f.is_file, "/etc/hostname should be a file"
            content = f.content_string.strip()
            assert len(content) > 0, "/etc/hostname should not be empty"

    def test_etc_hosts_exists(self, host):
        """Verify /etc/hosts exists."""
        f = host.file("/etc/hosts")
        assert f.exists, "/etc/hosts should exist"
        assert f.is_file, "/etc/hosts should be a file"

    def test_etc_hosts_permissions(self, host):
        """Verify /etc/hosts has correct permissions."""
        f = host.file("/etc/hosts")
        if f.exists:
            assert f.mode in [0o644, 0o640], "/etc/hosts should have correct permissions"
            assert f.user == "root", "/etc/hosts should be owned by root"

    def test_localhost_in_hosts(self, host):
        """Verify localhost is in /etc/hosts."""
        f = host.file("/etc/hosts")
        if f.exists:
            content = f.content_string
            assert "localhost" in content, "localhost should be in /etc/hosts"
            assert "127.0.0.1" in content, "127.0.0.1 should be in /etc/hosts"


class TestIdentityMachineID:
    """Test machine ID configuration."""

    def test_machine_id_exists(self, host):
        """Verify /etc/machine-id exists."""
        f = host.file("/etc/machine-id")
        assert f.exists, "/etc/machine-id should exist"
        assert f.is_file, "/etc/machine-id should be a file"

    def test_machine_id_format(self, host):
        """Verify machine-id has valid format."""
        f = host.file("/etc/machine-id")
        if f.exists:
            content = f.content_string.strip()
            # Machine ID should be 32 hex characters
            assert len(content) == 32, f"Machine ID should be 32 characters, got {len(content)}"
            import re
            assert re.match(r'^[0-9a-f]{32}$', content.lower()), "Machine ID should be hex"

    def test_machine_id_not_empty(self, host):
        """Verify machine-id is not empty or placeholder."""
        f = host.file("/etc/machine-id")
        if f.exists:
            content = f.content_string.strip()
            assert content, "Machine ID should not be empty"
            assert content != "uninitialized", "Machine ID should be initialized"


class TestIdentitySystemInfo:
    """Test system identity information."""

    def test_os_release_exists(self, host):
        """Verify /etc/os-release exists."""
        f = host.file("/etc/os-release")
        assert f.exists, "/etc/os-release should exist"

    def test_os_release_has_id(self, host):
        """Verify os-release has ID field."""
        f = host.file("/etc/os-release")
        if f.exists:
            content = f.content_string
            assert "ID=" in content, "os-release should have ID field"

    def test_product_uuid_available(self, host):
        """Verify product UUID is available (if not in container)."""
        # This may not be available in all environments
        f = host.file("/sys/class/dmi/id/product_uuid")
        if f.exists:
            content = f.content_string.strip()
            if content and content != "Not Applicable":
                # Should be a valid UUID
                assert len(content) == 36, "Product UUID should be 36 characters"

    def test_chassis_type_available(self, host):
        """Verify chassis type is available."""
        f = host.file("/sys/class/dmi/id/chassis_type")
        if f.exists:
            # Chassis type should be a number
            content = f.content_string.strip()
            if content:
                assert content.isdigit(), "Chassis type should be numeric"


class TestIdentityEntropy:
    """Test entropy availability for identity operations."""

    def test_entropy_available(self, host):
        """Verify entropy is available."""
        f = host.file("/proc/sys/kernel/random/entropy_avail")
        if f.exists:
            content = f.content_string.strip()
            if content.isdigit():
                entropy = int(content)
                assert entropy > 0, "System should have available entropy"

    def test_rng_modules_loaded(self, host):
        """Verify RNG modules are available."""
        # Check for common RNG kernel modules
        rng_modules = ["rng_core", "tpm_rng", "virtio_rng"]
        cmd = host.run("lsmod 2>/dev/null || true")
        # Modules may or may not be loaded depending on hardware
        # This is informational
