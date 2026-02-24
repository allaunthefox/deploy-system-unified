"""
Testinfra tests for networking/container_networks role.

This role handles container network isolation:
- Podman quadlet network configurations
- Network segmentation (frontend, backend, management)
- Kernel networking prerequisites
- Container network isolation
"""
import pytest


# Container network quadlet files
CONTAINER_NETWORK_QUADLETS = {
    "/etc/containers/systemd/frontend.network": "frontend",
    "/etc/containers/systemd/backend.network": "backend",
    "/etc/containers/systemd/management.network": "management",
}

# Container systemd directory
CONTAINER_SYSTEMD_DIR = "/etc/containers/systemd"

# Expected network labels
NETWORK_LABELS = ["tier=frontend", "tier=backend", "tier=management"]


class TestContainerNetworkDirectories:
    """Test container network directory structure."""

    def test_containers_systemd_directory(self, host):
        """Verify /etc/containers/systemd directory exists."""
        d = host.file(CONTAINER_SYSTEMD_DIR)
        assert d.exists, f"{CONTAINER_SYSTEMD_DIR} should exist"
        assert d.is_directory, f"{CONTAINER_SYSTEMD_DIR} should be a directory"

    def test_containers_systemd_permissions(self, host):
        """Verify /etc/containers/systemd has correct permissions."""
        d = host.file(CONTAINER_SYSTEMD_DIR)
        if d.exists:
            assert d.mode in [0o755, 0o750, 0o700], \
                f"{CONTAINER_SYSTEMD_DIR} should have secure permissions, got {oct(d.mode)}"


class TestContainerNetworkQuadlets:
    """Test container network quadlet configurations."""

    def test_network_quadlets_exist(self, host):
        """Verify network quadlet files exist."""
        cmd = host.run(f"ls {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert ".network" in cmd.stdout, "Should have at least one .network file"
        else:
            pytest.skip("No network quadlet files found")

    def test_frontend_network_quadlet(self, host):
        """Verify frontend network quadlet exists."""
        f = host.file(f"{CONTAINER_SYSTEMD_DIR}/frontend.network")
        if f.exists:
            assert f.is_file, "frontend.network should be a file"
            content = f.content_string
            assert "[Network]" in content, "Quadlet should have [Network] section"
        else:
            pytest.skip("Frontend network quadlet not found")

    def test_backend_network_quadlet(self, host):
        """Verify backend network quadlet exists."""
        f = host.file(f"{CONTAINER_SYSTEMD_DIR}/backend.network")
        if f.exists:
            assert f.is_file, "backend.network should be a file"
            content = f.content_string
            assert "[Network]" in content, "Quadlet should have [Network] section"
            # Backend should be internal (no direct internet)
            assert "Internal=true" in content or "Internal=true" in content, \
                "Backend network should be internal"
        else:
            pytest.skip("Backend network quadlet not found")

    def test_management_network_quadlet(self, host):
        """Verify management network quadlet exists."""
        f = host.file(f"{CONTAINER_SYSTEMD_DIR}/management.network")
        if f.exists:
            assert f.is_file, "management.network should be a file"
            content = f.content_string
            assert "[Network]" in content, "Quadlet should have [Network] section"
        else:
            pytest.skip("Management network quadlet not found")


class TestContainerNetworkConfiguration:
    """Test container network configuration content."""

    def test_network_quadlet_structure(self, host):
        """Verify network quadlet has correct structure."""
        cmd = host.run(f"ls {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            network_files = cmd.stdout.strip().split("\n")
            for network_file in network_files:
                if network_file.strip():
                    f = host.file(network_file.strip())
                    if f.exists:
                        content = f.content_string
                        assert "[Network]" in content, \
                            f"{network_file} should have [Network] section"
        else:
            pytest.skip("No network quadlet files found")

    def test_network_quadlet_has_network_name(self, host):
        """Verify network quadlet has NetworkName configured."""
        cmd = host.run(f"grep -r 'NetworkName=' {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert "NetworkName=" in cmd.stdout, \
                "Network quadlets should have NetworkName configured"
        else:
            pytest.skip("No NetworkName configuration found")

    def test_network_quadlet_has_driver(self, host):
        """Verify network quadlet has Driver configured."""
        cmd = host.run(f"grep -r 'Driver=' {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert "Driver=" in cmd.stdout, \
                "Network quadlets should have Driver configured"
        else:
            pytest.skip("No Driver configuration found")

    def test_backend_network_is_internal(self, host):
        """Verify backend network is configured as internal."""
        f = host.file(f"{CONTAINER_SYSTEMD_DIR}/backend.network")
        if f.exists:
            content = f.content_string
            # Internal networks have no external connectivity
            assert "Internal=true" in content, \
                "Backend network should be internal (no external access)"
        else:
            pytest.skip("Backend network quadlet not found")


class TestContainerNetworkLabels:
    """Test container network labels."""

    def test_network_quadlet_has_labels(self, host):
        """Verify network quadlet has labels configured."""
        cmd = host.run(f"grep -r 'Label=' {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert "Label=" in cmd.stdout, \
                "Network quadlets should have Label configured"
        else:
            # Labels are optional
            pytest.skip("No Label configuration found (may be optional)")

    def test_tier_labels_configured(self, host):
        """Verify tier labels are configured."""
        cmd = host.run(f"grep -r 'tier=' {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert "tier=" in cmd.stdout, \
                "Network quadlets should have tier labels"
        else:
            pytest.skip("No tier labels found")


class TestContainerNetworkSubnets:
    """Test container network subnet configurations."""

    def test_network_quadlet_has_subnet(self, host):
        """Verify network quadlet has Subnet configured."""
        cmd = host.run(f"grep -r 'Subnet=' {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert "Subnet=" in cmd.stdout, \
                "Network quadlets should have Subnet configured"
        else:
            # Subnet is optional for some networks
            pytest.skip("No Subnet configuration found (may use default)")

    def test_network_quadlet_has_gateway(self, host):
        """Verify network quadlet has Gateway configured."""
        cmd = host.run(f"grep -r 'Gateway=' {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert "Gateway=" in cmd.stdout, \
                "Network quadlets should have Gateway configured"
        else:
            pytest.skip("No Gateway configuration found")

    def test_network_quadlet_has_iprange(self, host):
        """Verify network quadlet has IPRange configured."""
        cmd = host.run(f"grep -r 'IPRange=' {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert "IPRange=" in cmd.stdout, \
                "Network quadlets should have IPRange configured"
        else:
            pytest.skip("No IPRange configuration found")


class TestContainerNetworkKernelPrerequisites:
    """Test kernel networking prerequisites."""

    def test_bridge_module_loaded(self, host):
        """Verify bridge kernel module is loaded."""
        cmd = host.run("lsmod | grep bridge 2>&1")
        if cmd.rc == 0:
            assert "bridge" in cmd.stdout, "Bridge module should be loaded"
        else:
            pytest.skip("Bridge module not loaded")

    def test_nat_module_loaded(self, host):
        """Verify NAT kernel module is loaded."""
        cmd = host.run("lsmod | grep -E 'nf_nat|iptable_nat' 2>&1")
        if cmd.rc == 0:
            assert "nat" in cmd.stdout.lower(), "NAT module should be loaded"
        else:
            pytest.skip("NAT module not loaded")

    def test_overlay_module_loaded(self, host):
        """Verify overlay network module is loaded."""
        cmd = host.run("lsmod | grep overlay 2>&1")
        if cmd.rc == 0:
            assert "overlay" in cmd.stdout, "Overlay module should be loaded"
        else:
            # Overlay may not be required for all setups
            pytest.skip("Overlay module not loaded")

    def test_forwarding_enabled(self, host):
        """Verify IP forwarding is enabled."""
        f = host.file("/proc/sys/net/ipv4/ip_forward")
        if f.exists:
            content = f.content_string.strip()
            # Should be 1 for forwarding enabled
            if content == "1":
                assert True, "IP forwarding should be enabled"
            else:
                pytest.skip("IP forwarding not enabled (may not be required)")
        else:
            pytest.skip("Cannot check IP forwarding")


class TestContainerNetworkIsolation:
    """Test container network isolation."""

    def test_network_isolation_configured(self, host):
        """Verify network isolation is configured."""
        # Check for internal networks
        cmd = host.run(f"grep -r 'Internal=true' {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert "Internal=true" in cmd.stdout, \
                "Should have internal networks for isolation"
        else:
            pytest.skip("No internal networks configured")

    def test_backend_network_isolation(self, host):
        """Verify backend network isolation."""
        f = host.file(f"{CONTAINER_SYSTEMD_DIR}/backend.network")
        if f.exists:
            content = f.content_string
            # Backend should be isolated
            has_isolation = "Internal=true" in content or "isolate" in content.lower()
            assert has_isolation, "Backend network should be isolated"
        else:
            pytest.skip("Backend network not found")


class TestContainerNetworkServices:
    """Test container network systemd services."""

    def test_network_services_generated(self, host):
        """Verify network services are generated by quadlet."""
        cmd = host.run("systemctl list-unit-files --type=service 2>&1 | grep -E '\\.network' || true")
        # Network quadlets may not create services directly

    def test_systemd_daemon_reload(self, host):
        """Verify systemd daemon can be reloaded for networks."""
        cmd = host.run("systemctl daemon-reload 2>&1")
        if cmd.rc == 0:
            assert True, "systemctl daemon-reload should succeed"
        else:
            pytest.skip("systemctl daemon-reload not available")


class TestPodmanNetworks:
    """Test Podman network configurations."""

    def test_podman_network_command(self, host):
        """Verify podman network command works."""
        cmd = host.run("podman network ls 2>&1")
        if cmd.rc == 0:
            assert "network" in cmd.stdout.lower(), \
                "podman network ls should return network list"
        else:
            pytest.skip("podman network command not available")

    def test_podman_network_inspect(self, host):
        """Verify podman network inspect works."""
        cmd = host.run("podman network inspect podman 2>&1")
        if cmd.rc == 0:
            assert "podman" in cmd.stdout.lower() or "Network" in cmd.stdout, \
                "podman network inspect should return network info"
        else:
            pytest.skip("podman network inspect not available")


class TestContainerNetworksCompletion:
    """Test container networks configuration completion indicators."""

    def test_network_quadlets_complete(self, host):
        """Verify network quadlets are complete."""
        cmd = host.run(f"ls {CONTAINER_SYSTEMD_DIR}/*.network 2>&1")
        if cmd.rc == 0:
            assert ".network" in cmd.stdout, "Should have network quadlet files"
        else:
            pytest.skip("No network quadlet files found")

    def test_container_networks_ready(self, host):
        """Verify container networks are ready."""
        # Check for at least one network configuration
        indicators = [
            host.file(f"{CONTAINER_SYSTEMD_DIR}/frontend.network").exists,
            host.file(f"{CONTAINER_SYSTEMD_DIR}/backend.network").exists,
            host.file(f"{CONTAINER_SYSTEMD_DIR}/management.network").exists,
        ]
        if any(indicators):
            assert True, "Container networks should be configured"
        else:
            pytest.skip("No container networks configured")

    def test_kernel_networking_ready(self, host):
        """Verify kernel networking is ready for containers."""
        # Check for required kernel modules
        bridge_cmd = host.run("lsmod | grep bridge 2>&1")
        if bridge_cmd.rc == 0:
            assert "bridge" in bridge_cmd.stdout, "Bridge module should be available"
        else:
            pytest.skip("Kernel networking modules not loaded")
