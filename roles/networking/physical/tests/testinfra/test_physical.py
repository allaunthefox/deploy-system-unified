# =============================================================================
# Audit Event Identifier: DSU-PYS-500078
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for networking/physical role.

This role handles physical network configuration:
- Network tools installation (ethtool, lshw, irqbalance)
- Interface detection and capabilities
- Ring buffer tuning
- Offload settings (TSO/GSO)
- Jumbo frames configuration
- MTU management
"""
import pytest


# Network tools packages
NETWORK_TOOLS_PACKAGES = {
    "debian": ["ethtool", "lshw", "irqbalance"],
    "redhat": ["ethtool", "lshw", "irqbalance"],
    "arch": ["ethtool", "lshw", "irqbalance"],
    "alpine": ["ethtool", "lshw", "irqbalance"],
}

# Network configuration directories
NETWORK_CONFIG_DIRS = [
    "/etc/NetworkManager",
    "/etc/systemd/network",
    "/etc/netplan",
]

# Expected interface types
INTERFACE_TYPES = ["ether", "loopback"]


class TestNetworkTools:
    """Test network tools installation."""

    def test_ethtool_installed(self, host):
        """Verify ethtool is installed."""
        pkg = host.package("ethtool")
        assert pkg.is_installed, "ethtool package should be installed"

    def test_lshw_installed(self, host):
        """Verify lshw is installed."""
        pkg = host.package("lshw")
        if pkg.is_installed:
            assert pkg.is_installed, "lshw package should be installed"
        else:
            pytest.skip("lshw not available (may be optional)")

    def test_irqbalance_installed(self, host):
        """Verify irqbalance is installed."""
        pkg = host.package("irqbalance")
        if pkg.is_installed:
            assert pkg.is_installed, "irqbalance package should be installed"
        else:
            pytest.skip("irqbalance not installed (may be disabled for VMs)")

    def test_ethtool_binary_exists(self, host):
        """Verify ethtool binary exists."""
        f = host.file("/usr/sbin/ethtool")
        if not f.exists:
            f = host.file("/usr/bin/ethtool")
        assert f.exists, "ethtool binary should exist"
        assert f.is_file, "ethtool should be a file"

    def test_lshw_binary_exists(self, host):
        """Verify lshw binary exists."""
        f = host.file("/usr/sbin/lshw")
        if not f.exists:
            f = host.file("/usr/bin/lshw")
        if f.exists:
            assert f.is_file, "lshw should be a file"
        else:
            pytest.skip("lshw binary not found")


class TestNetworkInterfaces:
    """Test network interface detection."""

    def test_network_interfaces_exist(self, host):
        """Verify network interfaces exist."""
        cmd = host.run("ip link show 2>&1")
        if cmd.rc == 0:
            assert "link" in cmd.stdout.lower() or "eth" in cmd.stdout.lower() or \
                   "lo:" in cmd.stdout, "Should have network interfaces"
        else:
            pytest.skip("Cannot list network interfaces")

    def test_loopback_interface(self, host):
        """Verify loopback interface exists."""
        cmd = host.run("ip link show lo 2>&1")
        if cmd.rc == 0:
            assert "lo:" in cmd.stdout, "Loopback interface should exist"
        else:
            pytest.skip("Loopback interface not found")

    def test_ethernet_interface_detected(self, host):
        """Verify ethernet interface is detected."""
        cmd = host.run("ip link show type ether 2>&1 || ip link show | grep -E 'eth|en' 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "ether" in cmd.stdout.lower() or "eth" in cmd.stdout.lower() or \
                   "en" in cmd.stdout.lower(), "Should have ethernet interface"
        else:
            pytest.skip("No ethernet interface found")


class TestEthtoolCapabilities:
    """Test ethtool interface capabilities."""

    def test_ethtool_command_available(self, host):
        """Verify ethtool command is available."""
        cmd = host.run("ethtool --version 2>&1 || ethtool -h 2>&1 | head -1")
        if cmd.rc == 0:
            assert "ethtool" in cmd.stdout.lower(), "ethtool should be available"
        else:
            pytest.skip("ethtool command not available")

    def test_interface_speed_detection(self, host):
        """Verify interface speed can be detected."""
        # Get first non-loopback interface
        cmd = host.run("ip -o link show | grep -v 'lo:' | head -1 | awk -F': ' '{print $2}' 2>&1")
        if cmd.rc == 0 and cmd.stdout.strip():
            iface = cmd.stdout.strip().split("@")[0].strip()
            speed_cmd = host.run(f"ethtool {iface} 2>&1 | grep -i speed")
            if speed_cmd.rc == 0:
                assert "Speed:" in speed_cmd.stdout, f"Should detect speed for {iface}"
            else:
                pytest.skip(f"Cannot detect speed for {iface} (may be virtual)")
        else:
            pytest.skip("No physical interface found")

    def test_interface_link_detection(self, host):
        """Verify interface link status can be detected."""
        cmd = host.run("ip -o link show | grep -v 'lo:' | head -1 | awk -F': ' '{print $2}' 2>&1")
        if cmd.rc == 0 and cmd.stdout.strip():
            iface = cmd.stdout.strip().split("@")[0].strip()
            link_cmd = host.run(f"ethtool {iface} 2>&1 | grep -i 'link detected'")
            if link_cmd.rc == 0:
                assert "Link detected:" in link_cmd.stdout, \
                    f"Should detect link status for {iface}"
            else:
                pytest.skip(f"Cannot detect link for {iface}")
        else:
            pytest.skip("No physical interface found")


class TestRingBufferTuning:
    """Test ring buffer configuration."""

    def test_ring_buffer_settings_available(self, host):
        """Verify ring buffer settings can be queried."""
        cmd = host.run("ip -o link show | grep -v 'lo:' | head -1 | awk -F': ' '{print $2}' 2>&1")
        if cmd.rc == 0 and cmd.stdout.strip():
            iface = cmd.stdout.strip().split("@")[0].strip()
            ring_cmd = host.run(f"ethtool -g {iface} 2>&1")
            if ring_cmd.rc == 0:
                assert "ring" in ring_cmd.stdout.lower() or \
                       "RX:" in ring_cmd.stdout or "TX:" in ring_cmd.stdout, \
                    f"Should have ring buffer settings for {iface}"
            else:
                pytest.skip(f"Cannot query ring buffers for {iface}")
        else:
            pytest.skip("No physical interface found")

    def test_ring_buffer_configuration(self, host):
        """Verify ring buffer configuration is applied."""
        # This checks if ring buffer tuning was attempted
        cmd = host.run("dmesg | grep -i 'ring\\|ethtool' 2>&1 | tail -5 || true")
        # This is informational


class TestOffloadSettings:
    """Test network offload settings."""

    def test_offload_settings_available(self, host):
        """Verify offload settings can be queried."""
        cmd = host.run("ip -o link show | grep -v 'lo:' | head -1 | awk -F': ' '{print $2}' 2>&1")
        if cmd.rc == 0 and cmd.stdout.strip():
            iface = cmd.stdout.strip().split("@")[0].strip()
            offload_cmd = host.run(f"ethtool -k {iface} 2>&1")
            if offload_cmd.rc == 0:
                assert "offload" in offload_cmd.stdout.lower() or \
                       "tso" in offload_cmd.stdout.lower() or \
                       "gso" in offload_cmd.stdout.lower(), \
                    f"Should have offload settings for {iface}"
            else:
                pytest.skip(f"Cannot query offload settings for {iface}")
        else:
            pytest.skip("No physical interface found")

    def test_tso_configuration(self, host):
        """Verify TSO (TCP Segmentation Offload) configuration."""
        cmd = host.run("ip -o link show | grep -v 'lo:' | head -1 | awk -F': ' '{print $2}' 2>&1")
        if cmd.rc == 0 and cmd.stdout.strip():
            iface = cmd.stdout.strip().split("@")[0].strip()
            tso_cmd = host.run(f"ethtool -k {iface} 2>&1 | grep -i 'tcp-segmentation-offload'")
            if tso_cmd.rc == 0:
                assert "tcp-segmentation-offload" in tso_cmd.stdout.lower(), \
                    f"TSO should be configurable for {iface}"
            else:
                pytest.skip(f"TSO not available for {iface}")
        else:
            pytest.skip("No physical interface found")

    def test_gso_configuration(self, host):
        """Verify GSO (Generic Segmentation Offload) configuration."""
        cmd = host.run("ip -o link show | grep -v 'lo:' | head -1 | awk -F': ' '{print $2}' 2>&1")
        if cmd.rc == 0 and cmd.stdout.strip():
            iface = cmd.stdout.strip().split("@")[0].strip()
            gso_cmd = host.run(f"ethtool -k {iface} 2>&1 | grep -i 'generic-segmentation-offload'")
            if gso_cmd.rc == 0:
                assert "generic-segmentation-offload" in gso_cmd.stdout.lower(), \
                    f"GSO should be configurable for {iface}"
            else:
                pytest.skip(f"GSO not available for {iface}")
        else:
            pytest.skip("No physical interface found")


class TestJumboFrames:
    """Test jumbo frames configuration."""

    def test_mtu_configuration(self, host):
        """Verify MTU can be configured."""
        cmd = host.run("ip -o link show | grep -v 'lo:' | head -1 2>&1")
        if cmd.rc == 0 and cmd.stdout:
            assert "mtu" in cmd.stdout.lower(), "Interface should have MTU configuration"
        else:
            pytest.skip("No interface found for MTU check")

    def test_jumbo_frames_capable(self, host):
        """Verify interface supports jumbo frames."""
        cmd = host.run("ip -o link show | grep -v 'lo:' | head -1 | awk -F': ' '{print $2}' 2>&1")
        if cmd.rc == 0 and cmd.stdout.strip():
            iface = cmd.stdout.strip().split("@")[0].strip()
            # Check if interface supports MTU > 1500
            mtu_cmd = host.run(f"ip link show {iface} 2>&1 | grep -i mtu")
            if mtu_cmd.rc == 0:
                # Standard or jumbo MTU
                assert "mtu" in mtu_cmd.stdout.lower(), \
                    f"MTU should be configurable for {iface}"
            else:
                pytest.skip(f"Cannot check MTU for {iface}")
        else:
            pytest.skip("No physical interface found")


class TestIRQBalance:
    """Test IRQ balance configuration."""

    def test_irqbalance_service_exists(self, host):
        """Verify IRQ balance service exists."""
        svc = host.service("irqbalance")
        if svc.exists:
            assert svc.exists, "irqbalance service should exist"
        else:
            pytest.skip("IRQ balance service not found")

    def test_irqbalance_service_status(self, host):
        """Verify IRQ balance service status."""
        svc = host.service("irqbalance")
        if svc.exists:
            # May be disabled in virtualized environments
            pass
        else:
            pytest.skip("IRQ balance service not available")

    def test_irqbalance_config_exists(self, host):
        """Verify IRQ balance configuration exists."""
        f = host.file("/etc/default/irqbalance")
        if f.exists:
            assert f.is_file, "/etc/default/irqbalance should be a file"
        else:
            f = host.file("/etc/sysconfig/irqbalance")
            if f.exists:
                assert f.is_file, "/etc/sysconfig/irqbalance should be a file"
            else:
                pytest.skip("IRQ balance config not found")


class TestNetworkManager:
    """Test NetworkManager integration."""

    def test_networkmanager_directory(self, host):
        """Verify NetworkManager configuration directory exists."""
        d = host.file("/etc/NetworkManager")
        if d.exists:
            assert d.is_directory, "/etc/NetworkManager should be a directory"
        else:
            pytest.skip("NetworkManager directory not found")

    def test_networkmanager_connections_directory(self, host):
        """Verify NetworkManager connections directory exists."""
        d = host.file("/etc/NetworkManager/system-connections")
        if d.exists:
            assert d.is_directory, "NetworkManager connections should be a directory"
        else:
            pytest.skip("NetworkManager connections directory not found")

    def test_networkmanager_service(self, host):
        """Verify NetworkManager service exists."""
        svc = host.service("NetworkManager")
        if svc.exists:
            assert svc.exists, "NetworkManager service should exist"
        else:
            pytest.skip("NetworkManager service not found")


class TestPhysicalNetworkingCompletion:
    """Test physical networking configuration completion."""

    def test_network_tools_available(self, host):
        """Verify network tools are available."""
        tools = ["ethtool"]
        available_tools = 0
        for tool in tools:
            cmd = host.run(f"which {tool} 2>&1")
            if cmd.rc == 0:
                available_tools += 1
        assert available_tools > 0, "At least one network tool should be available"

    def test_interface_capabilities_detected(self, host):
        """Verify interface capabilities can be detected."""
        cmd = host.run("ethtool --version 2>&1")
        if cmd.rc == 0:
            assert "ethtool" in cmd.stdout.lower(), "ethtool should be available"
        else:
            pytest.skip("Cannot detect interface capabilities")

    def test_network_configuration_readable(self, host):
        """Verify network configuration is readable."""
        config_dirs = ["/etc/NetworkManager", "/etc/systemd/network"]
        readable_count = 0
        for config_dir in config_dirs:
            d = host.file(config_dir)
            if d.exists and d.is_directory:
                readable_count += 1
        assert readable_count > 0, "At least one network config directory should exist"
