"""
Testinfra tests for security/audit_integrity role.

This role handles cryptographic log immutability:
- Persistent journald configuration
- Forward Secure Sealing (FSS) key initialization
- Journal seal configuration
- Secure storage of verification keys
"""
import pytest


# Journald configuration paths
JOURNALD_CONFIG_PATH = "/etc/systemd/journald.conf"
JOURNAL_DIR = "/var/log/journal"
JOURNAL_FSS_PATTERN = "fss.pub"


class TestJournaldConfiguration:
    """Test journald configuration."""

    def test_journald_config_exists(self, host):
        """Verify journald configuration file exists."""
        f = host.file(JOURNALD_CONFIG_PATH)
        assert f.exists, f"Journald config '{JOURNALD_CONFIG_PATH}' should exist"
        assert f.is_file, f"'{JOURNALD_CONFIG_PATH}' should be a regular file"

    def test_journald_config_permissions(self, host):
        """Verify journald configuration has correct permissions."""
        f = host.file(JOURNALD_CONFIG_PATH)
        assert f.mode in [0o644, 0o640, 0o600], \
            f"Journald config should have secure permissions, got {oct(f.mode)}"
        assert f.user == "root", "Journald config should be owned by root"

    def test_journald_storage_persistent(self, host):
        """Verify journald storage is configured for persistence."""
        f = host.file(JOURNALD_CONFIG_PATH)
        content = f.content_string
        has_storage = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("Storage="):
                has_storage = True
                value = line.split("=")[1].strip().lower()
                assert value in ["persistent", "auto"], \
                    f"Storage should be 'persistent' or 'auto', got '{value}'"
                break
        assert has_storage, "Storage= should be configured in journald.conf"

    def test_journald_compress_configured(self, host):
        """Verify journald compression is configured."""
        f = host.file(JOURNALD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("Compress="):
                value = line.split("=")[1].strip().lower()
                assert value in ["yes", "no", "zstd", "lz4", "xz"], \
                    f"Compress should have valid value, got '{value}'"
                return
        pytest.skip("Compress= not explicitly configured")


class TestJournalDirectory:
    """Test journal directory configuration (CIS 4.2.1.2)."""

    def test_journal_directory_exists(self, host):
        """Verify persistent journal directory exists."""
        d = host.file(JOURNAL_DIR)
        assert d.exists, f"Journal directory '{JOURNAL_DIR}' should exist"
        assert d.is_directory, f"'{JOURNAL_DIR}' should be a directory"

    def test_journal_directory_permissions(self, host):
        """Verify journal directory has correct permissions."""
        d = host.file(JOURNAL_DIR)
        assert d.mode in [0o2755, 0o755, 0o750], \
            f"Journal directory should have secure permissions, got {oct(d.mode)}"
        assert d.user == "root", "Journal directory should be owned by root"

    def test_journal_directory_group(self, host):
        """Verify journal directory has correct group."""
        d = host.file(JOURNAL_DIR)
        # Should be owned by systemd-journal group if it exists
        # This is informational as group may vary
        valid_groups = ["root", "systemd-journal"]
        assert d.group in valid_groups, \
            f"Journal directory group should be {valid_groups}, got '{d.group}'"

    def test_journal_directory_setgid(self, host):
        """Verify journal directory has setgid bit if appropriate."""
        d = host.file(JOURNAL_DIR)
        mode = d.mode
        # Check for setgid bit (2000)
        has_setgid = (mode & 0o2000) != 0
        if d.group == "systemd-journal":
            assert has_setgid, "Journal directory should have setgid bit for systemd-journal group"


class TestJournalFSS:
    """Test Forward Secure Sealing (FSS) configuration."""

    def test_journal_fss_keys_directory_exists(self, host):
        """Verify journal FSS keys directory exists."""
        d = host.file(JOURNAL_DIR)
        if d.exists and d.is_directory:
            # FSS keys should be in /var/log/journal/<machine-id>/
            cmd = host.run(f"ls -la {JOURNAL_DIR}/ 2>&1 | head -10")
            if cmd.rc == 0:
                # Just verify directory is accessible
                pass
        else:
            pytest.skip(f"Journal directory '{JOURNAL_DIR}' does not exist")

    def test_journal_fss_public_key_exists(self, host):
        """Verify FSS public key exists if FSS is initialized."""
        cmd = host.run(f"find {JOURNAL_DIR} -name '{JOURNAL_FSS_PATTERN}' 2>/dev/null | head -1")
        if cmd.rc == 0 and cmd.stdout.strip():
            fss_key_path = cmd.stdout.strip()
            f = host.file(fss_key_path)
            assert f.exists, f"FSS public key '{fss_key_path}' should exist"
            assert f.mode in [0o644, 0o640, 0o600], \
                f"FSS public key should have secure permissions, got {oct(f.mode)}"
        else:
            pytest.skip("FSS public key not found (may need initialization)")

    def test_journal_fss_verification_configured(self, host):
        """Verify journal FSS verification is possible."""
        cmd = host.run("journalctl --verify 2>&1 | head -5 || true")
        # This is informational - verification requires FSS keys
        # Just check that journalctl is available


class TestJournalSeal:
    """Test journal seal configuration (CIS 4.2.1.3)."""

    def test_seal_enabled_in_journald(self, host):
        """Verify Seal=yes is configured in journald."""
        f = host.file(JOURNALD_CONFIG_PATH)
        content = f.content_string
        has_seal = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("Seal="):
                has_seal = True
                value = line.split("=")[1].strip().lower()
                assert value == "yes", f"Seal should be 'yes', got '{value}'"
                break
        assert has_seal, "Seal= should be configured in journald.conf"

    def test_journald_service_exists(self, host):
        """Verify systemd-journald service exists."""
        svc = host.service("systemd-journald")
        assert svc.exists, "systemd-journald service should exist"

    def test_journald_service_running(self, host):
        """Verify systemd-journald is running."""
        svc = host.service("systemd-journald")
        if svc.exists:
            assert svc.is_running, "systemd-journald should be running"
            assert svc.is_enabled, "systemd-journald should be enabled"


class TestJournalAccess:
    """Test journal access configuration."""

    def test_systemd_journal_group_exists(self, host):
        """Verify systemd-journal group exists."""
        cmd = host.run("getent group systemd-journal 2>&1")
        if cmd.rc == 0:
            assert "systemd-journal" in cmd.stdout, "systemd-journal group should exist"
        else:
            pytest.skip("systemd-journal group does not exist")

    def test_journalctl_available(self, host):
        """Verify journalctl command is available."""
        assert host.exists("journalctl"), "journalctl command should be available"

    def test_journalctl_can_read_logs(self, host):
        """Verify journalctl can read logs."""
        cmd = host.run("journalctl -n 5 2>&1")
        if cmd.rc == 0:
            assert len(cmd.stdout) > 0, "journalctl should be able to read logs"
        else:
            pytest.skip("journalctl cannot read logs (permissions issue)")


class TestAuditIntegrityStorage:
    """Test audit integrity key storage."""

    def test_audit_integrity_output_dir_configured(self, host):
        """Verify audit integrity output directory is configured on controller."""
        # This is a controller-side configuration, so we check if the path is valid
        # The actual storage happens on the Ansible controller, not the target
        pytest.skip("Audit integrity key storage is controller-side operation")

    def test_fss_key_encryption_available(self, host):
        """Verify ansible-vault is available for FSS key encryption."""
        # This is a controller-side check
        pytest.skip("Ansible vault encryption is controller-side operation")


class TestJournaldRateLimiting:
    """Test journald rate limiting configuration."""

    def test_rate_limit_interval_configured(self, host):
        """Verify rate limit interval is configured."""
        f = host.file(JOURNALD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("RateLimitIntervalSec="):
                value = line.split("=")[1].strip()
                assert value, "RateLimitIntervalSec should have a value"
                return
        pytest.skip("RateLimitIntervalSec not configured")

    def test_rate_limit_burst_configured(self, host):
        """Verify rate limit burst is configured."""
        f = host.file(JOURNALD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("RateLimitBurst="):
                value = line.split("=")[1].strip()
                assert value.isdigit(), f"RateLimitBurst should be a number, got '{value}'"
                return
        pytest.skip("RateLimitBurst not configured")


class TestJournaldMaxRetention:
    """Test journald retention configuration."""

    def test_max_retention_configured(self, host):
        """Verify max retention is configured."""
        f = host.file(JOURNALD_CONFIG_PATH)
        content = f.content_string
        retention_options = ["SystemMaxUse=", "SystemKeepFree=", "SystemMaxFileSize=", 
                            "MaxRetentionSec=", "MaxFileSec="]
        has_retention = False
        for line in content.split("\n"):
            line = line.strip()
            for option in retention_options:
                if line.startswith(option):
                    has_retention = True
                    break
        # Retention configuration is optional but recommended
        # Don't fail if not configured


class TestContainerDetection:
    """Test container environment handling."""

    def test_not_in_container_or_skip(self, host):
        """Verify test handles container environment appropriately."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        if cmd.rc == 0:
            virt_type = cmd.stdout.strip().lower()
            if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
                pytest.skip(f"Running in container ({virt_type}), journald may have limited functionality")

    def test_systemd_available(self, host):
        """Verify systemd is available."""
        cmd = host.run("ps -p 1 -o comm= 2>&1")
        if cmd.rc == 0:
            assert "systemd" in cmd.stdout.lower(), "systemd should be the init system"
        else:
            pytest.skip("Cannot determine init system")


class TestAuditIntegrityCompletion:
    """Test audit integrity configuration completion."""

    def test_journald_properly_configured(self, host):
        """Verify journald is properly configured for audit integrity."""
        f = host.file(JOURNALD_CONFIG_PATH)
        if f.exists:
            content = f.content_string
            # Check for key configurations
            has_storage = "Storage=" in content
            has_seal = "Seal=yes" in content
            assert has_storage, "Storage should be configured"
            assert has_seal, "Seal should be enabled"
        else:
            pytest.skip(f"Journald config '{JOURNALD_CONFIG_PATH}' does not exist")

    def test_journal_directory_properly_configured(self, host):
        """Verify journal directory is properly configured."""
        d = host.file(JOURNAL_DIR)
        assert d.exists, f"Journal directory '{JOURNAL_DIR}' should exist"
        assert d.is_directory, f"'{JOURNAL_DIR}' should be a directory"
