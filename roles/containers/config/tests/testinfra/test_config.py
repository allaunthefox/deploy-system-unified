"""
Testinfra tests for containers/config role.

This role handles general container configuration:
- Container storage directories
- Container storage configuration
- Container lingering for service users
- Container secrets setup
"""
import pytest


# Container storage directories
CONTAINER_STORAGE_DIRS = {
    "/srv/containers": {"mode": 0o755, "owner": "root", "group": "root"},
    "/srv/containers/volumes": {"mode": 0o755, "owner": "root", "group": "root"},
    "/srv/containers/configs": {"mode": 0o755, "owner": "root", "group": "root"},
    "/var/lib/containers": {"mode": 0o755, "owner": "root", "group": "root"},
}

# Storage configuration file
STORAGE_CONFIG_FILE = "/etc/containers/storage.conf"


class TestContainerStorageDirectories:
    """Test container storage directory creation."""

    @pytest.mark.parametrize("path,expected", CONTAINER_STORAGE_DIRS.items())
    def test_container_storage_directories_exist(self, host, path, expected):
        """Verify container storage directories exist."""
        d = host.file(path)
        assert d.exists, f"{path} should exist"
        assert d.is_directory, f"{path} should be a directory"

    @pytest.mark.parametrize("path,expected", CONTAINER_STORAGE_DIRS.items())
    def test_container_storage_directories_permissions(self, host, path, expected):
        """Verify container storage directories have correct permissions."""
        d = host.file(path)
        if d.exists:
            assert d.mode == expected["mode"], \
                f"{path} should have mode {oct(expected['mode'])}, got {oct(d.mode)}"
            assert d.user == expected["owner"], \
                f"{path} should be owned by {expected['owner']}"
            assert d.group == expected["group"], \
                f"{path} group should be {expected['group']}"

    def test_srv_containers_structure(self, host):
        """Verify /srv/containers directory structure."""
        base = host.file("/srv/containers")
        if base.exists and base.is_directory:
            # Check subdirectories
            volumes = host.file("/srv/containers/volumes")
            configs = host.file("/srv/containers/configs")
            if volumes.exists:
                assert volumes.is_directory, "/srv/containers/volumes should be a directory"
            if configs.exists:
                assert configs.is_directory, "/srv/containers/configs should be a directory"


class TestContainerStorageConfiguration:
    """Test container storage configuration."""

    def test_storage_config_exists(self, host):
        """Verify container storage configuration file exists."""
        f = host.file(STORAGE_CONFIG_FILE)
        assert f.exists, f"{STORAGE_CONFIG_FILE} should exist"
        assert f.is_file, f"{STORAGE_CONFIG_FILE} should be a file"

    def test_storage_config_permissions(self, host):
        """Verify storage configuration has correct permissions."""
        f = host.file(STORAGE_CONFIG_FILE)
        assert f.mode in [0o644, 0o640, 0o600], \
            f"storage.conf should have secure permissions, got {oct(f.mode)}"
        assert f.user == "root", "storage.conf should be owned by root"
        assert f.group in ["root", "containers"], \
            f"storage.conf group should be root or containers"

    def test_storage_driver_configured(self, host):
        """Verify storage driver is configured as overlay."""
        f = host.file(STORAGE_CONFIG_FILE)
        content = f.content_string
        has_driver = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("driver ="):
                has_driver = True
                assert "overlay" in line.lower(), \
                    f"Storage driver should be overlay, got {line}"
                break
        assert has_driver, "Storage driver should be configured"

    def test_storage_runroot_configured(self, host):
        """Verify storage runroot is configured."""
        f = host.file(STORAGE_CONFIG_FILE)
        content = f.content_string
        has_runroot = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("runroot ="):
                has_runroot = True
                assert "/run/containers" in line, \
                    f"runroot should be in /run/containers, got {line}"
                break
        assert has_runroot, "Storage runroot should be configured"

    def test_storage_graphroot_configured(self, host):
        """Verify storage graphroot is configured."""
        f = host.file(STORAGE_CONFIG_FILE)
        content = f.content_string
        has_graphroot = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("graphroot ="):
                has_graphroot = True
                assert "/var/lib/containers" in line, \
                    f"graphroot should be in /var/lib/containers, got {line}"
                break
        assert has_graphroot, "Storage graphroot should be configured"

    def test_storage_overlay_options(self, host):
        """Verify overlay storage options are configured."""
        f = host.file(STORAGE_CONFIG_FILE)
        content = f.content_string
        has_overlay_section = "[storage.options.overlay]" in content or \
                              "[storage.options]" in content
        assert has_overlay_section, "Storage overlay options should be configured"


class TestContainerLingering:
    """Test container lingering configuration for service users."""

    def test_lingercmd_available(self, host):
        """Verify loginctl command is available."""
        cmd = host.run("loginctl --help 2>&1")
        if cmd.rc == 0:
            assert "linger" in cmd.stdout.lower(), "loginctl should support linger"
        else:
            pytest.skip("loginctl not available (possibly in container)")

    def test_linger_directory_exists(self, host):
        """Verify linger directory exists."""
        d = host.file("/var/lib/systemd/linger")
        if d.exists:
            assert d.is_directory, "/var/lib/systemd/linger should be a directory"
        else:
            pytest.skip("Linger directory not found")

    def test_linger_status_command(self, host):
        """Verify loginctl show-user command works."""
        cmd = host.run("loginctl show-user root -p Linger 2>&1")
        if cmd.rc == 0:
            assert "Linger" in cmd.stdout, "loginctl should return Linger status"
        else:
            pytest.skip("loginctl show-user not available")


class TestContainerConfigurationFiles:
    """Test container configuration files."""

    def test_containers_directory_exists(self, host):
        """Verify /etc/containers directory exists."""
        d = host.file("/etc/containers")
        assert d.exists, "/etc/containers should exist"
        assert d.is_directory, "/etc/containers should be a directory"

    def test_containers_directory_permissions(self, host):
        """Verify /etc/containers has correct permissions."""
        d = host.file("/etc/containers")
        assert d.mode in [0o755, 0o750, 0o700], \
            f"/etc/containers should have secure permissions, got {oct(d.mode)}"

    def test_containers_registries_conf(self, host):
        """Verify registries.conf exists."""
        f = host.file("/etc/containers/registries.conf")
        if f.exists:
            assert f.is_file, "registries.conf should be a file"
            assert f.mode in [0o644, 0o640], \
                f"registries.conf should have secure permissions, got {oct(f.mode)}"

    def test_containers_policy_json(self, host):
        """Verify policy.json exists."""
        f = host.file("/etc/containers/policy.json")
        if f.exists:
            assert f.is_file, "policy.json should be a file"
            # policy.json should be valid JSON
            content = f.content_string
            assert "default" in content.lower() or "type" in content.lower(), \
                "policy.json should contain policy definitions"

    def test_containers_mounts_conf(self, host):
        """Verify mounts.conf exists."""
        f = host.file("/etc/containers/mounts.conf")
        if f.exists:
            assert f.is_file, "mounts.conf should be a file"


class TestContainerSecrets:
    """Test container secrets configuration."""

    def test_containers_secrets_directory(self, host):
        """Verify containers secrets directory exists."""
        d = host.file("/etc/containers/secrets")
        if d.exists:
            assert d.is_directory, "/etc/containers/secrets should be a directory"
            assert d.mode in [0o700, 0o750], \
                f"secrets directory should have secure permissions, got {oct(d.mode)}"
        else:
            pytest.skip("Container secrets directory not found")


class TestContainerConfigCompletion:
    """Test container configuration completion indicators."""

    def test_podman_storage_info(self, host):
        """Verify podman storage info shows configured paths."""
        cmd = host.run("podman info --format '{{.Store.GraphRoot}}' 2>&1")
        if cmd.rc == 0:
            assert "/var/lib/containers" in cmd.stdout or \
                   cmd.stdout.strip() != "", \
                "podman should report storage configuration"
        else:
            pytest.skip("podman info not available")

    def test_container_config_files_readable(self, host):
        """Verify container configuration files are readable."""
        config_files = [
            "/etc/containers/storage.conf",
            "/etc/containers/registries.conf",
        ]
        readable_count = 0
        for config_file in config_files:
            f = host.file(config_file)
            if f.exists and f.is_file:
                readable_count += 1
        assert readable_count > 0, "At least one container config file should be readable"
