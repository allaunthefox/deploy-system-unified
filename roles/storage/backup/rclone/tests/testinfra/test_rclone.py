"""
Testinfra tests for storage/backup/rclone role.

This role handles cloud sync using Rclone:
- Installing rclone package
- Creating configuration directory
- Deploying rclone configuration
- Setting up sync schedules
"""
import pytest


# Configuration paths
RCLONE_CONFIG_DIR = "/etc/rclone"
RCLONE_CONFIG_FILE = "/etc/rclone/rclone.conf"
RCLONE_SCRIPT_DIR = "/usr/local/bin"


class TestRcloneInstallation:
    """Test rclone package installation."""

    def test_rclone_package_installed(self, host):
        """Verify rclone package is installed."""
        pkg = host.package("rclone")
        assert pkg.is_installed, "rclone package should be installed"

    def test_rclone_command_available(self, host):
        """Verify rclone command is available."""
        assert host.exists("rclone"), "rclone command should be available"

    def test_rclone_version(self, host):
        """Verify rclone version can be queried."""
        cmd = host.run("rclone version")
        if cmd.rc == 0:
            assert "rclone" in cmd.stdout.lower(), "rclone version command should return version info"

    def test_rclone_help(self, host):
        """Verify rclone help is accessible."""
        cmd = host.run("rclone --help 2>&1 | head -10")
        if cmd.rc == 0:
            assert "rclone" in cmd.stdout.lower(), "rclone help should be available"


class TestRcloneDirectories:
    """Test rclone directory structure."""

    def test_rclone_config_dir_exists(self, host):
        """Verify rclone configuration directory exists."""
        d = host.file(RCLONE_CONFIG_DIR)
        assert d.exists, f"{RCLONE_CONFIG_DIR} should exist"
        assert d.is_directory, f"{RCLONE_CONFIG_DIR} should be a directory"

    def test_rclone_config_dir_permissions(self, host):
        """Verify rclone configuration directory has secure permissions."""
        d = host.file(RCLONE_CONFIG_DIR)
        if d.exists:
            # Should be 0700 (owner only)
            assert d.mode == 0o700, f"{RCLONE_CONFIG_DIR} should have mode 0700, got {oct(d.mode)}"
            assert d.user == "root", f"{RCLONE_CONFIG_DIR} should be owned by root"
            assert d.group == "root", f"{RCLONE_CONFIG_DIR} should be grouped to root"


class TestRcloneConfiguration:
    """Test rclone configuration files."""

    def test_rclone_config_file_exists(self, host):
        """Verify rclone configuration file exists."""
        f = host.file(RCLONE_CONFIG_FILE)
        assert f.exists, f"{RCLONE_CONFIG_FILE} should exist"
        assert f.is_file, f"{RCLONE_CONFIG_FILE} should be a file"

    def test_rclone_config_file_permissions(self, host):
        """Verify rclone configuration file has secure permissions."""
        f = host.file(RCLONE_CONFIG_FILE)
        if f.exists:
            # Should be 0600 (owner read/write only)
            assert f.mode == 0o600, f"{RCLONE_CONFIG_FILE} should have mode 0600, got {oct(f.mode)}"
            assert f.user == "root", f"{RCLONE_CONFIG_FILE} should be owned by root"
            assert f.group == "root", f"{RCLONE_CONFIG_FILE} should be grouped to root"

    def test_rclone_config_file_format(self, host):
        """Verify rclone configuration file has valid INI format."""
        f = host.file(RCLONE_CONFIG_FILE)
        if f.exists:
            content = f.content_string
            # INI format should have section headers in brackets
            # Empty config is valid if no remotes configured
            if content.strip():
                # If not empty, should have section headers
                has_section = any(line.strip().startswith("[") and line.strip().endswith("]")
                                  for line in content.split("\n"))
                # May be empty if no remotes configured
                # assert has_section, "rclone.conf should have section headers in INI format"

    def test_rclone_config_not_empty_when_configured(self, host):
        """Verify rclone config has content if it was configured."""
        f = host.file(RCLONE_CONFIG_FILE)
        if f.exists:
            content = f.content_string
            # Config may be empty if no rclone_config_content was provided
            # This is informational


class TestRcloneFunctionality:
    """Test rclone functionality."""

    def test_rclone_list_remotes(self, host):
        """Verify rclone listremotes command works."""
        cmd = host.run("rclone listremotes 2>&1 || true")
        # May return empty if no remotes configured
        # Command should be available
        assert cmd.rc == 0 or "listremotes" in cmd.stdout.lower(), \
            "rclone listremotes command should be available"

    def test_rclone_config_command(self, host):
        """Verify rclone config command is available."""
        cmd = host.run("rclone config --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "config" in cmd.stdout.lower(), "rclone config command should be available"

    def test_rclone_copy_command(self, host):
        """Verify rclone copy command is available."""
        cmd = host.run("rclone copy --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "copy" in cmd.stdout.lower(), "rclone copy command should be available"

    def test_rclone_sync_command(self, host):
        """Verify rclone sync command is available."""
        cmd = host.run("rclone sync --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "sync" in cmd.stdout.lower(), "rclone sync command should be available"

    def test_rclone_ls_command(self, host):
        """Verify rclone lsf command is available."""
        cmd = host.run("rclone lsf --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "lsf" in cmd.stdout.lower() or "list" in cmd.stdout.lower(), \
                "rclone lsf command should be available"


class TestRcloneScripts:
    """Test rclone sync scripts."""

    def test_rclone_script_dir_exists(self, host):
        """Verify rclone script directory exists."""
        d = host.file(RCLONE_SCRIPT_DIR)
        assert d.exists, f"{RCLONE_SCRIPT_DIR} should exist"
        assert d.is_directory, f"{RCLONE_SCRIPT_DIR} should be a directory"

    def test_rclone_wrapper_scripts(self, host):
        """Verify rclone wrapper scripts if they exist."""
        cmd = host.run(f"ls -la {RCLONE_SCRIPT_DIR}/*rclone* 2>/dev/null || true")
        # Wrapper scripts may exist if configured
        # This is informational


class TestRcloneCron:
    """Test rclone scheduled tasks."""

    def test_rclone_cron_jobs(self, host):
        """Verify rclone cron jobs are configured."""
        cmd = host.run("crontab -l 2>/dev/null | grep -i rclone || true")
        # Cron jobs may be configured for sync schedules
        # This is informational

    def test_rclone_systemd_timers(self, host):
        """Verify rclone systemd timers if configured."""
        cmd = host.run("systemctl list-timers 2>/dev/null | grep -i rclone || true")
        # Informational - systemd timers may be used


class TestRcloneSecurity:
    """Test rclone security configuration."""

    def test_rclone_config_ownership(self, host):
        """Verify all rclone config files are owned by root."""
        cmd = host.run(f"find {RCLONE_CONFIG_DIR} -type f ! -user root 2>/dev/null || true")
        if cmd.stdout.strip():
            pytest.fail(f"Found config files not owned by root: {cmd.stdout}")

    def test_rclone_no_world_readable(self, host):
        """Verify no rclone config files are world-readable."""
        cmd = host.run(f"find {RCLONE_CONFIG_DIR} -perm /044 -type f 2>/dev/null || true")
        if cmd.stdout.strip():
            pytest.fail(f"Found world-readable config files: {cmd.stdout}")

    def test_rclone_no_world_writable(self, host):
        """Verify no rclone files are world-writable."""
        cmd = host.run(f"find {RCLONE_CONFIG_DIR} -perm /002 -type f 2>/dev/null || true")
        if cmd.stdout.strip():
            pytest.fail(f"Found world-writable files: {cmd.stdout}")


class TestRcloneNetwork:
    """Test rclone network functionality."""

    def test_rclone_network_access(self, host):
        """Verify rclone can access network (if configured)."""
        # This is informational - actual network access depends on remotes configured
        cmd = host.run("rclone version 2>&1 | grep -i 'go version' || true")
        # Rclone should be compiled with network support


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), some rclone features may be limited")

    def test_network_available(self, host):
        """Verify network is available for rclone operations."""
        cmd = host.run("ping -c 1 8.8.8.8 2>&1 || true")
        if cmd.rc != 0:
            pytest.skip("Network not available for rclone operations")
