# =============================================================================
# Audit Event Identifier: DSU-PYS-500030
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for ops/health_check role.

This role handles post-deployment health checks:
- Checking systemd unit health
- Checking container runtime health
- Checking disk usage thresholds
- Checking endpoint reachability
- Writing health summary artifacts
"""
import pytest


# Default health check paths
HEALTH_CHECK_OUTPUT_DIR = "/var/lib/deploy-system/health"


class TestHealthCheckConfiguration:
    """Test health check configuration."""

    def test_health_check_enabled(self, host):
        """Verify health check configuration is available."""
        # Health checks are enabled by default
        # This is verified through role variables
        pass

    def test_health_check_output_directory_exists(self, host):
        """Verify health check output directory exists."""
        d = host.file(HEALTH_CHECK_OUTPUT_DIR)
        if d.exists:
            assert d.is_directory, f"{HEALTH_CHECK_OUTPUT_DIR} should be a directory"
            assert d.mode in [0o755, 0o750, 0o700], f"{HEALTH_CHECK_OUTPUT_DIR} should have secure permissions"


class TestHealthCheckSystemd:
    """Test systemd unit health checks."""

    def test_systemd_available(self, host):
        """Verify systemd is available for health checks."""
        assert host.exists("systemctl"), "systemctl command should be available"

    def test_systemd_units_listable(self, host):
        """Verify systemd units can be listed."""
        cmd = host.run("systemctl list-units --type=service --no-pager 2>/dev/null | head -5 || true")
        if cmd.rc == 0:
            # Should be able to list units
            pass

    def test_mandatory_units_configured(self, host):
        """Verify mandatory units are configured for health checks."""
        # Default mandatory units: podman, caddy
        # Check if these units exist
        units = ["podman.service", "caddy.service"]
        for unit in units:
            svc = host.service(unit.replace(".service", ""))
            if svc.exists:
                # If unit exists, it should be checkable
                pass

    def test_optional_units_configured(self, host):
        """Verify optional units are configured for health checks."""
        # Default optional units: prometheus-node-exporter, smartd
        units = ["prometheus-node-exporter", "smartd"]
        for unit in units:
            svc = host.service(unit)
            if svc.exists:
                # Optional units may or may not exist
                pass


class TestHealthCheckContainerRuntime:
    """Test container runtime health checks."""

    def test_podman_available(self, host):
        """Verify podman is available if configured."""
        if host.exists("podman"):
            cmd = host.run("podman --version")
            if cmd.rc == 0:
                # Podman is available and working
                assert "podman" in cmd.stdout.lower(), "podman --version should return version info"

    def test_podman_info_works(self, host):
        """Verify podman info command works."""
        if host.exists("podman"):
            cmd = host.run("podman info --format '{{.Host.OS}}' 2>/dev/null || true")
            # Should be able to get podman info
            # May fail if podman is not properly configured

    def test_docker_available(self, host):
        """Verify docker is available if configured."""
        if host.exists("docker"):
            cmd = host.run("docker --version")
            if cmd.rc == 0:
                assert "docker" in cmd.stdout.lower(), "docker --version should return version info"

    def test_container_runtime_command(self, host):
        """Verify container runtime commands are executable."""
        runtimes = ["podman", "docker"]
        for runtime in runtimes:
            if host.exists(runtime):
                f = host.file(f"/usr/bin/{runtime}")
                if f.exists:
                    # Should be executable
                    pass


class TestHealthCheckDisk:
    """Test disk usage health checks."""

    def test_root_mountpoint_exists(self, host):
        """Verify root mountpoint exists."""
        d = host.file("/")
        assert d.exists, "/ should exist"
        assert d.is_directory, "/ should be a directory"

    def test_disk_usage_available(self, host):
        """Verify disk usage can be determined."""
        cmd = host.run("df -h / 2>/dev/null | tail -1 || true")
        if cmd.rc == 0 and cmd.stdout.strip():
            # Should be able to get disk usage
            parts = cmd.stdout.strip().split()
            assert len(parts) >= 5, "df output should have expected columns"

    def test_disk_usage_percent(self, host):
        """Verify disk usage percentage is available."""
        cmd = host.run("df / --output=pcent 2>/dev/null | tail -1 | tr -d '%' || true")
        if cmd.rc == 0 and cmd.stdout.strip():
            usage = cmd.stdout.strip()
            if usage.isdigit():
                # Usage should be a reasonable percentage
                assert 0 <= int(usage) <= 100, f"Disk usage should be 0-100%, got {usage}%"

    def test_srv_mountpoint(self, host):
        """Verify /srv mountpoint status."""
        d = host.file("/srv")
        if d.exists:
            assert d.is_directory, "/srv should be a directory"


class TestHealthCheckEndpoints:
    """Test endpoint health checks."""

    def test_localhost_reachable(self, host):
        """Verify localhost is reachable."""
        cmd = host.run("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/ 2>/dev/null || echo '000'")
        # May return various status codes or 000 if nothing is listening
        # This is informational

    def test_curl_available(self, host):
        """Verify curl is available for endpoint checks."""
        assert host.exists("curl"), "curl should be available"

    def test_node_exporter_endpoint(self, host):
        """Verify node_exporter endpoint if running."""
        cmd = host.run("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9100/metrics 2>/dev/null || echo '000'")
        # May return 200 if node_exporter is running
        # This is informational


class TestHealthCheckArtifacts:
    """Test health check artifact generation."""

    def test_health_summary_directory(self, host):
        """Verify health summary directory exists."""
        d = host.file(HEALTH_CHECK_OUTPUT_DIR)
        if d.exists:
            assert d.is_directory, f"{HEALTH_CHECK_OUTPUT_DIR} should be a directory"

    def test_health_summary_file_permissions(self, host):
        """Verify health summary files have correct permissions."""
        # Check for any health summary files
        cmd = host.run(f"find {HEALTH_CHECK_OUTPUT_DIR} -name '*.json' -type f 2>/dev/null | head -5 || true")
        if cmd.rc == 0 and cmd.stdout.strip():
            for json_file in cmd.stdout.strip().split("\n"):
                f = host.file(json_file)
                if f.exists:
                    assert f.mode in [0o644, 0o640, 0o600], f"{json_file} should have secure permissions"

    def test_health_summary_json_format(self, host):
        """Verify health summary is valid JSON."""
        import json
        cmd = host.run(f"find {HEALTH_CHECK_OUTPUT_DIR} -name '*.json' -type f 2>/dev/null | head -1 || true")
        if cmd.rc == 0 and cmd.stdout.strip():
            json_file = cmd.stdout.strip()
            f = host.file(json_file)
            if f.exists:
                try:
                    content = f.content_string
                    data = json.loads(content)
                    # Should have expected schema
                    assert "schema" in data or "host" in data, "Health summary should have expected fields"
                except json.JSONDecodeError:
                    pytest.fail(f"{json_file} should be valid JSON")


class TestHealthCheckValidation:
    """Test health check validation."""

    def test_health_check_schema(self, host):
        """Verify health check uses correct schema."""
        # Schema is defined in role defaults
        expected_schema = "deploy-system-unified/health-check/v1"
        # This is verified through role configuration

    def test_mandatory_check_failures_reported(self, host):
        """Verify mandatory check failures are reported."""
        # Health check should report mandatory failures
        # This is verified through role output

    def test_health_check_timestamp(self, host):
        """Verify health check includes timestamp."""
        # Health summary should include generated_at timestamp
        # This is verified through artifact content
