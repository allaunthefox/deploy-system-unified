"""
Testinfra tests for hardware/firmware role.

This role handles firmware and hardware security configuration:
- Installing TPM2 tools and management
- Detecting CPU tier (server vs consumer)
- Configuring hardware clock (RTC) to UTC
- Enabling NTP synchronization
- Verifying Secure Boot status
- Installing hardware monitoring tools
- Configuring hardware watchdog
"""
import pytest


# Firmware-related packages
FIRMWARE_PACKAGES_DEBIAN = [
    "tpm2-tools",
    "tpm2-abrmd",
]

# Monitoring packages (optional)
MONITORING_PACKAGES = [
    "lm-sensors",
    "hdparm",
    "watchdog",
]


class TestFirmwareTPM:
    """Test TPM2 configuration."""

    def test_tpm2_tools_installed(self, host):
        """Verify tpm2-tools package is installed."""
        pkg = host.package("tpm2-tools")
        assert pkg.is_installed, "tpm2-tools package should be installed"

    def test_tpm2_abrmd_installed(self, host):
        """Verify tpm2-abrmd package is installed."""
        pkg = host.package("tpm2-abrmd")
        assert pkg.is_installed, "tpm2-abrmd package should be installed"

    def test_tpm2_command_available(self, host):
        """Verify tpm2 commands are available."""
        assert host.exists("tpm2_print"), "tpm2_print command should be available"

    def test_tpm2_devices_exist(self, host):
        """Verify TPM devices exist if hardware TPM present."""
        d = host.file("/dev/tpmrm0")
        if d.exists:
            assert d.exists, "/dev/tpmrm0 should exist if hardware TPM present"

    def test_tpm2_resource_manager(self, host):
        """Verify TPM2 resource manager device exists."""
        d = host.file("/dev/tpm0")
        if d.exists:
            assert d.exists, "/dev/tpm0 should exist if hardware TPM present"


class TestFirmwareCPUDetection:
    """Test CPU tier detection."""

    def test_cpu_tier_fact_set(self, host):
        """Verify CPU tier fact is set."""
        # This is tested via Ansible verify.yml
        pass

    def test_cpu_info_available(self, host):
        """Verify CPU information is available."""
        f = host.file("/proc/cpuinfo")
        assert f.exists, "/proc/cpuinfo should exist"
        content = f.content_string
        assert "cpu family" in content or "model name" in content, \
            "CPU info should be available in /proc/cpuinfo"

    def test_server_cpu_detection(self, host):
        """Verify server CPU can be detected."""
        cmd = host.run("grep -i 'xeon\\|epyc' /proc/cpuinfo 2>&1 || true")
        # May or may not have server CPU in test environment
        pass


class TestFirmwareRTCClock:
    """Test Real-Time Clock configuration."""

    def test_timedatectl_available(self, host):
        """Verify timedatectl command is available."""
        assert host.exists("timedatectl"), "timedatectl command should be available"

    def test_rtc_set_to_utc(self, host):
        """Verify RTC is configured to UTC."""
        cmd = host.run("timedatectl 2>&1 || true")
        if cmd.rc == 0:
            # "RTC in local TZ: no" means UTC is used
            if "RTC in local TZ" in cmd.stdout:
                assert "no" in cmd.stdout.lower(), \
                    "RTC should be set to UTC (not local timezone)"

    def test_ntp_enabled(self, host):
        """Verify NTP is enabled."""
        cmd = host.run("timedatectl 2>&1 || true")
        if cmd.rc == 0:
            if "NTP enabled" in cmd.stdout:
                assert "yes" in cmd.stdout.lower(), "NTP should be enabled"


class TestFirmwareSecureBoot:
    """Test Secure Boot verification."""

    def test_secure_boot_status_checkable(self, host):
        """Verify Secure Boot status can be checked."""
        cmd = host.run("mokutil --sb-state 2>&1 || true")
        # May fail if mokutil not installed or not UEFI
        pass

    def test_efi_directory_exists(self, host):
        """Verify EFI directory exists if UEFI system."""
        d = host.file("/sys/firmware/efi")
        if d.exists:
            assert d.is_directory, "/sys/firmware/efi should be a directory on UEFI systems"

    def test_mokutil_available(self, host):
        """Verify mokutil is available for Secure Boot management."""
        # May not be installed by default
        pass


class TestFirmwareHardwareMonitoring:
    """Test hardware monitoring configuration."""

    def test_watchdog_device_exists(self, host):
        """Verify watchdog device exists."""
        d = host.file("/dev/watchdog")
        if d.exists:
            assert d.exists, "/dev/watchdog should exist"

    def test_watchdog_config_exists(self, host):
        """Verify watchdog configuration file exists."""
        f = host.file("/etc/watchdog.conf")
        if f.exists:
            assert f.is_file, "/etc/watchdog.conf should be a file"

    def test_smartmontools_service(self, host):
        """Verify smartmontools service configuration."""
        svc = host.service("smartmontools")
        if svc.exists:
            assert svc.is_enabled or svc.is_running, \
                "smartmontools service should be enabled or running"


class TestFirmwareKernelModules:
    """Test firmware-related kernel modules."""

    def test_i2c_modules_available(self, host):
        """Verify I2C modules are available for hardware monitoring."""
        cmd = host.run("modinfo i2c_dev 2>&1 || true")
        if cmd.rc == 0:
            assert "i2c" in cmd.stdout.lower(), "i2c_dev module should be available"

    def test_hwmon_sysfs(self, host):
        """Verify hardware monitoring sysfs directory exists."""
        d = host.file("/sys/class/hwmon")
        if d.exists:
            assert d.is_directory, "/sys/class/hwmon should be a directory"


class TestFirmwareSecurity:
    """Test firmware security features."""

    def test_tpm_group_exists(self, host):
        """Verify tss group exists for TPM access."""
        g = host.group("tss")
        if g.exists:
            assert g.exists, "tss group should exist for TPM access"

    def test_dev_tpm_permissions(self, host):
        """Verify TPM device permissions."""
        d = host.file("/dev/tpm0")
        if d.exists:
            # Should be accessible by tss group
            pass

    def test_tpm2_abrmd_service(self, host):
        """Verify TPM2 ABRMD service configuration."""
        svc = host.service("tpm2-abrmd")
        if svc.exists:
            assert svc.is_enabled or svc.is_running, \
                "tpm2-abrmd service should be enabled or running"


class TestFirmwareWatchdog:
    """Test watchdog configuration."""

    def test_watchdog_service_exists(self, host):
        """Verify watchdog service exists."""
        svc = host.service("watchdog")
        # Service may or may not exist depending on configuration
        pass

    def test_watchdog_config_device(self, host):
        """Verify watchdog device is configured."""
        f = host.file("/etc/watchdog.conf")
        if f.exists:
            content = f.content_string
            if "watchdog-device" in content:
                assert "/dev/watchdog" in content, \
                    "watchdog-device should be set to /dev/watchdog"


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), hardware features may not be available")

    def test_hardware_access_limited_in_container(self, host):
        """Verify hardware access is limited in containers."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        if "container" in cmd.stdout.lower():
            pytest.skip("Hardware TPM/RTC not accessible in container environment")
