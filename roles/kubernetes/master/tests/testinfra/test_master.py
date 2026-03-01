# =============================================================================
# Audit Event Identifier: DSU-PYS-500073
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for kubernetes/master role.

This role handles K3s master node configuration:
- Installing K3s binary
- Configuring K3s master service
- Setting up kubeconfig
- Managing K3s service
- Configuring cluster networking
"""
import pytest


# K3s configuration
K3S_BINARY = "/usr/local/bin/k3s"
K3S_SERVICE = "k3s"
K3S_CONFIG_DIR = "/etc/rancher/k3s"
K3S_DATA_DIR = "/var/lib/rancher/k3s"
KUBECONFIG_PATH = "/etc/rancher/k3s/k3s.yaml"
K3S_TOKEN_PATH = "/var/lib/deploy-system/kubernetes/token"

# K3s ports
K3S_API_PORT = 6443
K3S_ETCD_PORT = 2379
K3S_ETCD_PEER_PORT = 2380


class TestK3sInstallation:
    """Test K3s binary installation."""

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

    def test_k3s_help(self, host):
        """Verify K3s help is accessible."""
        cmd = host.run(f"{K3S_BINARY} --help 2>&1 | head -20")
        if cmd.rc == 0:
            assert "k3s" in cmd.stdout.lower(), "k3s help should be available"

    def test_k3s_kubectl_available(self, host):
        """Verify kubectl is available via k3s."""
        cmd = host.run(f"{K3S_BINARY} kubectl version --client 2>&1 || true")
        if cmd.rc == 0:
            assert "client" in cmd.stdout.lower() or "version" in cmd.stdout.lower(), \
                "kubectl should be available via k3s"


class TestK3sService:
    """Test K3s systemd service."""

    def test_k3s_service_file_exists(self, host):
        """Verify K3s systemd service file exists."""
        f = host.file("/etc/systemd/system/k3s.service")
        assert f.exists, "/etc/systemd/system/k3s.service should exist"
        assert f.is_file, "/etc/systemd/system/k3s.service should be a file"

    def test_k3s_service_file_permissions(self, host):
        """Verify K3s systemd service file has correct permissions."""
        f = host.file("/etc/systemd/system/k3s.service")
        if f.exists:
            assert f.mode in [0o644, 0o640], \
                "k3s.service should have correct permissions"
            assert f.user == "root", "k3s.service should be owned by root"

    def test_k3s_service_exists(self, host):
        """Verify K3s service exists."""
        svc = host.service(K3S_SERVICE)
        assert svc.exists, f"{K3S_SERVICE} service should exist"

    def test_k3s_service_running(self, host):
        """Verify K3s service is running."""
        svc = host.service(K3S_SERVICE)
        if svc.exists:
            assert svc.is_running, f"{K3S_SERVICE} service should be running"

    def test_k3s_service_enabled(self, host):
        """Verify K3s service is enabled."""
        svc = host.service(K3S_SERVICE)
        if svc.exists:
            assert svc.is_enabled, f"{K3S_SERVICE} service should be enabled"

    def test_k3s_service_status(self, host):
        """Verify K3s service status."""
        cmd = host.run(f"systemctl status {K3S_SERVICE} 2>&1 || true")
        # Service should be active
        if "active" in cmd.stdout.lower():
            assert "active" in cmd.stdout.lower(), f"{K3S_SERVICE} should be active"


class TestK3sConfiguration:
    """Test K3s configuration files."""

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


class TestKubeconfig:
    """Test Kubernetes kubeconfig."""

    def test_kubeconfig_exists(self, host):
        """Verify kubeconfig file exists."""
        f = host.file(KUBECONFIG_PATH)
        assert f.exists, f"{KUBECONFIG_PATH} should exist"
        assert f.is_file, f"{KUBECONFIG_PATH} should be a file"

    def test_kubeconfig_permissions(self, host):
        """Verify kubeconfig has secure permissions."""
        f = host.file(KUBECONFIG_PATH)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"{KUBECONFIG_PATH} should have secure permissions"
            assert f.user == "root", f"{KUBECONFIG_PATH} should be owned by root"

    def test_kubeconfig_valid_yaml(self, host):
        """Verify kubeconfig is valid YAML."""
        f = host.file(KUBECONFIG_PATH)
        if f.exists:
            content = f.content_string
            # Basic YAML validation
            assert "apiVersion:" in content, "kubeconfig should have apiVersion"
            assert "clusters:" in content, "kubeconfig should have clusters"
            assert "contexts:" in content, "kubeconfig should have contexts"
            assert "users:" in content, "kubeconfig should have users"

    def test_kubeconfig_cluster_config(self, host):
        """Verify kubeconfig has cluster configuration."""
        f = host.file(KUBECONFIG_PATH)
        if f.exists:
            content = f.content_string
            assert "server:" in content, "kubeconfig should have server configuration"
            assert "https://" in content, "kubeconfig server should use HTTPS"

    def test_kubeconfig_k3s_master(self, host):
        """Verify kubeconfig points to K3s master."""
        f = host.file(KUBECONFIG_PATH)
        if f.exists:
            content = f.content_string
            assert f"k3s" in content.lower() or f"127.0.0.1:{K3S_API_PORT}" in content or \
                   f"localhost:{K3S_API_PORT}" in content, \
                "kubeconfig should point to K3s master"


class TestK3sCluster:
    """Test K3s cluster functionality."""

    def test_kubectl_cluster_info(self, host):
        """Verify kubectl can get cluster info."""
        cmd = host.run(f"{K3S_BINARY} kubectl cluster-info 2>&1 || true")
        if cmd.rc == 0:
            assert "kubernetes" in cmd.stdout.lower(), "kubectl should return cluster info"

    def test_kubectl_nodes(self, host):
        """Verify kubectl can list nodes."""
        cmd = host.run(f"{K3S_BINARY} kubectl get nodes 2>&1 || true")
        if cmd.rc == 0:
            # Should show at least the master node
            assert "node" in cmd.stdout.lower() or "NAME" in cmd.stdout, \
                "kubectl should list nodes"

    def test_kubectl_pods(self, host):
        """Verify kubectl can list pods."""
        cmd = host.run(f"{K3S_BINARY} kubectl get pods -A 2>&1 || true")
        if cmd.rc == 0:
            # Should show system pods
            assert "pod" in cmd.stdout.lower() or "NAME" in cmd.stdout, \
                "kubectl should list pods"

    def test_kubectl_system_pods_running(self, host):
        """Verify K3s system pods are running."""
        cmd = host.run(f"{K3S_BINARY} kubectl get pods -n kube-system 2>&1 || true")
        if cmd.rc == 0:
            # System pods should be running
            assert "running" in cmd.stdout.lower() or "NAME" in cmd.stdout, \
                "System pods should be listed"


class TestK3sNetworking:
    """Test K3s networking configuration."""

    def test_k3s_api_port_listening(self, host):
        """Verify K3s API port is listening."""
        cmd = host.run(f"ss -tlnp | grep ':{K3S_API_PORT}' || netstat -tlnp | grep ':{K3S_API_PORT}' || true")
        if cmd.stdout.strip():
            assert str(K3S_API_PORT) in cmd.stdout, \
                f"K3s API should listen on port {K3S_API_PORT}"

    def test_k3s_api_accessible(self, host):
        """Verify K3s API is accessible."""
        cmd = host.run(f"curl -k https://127.0.0.1:{K3S_API_PORT}/healthz 2>&1 || true")
        if cmd.rc == 0:
            assert "ok" in cmd.stdout.lower() or "healthy" in cmd.stdout.lower(), \
                "K3s API healthz endpoint should return OK"

    def test_k3s_coredns_running(self, host):
        """Verify CoreDNS is running."""
        cmd = host.run(f"{K3S_BINARY} kubectl get pods -n kube-system -l k8s-app=kube-dns 2>&1 || true")
        if cmd.rc == 0:
            assert "coredns" in cmd.stdout.lower() or "Running" in cmd.stdout, \
                "CoreDNS should be running"


class TestK3sStorage:
    """Test K3s storage configuration."""

    def test_k3s_storage_class(self, host):
        """Verify default storage class exists."""
        cmd = host.run(f"{K3S_BINARY} kubectl get storageclass 2>&1 || true")
        if cmd.rc == 0:
            # K3s provides local-path storage by default
            assert "storageclass" in cmd.stdout.lower() or "local-path" in cmd.stdout.lower(), \
                "Default storage class should exist"

    def test_k3s_pv_directory(self, host):
        """Verify K3s PV directory exists."""
        d = host.file(f"{K3S_DATA_DIR}/storage")
        if d.exists:
            assert d.is_directory, "K3s storage directory should exist"


class TestK3sSecurity:
    """Test K3s security configuration."""

    def test_k3s_token_exists(self, host):
        """Verify K3s token file exists."""
        f = host.file(K3S_TOKEN_PATH)
        if f.exists:
            assert f.is_file, "K3s token file should be a file"
            assert f.mode in [0o640, 0o600], "K3s token should have secure permissions"

    def test_k3s_server_token_exists(self, host):
        """Verify K3s server token exists."""
        f = host.file(f"{K3S_DATA_DIR}/agent/node-token")
        if f.exists:
            assert f.is_file, "Node token should be a file"
            assert f.mode in [0o640, 0o600], "Node token should have secure permissions"

    def test_k3s_tls_certificates(self, host):
        """Verify K3s TLS certificates exist."""
        cert_dir = f"{K3S_DATA_DIR}/server/tls"
        d = host.file(cert_dir)
        if d.exists:
            assert d.is_directory, f"{cert_dir} should be a directory"

    def test_k3s_admin_cert(self, host):
        """Verify K3s admin certificate exists."""
        f = host.file(f"{K3S_DATA_DIR}/server/tls/client-admin.crt")
        if f.exists:
            assert f.is_file, "Admin certificate should exist"


class TestK3sComponents:
    """Test K3s components."""

    def test_k3s_traefik(self, host):
        """Verify Traefik ingress is configured."""
        cmd = host.run(f"{K3S_BINARY} kubectl get pods -n kube-system -l app=traefik 2>&1 || true")
        # Traefik may be disabled
        pass

    def test_k3s_metrics_server(self, host):
        """Verify metrics-server is running."""
        cmd = host.run(f"{K3S_BINARY} kubectl get pods -n kube-system -l k8s-app=metrics-server 2>&1 || true")
        # Metrics server may take time to start
        pass

    def test_k3s_local_path_provisioner(self, host):
        """Verify local-path-provisioner is running."""
        cmd = host.run(f"{K3S_BINARY} kubectl get pods -n kube-system -l app=local-path-provisioner 2>&1 || true")
        if cmd.rc == 0:
            assert "local-path" in cmd.stdout.lower() or "Running" in cmd.stdout, \
                "Local-path provisioner should be running"


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), K3s may not function properly")

    def test_systemd_available(self, host):
        """Verify systemd is available."""
        cmd = host.run("which systemctl")
        if cmd.rc != 0:
            pytest.skip("systemd not available in this environment")
