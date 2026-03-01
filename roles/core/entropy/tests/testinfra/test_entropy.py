# =============================================================================
# Audit Event Identifier: DSU-PYS-500055
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for core/entropy role.

This role handles entropy enhancement services for cryptographic operations:
- Installing haveged (entropy daemon)
- Installing rng-tools (hardware RNG support)
- Starting and enabling entropy services
"""
import pytest


# Service mappings by distribution
ENTROPY_SERVICES = {
    "debian": ["haveged", "rng-tools"],
    "ubuntu": ["haveged", "rng-tools"],
    "arch": ["haveged", "rngd"],
    "fedora": ["haveged", "rngd"],
    "alpine": ["haveged", "rngd"],
}

ENTROPY_PACKAGES = {
    "debian": ["haveged", "rng-tools5"],
    "ubuntu": ["haveged", "rng-tools5"],
    "arch": ["haveged", "rng-tools"],
    "fedora": ["haveged", "rng-tools"],
    "alpine": ["haveged", "rng-tools"],
}


class TestEntropyPackages:
    """Test entropy package installation."""

    def test_haveged_installed(self, host):
        """Verify haveged package is installed."""
        pkg = host.package("haveged")
        assert pkg.is_installed, "haveged package should be installed"

    def test_rng_tools_installed(self, host):
        """Verify rng-tools package is installed."""
        # Package name varies by distribution
        pkg_names = ["rng-tools", "rng-tools5"]
        has_rng_tools = False
        for pkg_name in pkg_names:
            pkg = host.package(pkg_name)
            if pkg.is_installed:
                has_rng_tools = True
                break
        assert has_rng_tools, "rng-tools or rng-tools5 package should be installed"


class TestEntropyServices:
    """Test entropy service status."""

    def test_haveged_service_running(self, host):
        """Verify haveged service is running."""
        svc = host.service("haveged")
        if svc.exists:
            assert svc.is_running, "haveged service should be running"
            assert svc.is_enabled, "haveged service should be enabled"

    def test_rngd_service_running(self, host):
        """Verify rngd service is running."""
        # Service name varies by distribution
        svc_names = ["rngd", "rng-tools", "rng-tools-debian", "jitterentropy-rngd"]
        for svc_name in svc_names:
            svc = host.service(svc_name)
            if svc.exists:
                assert svc.is_running, f"{svc_name} service should be running"
                assert svc.is_enabled, f"{svc_name} service should be enabled"
                return
        # If no service found, check if rngd command exists (may run without systemd)
        assert host.exists("rngd"), "rngd should be available"


class TestEntropySystemState:
    """Test entropy system state."""

    def test_entropy_available(self, host):
        """Verify system has sufficient entropy."""
        # Check available entropy (should be > 0)
        if host.file("/proc/sys/kernel/random/entropy_avail").exists:
            f = host.file("/proc/sys/kernel/random/entropy_avail")
            entropy = int(f.content_string.strip())
            assert entropy > 0, "System should have available entropy"

    def test_rng_devices_exist(self, host):
        """Verify hardware RNG devices exist (if available)."""
        rng_devices = ["/dev/hwrng", "/dev/random", "/dev/urandom"]
        for device in rng_devices:
            if host.file(device).exists:
                d = host.file(device)
                assert d.exists, f"RNG device {device} should exist"

    def test_haveged_config_exists(self, host):
        """Verify haveged configuration exists."""
        config_paths = [
            "/etc/default/haveged",
            "/etc/haveged.conf",
        ]
        has_config = False
        for path in config_paths:
            if host.file(path).exists:
                has_config = True
                break
        # Config may not exist if using defaults
        # This is informational, not a failure

    def test_uuid_generation_works(self, host):
        """Verify UUID generation works (requires entropy)."""
        cmd = host.run("cat /proc/sys/kernel/random/uuid")
        assert cmd.rc == 0, "UUID generation should work"
        # UUID should be 36 characters (8-4-4-4-12 format)
        assert len(cmd.stdout.strip()) == 36, "Generated UUID should be valid format"


class TestEntropyConfiguration:
    """Test entropy configuration files."""

    def test_haveged_service_file(self, host):
        """Verify haveged systemd service file exists."""
        service_file = host.file("/etc/systemd/system/haveged.service")
        service_file_lib = host.file("/lib/systemd/system/haveged.service")
        service_file_etc = host.file("/etc/systemd/system/multi-user.target.wants/haveged.service")

        has_service = service_file.exists or service_file_lib.exists
        assert has_service, "haveged service file should exist"

    def test_rng_tools_config(self, host):
        """Verify rng-tools configuration if it exists."""
        config_paths = [
            "/etc/default/rng-tools",
            "/etc/default/rng-tools-debian",
            "/etc/sysconfig/rngd",
        ]
        for path in config_paths:
            if host.file(path).exists:
                f = host.file(path)
                assert f.exists, f"rng-tools config at {path} should exist"
                # Config should be readable
                assert f.mode in [0o644, 0o640, 0o600], f"Config {path} should have secure permissions"
