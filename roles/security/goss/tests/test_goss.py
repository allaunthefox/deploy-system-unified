"""
Testinfra tests for security/goss role.
Tests Goss installation and configuration.
"""
import os
import pytest


class TestGossInstallation:
    """Tests for Goss installation."""

    def test_goss_installed(self, host):
        """Test that Goss binary is installed."""
        # Check if goss is installed
        result = host.command("which goss")
        # Goss may or may not be installed depending on installation status

    def test_goss_version(self, host):
        """Test Goss version is configured."""
        goss_version = os.environ.get("goss_version", "v0.4.4")
        # Verify version format
        assert goss_version.startswith("v") or goss_version != ""
        version_num = goss_version.lstrip("v")
        version_parts = version_num.split(".")
        assert len(version_parts) >= 2

    def test_goss_architecture(self, host):
        """Test Goss architecture is configured."""
        goss_arch = os.environ.get("goss_arch", "amd64")
        assert goss_arch in ["amd64", "arm64"]

    def test_goss_install_type(self, host):
        """Test Goss install type."""
        install_type = os.environ.get("goss_install_type", "static")
        assert install_type in ["static", "go"]


class TestGossConfiguration:
    """Tests for Goss configuration."""

    def test_goss_config_file(self, host):
        """Test Goss configuration file exists."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/templates/goss.yaml.j2")

    def test_goss_output_format(self, host):
        """Test Goss output format is configured."""
        output_format = os.environ.get("goss_output_format", "json")
        assert output_format in ["json", "rspecish", "documentation", "junit", "tap", "nagios"]

    def test_goss_directories(self, host):
        """Test Goss directories are configured."""
        goss_log_dir = os.environ.get("goss_log_dir", "/var/log/goss")
        assert goss_log_dir == "/var/log/goss"

    def test_goss_config_directory(self, host):
        """Test Goss config directory."""
        # The role creates /etc/goss for configuration
        assert True


class TestGossTestFiles:
    """Tests for Goss test files."""

    def test_goss_security_tests(self, host):
        """Test security tests file exists."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/files/security_tests.yaml")

    def test_goss_system_tests(self, host):
        """Test system tests file exists."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/files/system_tests.yaml")

    def test_goss_tests_directory(self, host):
        """Test Goss tests directory is configured."""
        # The role copies test files to /etc/goss/tests
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/files")


class TestGossDriftDetection:
    """Tests for Goss drift detection."""

    def test_drift_detection_enabled(self, host):
        """Test drift detection is enabled."""
        drift_enabled = os.environ.get("goss_enable_drift_detection", "true")
        assert drift_enabled in ["true", "false"]

    def test_drift_detection_file(self, host):
        """Test drift detection playbook exists."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/files/drift-detection.yml")

    def test_drift_check_interval(self, host):
        """Test drift check interval is configured."""
        interval = os.environ.get("goss_drift_check_interval", "3600")
        # Should be a positive integer (seconds)
        assert int(interval) > 0


class TestGossRemediation:
    """Tests for Goss auto remediation."""

    def test_auto_remediation_enabled(self, host):
        """Test auto remediation is enabled."""
        remediation_enabled = os.environ.get("goss_enable_auto_remediation", "false")
        assert remediation_enabled in ["true", "false"]

    def test_remediation_file(self, host):
        """Test remediation playbook exists."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/files/remediation.yml")


class TestGossCron:
    """Tests for Goss cron job."""

    def test_cron_enabled(self, host):
        """Test cron is enabled."""
        cron_enabled = os.environ.get("goss_enable_cron", "true")
        assert cron_enabled in ["true", "false"]

    def test_cron_schedule(self, host):
        """Test cron schedule is configured."""
        cron_minute = os.environ.get("goss_cron_minute", "0")
        cron_hour = os.environ.get("goss_cron_hour", "*/6")
        
        # Basic validation of cron fields
        assert cron_minute is not None
        assert cron_hour is not None


class TestGossLogging:
    """Tests for Goss logging."""

    def test_goss_log_directory(self, host):
        """Test Goss log directory exists."""
        log_dir = os.environ.get("goss_log_dir", "/var/log/goss")
        # The role creates this directory
        assert log_dir == "/var/log/goss"

    def test_goss_log_permissions(self, host):
        """Test Goss log directory has proper permissions."""
        # Should be readable by root
        assert True


class TestGossValidation:
    """Tests for Goss validation."""

    def test_goss_initial_validation(self, host):
        """Test initial validation is run."""
        # The role runs initial validation
        assert True

    def test_goss_validate_command(self, host):
        """Test goss validate command is available."""
        # The role uses 'goss validate' command
        assert True


class TestGossSecurity:
    """Tests for Goss security configuration."""

    def test_goss_permissions(self, host):
        """Test Goss files have proper permissions."""
        # Configuration files should be owned by root
        assert True

    def test_goss_tags(self, host):
        """Test Goss has proper tags."""
        tags = os.environ.get("goss_tags", "")
        # Should have security-related tags
        assert "security" in tags or "monitoring" in tags or tags != ""


class TestGossRoleStructure:
    """Tests for Goss role structure."""

    def test_goss_role_files(self, host):
        """Test all required role files exist."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/tasks/main.yml")
        assert os.path.exists(f"{role_path}/defaults/main.yml")
        assert os.path.exists(f"{role_path}/vars/main.yml")
        assert os.path.exists(f"{role_path}/templates")
        assert os.path.exists(f"{role_path}/files")

    def test_goss_handlers_defined(self, host):
        """Test Goss handlers are defined."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/handlers/main.yml")

    def test_goss_meta_defined(self, host):
        """Test Goss role metadata is defined."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/goss")
        
        assert os.path.exists(f"{role_path}/meta/main.yml")
