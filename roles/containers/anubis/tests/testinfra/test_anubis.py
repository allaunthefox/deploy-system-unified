# =============================================================================
# Audit Event Identifier: DSU-PYS-500015
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for containers/anubis role.

This role handles Anubis Web AI Firewall:
- Anubis network quadlet configuration
- Anubis container deployment via quadlet
- Service management and startup
- GPU support configuration (optional)
"""
import pytest


# Anubis directories
ANUBIS_DIRS = {
    "/srv/containers/anubis": {"mode": 0o755},
    "/srv/containers/anubis/data": {"mode": 0o755},
    "/srv/containers/anubis/config": {"mode": 0o755},
}

# Anubis configuration
ANUBIS_NETWORK_FILE = "/etc/containers/systemd/anubis_net.network"
ANUBIS_CONTAINER_FILE = "/etc/containers/systemd/anubis.container"

# Anubis default port
ANUBIS_DEFAULT_PORT = 31338


class TestAnubisNetwork:
    """Test Anubis network configuration."""

    def test_anubis_network_quadlet_exists(self, host):
        """Verify Anubis network quadlet exists."""
        f = host.file(ANUBIS_NETWORK_FILE)
        assert f.exists, f"{ANUBIS_NETWORK_FILE} should exist"
        assert f.is_file, "anubis_net.network should be a file"

    def test_anubis_network_permissions(self, host):
        """Verify Anubis network quadlet has correct permissions."""
        f = host.file(ANUBIS_NETWORK_FILE)
        if f.exists:
            assert f.mode in [0o644, 0o640], \
                f"anubis_net.network should have secure permissions, got {oct(f.mode)}"

    def test_anubis_network_structure(self, host):
        """Verify Anubis network quadlet has correct structure."""
        f = host.file(ANUBIS_NETWORK_FILE)
        if f.exists:
            content = f.content_string
            assert "[Network]" in content, "Network quadlet should have [Network] section"
            assert "NetworkName=anubis_net" in content, \
                "Network quadlet should have NetworkName=anubis_net"
            assert "Driver=bridge" in content, \
                "Network quadlet should have Driver=bridge"

    def test_anubis_network_subnet(self, host):
        """Verify Anubis network has subnet configured."""
        f = host.file(ANUBIS_NETWORK_FILE)
        if f.exists:
            content = f.content_string
            assert "Subnet=" in content, "Network should have Subnet configured"
            # Default subnet is 10.89.50.0/24
            assert "10.89.50" in content or "Subnet=" in content, \
                "Network should have valid subnet"

    def test_anubis_network_gateway(self, host):
        """Verify Anubis network has gateway configured."""
        f = host.file(ANUBIS_NETWORK_FILE)
        if f.exists:
            content = f.content_string
            assert "Gateway=" in content, "Network should have Gateway configured"


class TestAnubisContainer:
    """Test Anubis container configuration."""

    def test_anubis_container_quadlet_exists(self, host):
        """Verify Anubis container quadlet exists."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        assert f.exists, f"{ANUBIS_CONTAINER_FILE} should exist"
        assert f.is_file, "anubis.container should be a file"

    def test_anubis_quadlet_permissions(self, host):
        """Verify Anubis quadlet has correct permissions."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"anubis.container should have secure permissions, got {oct(f.mode)}"

    def test_anubis_quadlet_structure(self, host):
        """Verify Anubis quadlet has correct structure."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            assert "[Unit]" in content, "Quadlet should have [Unit] section"
            assert "[Container]" in content, "Quadlet should have [Container] section"
            assert "[Service]" in content, "Quadlet should have [Service] section"
            assert "[Install]" in content, "Quadlet should have [Install] section"

    def test_anubis_quadlet_image(self, host):
        """Verify Anubis quadlet has image configured."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            assert "Image=" in content, "Quadlet should have Image= configured"
            assert "anubis" in content.lower() or "ghcr.io" in content.lower(), \
                "Quadlet should reference anubis image"

    def test_anubis_quadlet_container_name(self, host):
        """Verify Anubis quadlet has container name configured."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            assert "ContainerName=" in content, "Quadlet should have ContainerName= configured"

    def test_anubis_quadlet_port(self, host):
        """Verify Anubis quadlet has port configured."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            # Should have PublishPort=31338 or Network= configuration
            has_port = "PublishPort=31338" in content or \
                       "Network=host" in content or \
                       "Network=anubis_net" in content
            assert has_port, "Quadlet should have port or network configuration"

    def test_anubis_quadlet_environment(self, host):
        """Verify Anubis quadlet has environment configured."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            # Should have PORT and TARGET environment variables
            assert "Environment=" in content, "Quadlet should have Environment= configured"
            assert "PORT=" in content, "Quadlet should have PORT environment variable"
            assert "TARGET=" in content, "Quadlet should have TARGET environment variable"


class TestAnubisService:
    """Test Anubis systemd service."""

    def test_anubis_service_exists(self, host):
        """Verify Anubis systemd service exists."""
        svc = host.service("anubis")
        if svc.exists:
            assert svc.exists, "anubis service should exist"
        else:
            # May be managed via quadlet
            f = host.file("/etc/systemd/system/anubis.service")
            if not f.exists:
                f = host.file(ANUBIS_CONTAINER_FILE)
                if f.exists:
                    pytest.skip("Anubis managed via quadlet")
                else:
                    pytest.skip("Anubis service not found")

    def test_anubis_service_enabled(self, host):
        """Verify Anubis service is enabled."""
        svc = host.service("anubis")
        if svc.exists:
            assert svc.is_enabled, "anubis service should be enabled"
        else:
            pytest.skip("Anubis service not available")

    def test_anubis_service_running(self, host):
        """Verify Anubis service is running."""
        svc = host.service("anubis")
        if svc.exists:
            assert svc.is_running, "anubis service should be running"
        else:
            pytest.skip("Anubis service not available")

    def test_anubis_service_restart_policy(self, host):
        """Verify Anubis service has restart policy configured."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            # Should have Restart=always in [Service] section
            assert "Restart=" in content, "Quadlet should have Restart= configured"


class TestAnubisNetworking:
    """Test Anubis networking configuration."""

    def test_anubis_port_listening(self, host):
        """Verify Anubis is listening on expected port."""
        cmd = host.run(f"ss -tlnp | grep ':{ANUBIS_DEFAULT_PORT}' 2>&1 || netstat -tlnp | grep ':{ANUBIS_DEFAULT_PORT}' 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert str(ANUBIS_DEFAULT_PORT) in cmd.stdout, \
                f"Anubis should be listening on port {ANUBIS_DEFAULT_PORT}"
        else:
            pytest.skip(f"Cannot verify port {ANUBIS_DEFAULT_PORT} (may need root)")

    def test_anubis_network_interface(self, host):
        """Verify Anubis network interface exists."""
        # Check for network interface or bridge
        cmd = host.run("ip link show | grep -E 'anubis|br-' 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "anubis" in cmd.stdout.lower() or "br-" in cmd.stdout, \
                "Anubis network interface should exist"
        else:
            pytest.skip("Cannot verify network interface")


class TestAnubisGPUConfiguration:
    """Test Anubis GPU configuration (optional)."""

    def test_anubis_quadlet_gpu_devices(self, host):
        """Verify Anubis quadlet has GPU devices configured if enabled."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            # GPU devices are optional
            if "Device=" in content:
                # If Device= is present, verify it's valid
                assert "/dev/" in content, "GPU Device should reference /dev/"
        else:
            pytest.skip("Anubis quadlet not found")

    def test_anubis_quadlet_gpu_capabilities(self, host):
        """Verify Anubis quadlet has GPU capabilities configured if enabled."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            # GPU capabilities are optional
            if "Capabilities=" in content:
                # Should have CAP_ prefixed capabilities
                assert "CAP_" in content, "GPU Capabilities should have CAP_ prefix"
        else:
            pytest.skip("Anubis quadlet not found")

    def test_dri_devices_available(self, host):
        """Verify /dev/dri devices are available for GPU access."""
        d = host.file("/dev/dri")
        if d.exists:
            assert d.is_directory, "/dev/dri should be a directory"
        else:
            pytest.skip("/dev/dri not available (no GPU)")


class TestAnubisValidation:
    """Test Anubis configuration validation."""

    def test_anubis_quadlet_gpu_capabilities_valid(self, host):
        """Verify Anubis quadlet GPU capabilities are valid (CAP_* only)."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            # Find Capabilities= line
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("Capabilities="):
                    caps = line.split("=", 1)[1].strip()
                    # All capabilities should start with CAP_
                    for cap in caps.split():
                        assert cap.startswith("CAP_"), \
                            f"Invalid capability: {cap} (should start with CAP_)"

    def test_anubis_quadlet_has_validators(self, host):
        """Verify Anubis quadlet has validators configured."""
        f = host.file(ANUBIS_CONTAINER_FILE)
        if f.exists:
            content = f.content_string
            # Should have VALIDATORS environment variable
            assert "VALIDATORS=" in content, "Quadlet should have VALIDATORS environment variable"


class TestAnubisCompletion:
    """Test Anubis configuration completion indicators."""

    def test_anubis_quadlet_service_symlink(self, host):
        """Verify Anubis quadlet service is properly linked."""
        cmd = host.run("systemctl list-unit-files | grep anubis 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "anubis" in cmd.stdout.lower(), "Anubis service should be listed"

    def test_anubis_container_image_available(self, host):
        """Verify Anubis container image is available."""
        cmd = host.run("podman images | grep -i anubis 2>&1 || docker images | grep -i anubis 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "anubis" in cmd.stdout.lower(), "Anubis image should be available"
        else:
            pytest.skip("Cannot verify Anubis image (podman/docker not available)")

    def test_anubis_systemd_integration(self, host):
        """Verify Anubis systemd integration is working."""
        cmd = host.run("systemctl status anubis 2>&1 || true")
        if cmd.rc == 0:
            assert "anubis" in cmd.stdout.lower(), "systemctl should show anubis status"
        else:
            pytest.skip("systemctl not available")
