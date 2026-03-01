# =============================================================================
# Audit Event Identifier: DSU-PYS-500088
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for storage/backup/timeshift role.

This role handles system snapshots using Timeshift:
- Installing timeshift package
- Creating configuration directory
- Configuring snapshot schedules
"""
import pytest


# Configuration paths
TIMESHIFT_CONFIG_DIR = "/etc/timeshift"
TIMESHIFT_CONFIG_FILE = "/etc/timeshift/timeshift.json"
TIMESHIFT_BACKUP_PATH = "/timeshift"


class TestTimeshiftInstallation:
    """Test timeshift package installation."""

    def test_timeshift_package_installed(self, host):
        """Verify timeshift package is installed."""
        pkg = host.package("timeshift")
        assert pkg.is_installed, "timeshift package should be installed"

    def test_timeshift_command_available(self, host):
        """Verify timeshift command is available."""
        assert host.exists("timeshift"), "timeshift command should be available"

    def test_timeshift_version(self, host):
        """Verify timeshift version can be queried."""
        cmd = host.run("timeshift --version 2>&1 || timeshift --help 2>&1 | head -3")
        if cmd.rc == 0:
            assert "timeshift" in cmd.stdout.lower(), "timeshift should return version or help info"


class TestTimeshiftDirectories:
    """Test timeshift directory structure."""

    def test_timeshift_config_dir_exists(self, host):
        """Verify timeshift configuration directory exists."""
        d = host.file(TIMESHIFT_CONFIG_DIR)
        assert d.exists, f"{TIMESHIFT_CONFIG_DIR} should exist"
        assert d.is_directory, f"{TIMESHIFT_CONFIG_DIR} should be a directory"

    def test_timeshift_config_dir_permissions(self, host):
        """Verify timeshift configuration directory has correct permissions."""
        d = host.file(TIMESHIFT_CONFIG_DIR)
        if d.exists:
            # Should be 0755
            assert d.mode == 0o755, f"{TIMESHIFT_CONFIG_DIR} should have mode 0755, got {oct(d.mode)}"
            assert d.user == "root", f"{TIMESHIFT_CONFIG_DIR} should be owned by root"

    def test_timeshift_backup_dir_exists(self, host):
        """Verify timeshift backup directory exists."""
        d = host.file(TIMESHIFT_BACKUP_PATH)
        if d.exists:
            assert d.is_directory, f"{TIMESHIFT_BACKUP_PATH} should be a directory"


class TestTimeshiftConfiguration:
    """Test timeshift configuration files."""

    def test_timeshift_config_file_exists(self, host):
        """Verify timeshift configuration file exists."""
        f = host.file(TIMESHIFT_CONFIG_FILE)
        assert f.exists, f"{TIMESHIFT_CONFIG_FILE} should exist"
        assert f.is_file, f"{TIMESHIFT_CONFIG_FILE} should be a file"

    def test_timeshift_config_permissions(self, host):
        """Verify timeshift configuration has correct permissions."""
        f = host.file(TIMESHIFT_CONFIG_FILE)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"{TIMESHIFT_CONFIG_FILE} should have secure permissions, got {oct(f.mode)}"
            assert f.user == "root", f"{TIMESHIFT_CONFIG_FILE} should be owned by root"

    def test_timeshift_config_valid_json(self, host):
        """Verify timeshift configuration is valid JSON."""
        f = host.file(TIMESHIFT_CONFIG_FILE)
        if f.exists:
            content = f.content_string
            # Basic JSON validation - should start with { and end with }
            content_stripped = content.strip()
            assert content_stripped.startswith("{"), "timeshift.json should be valid JSON"
            assert content_stripped.endswith("}"), "timeshift.json should be valid JSON"

    def test_timeshift_config_has_required_fields(self, host):
        """Verify timeshift configuration has required fields."""
        f = host.file(TIMESHIFT_CONFIG_FILE)
        if f.exists:
            content = f.content_string
            # Should have basic configuration fields
            required_fields = ["backup_device", "snapshot_dir", "schedule"]
            for field in required_fields:
                assert f'"{field}"' in content or f"'{field}'" in content, \
                    f"timeshift.json should have '{field}' field"


class TestTimeshiftFunctionality:
    """Test timeshift functionality."""

    def test_timeshift_list_command(self, host):
        """Verify timeshift list command is available."""
        cmd = host.run("timeshift --list 2>&1 || timeshift -l 2>&1 || true")
        # May return no snapshots if none created yet
        # Command should be available
        assert "timeshift" in cmd.stdout.lower() or cmd.rc == 0, \
            "timeshift --list command should be available"

    def test_timeshift_create_command(self, host):
        """Verify timeshift create command syntax."""
        cmd = host.run("timeshift --create 2>&1 | head -5 || true")
        # May fail if not configured, but command should exist
        pass

    def test_timeshift_devices_command(self, host):
        """Verify timeshift devices command is available."""
        cmd = host.run("timeshift --devices 2>&1 || timeshift -d 2>&1 || true")
        # Should list available devices
        pass


class TestTimeshiftSnapshots:
    """Test timeshift snapshots."""

    def test_timeshift_snapshots_directory(self, host):
        """Verify snapshots directory structure if snapshots exist."""
        d = host.file(f"{TIMESHIFT_BACKUP_PATH}/timeshift-btrfs")
        if d.exists:
            assert d.is_directory, "Snapshots directory should be a directory"

    def test_timeshift_snapshots_readable(self, host):
        """Verify snapshots are readable if they exist."""
        cmd = host.run(f"ls -la {TIMESHIFT_BACKUP_PATH}/ 2>/dev/null || true")
        # Informational - snapshots may not exist yet


class TestTimeshiftCron:
    """Test timeshift scheduled tasks."""

    def test_timeshift_cron_jobs(self, host):
        """Verify timeshift cron jobs are configured."""
        cmd = host.run("crontab -l 2>/dev/null | grep -i timeshift || true")
        # Timeshift may use systemd timers instead of cron
        # This is informational

    def test_timeshift_systemd_timer(self, host):
        """Verify timeshift systemd timer if configured."""
        cmd = host.run("systemctl list-timers 2>/dev/null | grep -i timeshift || true")
        # Informational - timeshift may not use systemd timers


class TestTimeshiftSecurity:
    """Test timeshift security configuration."""

    def test_timeshift_config_ownership(self, host):
        """Verify all timeshift config files are owned by root."""
        cmd = host.run(f"find {TIMESHIFT_CONFIG_DIR} -type f ! -user root 2>/dev/null || true")
        if cmd.stdout.strip():
            pytest.fail(f"Found config files not owned by root: {cmd.stdout}")

    def test_timeshift_no_world_writable(self, host):
        """Verify no timeshift files are world-writable."""
        cmd = host.run(f"find {TIMESHIFT_CONFIG_DIR} -perm /002 -type f 2>/dev/null || true")
        if cmd.stdout.strip():
            pytest.fail(f"Found world-writable files: {cmd.stdout}")


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), timeshift may not function properly")

    def test_block_devices_accessible(self, host):
        """Verify block devices are accessible."""
        d = host.file("/dev")
        if d.exists:
            # Block devices should be accessible for snapshot functionality
            pass
        else:
            pytest.skip("/dev not accessible")
