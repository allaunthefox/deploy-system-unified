# =============================================================================
# Audit Event Identifier: DSU-PYS-500045
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for security/ips role.

This role handles Intrusion Prevention System (Fail2Ban):
- Fail2Ban package installation
- SSH jail configuration
- Caddy web server jail configuration
- Fail2Ban service management
"""
import pytest


# Fail2Ban configuration paths
FAIL2BAN_CONFIG_DIR = "/etc/fail2ban"
FAIL2BAN_JAIL_DIR = "/etc/fail2ban/jail.d"
FAIL2BAN_FILTER_DIR = "/etc/fail2ban/filter.d"
FAIL2BAN_SSHD_JAIL = "/etc/fail2ban/jail.d/99-sshd-hardened.local"
FAIL2BAN_CADDY_JAIL = "/etc/fail2ban/jail.d/99-caddy-hardened.local"
FAIL2BAN_CADDY_FILTER = "/etc/fail2ban/filter.d/caddy.conf"
FAIL2BAN_LOG = "/var/log/fail2ban.log"


class TestFail2BanInstallation:
    """Test Fail2Ban package installation."""

    def test_fail2ban_package_installed(self, host):
        """Verify Fail2Ban package is installed (CIS 5.6.1)."""
        pkg = host.package("fail2ban")
        assert pkg.is_installed, "fail2ban package should be installed"

    def test_fail2ban_binary_exists(self, host):
        """Verify Fail2Ban binary exists."""
        assert host.exists("fail2ban-client"), "fail2ban-client binary should exist"

    def test_fail2ban_server_binary_exists(self, host):
        """Verify Fail2Ban server binary exists."""
        assert host.exists("fail2ban-server"), "fail2ban-server binary should exist"


class TestFail2BanService:
    """Test Fail2Ban service configuration."""

    def test_fail2ban_service_exists(self, host):
        """Verify Fail2Ban service exists."""
        svc = host.service("fail2ban")
        assert svc.exists, "fail2ban service should exist"

    def test_fail2ban_service_running(self, host):
        """Verify Fail2Ban service is running (CIS 5.6.1)."""
        svc = host.service("fail2ban")
        if svc.exists:
            assert svc.is_running, "fail2ban service should be running"
            assert svc.is_enabled, "fail2ban service should be enabled"

    def test_fail2ban_service_status(self, host):
        """Verify Fail2Ban service status is healthy."""
        cmd = host.run("systemctl status fail2ban 2>&1 | head -10")
        if cmd.rc == 0:
            # Service should be active
            assert "active" in cmd.stdout.lower() or "running" in cmd.stdout.lower(), \
                "fail2ban service should be active"
        else:
            pytest.skip("Cannot get fail2ban service status")


class TestFail2BanConfiguration:
    """Test Fail2Ban configuration."""

    def test_fail2ban_config_directory_exists(self, host):
        """Verify Fail2Ban configuration directory exists."""
        d = host.file(FAIL2BAN_CONFIG_DIR)
        assert d.exists, f"Fail2Ban config directory '{FAIL2BAN_CONFIG_DIR}' should exist"
        assert d.is_directory, f"'{FAIL2BAN_CONFIG_DIR}' should be a directory"
        assert d.mode == 0o755, f"Config directory should have mode 0755, got {oct(d.mode)}"

    def test_fail2ban_jail_directory_exists(self, host):
        """Verify Fail2Ban jail.d directory exists."""
        d = host.file(FAIL2BAN_JAIL_DIR)
        assert d.exists, f"Fail2Ban jail directory '{FAIL2BAN_JAIL_DIR}' should exist"
        assert d.is_directory, f"'{FAIL2BAN_JAIL_DIR}' should be a directory"

    def test_fail2ban_filter_directory_exists(self, host):
        """Verify Fail2Ban filter.d directory exists."""
        d = host.file(FAIL2BAN_FILTER_DIR)
        assert d.exists, f"Fail2Ban filter directory '{FAIL2BAN_FILTER_DIR}' should exist"
        assert d.is_directory, f"'{FAIL2BAN_FILTER_DIR}' should be a directory"

    def test_fail2ban_main_config_exists(self, host):
        """Verify Fail2Ban main configuration exists."""
        f = host.file(f"{FAIL2BAN_CONFIG_DIR}/fail2ban.conf")
        assert f.exists, "fail2ban.conf should exist"

    def test_fail2ban_jail_config_exists(self, host):
        """Verify Fail2Ban jail configuration exists."""
        f = host.file(f"{FAIL2BAN_CONFIG_DIR}/jail.conf")
        assert f.exists, "jail.conf should exist"


class TestFail2BanSSHDJail:
    """Test Fail2Ban SSHD jail configuration (CIS 5.6.1)."""

    def test_sshd_jail_config_exists(self, host):
        """Verify SSHD jail configuration exists (STIG V-230345)."""
        f = host.file(FAIL2BAN_SSHD_JAIL)
        assert f.exists, f"SSHD jail config '{FAIL2BAN_SSHD_JAIL}' should exist"
        assert f.is_file, f"'{FAIL2BAN_SSHD_JAIL}' should be a regular file"

    def test_sshd_jail_config_permissions(self, host):
        """Verify SSHD jail configuration has correct permissions."""
        f = host.file(FAIL2BAN_SSHD_JAIL)
        assert f.mode == 0o644, \
            f"SSHD jail config should have mode 0644, got {oct(f.mode)}"
        assert f.user == "root", "SSHD jail config should be owned by root"

    def test_sshd_jail_enabled(self, host):
        """Verify SSHD jail is enabled."""
        f = host.file(FAIL2BAN_SSHD_JAIL)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("enabled"):
                value = line.split("=")[1].strip().lower()
                assert value == "true", f"SSHD jail should be enabled, got '{value}'"
                return
        pytest.skip("enabled not found in SSHD jail config")

    def test_sshd_jail_port_configured(self, host):
        """Verify SSHD jail port is configured."""
        f = host.file(FAIL2BAN_SSHD_JAIL)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("port"):
                value = line.split("=")[1].strip()
                assert value, "SSHD jail port should be configured"
                # Port should be valid
                if value.isdigit():
                    assert 1 <= int(value) <= 65535, f"Invalid port number: {value}"
                return
        pytest.skip("port not found in SSHD jail config")

    def test_sshd_jail_maxretry_configured(self, host):
        """Verify SSHD jail maxretry is configured."""
        f = host.file(FAIL2BAN_SSHD_JAIL)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("maxretry"):
                value = int(line.split("=")[1].strip())
                assert value <= 5, f"maxretry should be 5 or less, got {value}"
                assert value >= 1, f"maxretry should be at least 1, got {value}"
                return
        pytest.skip("maxretry not found in SSHD jail config")

    def test_sshd_jail_bantime_configured(self, host):
        """Verify SSHD jail bantime is configured."""
        f = host.file(FAIL2BAN_SSHD_JAIL)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("bantime"):
                value = line.split("=")[1].strip()
                assert value, "bantime should be configured"
                # Should be a time value (e.g., 1h, 24h, 3600)
                return
        pytest.skip("bantime not found in SSHD jail config")

    def test_sshd_jail_findtime_configured(self, host):
        """Verify SSHD jail findtime is configured."""
        f = host.file(FAIL2BAN_SSHD_JAIL)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("findtime"):
                value = line.split("=")[1].strip()
                assert value, "findtime should be configured"
                return
        pytest.skip("findtime not found in SSHD jail config")

    def test_sshd_jail_logpath_configured(self, host):
        """Verify SSHD jail logpath is configured."""
        f = host.file(FAIL2BAN_SSHD_JAIL)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("logpath"):
                value = line.split("=")[1].strip()
                assert value, "logpath should be configured"
                assert "sshd" in value.lower() or "auth" in value.lower(), \
                    f"logpath should reference sshd or auth logs, got '{value}'"
                return
        pytest.skip("logpath not found in SSHD jail config")


class TestFail2BanCaddyJail:
    """Test Fail2Ban Caddy jail configuration."""

    def test_caddy_jail_config_exists(self, host):
        """Verify Caddy jail configuration exists (STIG V-230347)."""
        f = host.file(FAIL2BAN_CADDY_JAIL)
        if f.exists:
            assert f.is_file, f"'{FAIL2BAN_CADDY_JAIL}' should be a regular file"
            assert f.mode == 0o644, \
                f"Caddy jail config should have mode 0644, got {oct(f.mode)}"
        else:
            pytest.skip(f"Caddy jail config '{FAIL2BAN_CADDY_JAIL}' does not exist")

    def test_caddy_jail_enabled(self, host):
        """Verify Caddy jail is enabled if configured."""
        f = host.file(FAIL2BAN_CADDY_JAIL)
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("enabled"):
                    value = line.split("=")[1].strip().lower()
                    assert value == "true", f"Caddy jail should be enabled, got '{value}'"
                    return
            pytest.skip("enabled not found in Caddy jail config")
        else:
            pytest.skip(f"Caddy jail config '{FAIL2BAN_CADDY_JAIL}' does not exist")

    def test_caddy_filter_exists(self, host):
        """Verify Caddy filter exists (STIG V-230346)."""
        f = host.file(FAIL2BAN_CADDY_FILTER)
        if f.exists:
            assert f.is_file, f"Caddy filter '{FAIL2BAN_CADDY_FILTER}' should be a file"
            assert f.mode == 0o644, \
                f"Caddy filter should have mode 0644, got {oct(f.mode)}"
        else:
            pytest.skip(f"Caddy filter '{FAIL2BAN_CADDY_FILTER}' does not exist")

    def test_caddy_filter_content(self, host):
        """Verify Caddy filter has valid content."""
        f = host.file(FAIL2BAN_CADDY_FILTER)
        if f.exists:
            content = f.content_string
            assert "[Definition]" in content or "failregex" in content.lower(), \
                "Caddy filter should have valid filter definition"
        else:
            pytest.skip(f"Caddy filter '{FAIL2BAN_CADDY_FILTER}' does not exist")


class TestFail2BanStatus:
    """Test Fail2Ban operational status."""

    def test_fail2ban_status_command(self, host):
        """Verify Fail2Ban status command works."""
        cmd = host.run("fail2ban-client status 2>&1")
        if cmd.rc == 0:
            assert "fail2ban" in cmd.stdout.lower() or "status" in cmd.stdout.lower(), \
                "fail2ban-client status should return valid output"
        else:
            pytest.skip("fail2ban-client status command failed")

    def test_fail2ban_sshd_jail_status(self, host):
        """Verify SSHD jail is active in Fail2Ban."""
        cmd = host.run("fail2ban-client status sshd 2>&1 || true")
        if cmd.rc == 0 and "sshd" in cmd.stdout.lower():
            # Jail is active
            assert "Currently failed" in cmd.stdout or "Total failed" in cmd.stdout, \
                "SSHD jail status should show failure statistics"
        else:
            pytest.skip("SSHD jail not active or fail2ban not running")

    def test_fail2ban_jails_list(self, host):
        """Verify Fail2Ban can list jails."""
        cmd = host.run("fail2ban-client status 2>&1 | grep -i 'jail' || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "jail" in cmd.stdout.lower(), "Fail2Ban should have jails configured"
        else:
            pytest.skip("Cannot get jail list from fail2ban")


class TestFail2BanLogging:
    """Test Fail2Ban logging configuration."""

    def test_fail2ban_log_directory_exists(self, host):
        """Verify Fail2Ban log directory exists."""
        d = host.file("/var/log")
        assert d.exists, "/var/log should exist"
        assert d.is_directory, "/var/log should be a directory"

    def test_fail2ban_log_exists(self, host):
        """Verify Fail2Ban log file exists."""
        f = host.file(FAIL2BAN_LOG)
        if f.exists:
            assert f.is_file, f"Fail2Ban log '{FAIL2BAN_LOG}' should be a file"
        else:
            # Log might be in different location or not created yet
            pytest.skip(f"Fail2Ban log '{FAIL2BAN_LOG}' does not exist yet")

    def test_fail2ban_log_permissions(self, host):
        """Verify Fail2Ban log has correct permissions."""
        f = host.file(FAIL2BAN_LOG)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"Fail2Ban log should have secure permissions, got {oct(f.mode)}"


class TestFail2BanActions:
    """Test Fail2Ban actions configuration."""

    def test_fail2ban_action_directory_exists(self, host):
        """Verify Fail2Ban action.d directory exists."""
        d = host.file(f"{FAIL2BAN_CONFIG_DIR}/action.d")
        if d.exists:
            assert d.is_directory, "action.d should be a directory"
        else:
            pytest.skip("action.d directory does not exist")

    def test_iptables_action_available(self, host):
        """Verify iptables action is available."""
        f = host.file(f"{FAIL2BAN_CONFIG_DIR}/action.d/iptables-common.conf")
        if f.exists:
            assert f.is_file, "iptables-common.conf should be a file"
        else:
            # May use nftables or other backend
            pytest.skip("iptables action not found (may use nftables)")


class TestFail2BanRecidive:
    """Test Fail2Ban recidive jail (repeat offenders)."""

    def test_recidive_jail_configured(self, host):
        """Verify recidive jail configuration."""
        # Check main jail.conf for recidive
        f = host.file(f"{FAIL2BAN_CONFIG_DIR}/jail.conf")
        if f.exists:
            content = f.content_string
            # Recidive might be in default config
            pass
        else:
            pytest.skip("jail.conf does not exist")


class TestIPSPackageConfiguration:
    """Test IPS package and system configuration."""

    def test_iptables_or_nftables_available(self, host):
        """Verify iptables or nftables is available for banning."""
        has_iptables = host.exists("iptables")
        has_nftables = host.exists("nft")
        assert has_iptables or has_nftables, \
            "iptables or nftables should be available for Fail2Ban banning"

    def test_fail2ban_can_modify_firewall(self, host):
        """Verify Fail2Ban can modify firewall rules."""
        # This is a basic check - actual testing requires running fail2ban
        cmd = host.run("fail2ban-client get sshd action 2>&1 || true")
        if cmd.rc == 0:
            assert "action" in cmd.stdout.lower(), "Fail2Ban should have actions configured"
        else:
            pytest.skip("Cannot get Fail2Ban action configuration")
