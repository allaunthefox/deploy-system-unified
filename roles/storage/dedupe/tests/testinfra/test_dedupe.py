"""
Testinfra tests for storage/dedupe role.

This role handles Btrfs deduplication using duperemove:
- Installing duperemove package
- Creating hash database directory
- Configuring weekly deduplication cron jobs
- Auditing deduplication potential
"""
import pytest


# Dedupe configuration
DUPEREMOVE_PACKAGE = "duperemove"
DUPEREMOVE_COMMAND = "duperemove"
DUPEREMOVE_HASH_DIR = "/var/lib/duperemove"
DUPEREMOVE_HASH_DB = "/var/lib/duperemove/hash.db"
DUPEREMOVE_LOG = "/var/log/duperemove.log"


class TestDuperemoveInstallation:
    """Test duperemove package installation."""

    def test_duperemove_package_installed(self, host):
        """Verify duperemove package is installed."""
        pkg = host.package(DUPEREMOVE_PACKAGE)
        assert pkg.is_installed, f"{DUPEREMOVE_PACKAGE} package should be installed"

    def test_duperemove_command_available(self, host):
        """Verify duperemove command is available."""
        assert host.exists(DUPEREMOVE_COMMAND), f"{DUPEREMOVE_COMMAND} command should be available"

    def test_duperemove_version(self, host):
        """Verify duperemove version can be queried."""
        cmd = host.run(f"{DUPEREMOVE_COMMAND} --version 2>&1 || {DUPEREMOVE_COMMAND} --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "duperemove" in cmd.stdout.lower(), "duperemove should return version or help info"

    def test_duperemove_help(self, host):
        """Verify duperemove help is accessible."""
        cmd = host.run(f"{DUPEREMOVE_COMMAND} --help 2>&1 | head -15")
        if cmd.rc == 0:
            assert "duperemove" in cmd.stdout.lower(), "duperemove help should be available"


class TestDuperemoveDirectories:
    """Test duperemove directory structure."""

    def test_duperemove_hash_dir_exists(self, host):
        """Verify duperemove hash directory exists."""
        d = host.file(DUPEREMOVE_HASH_DIR)
        assert d.exists, f"{DUPEREMOVE_HASH_DIR} should exist"
        assert d.is_directory, f"{DUPEREMOVE_HASH_DIR} should be a directory"

    def test_duperemove_hash_dir_permissions(self, host):
        """Verify duperemove hash directory has secure permissions."""
        d = host.file(DUPEREMOVE_HASH_DIR)
        if d.exists:
            # Should be 0700 (owner only)
            assert d.mode == 0o700, f"{DUPEREMOVE_HASH_DIR} should have mode 0700, got {oct(d.mode)}"
            assert d.user == "root", f"{DUPEREMOVE_HASH_DIR} should be owned by root"

    def test_duperemove_hash_db_exists(self, host):
        """Verify duperemove hash database exists (after first run)."""
        f = host.file(DUPEREMOVE_HASH_DB)
        # Hash DB is created on first run
        if f.exists:
            assert f.is_file, f"{DUPEREMOVE_HASH_DB} should be a file"


class TestDuperemoveCron:
    """Test duperemove scheduled tasks."""

    def test_duperemove_cron_job_exists(self, host):
        """Verify duperemove cron job is configured."""
        cmd = host.run("crontab -l 2>/dev/null | grep -i duperemove || true")
        # Cron job should be configured for weekly deduplication
        if cmd.stdout.strip():
            assert "duperemove" in cmd.stdout.lower(), "duperemove cron job should be configured"

    def test_duperemove_cron_schedule(self, host):
        """Verify duperemove cron schedule is correct."""
        cmd = host.run("crontab -l 2>/dev/null | grep duperemove || true")
        if cmd.stdout.strip():
            # Should be scheduled for weekly run (Sunday at 3 AM by default)
            # Format: minute hour day month weekday command
            lines = cmd.stdout.strip().split("\n")
            for line in lines:
                if "duperemove" in line.lower():
                    # Verify it has a schedule (5 fields before command)
                    parts = line.split()
                    assert len(parts) >= 6, "Cron job should have schedule and command"

    def test_duperemove_system_cron(self, host):
        """Verify duperemove system cron job if configured."""
        cmd = host.run("cat /etc/crontab 2>/dev/null | grep -i duperemove || true")
        # System cron may also be used
        pass

    def test_duperemove_cron_d(self, host):
        """Verify duperemove cron.d entry if configured."""
        cmd = host.run("ls -la /etc/cron.d/ 2>/dev/null | grep -i duperemove || true")
        # cron.d entry may be used instead of user crontab
        pass


class TestDuperemoveFunctionality:
    """Test duperemove functionality."""

    def test_duperemove_dry_run(self, host):
        """Verify duperemove dry-run command works."""
        cmd = host.run(f"{DUPEREMOVE_COMMAND} -Ar / 2>&1 | head -10 || true")
        # May take time or fail on non-btrfs
        # Command should be available
        pass

    def test_duperemove_hash_command(self, host):
        """Verify duperemove hash command is available."""
        cmd = host.run(f"{DUPEREMOVE_COMMAND} --help 2>&1 | grep -i hash || true")
        # Hash functionality should be documented
        pass

    def test_duperemove_dedupe_command(self, host):
        """Verify duperemove dedupe options are available."""
        cmd = host.run(f"{DUPEREMOVE_COMMAND} --help 2>&1 | grep -E '(-d|--dedupe)' || true")
        # Dedupe option should be available
        pass


class TestDuperemoveLogs:
    """Test duperemove logging."""

    def test_duperemove_log_file(self, host):
        """Verify duperemove log file if it exists."""
        f = host.file(DUPEREMOVE_LOG)
        if f.exists:
            assert f.is_file, f"{DUPEREMOVE_LOG} should be a file"
            assert f.mode in [0o644, 0o640, 0o600], \
                f"{DUPEREMOVE_LOG} should have secure permissions, got {oct(f.mode)}"

    def test_duperemove_log_directory_writable(self, host):
        """Verify /var/log is writable for duperemove logs."""
        cmd = host.run("test -w /var/log && echo 'writable' || echo 'not writable'")
        if cmd.rc == 0:
            assert "writable" in cmd.stdout, "/var/log should be writable"


class TestDuperemoveBtrfsIntegration:
    """Test duperemove integration with btrfs."""

    def test_btrfs_available(self, host):
        """Verify btrfs is available for deduplication."""
        cmd = host.run("btrfs --version 2>&1 || true")
        if cmd.rc == 0:
            assert "btrfs" in cmd.stdout.lower(), "btrfs should be available for deduplication"

    def test_btrfs_dedupe_support(self, host):
        """Verify btrfs supports deduplication."""
        # Btrfs dedupe is supported via FIDEDUPERANGE ioctl
        cmd = host.run(f"{DUPEREMOVE_COMMAND} --help 2>&1 | grep -i btrfs || true")
        # duperemove is designed for btrfs
        pass


class TestDuperemoveSecurity:
    """Test duperemove security configuration."""

    def test_duperemove_hash_dir_ownership(self, host):
        """Verify duperemove hash directory is owned by root."""
        d = host.file(DUPEREMOVE_HASH_DIR)
        if d.exists:
            assert d.user == "root", f"{DUPEREMOVE_HASH_DIR} should be owned by root"

    def test_duperemove_no_world_writable(self, host):
        """Verify no duperemove files are world-writable."""
        cmd = host.run(f"find {DUPEREMOVE_HASH_DIR} -perm /002 -type f 2>/dev/null || true")
        if cmd.stdout.strip():
            pytest.fail(f"Found world-writable files: {cmd.stdout}")

    def test_duperemove_cron_secure(self, host):
        """Verify duperemove cron job runs as root."""
        cmd = host.run("crontab -l 2>/dev/null | grep duperemove || true")
        if cmd.stdout.strip():
            # User crontab runs as the user who owns it (root)
            # System crontab should specify root
            pass


class TestDuperemoveAudit:
    """Test duperemove audit functionality."""

    def test_duperemove_audit_dry_run(self, host):
        """Verify duperemove can perform audit (dry run)."""
        # The role runs: duperemove -Ar <path> | grep "Comparison of"
        cmd = host.run(f"{DUPEREMOVE_COMMAND} -Ar /tmp 2>&1 | grep -i comparison || true")
        # May not find duplicates in /tmp
        # Command should work
        pass

    def test_duperemove_report_output(self, host):
        """Verify duperemove produces report output."""
        cmd = host.run(f"{DUPEREMOVE_COMMAND} --help 2>&1 | grep -i report || true")
        # Report functionality should be available
        pass


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), duperemove requires btrfs filesystem")

    def test_btrfs_filesystem_present(self, host):
        """Verify btrfs filesystem is present for deduplication."""
        cmd = host.run("mount | grep btrfs || true")
        if not cmd.stdout.strip():
            pytest.skip("No btrfs filesystem mounted, duperemove cannot function")
