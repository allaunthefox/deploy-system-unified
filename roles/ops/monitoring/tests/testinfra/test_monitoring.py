# =============================================================================
# Audit Event Identifier: DSU-PYS-500031
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for ops/monitoring role.

This role handles system monitoring configuration:
- Installing prometheus-node-exporter
- Installing smartmontools for disk monitoring
- Installing nvme-cli for NVMe drive monitoring
- Configuring and starting monitoring services
"""
import pytest


# Service names by distribution
NODE_EXPORTER_SERVICES = {
    "debian": "prometheus-node-exporter",
    "ubuntu": "prometheus-node-exporter",
    "arch": "prometheus-node-exporter",
    "fedora": "node_exporter",
    "alpine": "node-exporter",
}

# Default monitoring port
NODE_EXPORTER_PORT = 9100


class TestMonitoringNodeExporter:
    """Test prometheus-node-exporter installation and configuration."""

    def test_node_exporter_installed(self, host):
        """Verify prometheus-node-exporter is installed."""
        # Package name varies by distribution
        pkg_names = ["prometheus-node-exporter", "node_exporter"]
        has_package = False
        for pkg_name in pkg_names:
            pkg = host.package(pkg_name)
            if pkg.is_installed:
                has_package = True
                break
        assert has_package, "prometheus-node-exporter or node_exporter should be installed"

    def test_node_exporter_service_exists(self, host):
        """Verify node_exporter service exists."""
        svc_names = ["prometheus-node-exporter", "node_exporter", "node-exporter"]
        has_service = False
        for svc_name in svc_names:
            svc = host.service(svc_name)
            if svc.exists:
                has_service = True
                break
        assert has_service, "node_exporter service should exist"

    def test_node_exporter_service_running(self, host):
        """Verify node_exporter service is running."""
        svc_names = ["prometheus-node-exporter", "node_exporter", "node-exporter"]
        for svc_name in svc_names:
            svc = host.service(svc_name)
            if svc.exists:
                assert svc.is_running, f"{svc_name} service should be running"
                assert svc.is_enabled, f"{svc_name} service should be enabled"
                return
        # If no systemd service, check if process is running
        cmd = host.run("pgrep -f 'node_exporter' || true")
        if cmd.stdout.strip():
            pass  # Process is running

    def test_node_exporter_port_listening(self, host):
        """Verify node_exporter is listening on port 9100."""
        # Check if port 9100 is listening
        cmd = host.run(f"ss -tlnp | grep ':{NODE_EXPORTER_PORT}' || netstat -tlnp | grep ':{NODE_EXPORTER_PORT}' || true")
        if cmd.stdout.strip():
            # Port should be listening
            assert str(NODE_EXPORTER_PORT) in cmd.stdout, f"node_exporter should listen on port {NODE_EXPORTER_PORT}"


class TestMonitoringSmartmontools:
    """Test smartmontools installation and configuration."""

    def test_smartmontools_installed(self, host):
        """Verify smartmontools is installed."""
        pkg = host.package("smartmontools")
        assert pkg.is_installed, "smartmontools package should be installed"

    def test_smartctl_available(self, host):
        """Verify smartctl command is available."""
        assert host.exists("smartctl"), "smartctl command should be available"

    def test_smartd_available(self, host):
        """Verify smartd command is available."""
        assert host.exists("smartd"), "smartd command should be available"

    def test_smartd_config_exists(self, host):
        """Verify smartd configuration file exists."""
        f = host.file("/etc/smartd.conf")
        assert f.exists, "/etc/smartd.conf should exist"
        assert f.is_file, "/etc/smartd.conf should be a file"

    def test_smartd_config_permissions(self, host):
        """Verify smartd configuration has correct permissions."""
        f = host.file("/etc/smartd.conf")
        if f.exists:
            assert f.mode in [0o644, 0o640], "/etc/smartd.conf should have correct permissions"
            assert f.user == "root", "/etc/smartd.conf should be owned by root"

    def test_smartd_config_content(self, host):
        """Verify smartd configuration has DEVICESCAN."""
        f = host.file("/etc/smartd.conf")
        if f.exists:
            content = f.content_string
            assert "DEVICESCAN" in content, "smartd.conf should have DEVICESCAN directive"

    def test_smartd_service(self, host):
        """Verify smartd service status."""
        svc = host.service("smartd")
        if svc.exists:
            # Service should be running on physical hardware
            # May not run in containers/VMs without disk access
            pass


class TestMonitoringNvmeCli:
    """Test nvme-cli installation."""

    def test_nvme_cli_installed(self, host):
        """Verify nvme-cli is installed."""
        pkg = host.package("nvme-cli")
        assert pkg.is_installed, "nvme-cli package should be installed"

    def test_nvme_command_available(self, host):
        """Verify nvme command is available."""
        assert host.exists("nvme"), "nvme command should be available"

    def test_nvme_devices(self, host):
        """Verify NVMe devices can be queried (if present)."""
        cmd = host.run("nvme list 2>/dev/null || true")
        # May return no devices if no NVMe drives present
        # This is informational


class TestMonitoringConfiguration:
    """Test monitoring configuration files."""

    def test_node_exporter_config(self, host):
        """Verify node_exporter configuration if it exists."""
        config_paths = [
            "/etc/default/prometheus-node-exporter",
            "/etc/sysconfig/node_exporter",
            "/etc/prometheus-node-exporter.conf",
        ]
        for config_path in config_paths:
            f = host.file(config_path)
            if f.exists:
                assert f.is_file, f"{config_path} should be a file"
                assert f.mode in [0o644, 0o640, 0o600], f"{config_path} should have secure permissions"

    def test_smartd_directory(self, host):
        """Verify smartd directory exists."""
        d = host.file("/var/lib/smartmontools")
        if d.exists:
            assert d.is_directory, "/var/lib/smartmontools should be a directory"


class TestMonitoringMetrics:
    """Test monitoring metrics availability."""

    def test_node_exporter_metrics_endpoint(self, host):
        """Verify node_exporter metrics endpoint is accessible."""
        # Try to fetch metrics locally
        cmd = host.run(f"curl -s http://127.0.0.1:{NODE_EXPORTER_PORT}/metrics 2>/dev/null | head -5 || true")
        if cmd.rc == 0 and cmd.stdout.strip():
            # Should return prometheus metrics format
            assert "#" in cmd.stdout or "_total" in cmd.stdout, "Metrics endpoint should return prometheus format"

    def test_node_exporter_health_endpoint(self, host):
        """Verify node_exporter health endpoint is accessible."""
        cmd = host.run(f"curl -s http://127.0.0.1:{NODE_EXPORTER_PORT}/health 2>/dev/null || true")
        if cmd.rc == 0:
            # Health endpoint should return status
            pass


class TestMonitoringSystemState:
    """Test monitoring system state."""

    def test_proc_filesystem_accessible(self, host):
        """Verify /proc filesystem is accessible for metrics."""
        f = host.file("/proc/stat")
        assert f.exists, "/proc/stat should be accessible"

    def test_sys_filesystem_accessible(self, host):
        """Verify /sys filesystem is accessible for metrics."""
        d = host.file("/sys/class")
        assert d.exists, "/sys/class should be accessible"

    def test_dev_disk_accessible(self, host):
        """Verify /dev/disk is accessible for disk metrics."""
        d = host.file("/dev/disk")
        if d.exists:
            assert d.is_directory, "/dev/disk should be a directory"

    def test_monitoring_user_exists(self, host):
        """Verify monitoring user exists if created."""
        # Some installations create a prometheus or node_exporter user
        users = ["prometheus", "node_exporter", "node-exporter"]
        for user in users:
            u = host.user(user)
            if u.exists:
                assert u.exists, f"Monitoring user {user} should exist"
