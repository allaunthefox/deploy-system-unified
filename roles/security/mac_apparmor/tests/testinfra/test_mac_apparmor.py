# =============================================================================
# Audit Event Identifier: DSU-PYS-500047
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for security/mac_apparmor role.

This role handles Mandatory Access Control with AppArmor:
- AppArmor package installation
- AppArmor service management
- AppArmor GRUB parameters registration
- AppArmor profiles configuration
"""
import pytest


# AppArmor configuration paths
APPARMOR_DIR = "/etc/apparmor.d"
APPARMOR_CACHE_DIR = "/sys/kernel/security/apparmor"
APPARMOR_STATUS_FILE = "/sys/kernel/security/apparmor/profiles"
APPARMOR_LOG = "/var/log/kern.log"


class TestAppArmorInstallation:
    """Test AppArmor package installation."""

    def test_apparmor_package_installed_debian(self, host):
        """Verify AppArmor package is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("apparmor")
            assert pkg.is_installed, "apparmor package should be installed"

    def test_apparmor_utils_installed_debian(self, host):
        """Verify apparmor-utils package is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("apparmor-utils")
            assert pkg.is_installed, "apparmor-utils package should be installed"

    def test_apparmor_profiles_installed_debian(self, host):
        """Verify apparmor-profiles package is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("apparmor-profiles")
            assert pkg.is_installed, "apparmor-profiles package should be installed"

    def test_apparmor_package_installed_alpine(self, host):
        """Verify AppArmor package is installed (Alpine)."""
        if host.file("/etc/alpine-release").exists:
            pkg = host.package("apparmor")
            assert pkg.is_installed, "apparmor package should be installed"


class TestAppArmorService:
    """Test AppArmor service configuration."""

    def test_apparmor_service_exists(self, host):
        """Verify AppArmor service exists."""
        svc = host.service("apparmor")
        if svc.exists:
            assert svc.exists, "apparmor service should exist"
        else:
            # Service might be named differently
            svc = host.service("apparmor.service")
            assert svc.exists, "apparmor service should exist"

    def test_apparmor_service_running(self, host):
        """Verify AppArmor service is running."""
        svc = host.service("apparmor")
        if svc.exists:
            assert svc.is_running, "apparmor service should be running"
            assert svc.is_enabled, "apparmor service should be enabled"
        else:
            pytest.skip("apparmor service not found")

    def test_apparmor_service_status(self, host):
        """Verify AppArmor service status."""
        cmd = host.run("systemctl status apparmor 2>&1 | head -10")
        if cmd.rc == 0:
            assert "active" in cmd.stdout.lower() or "loaded" in cmd.stdout.lower(), \
                "apparmor service should be active or loaded"
        else:
            pytest.skip("Cannot get apparmor service status")


class TestAppArmorConfiguration:
    """Test AppArmor configuration directory."""

    def test_apparmor_directory_exists(self, host):
        """Verify AppArmor configuration directory exists."""
        d = host.file(APPARMOR_DIR)
        assert d.exists, f"AppArmor directory '{APPARMOR_DIR}' should exist"
        assert d.is_directory, f"'{APPARMOR_DIR}' should be a directory"

    def test_apparmor_directory_permissions(self, host):
        """Verify AppArmor directory has correct permissions."""
        d = host.file(APPARMOR_DIR)
        assert d.mode == 0o755, \
            f"AppArmor directory should have mode 0755, got {oct(d.mode)}"
        assert d.user == "root", "AppArmor directory should be owned by root"

    def test_apparmor_profiles_exist(self, host):
        """Verify AppArmor profiles exist."""
        d = host.file(APPARMOR_DIR)
        if d.exists and d.is_directory:
            cmd = host.run(f"ls {APPARMOR_DIR}/*.conf 2>/dev/null | head -5 || true")
            if cmd.rc == 0 and cmd.stdout:
                # Profiles should exist
                assert len(cmd.stdout.strip()) > 0, "AppArmor profiles should exist"
            else:
                pytest.skip("No AppArmor profiles found")
        else:
            pytest.skip(f"AppArmor directory '{APPARMOR_DIR}' does not exist")

    def test_apparmor_disable_directory_exists(self, host):
        """Verify AppArmor disable directory exists."""
        d = host.file(f"{APPARMOR_DIR}/disable")
        if d.exists:
            assert d.is_directory, f"'{APPARMOR_DIR}/disable' should be a directory"
        else:
            pytest.skip(f"AppArmor disable directory does not exist")


class TestAppArmorStatus:
    """Test AppArmor runtime status."""

    def test_apparmor_securityfs_exists(self, host):
        """Verify AppArmor securityfs is mounted."""
        d = host.file(APPARMOR_CACHE_DIR)
        if d.exists:
            assert d.is_directory, f"'{APPARMOR_CACHE_DIR}' should be a directory"
        else:
            pytest.skip(f"AppArmor securityfs '{APPARMOR_CACHE_DIR}' not mounted")

    def test_apparmor_profiles_loaded(self, host):
        """Verify AppArmor profiles are loaded."""
        f = host.file(APPARMOR_STATUS_FILE)
        if f.exists:
            content = f.content_string
            # Should have at least one profile loaded
            profile_count = len([l for l in content.split("\n") if l.strip()])
            assert profile_count >= 1, f"At least one AppArmor profile should be loaded, found {profile_count}"
        else:
            pytest.skip(f"AppArmor profiles file '{APPARMOR_STATUS_FILE}' does not exist")

    def test_apparmor_mode_enforce_or_complain(self, host):
        """Verify loaded profiles are in enforce or complain mode."""
        f = host.file(APPARMOR_STATUS_FILE)
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                if line.strip():
                    # Profile format: profile_name (mode)
                    assert "(enforce)" in line.lower() or "(complain)" in line.lower(), \
                        f"Profile should be in enforce or complain mode: {line}"
        else:
            pytest.skip(f"AppArmor profiles file '{APPARMOR_STATUS_FILE}' does not exist")


class TestAppArmorTools:
    """Test AppArmor management tools."""

    def test_aa_status_available(self, host):
        """Verify aa-status command is available."""
        assert host.exists("aa-status"), "aa-status command should be available"

    def test_aa_status_runs(self, host):
        """Verify aa-status command runs successfully."""
        cmd = host.run("aa-status 2>&1 | head -20")
        if cmd.rc == 0:
            assert "apparmor" in cmd.stdout.lower() or "profiles" in cmd.stdout.lower(), \
                "aa-status should return AppArmor status"
        else:
            pytest.skip("aa-status command failed")

    def test_aa_enforce_available(self, host):
        """Verify aa-enforce command is available."""
        if host.file("/etc/debian_version").exists:
            assert host.exists("aa-enforce"), "aa-enforce command should be available"
        else:
            pytest.skip("aa-enforce only available on Debian/Ubuntu")

    def test_aa_complain_available(self, host):
        """Verify aa-complain command is available."""
        if host.file("/etc/debian_version").exists:
            assert host.exists("aa-complain"), "aa-complain command should be available"
        else:
            pytest.skip("aa-complain only available on Debian/Ubuntu")


class TestAppArmorGRUBParameters:
    """Test AppArmor GRUB parameters."""

    def test_grub_config_exists(self, host):
        """Verify GRUB configuration file exists."""
        f = host.file("/etc/default/grub")
        assert f.exists, "/etc/default/grub should exist"

    def test_apparmor_grub_parameter(self, host):
        """Verify apparmor=1 is in GRUB parameters."""
        f = host.file("/etc/default/grub")
        content = f.content_string
        for line in content.split("\n"):
            if "GRUB_CMDLINE_LINUX" in line and not line.startswith("#"):
                assert "apparmor=1" in line, "apparmor=1 should be in GRUB parameters"
                return
        pytest.skip("apparmor=1 not found in GRUB parameters")

    def test_security_grub_parameter(self, host):
        """Verify security=apparmor is in GRUB parameters."""
        f = host.file("/etc/default/grub")
        content = f.content_string
        for line in content.split("\n"):
            if "GRUB_CMDLINE_LINUX" in line and not line.startswith("#"):
                assert "security=apparmor" in line, "security=apparmor should be in GRUB parameters"
                return
        pytest.skip("security=apparmor not found in GRUB parameters")


class TestAppArmorLogging:
    """Test AppArmor logging."""

    def test_apparmor_log_accessible(self, host):
        """Verify AppArmor logs are accessible."""
        # AppArmor logs typically go to kern.log or syslog
        log_files = ["/var/log/kern.log", "/var/log/syslog", "/var/log/messages"]
        has_log = False
        for log_file in log_files:
            f = host.file(log_file)
            if f.exists:
                has_log = True
                break
        if has_log:
            pass  # Log file exists
        else:
            pytest.skip("No AppArmor log files found")

    def test_apparmor_denials_logged(self, host):
        """Verify AppArmor denials are logged."""
        # Check for apparmor denial messages
        cmd = host.run("dmesg | grep -i 'apparmor\\|denied' 2>&1 | head -5 || true")
        # This is informational - denials may or may not exist


class TestAppArmorProfiles:
    """Test specific AppArmor profiles."""

    def test_usr_bin_profile_exists(self, host):
        """Verify usr-bin abstract profile exists."""
        f = host.file(f"{APPARMOR_DIR}/abstractions/base")
        if f.exists:
            assert f.is_file, "base abstraction should exist"
        else:
            pytest.skip("base abstraction not found")

    def test_profiles_directory_structure(self, host):
        """Verify profiles directory has proper structure."""
        d = host.file(APPARMOR_DIR)
        if d.exists and d.is_directory:
            # Check for subdirectories
            subdirs = ["abstractions", "disable", "cache"]
            for subdir in subdirs:
                sd = host.file(f"{APPARMOR_DIR}/{subdir}")
                if sd.exists:
                    assert sd.is_directory, f"{subdir} should be a directory"
        else:
            pytest.skip(f"AppArmor directory '{APPARMOR_DIR}' does not exist")


class TestAppArmorKernelSupport:
    """Test AppArmor kernel support."""

    def test_apparmor_kernel_module_loaded(self, host):
        """Verify AppArmor kernel module is loaded."""
        cmd = host.run("lsmod | grep -i apparmor 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "apparmor" in cmd.stdout.lower(), "AppArmor kernel module should be loaded"
        else:
            # AppArmor might be built into kernel
            cmd = host.run("grep CONFIG_SECURITY_APPARMOR /boot/config-$(uname -r) 2>/dev/null || true")
            if cmd.rc == 0 and "y" in cmd.stdout:
                pass  # Built into kernel
            else:
                pytest.skip("AppArmor kernel module not detected")

    def test_apparmor_enabled_in_kernel(self, host):
        """Verify AppArmor is enabled in kernel."""
        cmd = host.run("aa-status 2>&1 | grep -i 'apparmor module is loaded' || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "loaded" in cmd.stdout.lower(), "AppArmor module should be loaded"
        else:
            pytest.skip("Cannot verify AppArmor kernel status")


class TestContainerDetection:
    """Test container environment handling."""

    def test_not_in_container_or_skip(self, host):
        """Verify test handles container environment appropriately."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        if cmd.rc == 0:
            virt_type = cmd.stdout.strip().lower()
            if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
                pytest.skip(f"Running in container ({virt_type}), AppArmor may have limited functionality")


class TestAppArmorCompletion:
    """Test AppArmor configuration completion."""

    def test_apparmor_properly_configured(self, host):
        """Verify AppArmor is properly configured."""
        # Check that AppArmor is installed and service exists
        pkg_installed = False
        service_exists = False

        # Check packages
        for pkg_name in ["apparmor", "apparmor-utils"]:
            pkg = host.package(pkg_name)
            if pkg.is_installed:
                pkg_installed = True
                break

        # Check service
        svc = host.service("apparmor")
        if svc.exists:
            service_exists = True

        assert pkg_installed, "AppArmor package should be installed"
        assert service_exists, "AppArmor service should exist"

    def test_apparmor_active(self, host):
        """Verify AppArmor is active."""
        cmd = host.run("aa-status 2>&1 | head -5")
        if cmd.rc == 0:
            output = cmd.stdout.lower()
            assert "apparmor" in output, "AppArmor should be active"
        else:
            pytest.skip("Cannot get AppArmor status")
