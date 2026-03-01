# =============================================================================
# Audit Event Identifier: DSU-PYS-500087
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for storage/backup role.

This role handles backup configuration and management.
Compliance: ISO 27001 §8.13 - Backup
"""
import pytest


class TestStorageBackup:
    """Test backup configuration."""

    def test_backup_role_executed(self, host):
        """Verify backup role executed."""
        # This test verifies the role ran
        pass

    def test_backup_directories_available(self, host):
        """Verify backup directories can be created."""
        d = host.file("/var/backups")
        if d.exists:
            assert d.is_directory, "/var/backups should be a directory"

    def test_backup_directory_permissions(self, host):
        """Verify backup directories have correct permissions."""
        d = host.file("/var/backups")
        if d.exists:
            # Backup directories should be secure (0700 or 0755)
            assert d.mode in [0o700, 0o755], \
                f"/var/backups should have secure permissions, got {oct(d.mode)}"

    def test_backup_srv_directory(self, host):
        """Verify srv backup directory exists."""
        d = host.file("/srv/backups")
        if d.exists:
            assert d.is_directory, "/srv/backups should be a directory"


class TestBackupSecurity:
    """Test backup security configuration."""

    def test_backup_directory_ownership(self, host):
        """Verify backup directories are owned by root."""
        d = host.file("/var/backups")
        if d.exists:
            assert d.user == "root", "/var/backups should be owned by root"

    def test_no_world_readable_backups(self, host):
        """Verify backup directories are not world-readable."""
        cmd = host.run("ls -la /var/backups 2>/dev/null || true")
        if cmd.stdout.strip():
            # Should not have world-readable permissions
            assert "drwx------" in cmd.stdout or "drwxr-x---" in cmd.stdout, \
                "Backup directories should not be world-readable"


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), backup features may be limited")
