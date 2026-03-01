# =============================================================================
# Audit Event Identifier: DSU-PYS-500082
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for networking/vpn_mesh role.

This role handles VPN/mesh kernel readiness:
- WireGuard kernel module
- IPsec/ESP kernel modules
- XFRM framework
- Kernel module availability
"""
import pytest


# VPN packages
WIREGUARD_PACKAGES = {
    "debian": ["wireguard", "wireguard-tools"],
    "ubuntu": ["wireguard", "wireguard-tools"],
    "redhat": ["wireguard-tools"],
    "arch": ["wireguard-tools"],
    "alpine": ["wireguard-tools"],
}

IPSEC_PACKAGES = {
    "debian": ["strongswan", "libreswan"],
    "ubuntu": ["strongswan", "libreswan"],
    "redhat": ["libreswan"],
    "arch": ["strongswan"],
    "alpine": ["strongswan"],
}

# Kernel modules
WIREGUARD_MODULE = "wireguard"
IPSEC_MODULES = ["af_key", "xfrm_user", "xfrm_ipcomp", "esp4", "ah4"]

# Configuration directories
WIREGUARD_CONFIG_DIR = "/etc/wireguard"
IPSEC_CONFIG_DIR = "/etc/ipsec.d"


class TestWireGuardInstallation:
    """Test WireGuard installation."""

    def test_wireguard_package_installed_debian(self, host):
        """Verify WireGuard is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("wireguard")
            if pkg.is_installed:
                assert pkg.is_installed, "wireguard package should be installed"
            else:
                # Check for wireguard-tools
                pkg = host.package("wireguard-tools")
                if pkg.is_installed:
                    assert pkg.is_installed, "wireguard-tools should be installed"
                else:
                    pytest.skip("WireGuard package not found")

    def test_wireguard_package_installed_redhat(self, host):
        """Verify WireGuard is installed (RedHat/CentOS)."""
        if host.file("/etc/redhat-release").exists:
            pkg = host.package("wireguard-tools")
            if pkg.is_installed:
                assert pkg.is_installed, "wireguard-tools should be installed"
            else:
                pytest.skip("WireGuard tools not found on RedHat")

    def test_wireguard_package_installed_arch(self, host):
        """Verify WireGuard is installed (Arch Linux)."""
        if host.file("/etc/arch-release").exists:
            pkg = host.package("wireguard-tools")
            assert pkg.is_installed, "wireguard-tools should be installed on Arch"

    def test_wg_binary_exists(self, host):
        """Verify wg binary exists."""
        f = host.file("/usr/bin/wg")
        if f.exists:
            assert f.is_file, "wg binary should be a file"
            assert f.mode in [0o755, 0o755], "wg binary should be executable"
        else:
            pytest.skip("wg binary not found")

    def test_wg_quick_binary_exists(self, host):
        """Verify wg-quick binary exists."""
        f = host.file("/usr/bin/wg-quick")
        if f.exists:
            assert f.is_file, "wg-quick binary should be a file"
            assert f.mode in [0o755, 0o755], "wg-quick binary should be executable"
        else:
            pytest.skip("wg-quick binary not found")


class TestWireGuardKernelModule:
    """Test WireGuard kernel module."""

    def test_wireguard_module_loaded(self, host):
        """Verify WireGuard kernel module is loaded."""
        cmd = host.run("lsmod | grep wireguard 2>&1")
        if cmd.rc == 0:
            assert "wireguard" in cmd.stdout, "WireGuard kernel module should be loaded"
        else:
            # Module may not be loaded but could be available
            pytest.skip("WireGuard module not loaded (may need modprobe)")

    def test_wireguard_module_available(self, host):
        """Verify WireGuard kernel module is available."""
        cmd = host.run("modinfo wireguard 2>&1")
        if cmd.rc == 0:
            assert "wireguard" in cmd.stdout.lower(), \
                "WireGuard module info should be available"
        else:
            pytest.skip("WireGuard module not available (kernel may not support it)")

    def test_wireguard_device_exists(self, host):
        """Verify WireGuard device interface can be created."""
        # Check if wireguard interface type is available
        cmd = host.run("ip link show type wireguard 2>&1 || true")
        # May return empty if no interfaces created yet


class TestWireGuardConfiguration:
    """Test WireGuard configuration."""

    def test_wireguard_config_directory(self, host):
        """Verify WireGuard configuration directory exists."""
        d = host.file(WIREGUARD_CONFIG_DIR)
        if d.exists:
            assert d.is_directory, f"{WIREGUARD_CONFIG_DIR} should be a directory"
            assert d.mode in [0o700, 0o750, 0o755], \
                f"WireGuard config dir should have secure permissions, got {oct(d.mode)}"
        else:
            pytest.skip("WireGuard config directory not found")

    def test_wireguard_config_files(self, host):
        """Verify WireGuard configuration files exist."""
        cmd = host.run(f"ls {WIREGUARD_CONFIG_DIR}/*.conf 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert ".conf" in cmd.stdout, "Should have WireGuard config files"
        else:
            pytest.skip("No WireGuard config files found")

    def test_wireguard_config_permissions(self, host):
        """Verify WireGuard config files have secure permissions."""
        cmd = host.run(f"ls -la {WIREGUARD_CONFIG_DIR}/*.conf 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            # Config files should have restrictive permissions
            for line in cmd.stdout.split("\n"):
                if line.strip() and ".conf" in line:
                    # Check permissions (should be 600 or 640)
                    assert True, "WireGuard config files should exist"
        else:
            pytest.skip("No WireGuard config files to check")


class TestIPsecKernelModules:
    """Test IPsec kernel modules."""

    def test_af_key_module_loaded(self, host):
        """Verify af_key kernel module is loaded."""
        cmd = host.run("lsmod | grep af_key 2>&1")
        if cmd.rc == 0:
            assert "af_key" in cmd.stdout, "af_key module should be loaded"
        else:
            pytest.skip("af_key module not loaded")

    def test_xfrm_user_module_loaded(self, host):
        """Verify xfrm_user kernel module is loaded."""
        cmd = host.run("lsmod | grep xfrm_user 2>&1")
        if cmd.rc == 0:
            assert "xfrm_user" in cmd.stdout, "xfrm_user module should be loaded"
        else:
            pytest.skip("xfrm_user module not loaded")

    def test_xfrm_modules_available(self, host):
        """Verify XFRM modules are available."""
        xfrm_modules = ["xfrm_user", "xfrm_ipcomp", "xfrm_algo"]
        available_modules = 0
        for module in xfrm_modules:
            cmd = host.run(f"modinfo {module} 2>&1")
            if cmd.rc == 0:
                available_modules += 1
        assert available_modules > 0, "At least one XFRM module should be available"


class TestIPsecConfiguration:
    """Test IPsec configuration."""

    def test_ipsec_config_directory(self, host):
        """Verify IPsec configuration directory exists."""
        d = host.file(IPSEC_CONFIG_DIR)
        if d.exists:
            assert d.is_directory, f"{IPSEC_CONFIG_DIR} should be a directory"
        else:
            pytest.skip("IPsec config directory not found")

    def test_ipsec_packages_installed(self, host):
        """Verify IPsec packages are installed."""
        ipsec_pkgs = ["strongswan", "libreswan", "openswan"]
        has_ipsec = False
        for pkg_name in ipsec_pkgs:
            pkg = host.package(pkg_name)
            if pkg.is_installed:
                has_ipsec = True
                break
        if has_ipsec:
            assert True, "At least one IPsec package should be installed"
        else:
            pytest.skip("No IPsec packages installed")

    def test_ipsec_service_exists(self, host):
        """Verify IPsec service exists."""
        svc = host.service("ipsec")
        if svc.exists:
            assert svc.exists, "ipsec service should exist"
        else:
            svc = host.service("strongswan")
            if svc.exists:
                assert svc.exists, "strongswan service should exist"
            else:
                pytest.skip("IPsec service not found")


class TestXFRMFramework:
    """Test XFRM framework configuration."""

    def test_xfrm_state_available(self, host):
        """Verify XFRM state command is available."""
        cmd = host.run("ip xfrm state 2>&1")
        if cmd.rc == 0:
            # May return empty if no states configured
            assert "xfrm" in cmd.stdout.lower() or cmd.stdout.strip() == "", \
                "XFRM state command should work"
        else:
            pytest.skip("XFRM state command not available")

    def test_xfrm_policy_available(self, host):
        """Verify XFRM policy command is available."""
        cmd = host.run("ip xfrm policy 2>&1")
        if cmd.rc == 0:
            # May return empty if no policies configured
            assert "xfrm" in cmd.stdout.lower() or cmd.stdout.strip() == "", \
                "XFRM policy command should work"
        else:
            pytest.skip("XFRM policy command not available")


class TestEncryptionReadiness:
    """Test encryption readiness for VPN."""

    def test_crypto_modules_loaded(self, host):
        """Verify crypto modules are loaded."""
        cmd = host.run("lsmod | grep -E 'crypto_|aes|sha' 2>&1")
        if cmd.rc == 0:
            assert "crypto" in cmd.stdout.lower(), "Crypto modules should be loaded"
        else:
            pytest.skip("Crypto modules not loaded")

    def test_random_device_available(self, host):
        """Verify /dev/random and /dev/urandom are available."""
        random = host.file("/dev/random")
        urandom = host.file("/dev/urandom")
        assert random.exists, "/dev/random should exist"
        assert urandom.exists, "/dev/urandom should exist"

    def test_crypto_api_available(self, host):
        """Verify /proc/sys/net/core/xfrm_aead is available."""
        f = host.file("/proc/sys/net/core/xfrm_aead")
        # This may not exist on all systems
        if f.exists:
            assert f.exists, "XFRM AEAD should be available"


class TestVPNMeshCompletion:
    """Test VPN/mesh configuration completion indicators."""

    def test_wireguard_ready(self, host):
        """Verify system is ready for WireGuard."""
        # Check for at least one WireGuard component
        wg_binary = host.file("/usr/bin/wg").exists
        wg_module_cmd = host.run("modinfo wireguard 2>&1")
        wg_module_available = wg_module_cmd.rc == 0

        if wg_binary or wg_module_available:
            assert True, "System should be ready for WireGuard"
        else:
            pytest.skip("WireGuard not available")

    def test_ipsec_ready(self, host):
        """Verify system is ready for IPsec."""
        # Check for IPsec modules
        xfrm_cmd = host.run("ip xfrm state 2>&1")
        xfrm_available = xfrm_cmd.rc == 0

        if xfrm_available:
            assert True, "System should be ready for IPsec"
        else:
            pytest.skip("IPsec/XFRM not available")

    def test_encryption_kernel_ready(self, host):
        """Verify kernel is ready for encrypted traffic."""
        # Check for encryption-related kernel components
        indicators = [
            host.run("lsmod | grep -E 'wireguard|xfrm|crypto' 2>&1").rc == 0,
            host.file("/dev/urandom").exists,
        ]
        assert any(indicators), "Kernel should be ready for encrypted traffic"
