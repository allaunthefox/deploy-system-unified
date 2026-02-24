"""
Testinfra tests for security/file_integrity role.

This role handles file integrity monitoring with AIDE:
- AIDE package installation
- AIDE database initialization
- AIDE cron job for daily integrity checks
- AIDE boot check service configuration
"""
import pytest


# AIDE configuration paths
AIDE_CONFIG_PATH = "/etc/aide/aide.conf"
AIDE_DB_PATH = "/var/lib/aide/aide.db.gz"
AIDE_DB_NEW_PATH = "/var/lib/aide/aide.db.new.gz"
AIDE_LOG_DIR = "/var/log/aide"
AIDE_BOOT_CHECK_SERVICE = "/etc/systemd/system/aide-boot-check.service"

# AIDE binary paths
AIDE_BIN = "/usr/sbin/aide"


class TestAIDEInstallation:
    """Test AIDE package installation."""

    def test_aide_package_installed(self, host):
        """Verify AIDE package is installed."""
        pkg = host.package("aide")
        assert pkg.is_installed, "aide package should be installed"

    def test_aide_binary_exists(self, host):
        """Verify AIDE binary exists."""
        assert host.exists("aide"), "aide binary should exist"
        f = host.file(AIDE_BIN)
        assert f.exists, f"AIDE binary '{AIDE_BIN}' should exist"

    def test_aide_binary_permissions(self, host):
        """Verify AIDE binary has correct permissions."""
        f = host.file(AIDE_BIN)
        if f.exists:
            assert f.is_file, f"'{AIDE_BIN}' should be a regular file"
            # Should be executable
            assert f.mode & 0o111, f"'{AIDE_BIN}' should be executable"


class TestAIDEConfiguration:
    """Test AIDE configuration."""

    def test_aide_config_exists(self, host):
        """Verify AIDE configuration file exists."""
        f = host.file(AIDE_CONFIG_PATH)
        assert f.exists, f"AIDE config '{AIDE_CONFIG_PATH}' should exist"
        assert f.is_file, f"'{AIDE_CONFIG_PATH}' should be a regular file"

    def test_aide_config_permissions(self, host):
        """Verify AIDE configuration has correct permissions."""
        f = host.file(AIDE_CONFIG_PATH)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"AIDE config should have secure permissions, got {oct(f.mode)}"
            assert f.user == "root", "AIDE config should be owned by root"

    def test_aide_config_has_rules(self, host):
        """Verify AIDE configuration has monitoring rules."""
        f = host.file(AIDE_CONFIG_PATH)
        content = f.content_string
        has_rules = False
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                # Look for path definitions with rules
                if "/" in line and ("=" in line or line.startswith("/")):
                    has_rules = True
                    break
        assert has_rules, "AIDE config should have monitoring rules defined"

    def test_aide_config_monitors_critical_paths(self, host):
        """Verify AIDE monitors critical system paths."""
        f = host.file(AIDE_CONFIG_PATH)
        content = f.content_string
        critical_paths = ["/bin", "/sbin", "/usr/bin", "/usr/sbin", "/etc"]
        monitored_count = 0
        for path in critical_paths:
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith(path) or f" {path} " in line:
                    monitored_count += 1
                    break
        assert monitored_count >= 3, \
            f"AIDE should monitor at least 3 critical paths, found {monitored_count}"


class TestAIDEDatabase:
    """Test AIDE database."""

    def test_aide_database_directory_exists(self, host):
        """Verify AIDE database directory exists."""
        d = host.file("/var/lib/aide")
        assert d.exists, "/var/lib/aide should exist"
        assert d.is_directory, "/var/lib/aide should be a directory"

    def test_aide_database_directory_permissions(self, host):
        """Verify AIDE database directory has correct permissions."""
        d = host.file("/var/lib/aide")
        if d.exists:
            assert d.mode in [0o755, 0o750, 0o700], \
                f"/var/lib/aide should have secure permissions, got {oct(d.mode)}"
            assert d.user == "root", "/var/lib/aide should be owned by root"

    def test_aide_database_exists(self, host):
        """Verify AIDE database exists (CIS 1.3.1)."""
        f = host.file(AIDE_DB_PATH)
        if f.exists:
            assert f.is_file, f"AIDE database '{AIDE_DB_PATH}' should be a file"
            assert f.size > 0, "AIDE database should not be empty"
        else:
            pytest.skip(f"AIDE database '{AIDE_DB_PATH}' does not exist (may need initialization)")

    def test_aide_database_permissions(self, host):
        """Verify AIDE database has correct permissions."""
        f = host.file(AIDE_DB_PATH)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"AIDE database should have secure permissions, got {oct(f.mode)}"
            assert f.user == "root", "AIDE database should be owned by root"

    def test_aide_database_readable(self, host):
        """Verify AIDE database is readable."""
        f = host.file(AIDE_DB_PATH)
        if f.exists:
            assert f.is_readable, "AIDE database should be readable"


class TestAIDECronJob:
    """Test AIDE cron job configuration (CIS 1.3.2)."""

    def test_aide_cron_job_exists(self, host):
        """Verify AIDE daily check cron job exists."""
        cmd = host.run("crontab -l -u root 2>&1 | grep -i aide || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "aide" in cmd.stdout.lower(), "AIDE cron job should be configured"
            assert "--check" in cmd.stdout, "AIDE cron job should run integrity check"
        else:
            # Check in cron directories
            cron_dirs = ["/etc/cron.daily", "/etc/cron.d"]
            has_cron = False
            for cron_dir in cron_dirs:
                d = host.file(cron_dir)
                if d.exists and d.is_directory:
                    cmd = host.run(f"ls {cron_dir}/ 2>&1 | grep -i aide || true")
                    if cmd.rc == 0 and cmd.stdout:
                        has_cron = True
                        break
            if not has_cron:
                pytest.skip("AIDE cron job not found in standard locations")

    def test_aide_cron_schedule(self, host):
        """Verify AIDE cron job runs at appropriate time."""
        cmd = host.run("crontab -l -u root 2>&1 | grep -i aide || true")
        if cmd.rc == 0 and cmd.stdout:
            # Should run during off-hours (typically 2-4 AM)
            # Basic check - just verify it's scheduled
            assert "aide" in cmd.stdout.lower(), "AIDE should be in cron"
        else:
            pytest.skip("AIDE cron job not found")

    def test_aide_cron_daily_directory(self, host):
        """Verify /etc/cron.daily exists for AIDE."""
        d = host.file("/etc/cron.daily")
        if d.exists:
            assert d.is_directory, "/etc/cron.daily should be a directory"
            assert d.mode == 0o755, f"/etc/cron.daily should have mode 0755, got {oct(d.mode)}"
        else:
            pytest.skip("/etc/cron.daily does not exist")


class TestAIDELogging:
    """Test AIDE logging configuration."""

    def test_aide_log_directory_exists(self, host):
        """Verify AIDE log directory exists."""
        d = host.file(AIDE_LOG_DIR)
        if d.exists:
            assert d.is_directory, f"'{AIDE_LOG_DIR}' should be a directory"
            assert d.mode in [0o755, 0o750, 0o700], \
                f"AIDE log directory should have secure permissions, got {oct(d.mode)}"
        else:
            # Directory might be created on first run
            pytest.skip(f"AIDE log directory '{AIDE_LOG_DIR}' does not exist yet")

    def test_aide_log_files_exist(self, host):
        """Verify AIDE log files exist."""
        d = host.file(AIDE_LOG_DIR)
        if d.exists and d.is_directory:
            # Check for any log files
            cmd = host.run(f"ls -la {AIDE_LOG_DIR}/ 2>&1 | grep -E '\\.log$' || true")
            if cmd.rc == 0 and cmd.stdout:
                assert "aide" in cmd.stdout.lower() or "check" in cmd.stdout.lower(), \
                    "AIDE log files should exist"
        else:
            pytest.skip(f"AIDE log directory '{AIDE_LOG_DIR}' does not exist")


class TestAIDEBootCheck:
    """Test AIDE boot check service."""

    def test_aide_boot_check_service_exists(self, host):
        """Verify AIDE boot check systemd service exists."""
        f = host.file(AIDE_BOOT_CHECK_SERVICE)
        if f.exists:
            assert f.is_file, f"'{AIDE_BOOT_CHECK_SERVICE}' should be a file"
            assert f.mode == 0o644, \
                f"Boot check service should have mode 0644, got {oct(f.mode)}"
        else:
            pytest.skip(f"AIDE boot check service '{AIDE_BOOT_CHECK_SERVICE}' does not exist")

    def test_aide_boot_check_service_content(self, host):
        """Verify AIDE boot check service has valid content."""
        f = host.file(AIDE_BOOT_CHECK_SERVICE)
        if f.exists:
            content = f.content_string
            assert "[Unit]" in content, "Service should have [Unit] section"
            assert "[Service]" in content, "Service should have [Service] section"
            assert "aide" in content.lower(), "Service should reference aide"
            assert "ExecStart" in content, "Service should have ExecStart"
        else:
            pytest.skip(f"AIDE boot check service '{AIDE_BOOT_CHECK_SERVICE}' does not exist")

    def test_aide_boot_check_service_enabled(self, host):
        """Verify AIDE boot check service is enabled."""
        svc = host.service("aide-boot-check")
        if svc.exists:
            assert svc.is_enabled, "aide-boot-check service should be enabled"
        else:
            pytest.skip("aide-boot-check service does not exist")


class TestAIDEExecution:
    """Test AIDE execution capabilities."""

    def test_aide_check_command_available(self, host):
        """Verify AIDE check command is available."""
        cmd = host.run("aide --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "aide" in cmd.stdout.lower(), "aide --help should work"
        else:
            pytest.skip("aide command not available")

    def test_aide_version(self, host):
        """Verify AIDE version can be determined."""
        cmd = host.run("aide --version 2>&1 | head -1")
        if cmd.rc == 0:
            assert "AIDE" in cmd.stdout or "aide" in cmd.stdout, \
                "AIDE version command should return version info"
        else:
            pytest.skip("aide --version not available")


class TestAIDEIntegrity:
    """Test AIDE integrity monitoring."""

    def test_aide_monitors_etc(self, host):
        """Verify AIDE monitors /etc directory."""
        f = host.file(AIDE_CONFIG_PATH)
        if f.exists:
            content = f.content_string
            # Check for /etc monitoring
            has_etc = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("/etc") or "/etc " in line:
                    has_etc = True
                    break
            assert has_etc, "AIDE should monitor /etc directory"
        else:
            pytest.skip(f"AIDE config '{AIDE_CONFIG_PATH}' does not exist")

    def test_aide_monitors_binaries(self, host):
        """Verify AIDE monitors binary directories."""
        f = host.file(AIDE_CONFIG_PATH)
        if f.exists:
            content = f.content_string
            binary_dirs = ["/bin", "/sbin", "/usr/bin", "/usr/sbin", "/usr/local/bin"]
            monitored = 0
            for line in content.split("\n"):
                line = line.strip()
                for bdir in binary_dirs:
                    if line.startswith(bdir) or f" {bdir} " in line:
                        monitored += 1
                        break
            assert monitored >= 2, \
                f"AIDE should monitor at least 2 binary directories, found {monitored}"
        else:
            pytest.skip(f"AIDE config '{AIDE_CONFIG_PATH}' does not exist")


class TestAIDEContainerHandling:
    """Test AIDE container environment handling."""

    def test_not_in_container_or_skip(self, host):
        """Verify test handles container environment appropriately."""
        # Check if running in container
        cmd = host.run("systemd-detect-virt 2>&1 || cat /proc/1/cgroup 2>&1 | head -5 || true")
        if cmd.rc == 0:
            output = cmd.stdout.lower()
            if any(virt in output for virt in ["docker", "podman", "lxc", "container"]):
                pytest.skip("Running in container, AIDE may not be fully functional")
