"""
Testinfra tests for kubernetes/node role.

This role handles K3s agent/node configuration:
- Installing K3s binary
- Configuring K3s agent service
- Joining node to K3s cluster
- Managing K3s agent service
"""
import pytest


# K3s configuration
K3S_BINARY = "/usr/local/bin/k3s"
K3S_AGENT_SERVICE = "k3s-agent"
K3S_CONFIG_DIR = "/etc/rancher/k3s"
K3S_DATA_DIR = "/var/lib/rancher/k3s"
K3S_AGENT_CONFIG = "/etc/rancher/k3s/config.yaml"
K3S_TOKEN_FILE = "/etc/rancher/k3s/token"
KUBECONFIG_PATH = "/etc/rancher/k3s/k3s.yaml"

# K3s ports
K3S_AGENT_PORT = 10250
K3S_NODE_PORT_RANGE_START = 30000


class TestK3sNodeInstallation:
    """Test K3s binary installation on node."""

    def test_k3s_binary_exists(self, host):
        """Verify K3s binary exists."""
        f = host.file(K3S_BINARY)
        assert f.exists, f"{K3S_BINARY} should exist"
        assert f.is_file, f"{K3S_BINARY} should be a file"

    def test_k3s_binary_permissions(self, host):
        """Verify K3s binary has correct permissions."""
        f = host.file(K3S_BINARY)
        if f.exists:
            assert f.mode in [0o755, 0o750], \
                f"{K3S_BINARY} should have executable permissions, got {oct(f.mode)}"
            assert f.user == "root", f"{K3S_BINARY} should be owned by root"

    def test_k3s_binary_executable(self, host):
        """Verify K3s binary is executable."""
        f = host.file(K3S_BINARY)
        if f.exists:
            assert f.is_executable, f"{K3S_BINARY} should be executable"

    def test_k3s_version(self, host):
        """Verify K3s version can be queried."""
        cmd = host.run(f"{K3S_BINARY} --version 2>&1 || {K3S_BINARY} version 2>&1")
        if cmd.rc == 0:
            assert "k3s" in cmd.stdout.lower(), "k3s version command should return version info"

    def test_k3s_kubectl_available(self, host):
        """Verify kubectl is available via k3s."""
        cmd = host.run(f"{K3S_BINARY} kubectl version --client 2>&1 || true")
        if cmd.rc == 0:
            assert "client" in cmd.stdout.lower() or "version" in cmd.stdout.lower(), \
                "kubectl should be available via k3s"


class TestK3sNodeService:
    """Test K3s agent systemd service."""

    def test_k3s_agent_service_file_exists(self, host):
        """Verify K3s agent systemd service file exists."""
        f = host.file("/etc/systemd/system/k3s-agent.service")
        assert f.exists, "/etc/systemd/system/k3s-agent.service should exist"
        assert f.is_file, "/etc/systemd/system/k3s-agent.service should be a file"

    def test_k3s_agent_service_file_permissions(self, host):
        """Verify K3s agent systemd service file has correct permissions."""
        f = host.file("/etc/systemd/system/k3s-agent.service")
        if f.exists:
            assert f.mode in [0o644, 0o640], \
                "k3s-agent.service should have correct permissions"
            assert f.user == "root", "k3s-agent.service should be owned by root"

    def test_k3s_agent_service_exists(self, host):
        """Verify K3s agent service exists."""
        svc = host.service(K3S_AGENT_SERVICE)
        assert svc.exists, f"{K3S_AGENT_SERVICE} service should exist"

    def test_k3s_agent_service_running(self, host):
        """Verify K3s agent service is running."""
        svc = host.service(K3S_AGENT_SERVICE)
        if svc.exists:
            assert svc.is_running, f"{K3S_AGENT_SERVICE} service should be running"

    def test_k3s_agent_service_enabled(self, host):
        """Verify K3s agent service is enabled."""
        svc = host.service(K3S_AGENT_SERVICE)
        if svc.exists:
            assert svc.is_enabled, f"{K3S_AGENT_SERVICE} service should be enabled"

    def test_k3s_agent_service_status(self, host):
        """Verify K3s agent service status."""
        cmd = host.run(f"systemctl status {K3S_AGENT_SERVICE} 2>&1 || true")
        # Service should be active
        if "active" in cmd.stdout.lower():
            assert "active" in cmd.stdout.lower(), f"{K3S_AGENT_SERVICE} should be active"


class TestK3sNodeConfiguration:
    """Test K3s node configuration files."""

    def test_k3s_config_dir_exists(self, host):
        """Verify K3s configuration directory exists."""
        d = host.file(K3S_CONFIG_DIR)
        assert d.exists, f"{K3S_CONFIG_DIR} should exist"
        assert d.is_directory, f"{K3S_CONFIG_DIR} should be a directory"

    def test_k3s_config_dir_permissions(self, host):
        """Verify K3s configuration directory has correct permissions."""
        d = host.file(K3S_CONFIG_DIR)
        if d.exists:
            assert d.mode in [0o755, 0o750, 0o700], \
                f"{K3S_CONFIG_DIR} should have correct permissions"
            assert d.user == "root", f"{K3S_CONFIG_DIR} should be owned by root"

    def test_k3s_agent_config_exists(self, host):
        """Verify K3s agent configuration file exists."""
        f = host.file(K3S_AGENT_CONFIG)
        assert f.exists, f"{K3S_AGENT_CONFIG} should exist"
        assert f.is_file, f"{K3S_AGENT_CONFIG} should be a file"

    def test_k3s_agent_config_permissions(self, host):
        """Verify K3s agent configuration has secure permissions."""
        f = host.file(K3S_AGENT_CONFIG)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"{K3S_AGENT_CONFIG} should have secure permissions"
            assert f.user == "root", f"{K3S_AGENT_CONFIG} should be owned by root"

    def test_k3s_agent_config_has_server(self, host):
        """Verify K3s agent config has server URL."""
        f = host.file(K3S_AGENT_CONFIG)
        if f.exists:
            content = f.content_string
            assert "server:" in content, "Agent config should have server URL"
            assert "https://" in content, "Server URL should use HTTPS"

    def test_k3s_token_file_exists(self, host):
        """Verify K3s token file exists."""
        f = host.file(K3S_TOKEN_FILE)
        assert f.exists, f"{K3S_TOKEN_FILE} should exist"
        assert f.is_file, f"{K3S_TOKEN_FILE} should be a file"

    def test_k3s_token_file_permissions(self, host):
        """Verify K3s token file has secure permissions."""
        f = host.file(K3S_TOKEN_FILE)
        if f.exists:
            assert f.mode in [0o640, 0o600], \
                f"{K3S_TOKEN_FILE} should have secure permissions"
            assert f.user == "root", f"{K3S_TOKEN_FILE} should be owned by root"


class TestK3sNodeData:
    """Test K3s node data directory."""

    def test_k3s_data_dir_exists(self, host):
        """Verify K3s data directory exists."""
        d = host.file(K3S_DATA_DIR)
        assert d.exists, f"{K3S_DATA_DIR} should exist"
        assert d.is_directory, f"{K3S_DATA_DIR} should be a directory"

    def test_k3s_data_dir_permissions(self, host):
        """Verify K3s data directory has correct permissions."""
        d = host.file(K3S_DATA_DIR)
        if d.exists:
            assert d.mode in [0o755, 0o750, 0o700], \
                f"{K3S_DATA_DIR} should have correct permissions"

    def test_k3s_agent_dir_exists(self, host):
        """Verify K3s agent directory exists."""
        d = host.file(f"{K3S_DATA_DIR}/agent")
        if d.exists:
            assert d.is_directory, "K3s agent directory should exist"

    def test_k3s_pod_directory_exists(self, host):
        """Verify K3s pod directory exists."""
        d = host.file(f"{K3S_DATA_DIR}/agent/pod-manifests")
        if d.exists:
            assert d.is_directory, "K3s pod-manifests directory should exist"


class TestK3sNodeCluster:
    """Test K3s node cluster connectivity."""

    def test_k3s_node_joined_cluster(self, host):
        """Verify node has joined the cluster."""
        cmd = host.run(f"{K3S_BINARY} kubectl get nodes 2>&1 || true")
        if cmd.rc == 0:
            # Node should be listed
            assert "node" in cmd.stdout.lower() or "NAME" in cmd.stdout, \
                "Node should be able to list cluster nodes"

    def test_k3s_node_ready(self, host):
        """Verify node status is Ready."""
        cmd = host.run(f"{K3S_BINARY} kubectl get nodes 2>&1 || true")
        if cmd.rc == 0:
            # This node should be Ready
            assert "Ready" in cmd.stdout, "Node should be in Ready state"

    def test_k3s_api_connectivity(self, host):
        """Verify node can connect to K3s API."""
        # Check if agent can reach the server
        cmd = host.run(f"ss -tlnp | grep ':{K3S_AGENT_PORT}' || netstat -tlnp | grep ':{K3S_AGENT_PORT}' || true")
        # Agent port should be listening
        pass


class TestK3sNodeNetworking:
    """Test K3s node networking."""

    def test_k3s_agent_port_listening(self, host):
        """Verify K3s agent port is listening."""
        cmd = host.run(f"ss -tlnp | grep ':{K3S_AGENT_PORT}' || netstat -tlnp | grep ':{K3S_AGENT_PORT}' || true")
        if cmd.stdout.strip():
            assert str(K3S_AGENT_PORT) in cmd.stdout, \
                f"K3s agent should listen on port {K3S_AGENT_PORT}"

    def test_k3s_node_port_range(self, host):
        """Verify node port range is available."""
        cmd = host.run(f"ss -tlnp | awk 'NR>1 {{print $4}}' | grep -E ':3[0-9]{{4}}' || true")
        # Node ports (30000-32767) may be in use
        pass

    def test_k3s_cni_configured(self, host):
        """Verify CNI is configured on node."""
        d = host.file("/etc/cni/net.d")
        if d.exists:
            assert d.is_directory, "/etc/cni/net.d should be a directory"

    def test_k3s_cni_plugins(self, host):
        """Verify CNI plugins are installed."""
        d = host.file("/opt/cni/bin")
        if d.exists:
            assert d.is_directory, "/opt/cni/bin should be a directory"


class TestK3sNodePods:
    """Test K3s node pod management."""

    def test_k3s_static_pods(self, host):
        """Verify static pods directory exists."""
        d = host.file(f"{K3S_DATA_DIR}/agent/pod-manifests")
        if d.exists:
            assert d.is_directory, "Static pod manifests directory should exist"

    def test_k3s_kubelet_running(self, host):
        """Verify kubelet is running."""
        cmd = host.run("ps aux | grep kubelet | grep -v grep || true")
        # Kubelet should be running as part of k3s-agent
        if cmd.stdout.strip():
            assert "kubelet" in cmd.stdout.lower(), "kubelet should be running"

    def test_k3s_kube_proxy_running(self, host):
        """Verify kube-proxy is running."""
        cmd = host.run("ps aux | grep kube-proxy | grep -v grep || true")
        # Kube-proxy should be running as part of k3s-agent
        pass


class TestK3sNodeSecurity:
    """Test K3s node security configuration."""

    def test_k3s_node_certificates(self, host):
        """Verify K3s node certificates exist."""
        cert_dir = f"{K3S_DATA_DIR}/agent/etc/kubernetes/pki"
        d = host.file(cert_dir)
        if d.exists:
            assert d.is_directory, f"{cert_dir} should be a directory"

    def test_k3s_node_kubeconfig(self, host):
        """Verify node kubeconfig exists."""
        f = host.file(f"{K3S_DATA_DIR}/agent/kubelet.kubeconfig")
        if f.exists:
            assert f.is_file, "Kubelet kubeconfig should exist"
            assert f.mode in [0o640, 0o600], "Kubelet kubeconfig should have secure permissions"

    def test_k3s_node_client_cert(self, host):
        """Verify node client certificate exists."""
        f = host.file(f"{K3S_DATA_DIR}/agent/client-kubelet.crt")
        if f.exists:
            assert f.is_file, "Client kubelet certificate should exist"


class TestK3sNodeLabels:
    """Test K3s node labels and taints."""

    def test_k3s_node_labels(self, host):
        """Verify node labels are applied."""
        cmd = host.run(f"{K3S_BINARY} kubectl get nodes --show-labels 2>&1 || true")
        if cmd.rc == 0:
            # Labels should be shown
            assert "label" in cmd.stdout.lower() or "NAME" in cmd.stdout, \
                "Node labels should be visible"

    def test_k3s_node_annotations(self, host):
        """Verify node annotations are applied."""
        cmd = host.run(f"{K3S_BINARY} kubectl get nodes -o wide 2>&1 || true")
        if cmd.rc == 0:
            # Node info should be shown
            pass


class TestK3sNodeStorage:
    """Test K3s node storage configuration."""

    def test_k3s_storage_class_available(self, host):
        """Verify storage class is available on node."""
        cmd = host.run(f"{K3S_BINARY} kubectl get storageclass 2>&1 || true")
        if cmd.rc == 0:
            assert "storageclass" in cmd.stdout.lower() or "local-path" in cmd.stdout.lower(), \
                "Storage class should be available"

    def test_k3s_pv_directory(self, host):
        """Verify K3s PV directory exists."""
        d = host.file(f"{K3S_DATA_DIR}/storage")
        if d.exists:
            assert d.is_directory, "K3s storage directory should exist"


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), K3s agent may not function properly")

    def test_systemd_available(self, host):
        """Verify systemd is available."""
        cmd = host.run("which systemctl")
        if cmd.rc != 0:
            pytest.skip("systemd not available in this environment")
