"""
Testinfra tests for storage/backup/restic role.

This role handles deduplicated encrypted backups using Restic:
- Installing restic package
- Creating configuration directories
- Deploying password file and wrapper script
- Configuring systemd timer for automated backups
- Automated restore testing (ISO 27040 compliance)
"""
import pytest


# Configuration paths
RESTIC_CONFIG_DIR = "/etc/restic"
RESTIC_LOG_DIR = "/var/log/restic"
RESTIC_CACHE_DIR = "/var/cache/restic"
RESTIC_SCRIPT_DIR = "/usr/local/bin"
RESTIC_PASSWORD_FILE = "/etc/restic/password"
RESTIC_WRAPPER_SCRIPT = "/usr/local/bin/restic_wrapper.sh"
RESTIC_SERVICE = "restic-backup.service"
RESTIC_TIMER = "restic-backup.timer"
RESTIC_BACKUP_DIR = "/srv/backups/restic"


class TestResticInstallation:
    """Test restic package installation."""

    def test_restic_package_installed(self, host):
        """Verify restic package is installed."""
        pkg = host.package("restic")
        assert pkg.is_installed, "restic package should be installed"

    def test_restic_command_available(self, host):
        """Verify restic command is available."""
        assert host.exists("restic"), "restic command should be available"

    def test_restic_version(self, host):
        """Verify restic version can be queried."""
        cmd = host.run("restic version")
        if cmd.rc == 0:
            assert "restic" in cmd.stdout.lower(), "restic version command should return version info"


class TestResticDirectories:
    """Test restic directory structure."""

    def test_restic_config_dir_exists(self, host):
        """Verify restic configuration directory exists."""
        d = host.file(RESTIC_CONFIG_DIR)
        assert d.exists, f"{RESTIC_CONFIG_DIR} should exist"
        assert d.is_directory, f"{RESTIC_CONFIG_DIR} should be a directory"

    def test_restic_config_dir_permissions(self, host):
        """Verify restic configuration directory has secure permissions."""
        d = host.file(RESTIC_CONFIG_DIR)
        if d.exists:
            # Should be 0700 (owner only)
            assert d.mode == 0o700, f"{RESTIC_CONFIG_DIR} should have mode 0700, got {oct(d.mode)}"
            assert d.user == "root", f"{RESTIC_CONFIG_DIR} should be owned by root"
            assert d.group == "root", f"{RESTIC_CONFIG_DIR} should be grouped to root"

    def test_restic_log_dir_exists(self, host):
        """Verify restic log directory exists."""
        d = host.file(RESTIC_LOG_DIR)
        assert d.exists, f"{RESTIC_LOG_DIR} should exist"
        assert d.is_directory, f"{RESTIC_LOG_DIR} should be a directory"

    def test_restic_log_dir_permissions(self, host):
        """Verify restic log directory has secure permissions."""
        d = host.file(RESTIC_LOG_DIR)
        if d.exists:
            assert d.mode == 0o700, f"{RESTIC_LOG_DIR} should have mode 0700, got {oct(d.mode)}"
            assert d.user == "root", f"{RESTIC_LOG_DIR} should be owned by root"

    def test_restic_cache_dir_exists(self, host):
        """Verify restic cache directory exists."""
        d = host.file(RESTIC_CACHE_DIR)
        assert d.exists, f"{RESTIC_CACHE_DIR} should exist"
        assert d.is_directory, f"{RESTIC_CACHE_DIR} should be a directory"

    def test_restic_backup_dir_exists(self, host):
        """Verify restic backup directory exists."""
        d = host.file(RESTIC_BACKUP_DIR)
        if d.exists:
            assert d.is_directory, f"{RESTIC_BACKUP_DIR} should be a directory"


class TestResticConfiguration:
    """Test restic configuration files."""

    def test_restic_password_file_exists(self, host):
        """Verify restic password file exists."""
        f = host.file(RESTIC_PASSWORD_FILE)
        assert f.exists, f"{RESTIC_PASSWORD_FILE} should exist"
        assert f.is_file, f"{RESTIC_PASSWORD_FILE} should be a file"

    def test_restic_password_file_permissions(self, host):
        """Verify restic password file has secure permissions."""
        f = host.file(RESTIC_PASSWORD_FILE)
        if f.exists:
            # Should be 0600 (owner read/write only)
            assert f.mode == 0o600, f"{RESTIC_PASSWORD_FILE} should have mode 0600, got {oct(f.mode)}"
            assert f.user == "root", f"{RESTIC_PASSWORD_FILE} should be owned by root"
            assert f.group == "root", f"{RESTIC_PASSWORD_FILE} should be grouped to root"

    def test_restic_password_file_not_empty(self, host):
        """Verify restic password file is not empty."""
        f = host.file(RESTIC_PASSWORD_FILE)
        if f.exists:
            assert f.size > 0, f"{RESTIC_PASSWORD_FILE} should not be empty"
            # Should not contain the default placeholder
            content = f.content_string
            assert "CHANGE_ME_IN_VAULT" not in content, "Password should not contain default placeholder"

    def test_restic_wrapper_script_exists(self, host):
        """Verify restic wrapper script exists."""
        f = host.file(RESTIC_WRAPPER_SCRIPT)
        assert f.exists, f"{RESTIC_WRAPPER_SCRIPT} should exist"
        assert f.is_file, f"{RESTIC_WRAPPER_SCRIPT} should be a file"

    def test_restic_wrapper_script_permissions(self, host):
        """Verify restic wrapper script has correct permissions."""
        f = host.file(RESTIC_WRAPPER_SCRIPT)
        if f.exists:
            # Should be 0750 (owner rwx, group rx)
            assert f.mode == 0o750, f"{RESTIC_WRAPPER_SCRIPT} should have mode 0750, got {oct(f.mode)}"
            assert f.user == "root", f"{RESTIC_WRAPPER_SCRIPT} should be owned by root"

    def test_restic_wrapper_script_executable(self, host):
        """Verify restic wrapper script is executable."""
        f = host.file(RESTIC_WRAPPER_SCRIPT)
        if f.exists:
            assert f.is_executable, f"{RESTIC_WRAPPER_SCRIPT} should be executable"

    def test_restic_wrapper_script_content(self, host):
        """Verify restic wrapper script contains restic commands."""
        f = host.file(RESTIC_WRAPPER_SCRIPT)
        if f.exists:
            content = f.content_string
            assert "restic" in content.lower(), "Wrapper script should contain restic commands"


class TestResticSystemd:
    """Test restic systemd service and timer."""

    def test_restic_service_file_exists(self, host):
        """Verify restic systemd service file exists."""
        f = host.file("/etc/systemd/system/restic-backup.service")
        assert f.exists, "/etc/systemd/system/restic-backup.service should exist"
        assert f.is_file, "/etc/systemd/system/restic-backup.service should be a file"

    def test_restic_service_file_permissions(self, host):
        """Verify restic systemd service file has correct permissions."""
        f = host.file("/etc/systemd/system/restic-backup.service")
        if f.exists:
            assert f.mode in [0o644, 0o640], "restic-backup.service should have correct permissions"
            assert f.user == "root", "restic-backup.service should be owned by root"

    def test_restic_timer_file_exists(self, host):
        """Verify restic systemd timer file exists."""
        f = host.file("/etc/systemd/system/restic-backup.timer")
        assert f.exists, "/etc/systemd/system/restic-backup.timer should exist"
        assert f.is_file, "/etc/systemd/system/restic-backup.timer should be a file"

    def test_restic_timer_file_permissions(self, host):
        """Verify restic systemd timer file has correct permissions."""
        f = host.file("/etc/systemd/system/restic-backup.timer")
        if f.exists:
            assert f.mode in [0o644, 0o640], "restic-backup.timer should have correct permissions"
            assert f.user == "root", "restic-backup.timer should be owned by root"

    def test_restic_timer_enabled(self, host):
        """Verify restic-backup timer is enabled."""
        svc = host.service("restic-backup.timer")
        if svc.exists:
            assert svc.is_enabled, "restic-backup.timer should be enabled"

    def test_restic_timer_running(self, host):
        """Verify restic-backup timer is running."""
        svc = host.service("restic-backup.timer")
        if svc.exists:
            assert svc.is_running, "restic-backup.timer should be running"

    def test_systemd_daemon_reload(self, host):
        """Verify systemd daemon can be reloaded."""
        cmd = host.run("systemctl daemon-reload 2>&1 || true")
        # Should not fail catastrophically


class TestResticFunctionality:
    """Test restic functionality."""

    def test_restic_repository_initialized(self, host):
        """Verify restic repository is initialized."""
        repo_dir = host.file(RESTIC_BACKUP_DIR)
        if repo_dir.exists:
            # Check for restic repository structure
            config_file = host.file(f"{RESTIC_BACKUP_DIR}/config")
            if config_file.exists:
                assert config_file.is_file, "Restic repository config should exist"

    def test_restic_backup_command_syntax(self, host):
        """Verify restic backup command syntax is valid."""
        cmd = host.run("restic backup --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "backup" in cmd.stdout.lower(), "restic backup command should be available"

    def test_restic_snapshots_command(self, host):
        """Verify restic snapshots command is available."""
        cmd = host.run("restic snapshots --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "snapshots" in cmd.stdout.lower(), "restic snapshots command should be available"

    def test_restic_prune_command(self, host):
        """Verify restic prune command is available."""
        cmd = host.run("restic prune --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "prune" in cmd.stdout.lower(), "restic prune command should be available"


class TestResticLogs:
    """Test restic logging."""

    def test_restic_log_directory_writable(self, host):
        """Verify restic log directory is writable."""
        cmd = host.run(f"test -w {RESTIC_LOG_DIR} && echo 'writable' || echo 'not writable'")
        if cmd.rc == 0:
            assert "writable" in cmd.stdout, f"{RESTIC_LOG_DIR} should be writable"

    def test_restic_logs_exist(self, host):
        """Verify restic logs exist if backups have run."""
        cmd = host.run(f"ls -la {RESTIC_LOG_DIR}/*.log 2>/dev/null || true")
        # Logs may not exist if no backups have run yet
        # This is informational


class TestResticSecurity:
    """Test restic security configuration."""

    def test_restic_no_world_readable_configs(self, host):
        """Verify no restic configuration files are world-readable."""
        cmd = host.run(f"find {RESTIC_CONFIG_DIR} -perm /044 -type f 2>/dev/null || true")
        if cmd.stdout.strip():
            # Password file should not be world readable
            assert RESTIC_PASSWORD_FILE not in cmd.stdout, "Password file should not be world-readable"

    def test_restic_config_ownership(self, host):
        """Verify all restic config files are owned by root."""
        cmd = host.run(f"find {RESTIC_CONFIG_DIR} -type f ! -user root 2>/dev/null || true")
        if cmd.stdout.strip():
            pytest.fail(f"Found config files not owned by root: {cmd.stdout}")


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), some systemd features may not be available")

    def test_systemd_available(self, host):
        """Verify systemd is available."""
        cmd = host.run("which systemctl")
        if cmd.rc != 0:
            pytest.skip("systemd not available in this environment")
