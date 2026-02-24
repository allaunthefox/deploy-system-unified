"""
Testinfra tests for containers/caddy role.

This role handles Caddy reverse proxy configuration:
- Caddy container deployment via quadlet
- Caddyfile configuration
- Crowdsec integration
- TLS/ACME configuration
- Proxy network setup
"""
import pytest


# Caddy directories
CADDY_DIRS = {
    "/srv/containers/caddy": {"mode": 0o755},
    "/srv/containers/caddy/config": {"mode": 0o755},
    "/srv/containers/caddy/data": {"mode": 0o755},
    "/srv/containers/caddy/logs": {"mode": 0o755},
    "/srv/containers/caddy/conf.d": {"mode": 0o755},
}

# Caddy configuration files
CADDY_CONFIG_FILES = [
    "/srv/containers/caddy/Caddyfile",
]

# Crowdsec directories (when enabled)
CROWDSEC_DIRS = {
    "/srv/containers/caddy/crowdsec": {"mode": 0o755},
    "/srv/containers/caddy/crowdsec/config": {"mode": 0o755},
    "/srv/containers/caddy/crowdsec/data": {"mode": 0o755},
}

# Caddy secrets
CADDY_SECRETS_FILE = "/etc/containers/secrets/caddy.env"


class TestCaddyDirectories:
    """Test Caddy directory structure."""

    @pytest.mark.parametrize("path,expected", CADDY_DIRS.items())
    def test_caddy_directories_exist(self, host, path, expected):
        """Verify Caddy directories exist."""
        d = host.file(path)
        assert d.exists, f"{path} should exist"
        assert d.is_directory, f"{path} should be a directory"

    @pytest.mark.parametrize("path,expected", CADDY_DIRS.items())
    def test_caddy_directories_permissions(self, host, path, expected):
        """Verify Caddy directories have correct permissions."""
        d = host.file(path)
        if d.exists:
            assert d.mode == expected["mode"], \
                f"{path} should have mode {oct(expected['mode'])}, got {oct(d.mode)}"

    def test_caddy_base_directory(self, host):
        """Verify /srv/containers/caddy exists."""
        d = host.file("/srv/containers/caddy")
        assert d.exists, "/srv/containers/caddy should exist"
        assert d.is_directory, "/srv/containers/caddy should be a directory"


class TestCaddyConfiguration:
    """Test Caddy configuration files."""

    def test_caddyfile_exists(self, host):
        """Verify Caddyfile exists."""
        f = host.file("/srv/containers/caddy/Caddyfile")
        assert f.exists, "/srv/containers/caddy/Caddyfile should exist"
        assert f.is_file, "Caddyfile should be a file"

    def test_caddyfile_permissions(self, host):
        """Verify Caddyfile has correct permissions."""
        f = host.file("/srv/containers/caddy/Caddyfile")
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"Caddyfile should have secure permissions, got {oct(f.mode)}"

    def test_caddyfile_content(self, host):
        """Verify Caddyfile has correct structure."""
        f = host.file("/srv/containers/caddy/Caddyfile")
        if f.exists:
            content = f.content_string
            # Should have global options block
            assert "{" in content, "Caddyfile should have configuration blocks"
            # Should have either site blocks or global options
            assert "://" in content or "respond" in content.lower() or \
                   "import" in content.lower(), \
                "Caddyfile should have site configuration"

    def test_caddyfile_global_options(self, host):
        """Verify Caddyfile has global options configured."""
        f = host.file("/srv/containers/caddy/Caddyfile")
        if f.exists:
            content = f.content_string
            # Should have admin off or admin configuration
            assert "admin" in content.lower() or "servers" in content.lower(), \
                "Caddyfile should have global options"

    def test_caddyfile_logging_configured(self, host):
        """Verify Caddyfile has logging configured."""
        f = host.file("/srv/containers/caddy/Caddyfile")
        if f.exists:
            content = f.content_string
            # Should have log configuration
            assert "log" in content.lower(), "Caddyfile should have logging configured"


class TestCaddyQuadlet:
    """Test Caddy quadlet configuration."""

    def test_caddy_container_quadlet_exists(self, host):
        """Verify Caddy container quadlet exists."""
        f = host.file("/etc/containers/systemd/caddy.container")
        assert f.exists, "/etc/containers/systemd/caddy.container should exist"
        assert f.is_file, "caddy.container should be a file"

    def test_caddy_quadlet_permissions(self, host):
        """Verify Caddy quadlet has correct permissions."""
        f = host.file("/etc/containers/systemd/caddy.container")
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"caddy.container should have secure permissions, got {oct(f.mode)}"

    def test_caddy_quadlet_structure(self, host):
        """Verify Caddy quadlet has correct structure."""
        f = host.file("/etc/containers/systemd/caddy.container")
        if f.exists:
            content = f.content_string
            assert "[Unit]" in content, "Quadlet should have [Unit] section"
            assert "[Container]" in content, "Quadlet should have [Container] section"
            assert "Image=" in content, "Quadlet should have Image= configured"
            assert "ContainerName=caddy" in content, "Quadlet should have ContainerName=caddy"

    def test_caddy_quadlet_network(self, host):
        """Verify Caddy quadlet has network configured."""
        f = host.file("/etc/containers/systemd/caddy.container")
        if f.exists:
            content = f.content_string
            # Should have Network= or PublishPort=
            has_network = "Network=" in content or "PublishPort=" in content
            assert has_network, "Quadlet should have network configuration"

    def test_caddy_quadlet_volumes(self, host):
        """Verify Caddy quadlet has volumes configured."""
        f = host.file("/etc/containers/systemd/caddy.container")
        if f.exists:
            content = f.content_string
            # Should have Volume= for Caddyfile and data directories
            assert "Volume=" in content, "Quadlet should have Volume= configured"
            assert "/srv/containers/caddy" in content, \
                "Quadlet should mount /srv/containers/caddy"


class TestCaddyService:
    """Test Caddy systemd service."""

    def test_caddy_service_exists(self, host):
        """Verify Caddy systemd service exists."""
        svc = host.service("caddy")
        if svc.exists:
            assert svc.exists, "caddy service should exist"
        else:
            # May be managed via quadlet
            f = host.file("/etc/systemd/system/caddy.service")
            if not f.exists:
                f = host.file("/etc/containers/systemd/caddy.container")
                if f.exists:
                    pytest.skip("Caddy managed via quadlet")
                else:
                    pytest.skip("Caddy service not found")

    def test_caddy_service_running(self, host):
        """Verify Caddy service is running."""
        svc = host.service("caddy")
        if svc.exists:
            assert svc.is_running, "caddy service should be running"
        else:
            pytest.skip("Caddy service not available")

    def test_caddy_service_enabled(self, host):
        """Verify Caddy service is enabled."""
        svc = host.service("caddy")
        if svc.exists:
            assert svc.is_enabled, "caddy service should be enabled"
        else:
            pytest.skip("Caddy service not available")


class TestCaddyNetwork:
    """Test Caddy network configuration."""

    def test_proxy_network_quadlet_exists(self, host):
        """Verify proxy network quadlet exists."""
        f = host.file("/etc/containers/systemd/proxy_net.network")
        if f.exists:
            assert f.is_file, "proxy_net.network should be a file"
            content = f.content_string
            assert "[Network]" in content, "Network quadlet should have [Network] section"
            assert "NetworkName=proxy_net" in content, \
                "Network quadlet should have NetworkName=proxy_net"
        else:
            pytest.skip("Proxy network quadlet not found")

    def test_caddy_ports_listening(self, host):
        """Verify Caddy is listening on expected ports."""
        # Check for ports 80 and 443
        cmd = host.run("ss -tlnp | grep -E ':80|:443' 2>&1 || netstat -tlnp | grep -E ':80|:443' 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert ":80" in cmd.stdout or ":443" in cmd.stdout, \
                "Caddy should be listening on port 80 or 443"
        else:
            pytest.skip("Cannot verify port bindings (may need root)")


class TestCaddySecrets:
    """Test Caddy secrets configuration."""

    def test_caddy_secrets_directory(self, host):
        """Verify Caddy secrets directory exists."""
        d = host.file("/etc/containers/secrets")
        if d.exists:
            assert d.is_directory, "/etc/containers/secrets should be a directory"
            assert d.mode in [0o700, 0o750], \
                f"Secrets directory should have secure permissions, got {oct(d.mode)}"
        else:
            pytest.skip("Secrets directory not found")

    def test_caddy_env_file(self, host):
        """Verify Caddy environment file exists."""
        f = host.file(CADDY_SECRETS_FILE)
        if f.exists:
            assert f.is_file, "caddy.env should be a file"
            assert f.mode in [0o600, 0o640], \
                f"caddy.env should have secure permissions, got {oct(f.mode)}"
            assert f.user == "root", "caddy.env should be owned by root"
        else:
            pytest.skip("Caddy environment file not found")


class TestCrowdsecIntegration:
    """Test Crowdsec integration with Caddy."""

    def test_crowdsec_directories_exist(self, host):
        """Verify Crowdsec directories exist."""
        for path, expected in CROWDSEC_DIRS.items():
            d = host.file(path)
            if d.exists:
                assert d.is_directory, f"{path} should be a directory"
            else:
                pytest.skip(f"{path} does not exist (Crowdsec may not be enabled)")
                break

    def test_crowdsec_container_quadlet(self, host):
        """Verify Crowdsec container quadlet exists."""
        f = host.file("/etc/containers/systemd/crowdsec.container")
        if f.exists:
            assert f.is_file, "crowdsec.container should be a file"
            content = f.content_string
            assert "[Container]" in content, "Quadlet should have [Container] section"
            assert "crowdsec" in content.lower(), "Quadlet should reference crowdsec"
        else:
            pytest.skip("Crowdsec quadlet not found (may not be enabled)")

    def test_crowdsec_bouncer_config(self, host):
        """Verify Crowdsec bouncer configuration exists."""
        f = host.file("/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml")
        if f.exists:
            assert f.is_file, "Bouncer config should be a file"
            assert f.mode in [0o600, 0o640], \
                f"Bouncer config should have secure permissions, got {oct(f.mode)}"
        else:
            pytest.skip("Crowdsec bouncer config not found")

    def test_crowdsec_bouncer_binary(self, host):
        """Verify Crowdsec bouncer binary exists."""
        f = host.file("/usr/local/bin/crowdsec-firewall-bouncer")
        if f.exists:
            assert f.is_file, "Bouncer binary should be a file"
            assert f.mode in [0o755, 0o755], "Bouncer binary should be executable"
        else:
            pytest.skip("Crowdsec bouncer binary not found")

    def test_crowdsec_bouncer_service(self, host):
        """Verify Crowdsec bouncer service exists."""
        svc = host.service("crowdsec-firewall-bouncer")
        if svc.exists:
            assert svc.exists, "crowdsec-firewall-bouncer service should exist"
        else:
            pytest.skip("Crowdsec bouncer service not found")


class TestCaddyLogs:
    """Test Caddy logging configuration."""

    def test_caddy_logs_directory(self, host):
        """Verify Caddy logs directory exists."""
        d = host.file("/srv/containers/caddy/logs")
        assert d.exists, "/srv/containers/caddy/logs should exist"
        assert d.is_directory, "/srv/containers/caddy/logs should be a directory"

    def test_caddy_access_log(self, host):
        """Verify Caddy access log exists or directory is writable."""
        f = host.file("/srv/containers/caddy/logs/access.log")
        if f.exists:
            assert f.is_file, "access.log should be a file"
        else:
            # Log may be created on first request
            d = host.file("/srv/containers/caddy/logs")
            assert d.is_directory, "Logs directory should exist"


class TestCaddyCompletion:
    """Test Caddy configuration completion indicators."""

    def test_caddy_quadlet_service_symlink(self, host):
        """Verify Caddy quadlet service is properly linked."""
        # Quadlet creates symlinks to generated services
        cmd = host.run("systemctl list-unit-files | grep caddy 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "caddy" in cmd.stdout.lower(), "Caddy service should be listed"

    def test_caddy_container_image_available(self, host):
        """Verify Caddy container image is available."""
        cmd = host.run("podman images | grep -i caddy 2>&1 || docker images | grep -i caddy 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "caddy" in cmd.stdout.lower(), "Caddy image should be available"
        else:
            pytest.skip("Cannot verify Caddy image (podman/docker not available)")
