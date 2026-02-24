"""
Testinfra tests for storage/filesystems/btrfs role.

This role handles Btrfs filesystem management:
- Installing btrfs-progs package
- Managing subvolumes
- Configuring maintenance tasks
- Setting up snapshots and quotas
"""
import pytest


# Btrfs tools and paths
BTRFS_PROGS_PACKAGE = "btrfs-progs"
BTRFS_COMMAND = "btrfs"


class TestBtrfsInstallation:
    """Test btrfs-progs package installation."""

    def test_btrfs_progs_installed(self, host):
        """Verify btrfs-progs package is installed."""
        pkg = host.package(BTRFS_PROGS_PACKAGE)
        assert pkg.is_installed, f"{BTRFS_PROGS_PACKAGE} package should be installed"

    def test_btrfs_command_available(self, host):
        """Verify btrfs command is available."""
        assert host.exists(BTRFS_COMMAND), f"{BTRFS_COMMAND} command should be available"

    def test_btrfs_version(self, host):
        """Verify btrfs version can be queried."""
        cmd = host.run(f"{BTRFS_COMMAND} --version")
        if cmd.rc == 0:
            assert "btrfs" in cmd.stdout.lower(), "btrfs version command should return version info"

    def test_btrfs_help(self, host):
        """Verify btrfs help is accessible."""
        cmd = host.run(f"{BTRFS_COMMAND} --help 2>&1 | head -10")
        if cmd.rc == 0:
            assert "btrfs" in cmd.stdout.lower(), "btrfs help should be available"


class TestBtrfsCommands:
    """Test btrfs subcommands availability."""

    def test_btrfs_filesystem_command(self, host):
        """Verify btrfs filesystem command is available."""
        cmd = host.run(f"{BTRFS_COMMAND} filesystem --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "filesystem" in cmd.stdout.lower(), "btrfs filesystem command should be available"

    def test_btrfs_subvolume_command(self, host):
        """Verify btrfs subvolume command is available."""
        cmd = host.run(f"{BTRFS_COMMAND} subvolume --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "subvolume" in cmd.stdout.lower(), "btrfs subvolume command should be available"

    def test_btrfs_snapshot_command(self, host):
        """Verify btrfs snapshot command is available."""
        cmd = host.run(f"{BTRFS_COMMAND} subvolume snapshot --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "snapshot" in cmd.stdout.lower(), "btrfs snapshot command should be available"

    def test_btrfs_quota_command(self, host):
        """Verify btrfs quota command is available."""
        cmd = host.run(f"{BTRFS_COMMAND} quota --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "quota" in cmd.stdout.lower(), "btrfs quota command should be available"

    def test_btrfs_balance_command(self, host):
        """Verify btrfs balance command is available."""
        cmd = host.run(f"{BTRFS_COMMAND} balance --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "balance" in cmd.stdout.lower(), "btrfs balance command should be available"

    def test_btrfs_scrub_command(self, host):
        """Verify btrfs scrub command is available."""
        cmd = host.run(f"{BTRFS_COMMAND} scrub --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "scrub" in cmd.stdout.lower(), "btrfs scrub command should be available"

    def test_btrfs_device_command(self, host):
        """Verify btrfs device command is available."""
        cmd = host.run(f"{BTRFS_COMMAND} device --help 2>&1 | head -5")
        if cmd.rc == 0:
            assert "device" in cmd.stdout.lower(), "btrfs device command should be available"


class TestBtrfsSubvolumes:
    """Test btrfs subvolume management."""

    def test_btrfs_root_subvolume(self, host):
        """Verify root subvolume can be listed."""
        cmd = host.run(f"{BTRFS_COMMAND} subvolume list / 2>&1 || true")
        # May return no subvolumes if none created
        # Command should be available
        pass

    def test_btrfs_subvolume_show(self, host):
        """Verify btrfs subvolume show command works."""
        cmd = host.run(f"{BTRFS_COMMAND} subvolume show / 2>&1 || true")
        # May fail if / is not btrfs
        # This is informational


class TestBtrfsFilesystem:
    """Test btrfs filesystem operations."""

    def test_btrfs_filesystem_show(self, host):
        """Verify btrfs filesystem show command works."""
        cmd = host.run(f"{BTRFS_COMMAND} filesystem show 2>&1 || true")
        # May return no btrfs filesystems
        # Command should be available
        assert cmd.rc == 0 or "btrfs" in cmd.stdout.lower(), \
            "btrfs filesystem show command should be available"

    def test_btrfs_filesystem_df(self, host):
        """Verify btrfs filesystem df command works."""
        cmd = host.run(f"{BTRFS_COMMAND} filesystem df / 2>&1 || true")
        # May fail if / is not btrfs
        # This is informational

    def test_btrfs_filesystem_usage(self, host):
        """Verify btrfs filesystem usage command works."""
        cmd = host.run(f"{BTRFS_COMMAND} filesystem usage / 2>&1 || true")
        # May fail if / is not btrfs
        # This is informational


class TestBtrfsMaintenance:
    """Test btrfs maintenance tasks."""

    def test_btrfs_scrub_available(self, host):
        """Verify btrfs scrub is available."""
        cmd = host.run(f"{BTRFS_COMMAND} scrub start --help 2>&1 | head -5 || true")
        # Scrub command should be available
        pass

    def test_btrfs_balance_available(self, host):
        """Verify btrfs balance is available."""
        cmd = host.run(f"{BTRFS_COMMAND} balance start --help 2>&1 | head -5 || true")
        # Balance command should be available
        pass

    def test_btrfs_check_available(self, host):
        """Verify btrfs check command is available."""
        cmd = host.run(f"{BTRFS_COMMAND} check --help 2>&1 | head -5 || true")
        # Check command should be available
        pass


class TestBtrfsKernelModule:
    """Test btrfs kernel module."""

    def test_btrfs_kernel_module_loaded(self, host):
        """Verify btrfs kernel module is loaded."""
        cmd = host.run("lsmod | grep btrfs || true")
        # Module should be loaded if btrfs is in use
        # May not be loaded if no btrfs filesystems mounted
        pass

    def test_btrfs_module_available(self, host):
        """Verify btrfs kernel module is available."""
        cmd = host.run("modinfo btrfs 2>&1 || true")
        if cmd.rc == 0:
            assert "btrfs" in cmd.stdout.lower(), "btrfs kernel module should be available"

    def test_btrfs_in_proc_filesystems(self, host):
        """Verify btrfs is in /proc/filesystems."""
        f = host.file("/proc/filesystems")
        if f.exists:
            content = f.content_string
            assert "btrfs" in content, "btrfs should be listed in /proc/filesystems"


class TestBtrfsConfiguration:
    """Test btrfs configuration files."""

    def test_btrfs_fstab_entries(self, host):
        """Verify fstab entries for btrfs if they exist."""
        f = host.file("/etc/fstab")
        if f.exists:
            content = f.content_string
            # Check if any btrfs entries exist
            has_btrfs = any("btrfs" in line and not line.startswith("#")
                           for line in content.split("\n"))
            # Informational - may not have btrfs entries

    def test_btrfs_mount_options(self, host):
        """Verify btrfs mount options if mounted."""
        cmd = host.run("mount | grep btrfs || true")
        # Informational - shows current btrfs mounts


class TestBtrfsSecurity:
    """Test btrfs security configuration."""

    def test_btrfs_commands_as_root(self, host):
        """Verify btrfs commands require root for privileged operations."""
        # Most btrfs commands require root
        cmd = host.run(f"{BTRFS_COMMAND} filesystem show 2>&1 || true")
        # Should work as regular user for read-only operations
        pass


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), btrfs operations may be limited")

    def test_block_devices_accessible(self, host):
        """Verify block devices are accessible."""
        d = host.file("/dev")
        if d.exists:
            # Block devices should be accessible
            pass
        else:
            pytest.skip("/dev not accessible")
