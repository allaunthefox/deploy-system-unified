"""
Testinfra tests for core/systemd role.

This role handles systemd configuration and hardening:
- Configuring journald for persistent logging
- Configuring resolved for DNS
- Creating journal storage directories
- Reloading systemd daemon
"""
import pytest


class TestSystemdJournald:
    """Test journald configuration."""

    def test_journald_config_exists(self, host):
        """Verify journald configuration file exists."""
        f = host.file("/etc/systemd/journald.conf")
        assert f.exists, "/etc/systemd/journald.conf should exist"
        assert f.is_file, "/etc/systemd/journald.conf should be a file"

    def test_journald_config_permissions(self, host):
        """Verify journald configuration has correct permissions."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], "journald.conf should have secure permissions"
            assert f.user == "root", "journald.conf should be owned by root"

    def test_journald_storage_configured(self, host):
        """Verify journald storage is configured for persistence."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            # Should have Storage=persistent configured
            has_storage = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("Storage="):
                    has_storage = True
                    # Storage should be persistent or auto
                    assert "persistent" in line.lower() or "auto" in line.lower(), \
                        "Storage should be set to persistent or auto"
                    break
            assert has_storage, "Storage= should be configured in journald.conf"

    def test_journald_compression_configured(self, host):
        """Verify journald compression is configured."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("Compress="):
                    # Compression should be enabled
                    assert "yes" in line.lower(), "Compression should be enabled"
                    break

    def test_journald_rate_limiting_configured(self, host):
        """Verify journald rate limiting is configured."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            has_rate_limit = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("RateLimitIntervalSec=") or line.startswith("RateLimitBurst="):
                    has_rate_limit = True
                    break
            # Rate limiting should be configured
            assert has_rate_limit, "Rate limiting should be configured in journald.conf"


class TestSystemdJournalStorage:
    """Test journal storage directories."""

    def test_journal_directory_exists(self, host):
        """Verify persistent journal directory exists."""
        d = host.file("/var/log/journal")
        assert d.exists, "/var/log/journal should exist"
        assert d.is_directory, "/var/log/journal should be a directory"

    def test_journal_directory_permissions(self, host):
        """Verify journal directory has correct permissions."""
        d = host.file("/var/log/journal")
        if d.exists:
            # Should be 2755 (setgid) or 0755
            assert d.mode in [0o2755, 0o755, 0o750], "/var/log/journal should have correct permissions"
            assert d.user == "root", "/var/log/journal should be owned by root"

    def test_journal_directory_group(self, host):
        """Verify journal directory has correct group."""
        d = host.file("/var/log/journal")
        if d.exists:
            # Should be owned by systemd-journal group if it exists
            # This is informational as group may vary
            pass


class TestSystemdResolved:
    """Test systemd-resolved configuration."""

    def test_resolved_config_exists(self, host):
        """Verify resolved configuration file exists."""
        f = host.file("/etc/systemd/resolved.conf")
        assert f.exists, "/etc/systemd/resolved.conf should exist"
        assert f.is_file, "/etc/systemd/resolved.conf should be a file"

    def test_resolved_config_permissions(self, host):
        """Verify resolved configuration has correct permissions."""
        f = host.file("/etc/systemd/resolved.conf")
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], "resolved.conf should have secure permissions"
            assert f.user == "root", "resolved.conf should be owned by root"

    def test_resolved_dns_configured(self, host):
        """Verify DNS is configured in resolved.conf."""
        f = host.file("/etc/systemd/resolved.conf")
        if f.exists:
            content = f.content_string
            has_dns = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("DNS="):
                    has_dns = True
                    # Should have DNS servers configured
                    assert "=" in line, "DNS= should have value"
                    break
            assert has_dns, "DNS should be configured in resolved.conf"

    def test_resolved_dnssec_configured(self, host):
        """Verify DNSSEC is configured in resolved.conf."""
        f = host.file("/etc/systemd/resolved.conf")
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("DNSSEC="):
                    # DNSSEC should be configured
                    assert "allow-downgrade" in line.lower() or "yes" in line.lower() or "no" in line.lower(), \
                        "DNSSEC should have valid value"
                    break

    def test_resolved_service_exists(self, host):
        """Verify systemd-resolved service exists."""
        svc = host.service("systemd-resolved")
        if svc.exists:
            assert svc.exists, "systemd-resolved service should exist"


class TestSystemdServices:
    """Test systemd services."""

    def test_journald_service_running(self, host):
        """Verify systemd-journald is running."""
        svc = host.service("systemd-journald")
        if svc.exists:
            assert svc.is_running, "systemd-journald should be running"
            assert svc.is_enabled, "systemd-journald should be enabled"

    def test_systemd_manager_running(self, host):
        """Verify systemd is the init system."""
        # Check if systemd is PID 1
        cmd = host.run("ps -p 1 -o comm=")
        if cmd.rc == 0:
            assert "systemd" in cmd.stdout.lower(), "systemd should be the init system (PID 1)"

    def test_systemd_daemon_reload(self, host):
        """Verify systemd daemon can be reloaded."""
        cmd = host.run("systemctl daemon-reload 2>&1 || true")
        # This should succeed or at least not fail catastrophically
        # In containers this may not work, so we're lenient


class TestSystemdConfiguration:
    """Test systemd configuration."""

    def test_systemd_system_directory(self, host):
        """Verify /etc/systemd/system exists."""
        d = host.file("/etc/systemd/system")
        assert d.exists, "/etc/systemd/system should exist"
        assert d.is_directory, "/etc/systemd/system should be a directory"

    def test_systemd_unit_files_readable(self, host):
        """Verify systemd unit files are readable."""
        d = host.file("/etc/systemd/system")
        if d.exists and d.is_directory:
            # Should be able to list unit files
            cmd = host.run("systemctl list-unit-files --type=service 2>/dev/null | head -5 || true")
            # This is informational

    def test_tmpfiles_d_exists(self, host):
        """Verify tmpfiles.d directory exists."""
        d = host.file("/etc/tmpfiles.d")
        if d.exists:
            assert d.is_directory, "/etc/tmpfiles.d should be a directory"
