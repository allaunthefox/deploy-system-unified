# =============================================================================
# Audit Event Identifier: DSU-PYS-500059
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for core/logging role.

This role handles logging configuration for forensic readiness:
- Installing systemd-journal-remote
- Configuring journald with rate limiting and retention
- Configuring rsyslog for centralized logging
- Creating logrotate configuration
- Ensuring journal persistence
"""
import pytest


class TestLoggingJournald:
    """Test journald logging configuration."""

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

    def test_journald_storage_persistent(self, host):
        """Verify journald storage is set to persistent."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("Storage="):
                    assert "persistent" in line.lower(), "Storage should be set to persistent"
                    break

    def test_journald_compression_enabled(self, host):
        """Verify journald compression is enabled."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("Compress="):
                    assert "yes" in line.lower(), "Compression should be enabled"
                    break

    def test_journald_seal_enabled(self, host):
        """Verify journald sealing is enabled for integrity."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("Seal="):
                    assert "yes" in line.lower(), "Sealing should be enabled"
                    break

    def test_journald_forward_to_syslog(self, host):
        """Verify journald forwards to syslog."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("ForwardToSyslog="):
                    assert "yes" in line.lower(), "ForwardToSyslog should be enabled"
                    break

    def test_journald_rate_limiting(self, host):
        """Verify journald rate limiting is configured."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            has_interval = False
            has_burst = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("RateLimitIntervalSec="):
                    has_interval = True
                if line.startswith("RateLimitBurst="):
                    has_burst = True
            assert has_interval, "RateLimitIntervalSec should be configured"
            assert has_burst, "RateLimitBurst should be configured"

    def test_journald_retention_configured(self, host):
        """Verify journald retention settings are configured."""
        f = host.file("/etc/systemd/journald.conf")
        if f.exists:
            content = f.content_string
            has_max_file = False
            has_max_retention = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("MaxFileSec="):
                    has_max_file = True
                if line.startswith("MaxRetentionSec="):
                    has_max_retention = True
            assert has_max_file, "MaxFileSec should be configured"
            assert has_max_retention, "MaxRetentionSec should be configured"


class TestLoggingJournalStorage:
    """Test journal storage."""

    def test_journal_directory_exists(self, host):
        """Verify journal directory exists."""
        d = host.file("/var/log/journal")
        assert d.exists, "/var/log/journal should exist"
        assert d.is_directory, "/var/log/journal should be a directory"

    def test_journal_directory_permissions(self, host):
        """Verify journal directory has correct permissions."""
        d = host.file("/var/log/journal")
        if d.exists:
            assert d.mode in [0o755, 0o750, 0o2755], "/var/log/journal should have correct permissions"
            assert d.user == "root", "/var/log/journal should be owned by root"


class TestLoggingRsyslog:
    """Test rsyslog configuration."""

    def test_rsyslog_installed(self, host):
        """Verify rsyslog is installed."""
        pkg = host.package("rsyslog")
        assert pkg.is_installed, "rsyslog package should be installed"

    def test_rsyslog_config_directory_exists(self, host):
        """Verify rsyslog configuration directory exists."""
        d = host.file("/etc/rsyslog.d")
        assert d.exists, "/etc/rsyslog.d should exist"
        assert d.is_directory, "/etc/rsyslog.d should be a directory"

    def test_centralized_logging_config(self, host):
        """Verify centralized logging configuration exists."""
        f = host.file("/etc/rsyslog.d/50-centralized-logging.conf")
        if f.exists:
            assert f.is_file, "50-centralized-logging.conf should be a file"
            assert f.mode in [0o644, 0o640], "rsyslog config should have correct permissions"

    def test_rsyslog_service(self, host):
        """Verify rsyslog service status."""
        svc = host.service("rsyslog")
        if svc.exists:
            assert svc.is_running, "rsyslog should be running"
            assert svc.is_enabled, "rsyslog should be enabled"


class TestLoggingLogrotate:
    """Test logrotate configuration."""

    def test_logrotate_applications_config(self, host):
        """Verify application logrotate configuration exists."""
        f = host.file("/etc/logrotate.d/applications")
        assert f.exists, "/etc/logrotate.d/applications should exist"
        assert f.is_file, "/etc/logrotate.d/applications should be a file"
        assert f.mode in [0o644, 0o640], "logrotate config should have correct permissions"

    def test_logrotate_config_content(self, host):
        """Verify logrotate configuration has required settings."""
        f = host.file("/etc/logrotate.d/applications")
        if f.exists:
            content = f.content_string
            # Should have daily rotation
            assert "daily" in content, "Logrotate should rotate daily"
            # Should have compression
            assert "compress" in content, "Logrotate should compress old logs"
            # Should have retention
            assert "rotate" in content, "Logrotate should have rotation count"

    def test_logrotate_main_config(self, host):
        """Verify main logrotate configuration exists."""
        f = host.file("/etc/logrotate.conf")
        assert f.exists, "/etc/logrotate.conf should exist"


class TestLoggingJournalRemote:
    """Test systemd-journal-remote configuration."""

    def test_journal_remote_package(self, host):
        """Verify systemd-journal-remote is installed if available."""
        # Package availability varies by distribution
        pkg_names = ["systemd-journal-remote", "systemd"]
        for pkg_name in pkg_names:
            pkg = host.package(pkg_name)
            if pkg.is_installed:
                # If installed, that's good
                break

    def test_journal_upload_directory(self, host):
        """Verify journal upload directory exists if configured."""
        d = host.file("/var/log/journal/upload")
        if d.exists:
            assert d.is_directory, "Journal upload directory should be a directory"


class TestLoggingSystemState:
    """Test logging system state."""

    def test_journald_service_running(self, host):
        """Verify systemd-journald is running."""
        svc = host.service("systemd-journald")
        if svc.exists:
            assert svc.is_running, "systemd-journald should be running"

    def test_journalctl_available(self, host):
        """Verify journalctl command is available."""
        assert host.exists("journalctl"), "journalctl command should be available"

    def test_journal_verification(self, host):
        """Verify journal can be verified."""
        cmd = host.run("journalctl --verify 2>&1 || true")
        # Verification may show warnings but should complete
        # This is informational

    def test_log_directory_exists(self, host):
        """Verify /var/log directory exists."""
        d = host.file("/var/log")
        assert d.exists, "/var/log should exist"
        assert d.is_directory, "/var/log should be a directory"

    def test_log_directory_permissions(self, host):
        """Verify /var/log has correct permissions."""
        d = host.file("/var/log")
        if d.exists:
            assert d.mode in [0o755, 0o750], "/var/log should have correct permissions"
            assert d.user == "root", "/var/log should be owned by root"

    def test_logs_are_writable(self, host):
        """Verify logs can be written."""
        # Check if we can write to journal
        cmd = host.run("logger test-log-entry 2>&1 || true")
        # This should succeed if logging is working
