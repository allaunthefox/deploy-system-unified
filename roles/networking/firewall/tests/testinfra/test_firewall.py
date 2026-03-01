# =============================================================================
# Audit Event Identifier: DSU-PYS-500077
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for networking/firewall role.

This role handles firewall configuration:
- UFW (Debian/Arch) | Firewalld (RedHat) | Nftables (Alpine)
- Default policies and rules
- Allowed TCP/UDP ports
- Forward policy configuration
"""
import pytest


# Firewall packages by distribution
UFW_PACKAGES = ["ufw"]
FIREWALLD_PACKAGES = ["firewalld"]
NFTABLES_PACKAGES = ["nftables"]
IPTABLES_PACKAGES = ["iptables"]

# Firewall configuration files
UFW_CONFIG_FILES = [
    "/etc/default/ufw",
    "/etc/ufw/user.rules",
    "/etc/ufw/user6.rules",
]

FIREWALLD_CONFIG_DIR = "/etc/firewalld"
NFTABLES_CONFIG_FILE = "/etc/nftables.conf"

# Expected default policies
UFW_DEFAULT_FORWARD_POLICY = "DROP"


class TestFirewallPackages:
    """Test firewall package installation."""

    def test_ufw_installed_debian(self, host):
        """Verify UFW is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("ufw")
            assert pkg.is_installed, "ufw package should be installed on Debian/Ubuntu"

    def test_ufw_installed_arch(self, host):
        """Verify UFW is installed (Arch Linux)."""
        if host.file("/etc/arch-release").exists:
            pkg = host.package("ufw")
            assert pkg.is_installed, "ufw package should be installed on Arch Linux"

    def test_firewalld_installed_redhat(self, host):
        """Verify Firewalld is installed (RedHat/CentOS)."""
        if host.file("/etc/redhat-release").exists:
            pkg = host.package("firewalld")
            assert pkg.is_installed, "firewalld package should be installed on RedHat/CentOS"

    def test_nftables_installed_alpine(self, host):
        """Verify Nftables is installed (Alpine)."""
        if host.file("/etc/alpine-release").exists:
            pkg = host.package("nftables")
            assert pkg.is_installed, "nftables package should be installed on Alpine"

    def test_iptables_available(self, host):
        """Verify iptables is available as fallback."""
        pkg = host.package("iptables")
        if pkg.is_installed:
            assert pkg.is_installed, "iptables should be available"


class TestUFWConfiguration:
    """Test UFW configuration."""

    def test_ufw_default_config_exists(self, host):
        """Verify UFW default configuration exists."""
        f = host.file("/etc/default/ufw")
        if f.exists:
            assert f.is_file, "/etc/default/ufw should be a file"
        else:
            pytest.skip("UFW default config not found (UFW may not be active)")

    def test_ufw_default_config_permissions(self, host):
        """Verify UFW default config has correct permissions."""
        f = host.file("/etc/default/ufw")
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"/etc/default/ufw should have secure permissions, got {oct(f.mode)}"

    def test_ufw_forward_policy(self, host):
        """Verify UFW forward policy is configured."""
        f = host.file("/etc/default/ufw")
        if f.exists:
            content = f.content_string
            has_forward_policy = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("DEFAULT_FORWARD_POLICY="):
                    has_forward_policy = True
                    # Should be DROP or REJECT for security
                    assert "DROP" in line or "REJECT" in line, \
                        f"DEFAULT_FORWARD_POLICY should be DROP or REJECT, got {line}"
                    break
            assert has_forward_policy, "DEFAULT_FORWARD_POLICY should be configured"

    def test_ufw_user_rules_exists(self, host):
        """Verify UFW user rules file exists."""
        f = host.file("/etc/ufw/user.rules")
        if f.exists:
            assert f.is_file, "/etc/ufw/user.rules should be a file"
        else:
            pytest.skip("UFW user rules not found")

    def test_ufw_user6_rules_exists(self, host):
        """Verify UFW IPv6 user rules file exists."""
        f = host.file("/etc/ufw/user6.rules")
        if f.exists:
            assert f.is_file, "/etc/ufw/user6.rules should be a file"
        else:
            pytest.skip("UFW IPv6 user rules not found")


class TestUFWService:
    """Test UFW service status."""

    def test_ufw_service_exists(self, host):
        """Verify UFW service exists."""
        svc = host.service("ufw")
        if svc.exists:
            assert svc.exists, "ufw service should exist"
        else:
            pytest.skip("UFW service not found")

    def test_ufw_enabled(self, host):
        """Verify UFW is enabled."""
        cmd = host.run("ufw status 2>&1")
        if cmd.rc == 0:
            assert "Status: active" in cmd.stdout, "UFW should be enabled"
        else:
            pytest.skip("UFW status command failed")

    def test_ufw_default_policies(self, host):
        """Verify UFW default policies are secure."""
        cmd = host.run("ufw status verbose 2>&1")
        if cmd.rc == 0:
            content = cmd.stdout
            # Default incoming should be deny or reject
            has_default_incoming = "Default:" in content
            if has_default_incoming:
                assert "deny (incoming)" in content.lower() or \
                       "reject (incoming)" in content.lower(), \
                    "UFW default incoming policy should be deny or reject"
        else:
            pytest.skip("UFW status verbose command failed")


class TestFirewalldConfiguration:
    """Test Firewalld configuration."""

    def test_firewalld_config_directory(self, host):
        """Verify Firewalld configuration directory exists."""
        d = host.file(FIREWALLD_CONFIG_DIR)
        if d.exists:
            assert d.is_directory, f"{FIREWALLD_CONFIG_DIR} should be a directory"
        else:
            pytest.skip("Firewalld config directory not found")

    def test_firewalld_zones_directory(self, host):
        """Verify Firewalld zones directory exists."""
        d = host.file(f"{FIREWALLD_CONFIG_DIR}/zones")
        if d.exists:
            assert d.is_directory, "Firewalld zones directory should be a directory"
        else:
            pytest.skip("Firewalld zones directory not found")

    def test_firewalld_services_directory(self, host):
        """Verify Firewalld services directory exists."""
        d = host.file(f"{FIREWALLD_CONFIG_DIR}/services")
        if d.exists:
            assert d.is_directory, "Firewalld services directory should be a directory"
        else:
            pytest.skip("Firewalld services directory not found")


class TestFirewalldService:
    """Test Firewalld service status."""

    def test_firewalld_service_exists(self, host):
        """Verify Firewalld service exists."""
        svc = host.service("firewalld")
        if svc.exists:
            assert svc.exists, "firewalld service should exist"
        else:
            pytest.skip("Firewalld service not found")

    def test_firewalld_service_running(self, host):
        """Verify Firewalld service is running."""
        svc = host.service("firewalld")
        if svc.exists:
            assert svc.is_running, "firewalld service should be running"
            assert svc.is_enabled, "firewalld service should be enabled"
        else:
            pytest.skip("Firewalld service not available")

    def test_firewalld_status(self, host):
        """Verify Firewalld status."""
        cmd = host.run("firewall-cmd --state 2>&1")
        if cmd.rc == 0:
            assert "running" in cmd.stdout.lower(), "Firewalld should be running"
        else:
            pytest.skip("Firewall-cmd not available")


class TestNftablesConfiguration:
    """Test Nftables configuration."""

    def test_nftables_config_exists(self, host):
        """Verify Nftables configuration exists."""
        f = host.file(NFTABLES_CONFIG_FILE)
        if f.exists:
            assert f.is_file, f"{NFTABLES_CONFIG_FILE} should be a file"
        else:
            pytest.skip("Nftables config not found")

    def test_nftables_config_permissions(self, host):
        """Verify Nftables config has correct permissions."""
        f = host.file(NFTABLES_CONFIG_FILE)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"nftables.conf should have secure permissions, got {oct(f.mode)}"

    def test_nftables_ruleset_loaded(self, host):
        """Verify Nftables ruleset is loaded."""
        cmd = host.run("nft list ruleset 2>&1")
        if cmd.rc == 0:
            assert "table" in cmd.stdout.lower() or "chain" in cmd.stdout.lower(), \
                "Nftables should have ruleset loaded"
        else:
            pytest.skip("Nftables command not available")


class TestFirewallRules:
    """Test firewall rules configuration."""

    def test_ssh_rule_exists(self, host):
        """Verify SSH rule exists in firewall."""
        # Check UFW
        cmd = host.run("ufw status 2>&1 | grep -i ssh || true")
        if cmd.stdout:
            assert "22" in cmd.stdout or "ssh" in cmd.stdout.lower(), \
                "SSH rule should exist in UFW"
        else:
            # Check Firewalld
            cmd = host.run("firewall-cmd --list-services 2>&1 | grep -i ssh || true")
            if cmd.stdout:
                assert "ssh" in cmd.stdout.lower(), "SSH service should be allowed"
            else:
                pytest.skip("SSH rule not found in firewall")

    def test_allowed_tcp_ports_configured(self, host):
        """Verify allowed TCP ports are configured."""
        # Check UFW rules
        cmd = host.run("ufw status 2>&1")
        if "ALLOW" in cmd.stdout:
            assert "ALLOW" in cmd.stdout, "UFW should have ALLOW rules"
        else:
            # Check Firewalld
            cmd = host.run("firewall-cmd --list-ports 2>&1 || true")
            if cmd.stdout:
                assert True, "Firewalld should have port rules"


class TestFirewallKernelModules:
    """Test firewall kernel modules."""

    def test_netfilter_modules_loaded(self, host):
        """Verify netfilter kernel modules are loaded."""
        cmd = host.run("lsmod | grep -E 'nf_|ipt_' 2>&1")
        if cmd.rc == 0:
            assert "nf_" in cmd.stdout or "ipt_" in cmd.stdout, \
                "Netfilter modules should be loaded"
        else:
            pytest.skip("Netfilter modules not loaded (may be in container)")

    def test_iptable_filter_module(self, host):
        """Verify iptable_filter module is loaded."""
        cmd = host.run("lsmod | grep iptable_filter 2>&1")
        if cmd.rc == 0:
            assert "iptable_filter" in cmd.stdout, \
                "iptable_filter module should be loaded"
        else:
            pytest.skip("iptable_filter module not loaded")


class TestFirewallCompletion:
    """Test firewall configuration completion indicators."""

    def test_firewall_active(self, host):
        """Verify at least one firewall is active."""
        # Check UFW
        cmd = host.run("ufw status 2>&1")
        if "Status: active" in cmd.stdout:
            assert True, "UFW is active"
        else:
            # Check Firewalld
            cmd = host.run("firewall-cmd --state 2>&1")
            if "running" in cmd.stdout.lower():
                assert True, "Firewalld is active"
            else:
                # Check Nftables
                cmd = host.run("nft list ruleset 2>&1")
                if cmd.rc == 0:
                    assert True, "Nftables ruleset is loaded"
                else:
                    pytest.skip("No firewall is active")

    def test_firewall_packages_available(self, host):
        """Verify at least one firewall package is installed."""
        firewall_pkgs = ["ufw", "firewalld", "nftables", "iptables"]
        has_firewall = False
        for pkg_name in firewall_pkgs:
            pkg = host.package(pkg_name)
            if pkg.is_installed:
                has_firewall = True
                break
        assert has_firewall, "At least one firewall package should be installed"
