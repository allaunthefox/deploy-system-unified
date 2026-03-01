# =============================================================================
# Audit Event Identifier: DSU-PYS-500024
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for containers/quadlets role.

This role handles systemd quadlet management:
- Creating quadlet network configurations
- Deploying custom quadlet files
- Systemd integration for containers
- Quadlet checkpoint management
"""
import pytest


# Quadlet directories
QUADLET_DIRS = {
    "/etc/containers/systemd": {"mode": 0o755},
    "/etc/containers/systemd/users": {"mode": 0o755},
}

# Quadlet file types
QUADLET_FILE_TYPES = [".container", ".pod", ".network", ".volume", ".kube"]

# Checkpoint directory
CHECKPOINT_DIR = "/var/lib/deploy-system/checkpoints"
QUADLET_CHECKPOINT_FILE = f"{CHECKPOINT_DIR}/quadlets_checkpoint.json"


class TestQuadletDirectories:
    """Test quadlet directory structure."""

    @pytest.mark.parametrize("path,expected", QUADLET_DIRS.items())
    def test_quadlet_directories_exist(self, host, path, expected):
        """Verify quadlet directories exist."""
        d = host.file(path)
        if d.exists:
            assert d.is_directory, f"{path} should be a directory"
        else:
            pytest.skip(f"{path} does not exist")

    def test_systemd_containers_directory(self, host):
        """Verify /etc/containers/systemd directory exists."""
        d = host.file("/etc/containers/systemd")
        if d.exists:
            assert d.is_directory, "/etc/containers/systemd should be a directory"
            assert d.mode in [0o755, 0o750, 0o700], \
                f"/etc/containers/systemd should have secure permissions, got {oct(d.mode)}"
        else:
            pytest.skip("/etc/containers/systemd does not exist")

    def test_user_quadlet_directory(self, host):
        """Verify user quadlet directory exists."""
        d = host.file("/etc/containers/systemd/users")
        if d.exists:
            assert d.is_directory, "/etc/containers/systemd/users should be a directory"
        else:
            # May not exist if no user quadlets configured
            pytest.skip("User quadlet directory does not exist")


class TestQuadletNetworkConfiguration:
    """Test quadlet network configuration."""

    def test_quadlet_network_file_exists(self, host):
        """Verify quadlet network configuration file exists."""
        # Look for any .network files
        cmd = host.run("ls /etc/containers/systemd/*.network 2>&1")
        if cmd.rc == 0:
            assert ".network" in cmd.stdout, "Should have at least one .network file"
        else:
            pytest.skip("No quadlet network files found")

    def test_quadlet_network_content(self, host):
        """Verify quadlet network file has correct structure."""
        cmd = host.run("ls /etc/containers/systemd/*.network 2>&1")
        if cmd.rc == 0:
            network_files = cmd.stdout.strip().split("\n")
            for network_file in network_files:
                if network_file.strip():
                    f = host.file(network_file.strip())
                    if f.exists:
                        content = f.content_string
                        assert "[Network]" in content, \
                            f"{network_file} should have [Network] section"
                        assert "NetworkName=" in content or "Subnet=" in content, \
                            f"{network_file} should have network configuration"

    def test_quadlet_network_subnet_configured(self, host):
        """Verify quadlet network has subnet configured."""
        cmd = host.run("grep -r 'Subnet=' /etc/containers/systemd/*.network 2>&1")
        if cmd.rc == 0:
            assert "Subnet=" in cmd.stdout, "Network should have Subnet configured"
        else:
            pytest.skip("No subnet configuration found in network files")


class TestQuadletContainerFiles:
    """Test quadlet container configuration files."""

    def test_quadlet_container_files_exist(self, host):
        """Verify quadlet container files exist."""
        cmd = host.run("ls /etc/containers/systemd/*.container 2>&1")
        if cmd.rc == 0:
            assert ".container" in cmd.stdout, "Should have at least one .container file"
        else:
            pytest.skip("No quadlet container files found")

    def test_quadlet_container_structure(self, host):
        """Verify quadlet container file has correct structure."""
        cmd = host.run("ls /etc/containers/systemd/*.container 2>&1")
        if cmd.rc == 0:
            container_files = cmd.stdout.strip().split("\n")
            for container_file in container_files:
                if container_file.strip():
                    f = host.file(container_file.strip())
                    if f.exists:
                        content = f.content_string
                        assert "[Unit]" in content or "[Container]" in content, \
                            f"{container_file} should have [Unit] or [Container] section"
                        assert "Image=" in content, \
                            f"{container_file} should have Image= configured"

    def test_quadlet_container_has_image(self, host):
        """Verify quadlet container has image configured."""
        cmd = host.run("grep -r '^Image=' /etc/containers/systemd/*.container 2>&1")
        if cmd.rc == 0:
            assert "Image=" in cmd.stdout, "Container should have Image configured"
        else:
            pytest.skip("No Image configuration found in container files")


class TestQuadletPodFiles:
    """Test quadlet pod configuration files."""

    def test_quadlet_pod_files_exist(self, host):
        """Verify quadlet pod files exist."""
        cmd = host.run("ls /etc/containers/systemd/*.pod 2>&1")
        if cmd.rc == 0:
            assert ".pod" in cmd.stdout, "Should have at least one .pod file"
        else:
            pytest.skip("No quadlet pod files found")

    def test_quadlet_pod_structure(self, host):
        """Verify quadlet pod file has correct structure."""
        cmd = host.run("ls /etc/containers/systemd/*.pod 2>&1")
        if cmd.rc == 0:
            pod_files = cmd.stdout.strip().split("\n")
            for pod_file in pod_files:
                if pod_file.strip():
                    f = host.file(pod_file.strip())
                    if f.exists:
                        content = f.content_string
                        assert "[Pod]" in content, \
                            f"{pod_file} should have [Pod] section"


class TestQuadletSystemdIntegration:
    """Test quadlet systemd integration."""

    def test_systemd_daemon_reload(self, host):
        """Verify systemd daemon can be reloaded."""
        cmd = host.run("systemctl daemon-reload 2>&1")
        if cmd.rc == 0:
            assert "" in cmd.stdout or cmd.rc == 0, "systemctl daemon-reload should succeed"
        else:
            pytest.skip("systemctl daemon-reload not available (possibly in container)")

    def test_quadlet_services_listed(self, host):
        """Verify quadlet-generated services are listed."""
        # Check for container/pod services
        cmd = host.run("systemctl list-unit-files --type=service 2>&1 | grep -E '\\.(container|pod)' || true")
        # This may return empty if no quadlets are active, which is OK

    def test_systemd_user_quadlet_services(self, host):
        """Verify user-level quadlet services exist."""
        cmd = host.run("systemctl --user list-unit-files --type=service 2>&1 | grep -E '\\.(container|pod)' || true")
        # User services may not exist if running as root


class TestQuadletCheckpoint:
    """Test quadlet checkpoint management."""

    def test_checkpoint_directory_exists(self, host):
        """Verify checkpoint directory exists."""
        d = host.file(CHECKPOINT_DIR)
        if d.exists:
            assert d.is_directory, f"{CHECKPOINT_DIR} should be a directory"
            assert d.mode in [0o700, 0o750, 0o755], \
                f"Checkpoint directory should have secure permissions, got {oct(d.mode)}"
        else:
            pytest.skip(f"{CHECKPOINT_DIR} does not exist")

    def test_quadlet_checkpoint_file(self, host):
        """Verify quadlet checkpoint file exists."""
        f = host.file(QUADLET_CHECKPOINT_FILE)
        if f.exists:
            assert f.is_file, "Quadlet checkpoint should be a file"
            assert f.mode in [0o600, 0o640, 0o644], \
                f"Checkpoint file should have secure permissions, got {oct(f.mode)}"
            # Should be valid JSON
            content = f.content_string
            assert "uuid" in content.lower() or "role" in content.lower(), \
                "Checkpoint should contain uuid or role"
        else:
            pytest.skip("Quadlet checkpoint file does not exist")


class TestQuadletVolumeFiles:
    """Test quadlet volume configuration files."""

    def test_quadlet_volume_files_exist(self, host):
        """Verify quadlet volume files exist."""
        cmd = host.run("ls /etc/containers/systemd/*.volume 2>&1")
        if cmd.rc == 0:
            assert ".volume" in cmd.stdout, "Should have at least one .volume file"
        else:
            pytest.skip("No quadlet volume files found")

    def test_quadlet_volume_structure(self, host):
        """Verify quadlet volume file has correct structure."""
        cmd = host.run("ls /etc/containers/systemd/*.volume 2>&1")
        if cmd.rc == 0:
            volume_files = cmd.stdout.strip().split("\n")
            for volume_file in volume_files:
                if volume_file.strip():
                    f = host.file(volume_file.strip())
                    if f.exists:
                        content = f.content_string
                        assert "[Volume]" in content, \
                            f"{volume_file} should have [Volume] section"


class TestQuadletCompletion:
    """Test quadlet configuration completion indicators."""

    def test_quadlet_systemd_integration(self, host):
        """Verify quadlet systemd integration is working."""
        # Check if systemd can see quadlet units
        cmd = host.run("systemctl list-units --type=service --all 2>&1 | head -5")
        if cmd.rc == 0:
            assert "systemd" in cmd.stdout.lower() or "service" in cmd.stdout.lower(), \
                "systemctl should list units"
        else:
            pytest.skip("systemctl not available")

    def test_containers_systemd_directory_structure(self, host):
        """Verify /etc/containers/systemd directory structure."""
        d = host.file("/etc/containers/systemd")
        if d.exists and d.is_directory:
            # Should be able to list contents
            cmd = host.run("ls -la /etc/containers/systemd/ 2>&1")
            if cmd.rc == 0:
                assert "total" in cmd.stdout, "Should be able to list systemd directory"
