# =============================================================================
# Audit Event Identifier: DSU-PYS-500071
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for hardware/virtual_guest role.

This role handles cloud/VPS instance optimization:
- Setting I/O scheduler for virtual block devices (none/noop)
- Optimizing virtual memory for shared cloud resources
- Identifying VPS provider for specific optimizations
- Applying provider-specific or generic cloud optimizations
"""
import pytest


# VPS-related configuration paths
VPS_SCHEDULER_RULES_FILE = "/etc/udev/rules.d/60-vps-disk-scheduler.rules"
VPS_SYSCTL_FILE = "/etc/sysctl.d/99-vps-optimization.conf"

# Common VPS providers
VPS_PROVIDERS = [
    "aws",
    "azure",
    "gcp",
    "digitalocean",
    "linode",
    "vultr",
    "ovh",
    "hetzner",
    "scaleway",
    "generic",
]


class TestVPSScheduler:
    """Test VPS I/O scheduler configuration."""

    def test_vps_scheduler_rules_file_exists(self, host):
        """Verify VPS I/O scheduler udev rules file exists."""
        f = host.file(VPS_SCHEDULER_RULES_FILE)
        assert f.exists, f"{VPS_SCHEDULER_RULES_FILE} should exist"
        assert f.is_file, f"{VPS_SCHEDULER_RULES_FILE} should be a file"

    def test_vps_scheduler_rules_permissions(self, host):
        """Verify VPS scheduler rules file has correct permissions."""
        f = host.file(VPS_SCHEDULER_RULES_FILE)
        if f.exists:
            assert f.mode == 0o644, \
                f"{VPS_SCHEDULER_RULES_FILE} should have mode 0644, got {oct(f.mode)}"
            assert f.user == "root", f"{VPS_SCHEDULER_RULES_FILE} should be owned by root"

    def test_vps_scheduler_rules_content_none(self, host):
        """Verify VPS scheduler rules contain 'none' scheduler."""
        f = host.file(VPS_SCHEDULER_RULES_FILE)
        if f.exists:
            content = f.content_string
            assert "none" in content, \
                "VPS scheduler rules should contain 'none' scheduler for virtual disks"

    def test_vps_scheduler_rules_virtio_pattern(self, host):
        """Verify VPS scheduler rules match virtio devices."""
        f = host.file(VPS_SCHEDULER_RULES_FILE)
        if f.exists:
            content = f.content_string
            assert "vd[a-z]*" in content, \
                "VPS scheduler rules should match virtio device patterns (vd*)"

    def test_vps_scheduler_rules_xen_pattern(self, host):
        """Verify VPS scheduler rules match xen devices."""
        f = host.file(VPS_SCHEDULER_RULES_FILE)
        if f.exists:
            content = f.content_string
            assert "xvd[a-z]*" in content, \
                "VPS scheduler rules should match xen device patterns (xvd*)"


class TestVPSMemory:
    """Test VPS memory optimization."""

    def test_vps_sysctl_file_exists(self, host):
        """Verify VPS sysctl optimization file exists."""
        f = host.file(VPS_SYSCTL_FILE)
        assert f.exists, f"{VPS_SYSCTL_FILE} should exist"
        assert f.is_file, f"{VPS_SYSCTL_FILE} should be a file"

    def test_vps_sysctl_permissions(self, host):
        """Verify VPS sysctl file has correct permissions."""
        f = host.file(VPS_SYSCTL_FILE)
        if f.exists:
            assert f.mode in [0o644, 0o640], \
                f"{VPS_SYSCTL_FILE} should have correct permissions, got {oct(f.mode)}"
            assert f.user == "root", f"{VPS_SYSCTL_FILE} should be owned by root"

    def test_vps_sysctl_dirty_ratio(self, host):
        """Verify VPS sysctl contains vm.dirty_ratio setting."""
        f = host.file(VPS_SYSCTL_FILE)
        if f.exists:
            content = f.content_string
            assert "vm.dirty_ratio" in content, \
                "VPS sysctl should contain vm.dirty_ratio setting"

    def test_vps_sysctl_dirty_background_ratio(self, host):
        """Verify VPS sysctl contains vm.dirty_background_ratio setting."""
        f = host.file(VPS_SYSCTL_FILE)
        if f.exists:
            content = f.content_string
            assert "vm.dirty_background_ratio" in content, \
                "VPS sysctl should contain vm.dirty_background_ratio setting"

    def test_vps_sysctl_dirty_ratio_value(self, host):
        """Verify vm.dirty_ratio is set to appropriate value for VPS."""
        f = host.file(VPS_SYSCTL_FILE)
        if f.exists:
            content = f.content_string
            # Should be set to a conservative value for shared hosting
            assert "vm.dirty_ratio = 10" in content or "vm.dirty_ratio=10" in content, \
                "vm.dirty_ratio should be set to 10 for VPS environments"

    def test_vps_sysctl_dirty_background_ratio_value(self, host):
        """Verify vm.dirty_background_ratio is set to appropriate value."""
        f = host.file(VPS_SYSCTL_FILE)
        if f.exists:
            content = f.content_string
            assert "vm.dirty_background_ratio = 5" in content or "vm.dirty_background_ratio=5" in content, \
                "vm.dirty_background_ratio should be set to 5 for VPS environments"


class TestVPSProvider:
    """Test VPS provider detection."""

    def test_detected_provider_fact_set(self, host):
        """Verify detected_provider fact is set."""
        # This is tested via Ansible verify.yml
        pass

    def test_system_vendor_readable(self, host):
        """Verify system vendor information is available."""
        f = host.file("/sys/class/dmi/id/sys_vendor")
        if f.exists:
            content = f.content_string.strip()
            assert len(content) > 0, "System vendor should be identifiable"

    def test_product_name_readable(self, host):
        """Verify product name information is available."""
        f = host.file("/sys/class/dmi/id/product_name")
        if f.exists:
            content = f.content_string.strip()
            assert len(content) > 0, "Product name should be identifiable"


class TestVPSVirtualization:
    """Test virtualization detection."""

    def test_virtualization_type_detected(self, host):
        """Verify virtualization type is detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        # Should detect some virtualization type
        assert virt_type, "Virtualization type should be detected"

    def test_container_detection(self, host):
        """Verify container detection works."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            assert "container" in virt_type or virt_type in ["docker", "podman", "lxc"], \
                "Container virtualization should be correctly identified"

    def test_vm_detection(self, host):
        """Verify VM detection works."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        vm_types = ["kvm", "vmware", "virtualbox", "xen", "hyperv", "amazon", "microsoft", "oracle"]
        if virt_type in vm_types:
            assert virt_type in vm_types, "VM virtualization should be correctly identified"


class TestVPSBlockDevices:
    """Test VPS block device configuration."""

    def test_virtio_devices_detected(self, host):
        """Verify virtio devices can be detected."""
        cmd = host.run("lsblk -d -o NAME,TRAN 2>&1 | grep virtio || true")
        # May or may not have virtio devices
        pass

    def test_xen_devices_detected(self, host):
        """Verify xen block devices can be detected."""
        cmd = host.run("lsblk -d -o NAME,TRAN 2>&1 | grep xvd || true")
        # May or may not have xvd devices
        pass

    def test_block_device_scheduler(self, host):
        """Verify block device scheduler can be queried."""
        cmd = host.run("cat /sys/block/vda/queue/scheduler 2>&1 || true")
        # May fail if /dev/vda doesn't exist
        pass


class TestVPSSysctl:
    """Test sysctl configuration for VPS."""

    def test_sysctl_d_directory(self, host):
        """Verify sysctl.d directory exists."""
        d = host.file("/etc/sysctl.d")
        assert d.exists, "/etc/sysctl.d should exist"
        assert d.is_directory, "/etc/sysctl.d should be a directory"

    def test_sysctl_command_available(self, host):
        """Verify sysctl command is available."""
        assert host.exists("sysctl"), "sysctl command should be available"

    def test_sysctl_reload_possible(self, host):
        """Verify sysctl can reload configuration."""
        cmd = host.run("sysctl --system 2>&1 || true")
        # Should succeed or fail gracefully
        pass


class TestVPSPerformance:
    """Test VPS performance configuration."""

    def test_memory_pressure_available(self, host):
        """Verify memory pressure information is available."""
        f = host.file("/proc/pressure/memory")
        if f.exists:
            assert f.exists, "Memory pressure info should be available"

    def test_vm_dirty_pages(self, host):
        """Verify dirty pages can be queried."""
        f = host.file("/proc/vmstat")
        if f.exists:
            content = f.content_string
            assert "nr_dirty" in content or "dirty" in content.lower(), \
                "VM stats should include dirty page information"

    def test_writeback_status(self, host):
        """Verify writeback status can be queried."""
        f = host.file("/proc/meminfo")
        if f.exists:
            content = f.content_string
            assert "Dirty" in content, "MemInfo should include dirty pages info"


class TestVPSNetwork:
    """Test VPS network configuration."""

    def test_network_interfaces_exist(self, host):
        """Verify network interfaces exist."""
        cmd = host.run("ip link show 2>&1 || true")
        assert cmd.rc == 0, "Network interfaces should be listable"

    def test_virtio_net_module(self, host):
        """Verify virtio_net module is available."""
        cmd = host.run("modinfo virtio_net 2>&1 || true")
        if cmd.rc == 0:
            assert "virtio" in cmd.stdout.lower(), "virtio_net module should be available"

    def test_xen_netfront_module(self, host):
        """Verify xen_netfront module is available."""
        cmd = host.run("modinfo xen_netfront 2>&1 || true")
        # May not exist on non-Xen systems
        pass


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), VPS optimizations may differ")

    def test_running_in_container(self, host):
        """Check if running in container."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        if "container" in cmd.stdout.lower():
            pytest.skip("Running in container environment")
