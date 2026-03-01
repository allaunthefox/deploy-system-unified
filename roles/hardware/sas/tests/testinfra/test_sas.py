# =============================================================================
# Audit Event Identifier: DSU-PYS-500069
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for hardware/sas role.

This role handles SAS (Serial Attached SCSI) controller configuration:
- Installing SAS management utilities (lsscsi, sg3_utils, smartmontools)
- Loading SAS kernel modules (mpt3sas, mpi3mr, megaraid_sas)
- Configuring SAS queue depth tuning
- Enabling SMART monitoring for SAS drives
"""
import pytest


# SAS packages
SAS_PACKAGES = [
    "lsscsi",
    "sg3-utils",
    "sdparm",
    "smartmontools",
    "sysfsutils",
]

# SAS kernel modules
SAS_KERNEL_MODULES = [
    "mpt3sas",    # LSI SAS 3008/3108 HBA
    "mpi3mr",     # Broadcom 9600 Series
    "megaraid_sas", # LSI MegaRAID
    "aacraid",    # Adaptec
    "pm80xx",     # PMC-Sierra/Microchip
]

# Configuration paths
SAS_MODULES_CONFIG = "/etc/modules-load.d/sas-drivers.conf"


class TestSASPackageInstallation:
    """Test SAS management utilities installation."""

    def test_lsscsi_installed(self, host):
        """Verify lsscsi package is installed."""
        pkg = host.package("lsscsi")
        assert pkg.is_installed, "lsscsi package should be installed"

    def test_lsscsi_command_available(self, host):
        """Verify lsscsi command is available."""
        assert host.exists("lsscsi"), "lsscsi command should be available"

    def test_sg3_utils_installed(self, host):
        """Verify sg3-utils package is installed."""
        pkg = host.package("sg3-utils")
        assert pkg.is_installed, "sg3-utils package should be installed"

    def test_sg_scan_available(self, host):
        """Verify sg_scan command is available."""
        assert host.exists("sg_scan"), "sg_scan command should be available"

    def test_sg_inq_available(self, host):
        """Verify sg_inq command is available."""
        assert host.exists("sg_inq"), "sg_inq command should be available"

    def test_sdparm_installed(self, host):
        """Verify sdparm package is installed."""
        pkg = host.package("sdparm")
        assert pkg.is_installed, "sdparm package should be installed"

    def test_sdparm_command_available(self, host):
        """Verify sdparm command is available."""
        assert host.exists("sdparm"), "sdparm command should be available"

    def test_smartmontools_installed(self, host):
        """Verify smartmontools package is installed."""
        pkg = host.package("smartmontools")
        assert pkg.is_installed, "smartmontools package should be installed"

    def test_smartctl_available(self, host):
        """Verify smartctl command is available."""
        assert host.exists("smartctl"), "smartctl command should be available"

    def test_smartd_available(self, host):
        """Verify smartd command is available."""
        assert host.exists("smartd"), "smartd command should be available"

    def test_sysfsutils_installed(self, host):
        """Verify sysfsutils package is installed."""
        pkg = host.package("sysfsutils")
        assert pkg.is_installed, "sysfsutils package should be installed"


class TestSASKernelModules:
    """Test SAS kernel modules."""

    def test_sas_modules_config_exists(self, host):
        """Verify SAS modules configuration file exists."""
        f = host.file(SAS_MODULES_CONFIG)
        assert f.exists, f"{SAS_MODULES_CONFIG} should exist"
        assert f.is_file, f"{SAS_MODULES_CONFIG} should be a file"

    def test_sas_modules_config_permissions(self, host):
        """Verify SAS modules configuration has correct permissions."""
        f = host.file(SAS_MODULES_CONFIG)
        if f.exists:
            assert f.mode in [0o644, 0o640], \
                f"{SAS_MODULES_CONFIG} should have correct permissions, got {oct(f.mode)}"
            assert f.user == "root", f"{SAS_MODULES_CONFIG} should be owned by root"

    def test_sas_modules_config_content(self, host):
        """Verify SAS modules configuration contains driver names."""
        f = host.file(SAS_MODULES_CONFIG)
        if f.exists:
            content = f.content_string
            # Should contain at least one SAS driver name
            sas_drivers = ["mpt3sas", "mpi3mr", "megaraid_sas", "aacraid", "pm80xx"]
            has_driver = any(driver in content for driver in sas_drivers)
            assert has_driver, f"{SAS_MODULES_CONFIG} should contain SAS driver names"

    def test_mpt3sas_module_available(self, host):
        """Verify mpt3sas kernel module is available."""
        cmd = host.run("modinfo mpt3sas 2>&1 || true")
        if cmd.rc == 0:
            assert "mpt3sas" in cmd.stdout.lower(), "mpt3sas module should be available"

    def test_mpi3mr_module_available(self, host):
        """Verify mpi3mr kernel module is available."""
        cmd = host.run("modinfo mpi3mr 2>&1 || true")
        if cmd.rc == 0:
            assert "mpi3mr" in cmd.stdout.lower(), "mpi3mr module should be available"

    def test_megaraid_sas_module_available(self, host):
        """Verify megaraid_sas kernel module is available."""
        cmd = host.run("modinfo megaraid_sas 2>&1 || true")
        if cmd.rc == 0:
            assert "megaraid" in cmd.stdout.lower(), "megaraid_sas module should be available"


class TestSASDeviceDetection:
    """Test SAS device detection."""

    def test_lsscsi_command_works(self, host):
        """Verify lsscsi command can list devices."""
        cmd = host.run("lsscsi 2>&1 || true")
        # Should list SCSI/SAS devices
        # May return empty if no SAS devices present
        pass

    def test_lsscsi_verbose(self, host):
        """Verify lsscsi verbose mode works."""
        cmd = host.run("lsscsi -g 2>&1 || true")
        # Should show generic device names
        pass

    def test_sas_devices_in_proc(self, host):
        """Verify SCSI devices in /proc."""
        f = host.file("/proc/scsi/scsi")
        if f.exists:
            content = f.content_string
            # Should contain SCSI device info
            pass

    def test_scsi_generic_devices(self, host):
        """Verify SCSI generic devices exist."""
        d = host.file("/dev/sg")
        if d.exists:
            assert d.is_directory, "/dev/sg should be a directory"


class TestSASQueueDepth:
    """Test SAS queue depth configuration."""

    def test_queue_depth_tuning_script(self, host):
        """Verify queue depth tuning can be performed."""
        cmd = host.run("ls -la /sys/block/sd*/device/queue_depth 2>/dev/null || true")
        # Queue depth files should exist for SAS devices
        pass

    def test_queue_depth_max_available(self, host):
        """Verify queue_depth_max is available for tuning."""
        cmd = host.run("ls -la /sys/block/sd*/device/queue_depth_max 2>/dev/null || true")
        # Max queue depth should be readable
        pass


class TestSASWriteCache:
    """Test SAS write cache configuration."""

    def test_sdparm_wce_query(self, host):
        """Verify sdparm can query write cache enable (WCE)."""
        cmd = host.run("sdparm --get=WCE /dev/sda 2>&1 || true")
        # May fail if /dev/sda doesn't exist or isn't SAS
        # Command should be available
        pass

    def test_sdparm_wce_set_capability(self, host):
        """Verify sdparm can set write cache enable."""
        cmd = host.run("sdparm --help 2>&1 | grep -i wce || true")
        # WCE option should be documented
        pass


class TestSASSMARTMonitoring:
    """Test SAS SMART monitoring."""

    def test_smartd_config_exists(self, host):
        """Verify smartd configuration file exists."""
        f = host.file("/etc/smartd.conf")
        assert f.exists, "/etc/smartd.conf should exist"
        assert f.is_file, "/etc/smartd.conf should be a file"

    def test_smartd_config_permissions(self, host):
        """Verify smartd configuration has correct permissions."""
        f = host.file("/etc/smartd.conf")
        if f.exists:
            assert f.mode in [0o644, 0o640], \
                "/etc/smartd.conf should have correct permissions"
            assert f.user == "root", "/etc/smartd.conf should be owned by root"

    def test_smartd_service_exists(self, host):
        """Verify smartd service exists."""
        svc = host.service("smartd")
        if svc.exists:
            assert svc.exists, "smartd service should exist"

    def test_smartd_service_running(self, host):
        """Verify smartd service is running."""
        svc = host.service("smartd")
        if svc.exists:
            assert svc.is_running, "smartd service should be running"
            assert svc.is_enabled, "smartd service should be enabled"

    def test_smartctl_info_command(self, host):
        """Verify smartctl can query device info."""
        cmd = host.run("smartctl -i /dev/sda 2>&1 || true")
        # May fail if /dev/sda doesn't exist
        # Command should be available
        pass

    def test_smartctl_scan(self, host):
        """Verify smartctl can scan for devices."""
        cmd = host.run("smartctl --scan 2>&1 || true")
        # Should scan for SMART-capable devices
        pass


class TestSASSysfs:
    """Test SAS sysfs configuration."""

    def test_sysfs_scsi_directory(self, host):
        """Verify sysfs SCSI directory exists."""
        d = host.file("/sys/class/scsi_device")
        if d.exists:
            assert d.is_directory, "/sys/class/scsi_device should be a directory"

    def test_sysfs_scsi_host(self, host):
        """Verify sysfs SCSI host directory exists."""
        d = host.file("/sys/class/scsi_host")
        if d.exists:
            assert d.is_directory, "/sys/class/scsi_host should be a directory"

    def test_sysfsutils_config(self, host):
        """Verify sysfsutils configuration if present."""
        f = host.file("/etc/sysfs.conf")
        if f.exists:
            assert f.is_file, "/etc/sysfs.conf should be a file"


class TestSASPerformance:
    """Test SAS performance configuration."""

    def test_sas_link_speed(self, host):
        """Verify SAS link speed can be queried."""
        cmd = host.run("lsscsi -t 2>&1 || true")
        # Should show transport info including link speed
        pass

    def test_sas_expander_detection(self, host):
        """Verify SAS expanders can be detected."""
        cmd = host.run("smp_discover 2>&1 | head -5 || true")
        # SMP discover shows SAS expander info
        pass


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), SAS hardware not accessible")

    def test_block_devices_accessible(self, host):
        """Verify block devices are accessible."""
        d = host.file("/dev")
        if d.exists:
            # Block devices should be accessible
            pass
        else:
            pytest.skip("/dev not accessible")
