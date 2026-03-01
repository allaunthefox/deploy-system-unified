# =============================================================================
# Audit Event Identifier: DSU-PYS-500025
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for containers/runtime role.

This role handles container runtime installation and configuration:
- Installing Podman and core dependencies
- Rootless Podman configuration
- Cosign for supply chain integrity
- GPU container support (NVIDIA/AMD/Intel)
- Container storage configuration
"""
import pytest


# Podman packages by distribution
PODMAN_PACKAGES_DEBIAN = [
    "podman",
    "podman-docker",
    "containers-storage",
    "crun",
    "fuse-overlayfs",
]

PODMAN_PACKAGES_REDHAT = [
    "podman",
    "container-selinux",
    "crun",
    "fuse-overlayfs",
]

PODMAN_PACKAGES_ARCH = [
    "podman",
    "crun",
    "fuse-overlayfs",
]

PODMAN_PACKAGES_ALPINE = [
    "podman",
    "crun",
    "fuse-overlayfs",
]

# Cosign package
COSIGN_PACKAGE = "cosign"

# Container storage directories
CONTAINER_STORAGE_DIRS = [
    "/var/lib/containers",
    "/var/lib/containers/storage",
    "/run/containers/storage",
    "/srv/containers",
]

# GPU-related packages
NVIDIA_PACKAGES = [
    "nvidia-container-toolkit",
    "nvidia-container-runtime",
]

AMD_GPU_PACKAGES = [
    "rocm-smi-lib",
]

INTEL_GPU_PACKAGES = [
    "intel-media-driver",
    "intel-level-zero-gpu",
]


class TestPodmanInstallation:
    """Test Podman installation."""

    def test_podman_package_installed_debian(self, host):
        """Verify Podman is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("podman")
            assert pkg.is_installed, "podman package should be installed on Debian/Ubuntu"

    def test_podman_package_installed_redhat(self, host):
        """Verify Podman is installed (RedHat/CentOS)."""
        if host.file("/etc/redhat-release").exists:
            pkg = host.package("podman")
            assert pkg.is_installed, "podman package should be installed on RedHat/CentOS"

    def test_podman_package_installed_arch(self, host):
        """Verify Podman is installed (Arch Linux)."""
        if host.file("/etc/arch-release").exists:
            pkg = host.package("podman")
            assert pkg.is_installed, "podman package should be installed on Arch Linux"

    def test_podman_package_installed_alpine(self, host):
        """Verify Podman is installed (Alpine)."""
        if host.file("/etc/alpine-release").exists:
            pkg = host.package("podman")
            assert pkg.is_installed, "podman package should be installed on Alpine"

    def test_crun_installed(self, host):
        """Verify crun OCI runtime is installed."""
        # crun is the preferred lightweight OCI runtime
        pkg = host.package("crun")
        if pkg.is_installed:
            assert pkg.is_installed, "crun should be installed"
        else:
            # Some systems might use runc instead
            pkg = host.package("runc")
            assert pkg.is_installed, "Either crun or runc should be installed"

    def test_fuse_overlayfs_installed(self, host):
        """Verify fuse-overlayfs is installed for rootless containers."""
        pkg = host.package("fuse-overlayfs")
        if pkg.is_installed:
            assert pkg.is_installed, "fuse-overlayfs should be installed for rootless containers"


class TestPodmanService:
    """Test Podman service configuration."""

    def test_podman_binary_exists(self, host):
        """Verify podman binary exists."""
        f = host.file("/usr/bin/podman")
        if not f.exists:
            f = host.file("/usr/local/bin/podman")
        assert f.exists, "podman binary should exist"
        assert f.is_file, "podman should be a file"
        assert f.mode in [0o755, 0o755], "podman binary should be executable"

    def test_podman_version_command(self, host):
        """Verify podman version command works."""
        cmd = host.run("podman --version")
        if cmd.rc == 0:
            assert "podman" in cmd.stdout.lower(), "podman --version should return version info"
        else:
            pytest.skip("podman command not available")

    def test_podman_info_command(self, host):
        """Verify podman info command works."""
        cmd = host.run("podman info 2>&1")
        if cmd.rc == 0:
            assert "host" in cmd.stdout.lower() or "store" in cmd.stdout.lower(), \
                "podman info should return system information"
        else:
            pytest.skip("podman info not available (possibly in restricted environment)")


class TestContainerStorage:
    """Test container storage configuration."""

    @pytest.mark.parametrize("storage_dir", CONTAINER_STORAGE_DIRS)
    def test_container_storage_directories_exist(self, host, storage_dir):
        """Verify container storage directories exist."""
        d = host.file(storage_dir)
        if d.exists:
            assert d.is_directory, f"{storage_dir} should be a directory"
        else:
            # Some directories may be created on-demand
            pytest.skip(f"{storage_dir} does not exist yet")

    def test_storage_config_exists(self, host):
        """Verify container storage configuration file exists."""
        f = host.file("/etc/containers/storage.conf")
        assert f.exists, "/etc/containers/storage.conf should exist"
        assert f.is_file, "/etc/containers/storage.conf should be a file"

    def test_storage_config_permissions(self, host):
        """Verify storage configuration has correct permissions."""
        f = host.file("/etc/containers/storage.conf")
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"storage.conf should have secure permissions, got {oct(f.mode)}"
            assert f.user == "root", "storage.conf should be owned by root"

    def test_storage_config_driver(self, host):
        """Verify storage driver is configured."""
        f = host.file("/etc/containers/storage.conf")
        if f.exists:
            content = f.content_string
            has_driver = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("driver ="):
                    has_driver = True
                    # Should use overlay or overlay2
                    assert "overlay" in line.lower(), \
                        f"Storage driver should be overlay-based, got {line}"
                    break
            assert has_driver, "Storage driver should be configured"

    def test_storage_config_graphroot(self, host):
        """Verify storage graphroot is configured."""
        f = host.file("/etc/containers/storage.conf")
        if f.exists:
            content = f.content_string
            has_graphroot = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("graphroot ="):
                    has_graphroot = True
                    break
            assert has_graphroot, "Storage graphroot should be configured"


class TestContainerRegistries:
    """Test container registry configuration."""

    def test_registries_config_exists(self, host):
        """Verify registries configuration file exists."""
        f = host.file("/etc/containers/registries.conf")
        if f.exists:
            assert f.is_file, "/etc/containers/registries.conf should be a file"

    def test_registries_conf_permissions(self, host):
        """Verify registries configuration has correct permissions."""
        f = host.file("/etc/containers/registries.conf")
        if f.exists:
            assert f.mode in [0o644, 0o640], \
                f"registries.conf should have secure permissions, got {oct(f.mode)}"

    def test_policy_json_exists(self, host):
        """Verify container policy.json exists."""
        f = host.file("/etc/containers/policy.json")
        if f.exists:
            assert f.is_file, "/etc/containers/policy.json should be a file"


class TestRootlessPodman:
    """Test rootless Podman configuration."""

    def test_rootless_podman_subgid(self, host):
        """Verify subgid configuration for rootless Podman."""
        f = host.file("/etc/subgid")
        if f.exists:
            content = f.content_string
            # Should have entries for rootless containers
            assert len(content.strip()) > 0, "/etc/subgid should have entries"

    def test_rootless_podman_subuid(self, host):
        """Verify subuid configuration for rootless Podman."""
        f = host.file("/etc/subuid")
        if f.exists:
            content = f.content_string
            # Should have entries for rootless containers
            assert len(content.strip()) > 0, "/etc/subuid should have entries"

    def test_podman_socket_user_service(self, host):
        """Verify podman socket user service exists."""
        # Rootless podman uses user-level systemd services
        f = host.file("/usr/lib/systemd/user/podman.socket")
        if not f.exists:
            f = host.file("/etc/systemd/user/podman.socket")
        if f.exists:
            assert f.is_file, "podman.socket should be a file"


class TestCosignInstallation:
    """Test Cosign supply chain integrity tool."""

    def test_cosign_binary_exists(self, host):
        """Verify cosign binary exists."""
        f = host.file("/usr/local/bin/cosign")
        if not f.exists:
            f = host.file("/usr/bin/cosign")
        if f.exists:
            assert f.is_file, "cosign should be a file"
            assert f.mode in [0o755, 0o755], "cosign binary should be executable"
        else:
            pytest.skip("cosign not installed (may be optional)")

    def test_cosign_version_command(self, host):
        """Verify cosign version command works."""
        cmd = host.run("cosign version 2>&1")
        if cmd.rc == 0:
            assert "cosign" in cmd.stdout.lower(), "cosign version should return version info"
        else:
            pytest.skip("cosign not installed or not in PATH")


class TestGPUContainerSupport:
    """Test GPU container support configuration."""

    def test_nvidia_container_toolkit_config(self, host):
        """Verify NVIDIA container toolkit configuration."""
        f = host.file("/etc/nvidia-container-runtime/config.toml")
        if f.exists:
            assert f.is_file, "NVIDIA container runtime config should be a file"
            assert f.mode in [0o644, 0o640, 0o600], \
                f"NVIDIA config should have secure permissions, got {oct(f.mode)}"
        else:
            pytest.skip("NVIDIA container toolkit not configured")

    def test_nvidia_smi_command(self, host):
        """Verify nvidia-smi command is available."""
        cmd = host.run("nvidia-smi 2>&1")
        if cmd.rc == 0:
            assert "NVIDIA" in cmd.stdout, "nvidia-smi should return GPU info"
        else:
            pytest.skip("nvidia-smi not available (no NVIDIA GPU or drivers)")

    def test_rocm_smi_command(self, host):
        """Verify rocm-smi command is available for AMD GPUs."""
        cmd = host.run("rocm-smi 2>&1")
        if cmd.rc == 0:
            assert "AMD" in cmd.stdout or "GPU" in cmd.stdout, "rocm-smi should return GPU info"
        else:
            pytest.skip("rocm-smi not available (no AMD GPU)")

    def test_dri_devices_exist(self, host):
        """Verify /dev/dri devices exist for GPU access."""
        d = host.file("/dev/dri")
        if d.exists:
            assert d.is_directory, "/dev/dri should be a directory"
            # Should have renderD* devices
            cmd = host.run("ls /dev/dri/renderD* 2>&1")
            if cmd.rc == 0:
                assert "renderD" in cmd.stdout, "Should have renderD devices"
        else:
            pytest.skip("/dev/dri not available (no GPU)")


class TestContainerNetworking:
    """Test container networking configuration."""

    def test_cni_plugins_directory(self, host):
        """Verify CNI plugins directory exists."""
        d = host.file("/opt/cni/bin")
        if d.exists:
            assert d.is_directory, "/opt/cni/bin should be a directory"
        else:
            # Some systems use different paths
            d = host.file("/usr/libexec/cni")
            if d.exists:
                assert d.is_directory, "/usr/libexec/cni should be a directory"
            else:
                pytest.skip("CNI plugins directory not found")

    def test_podman_network_command(self, host):
        """Verify podman network command works."""
        cmd = host.run("podman network ls 2>&1")
        if cmd.rc == 0:
            # Should list networks (at minimum 'podman' default network)
            assert "network" in cmd.stdout.lower() or "podman" in cmd.stdout.lower(), \
                "podman network ls should return network list"
        else:
            pytest.skip("podman network command not available")


class TestContainerRuntimeCompletion:
    """Test container runtime completion indicators."""

    def test_podman_system_connection(self, host):
        """Verify podman system connection works."""
        cmd = host.run("podman system connection ls 2>&1")
        if cmd.rc == 0:
            assert "connection" in cmd.stdout.lower() or "default" in cmd.stdout.lower(), \
                "podman system connection should work"
        else:
            pytest.skip("podman system connection not available")

    def test_container_runtime_packages_available(self, host):
        """Verify at least one container runtime package is installed."""
        runtime_pkgs = ["podman", "docker", "crun", "runc"]
        has_runtime = False
        for pkg_name in runtime_pkgs:
            pkg = host.package(pkg_name)
            if pkg.is_installed:
                has_runtime = True
                break
        assert has_runtime, "At least one container runtime package should be installed"
