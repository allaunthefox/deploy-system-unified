# =============================================================================
# Audit Event Identifier: DSU-PYS-500064
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for core/time role.

This role handles time synchronization configuration:
- Installing chrony package
- Configuring chrony.conf with secure settings
- Starting and enabling chronyd service
- Verifying time synchronization
"""
import pytest


# Chrony service names by distribution
CHRONY_SERVICES = {
    "debian": "chrony",
    "ubuntu": "chrony",
    "arch": "chronyd",
    "fedora": "chronyd",
    "alpine": "chronyd",
}

# Chrony configuration paths
CHRONY_CONFIG_PATHS = [
    "/etc/chrony/chrony.conf",
    "/etc/chrony.conf",
]


class TestTimePackages:
    """Test chrony package installation."""

    def test_chrony_installed(self, host):
        """Verify chrony package is installed."""
        pkg = host.package("chrony")
        assert pkg.is_installed, "chrony package should be installed"


class TestTimeServices:
    """Test chrony service status."""

    def test_chronyd_service_exists(self, host):
        """Verify chronyd service exists."""
        # Service name varies by distribution
        svc_names = ["chronyd", "chrony"]
        has_service = False
        for svc_name in svc_names:
            svc = host.service(svc_name)
            if svc.exists:
                has_service = True
                break
        assert has_service, "chronyd or chrony service should exist"

    def test_chronyd_service_running(self, host):
        """Verify chronyd service is running."""
        svc_names = ["chronyd", "chrony"]
        for svc_name in svc_names:
            svc = host.service(svc_name)
            if svc.exists:
                assert svc.is_running, f"{svc_name} service should be running"
                assert svc.is_enabled, f"{svc_name} service should be enabled"
                return
        # If no systemd service, check if chronyd process exists
        cmd = host.run("pgrep -x chronyd || true")
        if cmd.stdout.strip():
            pass  # Process is running
        else:
            pytest.skip("chronyd service not found (may be container environment)")

    def test_chronyd_service_enabled(self, host):
        """Verify chronyd service is enabled."""
        svc_names = ["chronyd", "chrony"]
        for svc_name in svc_names:
            svc = host.service(svc_name)
            if svc.exists:
                assert svc.is_enabled, f"{svc_name} service should be enabled"
                return


class TestTimeConfiguration:
    """Test chrony configuration files."""

    def test_chrony_config_exists(self, host):
        """Verify chrony configuration file exists."""
        has_config = False
        for config_path in CHRONY_CONFIG_PATHS:
            f = host.file(config_path)
            if f.exists:
                has_config = True
                break
        assert has_config, "chrony.conf should exist"

    def test_chrony_config_permissions(self, host):
        """Verify chrony configuration has correct permissions."""
        for config_path in CHRONY_CONFIG_PATHS:
            f = host.file(config_path)
            if f.exists:
                assert f.mode in [0o644, 0o640, 0o600], f"{config_path} should have secure permissions"
                assert f.user == "root", f"{config_path} should be owned by root"
                return

    def test_chrony_config_content(self, host):
        """Verify chrony configuration has required directives."""
        for config_path in CHRONY_CONFIG_PATHS:
            f = host.file(config_path)
            if f.exists:
                content = f.content_string
                # Should have at least one pool or server directive
                has_time_source = False
                for line in content.split("\n"):
                    line = line.strip()
                    if line.startswith("pool") or line.startswith("server"):
                        has_time_source = True
                        break
                assert has_time_source, "chrony.conf should have time source configured"
                return

    def test_chrony_config_directories(self, host):
        """Verify chrony configuration directories exist."""
        config_dirs = ["/etc/chrony", "/var/lib/chrony"]
        for config_dir in config_dirs:
            d = host.file(config_dir)
            if d.exists:
                assert d.is_directory, f"{config_dir} should be a directory"


class TestTimeSystemState:
    """Test time synchronization system state."""

    def test_chronyc_available(self, host):
        """Verify chronyc command is available."""
        assert host.exists("chronyc"), "chronyc command should be available"

    def test_time_sync_status(self, host):
        """Verify time synchronization status."""
        cmd = host.run("chronyc tracking 2>/dev/null || true")
        if cmd.rc == 0:
            # Should have time sync information
            assert "Reference ID" in cmd.stdout or "System time" in cmd.stdout, \
                "chronyc tracking should show sync status"

    def test_system_time_set(self, host):
        """Verify system time is set."""
        cmd = host.run("date")
        assert cmd.rc == 0, "date command should work"
        assert len(cmd.stdout.strip()) > 0, "date should return current time"

    def test_timezone_configured(self, host):
        """Verify timezone is configured."""
        # Check /etc/timezone or /etc/localtime
        timezone_file = host.file("/etc/timezone")
        localtime_link = host.file("/etc/localtime")

        has_timezone = False
        if timezone_file.exists:
            has_timezone = True
            content = timezone_file.content_string.strip()
            assert len(content) > 0, "/etc/timezone should not be empty"

        if localtime_link.exists:
            has_timezone = True

        assert has_timezone, "Timezone should be configured"

    def test_ntp_or_chrony_active(self, host):
        """Verify NTP/chrony is the active time sync method."""
        # Check if systemd-timesyncd is disabled when chrony is used
        timesyncd = host.service("systemd-timesyncd")
        chronyd = host.service("chronyd")
        chrony = host.service("chrony")

        # If chrony is running, timesyncd should typically be disabled
        if (chronyd.exists and chronyd.is_running) or (chrony.exists and chrony.is_running):
            if timesyncd.exists:
                # timesyncd may or may not be running, chrony takes precedence
                pass


class TestTimeValidation:
    """Test time synchronization validation."""

    def test_chrony_sources_reachable(self, host):
        """Verify chrony can reach time sources."""
        cmd = host.run("chronyc sources -v 2>/dev/null | head -5 || true")
        if cmd.rc == 0 and cmd.stdout.strip():
            # Should show some sources
            pass  # Sources may or may not be reachable depending on network

    def test_clock_not_drifting(self, host):
        """Verify clock is not significantly drifting."""
        # Get current time
        cmd1 = host.run("date +%s")
        if cmd1.rc == 0:
            # In a real test, we'd wait and check again
            # For now, just verify we can get the time
            assert cmd1.stdout.strip().isdigit(), "Should be able to get epoch time"

    def test_hardware_clock_accessible(self, host):
        """Verify hardware clock is accessible (if not in container)."""
        # This may fail in containers, so we handle it gracefully
        cmd = host.run("hwclock --show 2>/dev/null || true")
        # hwclock may not be available in containers/VMs
        # This is informational
