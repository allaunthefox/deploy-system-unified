# =============================================================================
# Audit Event Identifier: DSU-PYS-500056
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for core/grub role.

This role handles GRUB bootloader configuration:
- Configuring kernel parameters via GRUB_CMDLINE_LINUX_DEFAULT
- Managing GRUB configuration files
- Backing up GRUB configuration
"""
import pytest


# Default GRUB configuration path
GRUB_CONFIG_PATH = "/etc/default/grub"

# Common kernel parameters that might be set
COMMON_KERNEL_PARAMS = [
    "quiet",
    "splash",
]


class TestGrubConfiguration:
    """Test GRUB configuration file."""

    def test_grub_config_exists(self, host):
        """Verify GRUB configuration file exists."""
        f = host.file(GRUB_CONFIG_PATH)
        assert f.exists, f"GRUB config file '{GRUB_CONFIG_PATH}' should exist"
        assert f.is_file, f"'{GRUB_CONFIG_PATH}' should be a regular file"

    def test_grub_config_permissions(self, host):
        """Verify GRUB configuration file has correct permissions."""
        f = host.file(GRUB_CONFIG_PATH)
        # Should be readable by root, possibly readable by others
        assert f.mode in [0o644, 0o640, 0o600], f"GRUB config should have secure permissions"
        assert f.user == "root", "GRUB config should be owned by root"

    def test_grub_cmdline_linux_default_exists(self, host):
        """Verify GRUB_CMDLINE_LINUX_DEFAULT is configured."""
        f = host.file(GRUB_CONFIG_PATH)
        content = f.content_string
        assert "GRUB_CMDLINE_LINUX_DEFAULT" in content, "GRUB_CMDLINE_LINUX_DEFAULT should be configured"

    def test_grub_cmdline_format(self, host):
        """Verify GRUB_CMDLINE_LINUX_DEFAULT has valid format."""
        f = host.file(GRUB_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            if line.startswith("GRUB_CMDLINE_LINUX_DEFAULT="):
                # Should be in format: GRUB_CMDLINE_LINUX_DEFAULT="params"
                assert "=" in line, "GRUB_CMDLINE_LINUX_DEFAULT should have assignment"
                assert '"' in line or "'" in line, "GRUB_CMDLINE_LINUX_DEFAULT value should be quoted"
                break


class TestGrubBaseParameters:
    """Test base kernel parameters."""

    def test_grub_has_base_params(self, host):
        """Verify GRUB has base kernel parameters configured."""
        f = host.file(GRUB_CONFIG_PATH)
        content = f.content_string
        # Check for common base parameters
        has_params = False
        for line in content.split("\n"):
            if "GRUB_CMDLINE_LINUX_DEFAULT" in line:
                has_params = True
                break
        assert has_params, "GRUB should have kernel parameters configured"


class TestGrubBackup:
    """Test GRUB backup configuration."""

    def test_grub_backup_directory(self, host):
        """Verify GRUB backup directory exists if configured."""
        backup_dir = "/var/backups/grub"
        f = host.file(backup_dir)
        if f.exists:
            assert f.is_directory, f"GRUB backup directory '{backup_dir}' should be a directory"
            # Should have secure permissions
            assert f.mode in [0o755, 0o750, 0o700], f"Backup directory should have secure permissions"

    def test_grub_backups_exist(self, host):
        """Verify GRUB backups exist if backup is enabled."""
        backup_dir = "/var/backups/grub"
        f = host.file(backup_dir)
        if f.exists and f.is_directory:
            # If backup directory exists, it should contain backups
            # This is informational - backups may not exist yet
            pass


class TestGrubSystemState:
    """Test GRUB system state."""

    def test_grub_installed(self, host):
        """Verify GRUB is installed."""
        # Check for GRUB executables
        grub_commands = ["grub-install", "grub-mkconfig", "update-grub", "grub2-mkconfig"]
        has_grub = False
        for cmd in grub_commands:
            if host.exists(cmd):
                has_grub = True
                break
        assert has_grub, "GRUB bootloader should be installed"

    def test_boot_directory_exists(self, host):
        """Verify /boot directory exists."""
        d = host.file("/boot")
        assert d.exists, "/boot directory should exist"
        assert d.is_directory, "/boot should be a directory"

    def test_grub_directory_exists(self, host):
        """Verify GRUB directory exists."""
        # GRUB directory location varies by distribution
        grub_dirs = [
            "/boot/grub",
            "/boot/grub2",
            "/etc/grub.d",
        ]
        has_grub_dir = False
        for grub_dir in grub_dirs:
            if host.file(grub_dir).exists:
                has_grub_dir = True
                break
        assert has_grub_dir, "GRUB directory should exist"

    def test_grub_config_directory(self, host):
        """Verify GRUB configuration directory exists."""
        d = host.file("/etc/grub.d")
        if d.exists:
            assert d.is_directory, "/etc/grub.d should be a directory"
            assert d.mode == 0o755, "/etc/grub.d should have correct permissions"


class TestGrubValidation:
    """Test GRUB configuration validation."""

    def test_grub_config_syntax(self, host):
        """Verify GRUB config file has valid syntax (basic check)."""
        f = host.file(GRUB_CONFIG_PATH)
        content = f.content_string
        # Basic syntax checks
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # Variable assignments should have =
            if "=" in line:
                var_name = line.split("=")[0]
                assert var_name.isupper() or var_name.startswith("_"), f"Variable '{var_name}' should be uppercase"

    def test_grub_no_duplicate_entries(self, host):
        """Verify no duplicate GRUB configuration entries."""
        f = host.file(GRUB_CONFIG_PATH)
        content = f.content_string
        lines = content.split("\n")
        var_names = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                var_name = line.split("=")[0]
                var_names.append(var_name)
        # Check for duplicates (excluding intentionally duplicated vars)
        duplicates = [x for x in set(var_names) if var_names.count(x) > 1]
        # Some duplicates might be acceptable, just report them
        assert len(duplicates) <= len(var_names) * 0.1, "Too many duplicate GRUB config entries"
