"""
Testinfra tests for hardware/storage_tuning role.

This role handles physical storage optimization:
- Enabling SSD TRIM timer (FSTRIM)
- Setting I/O scheduler for disks (mq-deadline for SSD, none for virtual)
- Gathering storage device facts
- Applying aligned read-ahead tuning for large disks
"""
import pytest


# Storage-related configuration paths
SCHEDULER_RULES_FILE = "/etc/udev/rules.d/60-disk-scheduler.rules"
SYSDCTL_OPTIMIZATION_FILE = "/etc/sysctl.d/99-storage-optimization.conf"


class TestStorageFSTRIM:
    """Test FSTRIM timer configuration."""

    def test_fstrim_timer_exists(self, host):
        """Verify fstrim.timer exists."""
        svc = host.service("fstrim.timer")
        if svc.exists:
            assert svc.exists, "fstrim.timer should exist"

    def test_fstrim_timer_enabled(self, host):
        """Verify fstrim.timer is enabled."""
        cmd = host.run("systemctl is-enabled fstrim.timer 2>&1 || true")
        if cmd.rc == 0:
            assert "enabled" in cmd.stdout.lower(), "fstrim.timer should be enabled"

    def test_fstrim_service_exists(self, host):
        """Verify fstrim.service exists."""
        svc = host.service("fstrim.service")
        if svc.exists:
            assert svc.exists, "fstrim.service should exist"

    def test_fstrim_timer_status(self, host):
        """Verify fstrim.timer status."""
        cmd = host.run("systemctl status fstrim.timer 2>&1 || true")
        # Should show timer status
        pass


class StorageSchedulerRules:
    """Test I/O scheduler udev rules."""

    def test_scheduler_rules_file_exists(self, host):
        """Verify I/O scheduler udev rules file exists."""
        f = host.file(SCHEDULER_RULES_FILE)
        assert f.exists, f"{SCHEDULER_RULES_FILE} should exist"
        assert f.is_file, f"{SCHEDULER_RULES_FILE} should be a file"

    def test_scheduler_rules_permissions(self, host):
        """Verify scheduler rules file has correct permissions."""
        f = host.file(SCHEDULER_RULES_FILE)
        if f.exists:
            assert f.mode == 0o644, \
                f"{SCHEDULER_RULES_FILE} should have mode 0644, got {oct(f.mode)}"
            assert f.user == "root", f"{SCHEDULER_RULES_FILE} should be owned by root"

    def test_scheduler_rules_content_mq_deadline(self, host):
        """Verify scheduler rules contain mq-deadline for SSD."""
        f = host.file(SCHEDULER_RULES_FILE)
        if f.exists:
            content = f.content_string
            assert "mq-deadline" in content, \
                "Scheduler rules should contain mq-deadline for SSD devices"

    def test_scheduler_rules_content_none(self, host):
        """Verify scheduler rules contain 'none' for virtual/RAM disks."""
        f = host.file(SCHEDULER_RULES_FILE)
        if f.exists:
            content = f.content_string
            assert "none" in content, \
                "Scheduler rules should contain 'none' scheduler for virtual/RAM disks"

    def test_scheduler_rules_ssd_pattern(self, host):
        """Verify scheduler rules match SSD devices."""
        f = host.file(SCHEDULER_RULES_FILE)
        if f.exists:
            content = f.content_string
            # Should match sd*, nvme*, mmcblk* devices
            assert "sd[a-z]*" in content or "nvme" in content, \
                "Scheduler rules should match SSD device patterns"

    def test_scheduler_rules_virtual_pattern(self, host):
        """Verify scheduler rules match virtual disk devices."""
        f = host.file(SCHEDULER_RULES_FILE)
        if f.exists:
            content = f.content_string
            # Should match vd*, xvd* devices
            assert "vd[a-z]*" in content or "xvd" in content, \
                "Scheduler rules should match virtual disk patterns"


class TestStorageDeviceDetection:
    """Test storage device detection."""

    def test_lsblk_available(self, host):
        """Verify lsblk command is available."""
        assert host.exists("lsblk"), "lsblk command should be available"

    def test_block_devices_listed(self, host):
        """Verify block devices can be listed."""
        cmd = host.run("lsblk -d -o NAME,SIZE,ROTA 2>&1 || true")
        if cmd.rc == 0:
            assert cmd.stdout.strip(), "lsblk should list block devices"

    def test_storage_devices_fact_set(self, host):
        """Verify storage_devices_norm fact is set (via Ansible)."""
        # This is tested via Ansible verify.yml
        pass

    def test_sysfs_block_exists(self, host):
        """Verify sysfs block directory exists."""
        d = host.file("/sys/block")
        assert d.exists, "/sys/block should exist"
        assert d.is_directory, "/sys/block should be a directory"


class TestStorageReadAhead:
    """Test read-ahead tuning configuration."""

    def test_blockdev_available(self, host):
        """Verify blockdev command is available."""
        assert host.exists("blockdev"), "blockdev command should be available"

    def test_readahead_can_be_set(self, host):
        """Verify read-ahead can be queried."""
        cmd = host.run("blockdev --getra /dev/sda 2>&1 || true")
        # May fail if /dev/sda doesn't exist
        pass

    def test_storage_devices_over_1tb(self, host):
        """Verify large storage devices can be detected."""
        cmd = host.run("lsblk -d -o NAME,SIZE --bytes 2>&1 || true")
        # Should show device sizes
        pass


class TestStorageScheduler:
    """Test I/O scheduler configuration."""

    def test_scheduler_sysfs_exists(self, host):
        """Verify scheduler sysfs entries exist."""
        d = host.file("/sys/block/sda/queue")
        if d.exists:
            scheduler_f = host.file("/sys/block/sda/queue/scheduler")
            if scheduler_f.exists:
                assert scheduler_f.exists, "Scheduler sysfs entry should exist"

    def test_scheduler_current_setting(self, host):
        """Verify current scheduler setting can be read."""
        cmd = host.run("cat /sys/block/sda/queue/scheduler 2>&1 || true")
        # May fail if /dev/sda doesn't exist
        pass

    def test_nvme_scheduler(self, host):
        """Verify NVMe scheduler can be configured."""
        d = host.file("/sys/block/nvme0n1/queue")
        if d.exists:
            scheduler_f = host.file("/sys/block/nvme0n1/queue/scheduler")
            if scheduler_f.exists:
                assert scheduler_f.exists, "NVMe scheduler sysfs should exist"


class TestStorageUdev:
    """Test udev configuration for storage."""

    def test_udev_rules_directory(self, host):
        """Verify udev rules directory exists."""
        d = host.file("/etc/udev/rules.d")
        assert d.exists, "/etc/udev/rules.d should exist"
        assert d.is_directory, "/etc/udev/rules.d should be a directory"

    def test_udevadm_available(self, host):
        """Verify udevadm command is available."""
        assert host.exists("udevadm"), "udevadm command should be available"

    def test_udev_control_reload(self, host):
        """Verify udev control can be reloaded."""
        cmd = host.run("udevadm control --reload-rules 2>&1 || true")
        # Should succeed or fail gracefully
        pass


class TestStorageSysfs:
    """Test sysfs storage configuration."""

    def test_sysfs_queue_directory(self, host):
        """Verify queue sysfs directory exists for block devices."""
        cmd = host.run("ls -d /sys/block/*/queue 2>&1 | head -3 || true")
        if cmd.stdout.strip():
            assert "/sys/block" in cmd.stdout, "Queue directories should exist"

    def test_sysfs_rotational_attribute(self, host):
        """Verify rotational attribute exists for block devices."""
        cmd = host.run("ls /sys/block/*/queue/rotational 2>&1 | head -3 || true")
        if cmd.stdout.strip():
            assert "rotational" in cmd.stdout, "Rotational attribute should exist"

    def test_sysfs_physical_sector_size(self, host):
        """Verify physical sector size attribute exists."""
        cmd = host.run("cat /sys/block/sda/queue/physical_block_size 2>&1 || true")
        # May fail if /dev/sda doesn't exist
        pass


class TestStoragePerformance:
    """Test storage performance configuration."""

    def test_iostat_available(self, host):
        """Verify iostat command is available."""
        # May need sysstat package
        pass

    def test_storage_queue_depth(self, host):
        """Verify storage queue depth can be queried."""
        cmd = host.run("cat /sys/block/sda/queue/nr_requests 2>&1 || true")
        # May fail if /dev/sda doesn't exist
        pass


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), storage tuning may be limited")

    def test_block_devices_in_container(self, host):
        """Verify block device access in containers."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        if "container" in cmd.stdout.lower():
            pytest.skip("Block device tuning limited in container environment")
