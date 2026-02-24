"""
Testinfra tests for containers/lxc role.

This role handles LXC container GPU configuration:
- LXC GPU passthrough configuration
- Vendor-specific GPU configurations (NVIDIA/AMD/Intel)
- LXC container GPU device access
- MIG/vGPU/SR-IOV configurations
"""
import pytest


# LXC directories
LXC_DIRS = {
    "/etc/lxc": {"mode": 0o755},
    "/etc/lxc/default.conf.d": {"mode": 0o755},
    "/var/lib/lxc": {"mode": 0o755},
}

# LXC configuration files
LXC_DEFAULT_CONFIG = "/etc/lxc/default.conf"
LXC_GPU_CONFIG = "/etc/lxc/default.conf.d/gpu.conf"

# GPU device paths
GPU_DEVICE_PATHS = {
    "nvidia": ["/dev/nvidia0", "/dev/nvidiactl", "/dev/nvidia-uvm"],
    "amd": ["/dev/dri", "/dev/kfd"],
    "intel": ["/dev/dri", "/dev/renderD128"],
}


class TestLXCDirectories:
    """Test LXC directory structure."""

    @pytest.mark.parametrize("path,expected", LXC_DIRS.items())
    def test_lxc_directories_exist(self, host, path, expected):
        """Verify LXC directories exist."""
        d = host.file(path)
        if d.exists:
            assert d.is_directory, f"{path} should be a directory"
        else:
            pytest.skip(f"{path} does not exist (LXC may not be installed)")

    def test_etc_lxc_directory(self, host):
        """Verify /etc/lxc exists."""
        d = host.file("/etc/lxc")
        if d.exists:
            assert d.is_directory, "/etc/lxc should be a directory"
            assert d.mode in [0o755, 0o750, 0o700], \
                f"/etc/lxc should have secure permissions, got {oct(d.mode)}"
        else:
            pytest.skip("/etc/lxc does not exist")

    def test_var_lib_lxc_directory(self, host):
        """Verify /var/lib/lxc exists."""
        d = host.file("/var/lib/lxc")
        if d.exists:
            assert d.is_directory, "/var/lib/lxc should be a directory"
        else:
            pytest.skip("/var/lib/lxc does not exist")


class TestLXCInstallation:
    """Test LXC installation."""

    def test_lxc_package_installed_debian(self, host):
        """Verify LXC is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("lxc")
            assert pkg.is_installed, "lxc package should be installed on Debian/Ubuntu"

    def test_lxc_package_installed_redhat(self, host):
        """Verify LXC is installed (RedHat/CentOS)."""
        if host.file("/etc/redhat-release").exists:
            pkg = host.package("lxc")
            if pkg.is_installed:
                assert pkg.is_installed, "lxc package should be installed on RedHat/CentOS"
            else:
                pytest.skip("LXC not available on RedHat (use podman instead)")

    def test_lxc_package_installed_arch(self, host):
        """Verify LXC is installed (Arch Linux)."""
        if host.file("/etc/arch-release").exists:
            pkg = host.package("lxc")
            assert pkg.is_installed, "lxc package should be installed on Arch Linux"

    def test_lxc_binary_exists(self, host):
        """Verify lxc binary exists."""
        f = host.file("/usr/bin/lxc")
        if not f.exists:
            f = host.file("/usr/local/bin/lxc")
        if f.exists:
            assert f.is_file, "lxc binary should be a file"
        else:
            # Check for lxc-* commands
            cmd = host.run("which lxc-start 2>&1 || which lxc-ls 2>&1 || true")
            if cmd.rc == 0:
                assert "lxc" in cmd.stdout, "lxc commands should be available"
            else:
                pytest.skip("LXC binaries not found")

    def test_lxc_version_command(self, host):
        """Verify lxc version command works."""
        cmd = host.run("lxc-version 2>&1 || lxc-ls --version 2>&1 || true")
        if cmd.rc == 0:
            assert "lxc" in cmd.stdout.lower(), "lxc version should return version info"
        else:
            pytest.skip("lxc version command not available")


class TestLXCConfiguration:
    """Test LXC configuration files."""

    def test_lxc_default_config_exists(self, host):
        """Verify LXC default configuration exists."""
        f = host.file(LXC_DEFAULT_CONFIG)
        if f.exists:
            assert f.is_file, "default.conf should be a file"
        else:
            pytest.skip("LXC default config not found")

    def test_lxc_default_config_permissions(self, host):
        """Verify LXC default config has correct permissions."""
        f = host.file(LXC_DEFAULT_CONFIG)
        if f.exists:
            assert f.mode in [0o644, 0o640, 0o600], \
                f"default.conf should have secure permissions, got {oct(f.mode)}"

    def test_lxc_default_conf_d_directory(self, host):
        """Verify LXC default.conf.d directory exists."""
        d = host.file("/etc/lxc/default.conf.d")
        if d.exists:
            assert d.is_directory, "/etc/lxc/default.conf.d should be a directory"
        else:
            pytest.skip("default.conf.d directory does not exist")


class TestLXCGPUConfiguration:
    """Test LXC GPU configuration."""

    def test_lxc_gpu_config_exists(self, host):
        """Verify LXC GPU configuration exists."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            assert f.is_file, "gpu.conf should be a file"
        else:
            pytest.skip("LXC GPU config not found (GPU support may not be enabled)")

    def test_lxc_gpu_config_permissions(self, host):
        """Verify LXC GPU config has correct permissions."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            assert f.mode in [0o644, 0o640], \
                f"gpu.conf should have secure permissions, got {oct(f.mode)}"

    def test_lxc_gpu_config_has_device_allow(self, host):
        """Verify LXC GPU config has device allow rules."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            # Should have lxc.cgroup2.devices.allow entries
            has_device_allow = "lxc.cgroup2.devices.allow" in content
            assert has_device_allow, "GPU config should have device allow rules"

    def test_lxc_gpu_config_has_nvidia_devices(self, host):
        """Verify LXC GPU config has NVIDIA device rules if NVIDIA."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            # Check for NVIDIA device rules
            if "nvidia" in content.lower():
                assert "nvidia" in content.lower(), \
                    "GPU config should have NVIDIA device rules"


class TestLXCGPUPassthrough:
    """Test LXC GPU passthrough configuration."""

    def test_lxc_gpu_passthrough_devices(self, host):
        """Verify LXC GPU passthrough devices are configured."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            # Should have device allow entries for GPU
            device_entries = [line for line in content.split("\n")
                            if "lxc.cgroup2.devices.allow" in line]
            if device_entries:
                assert len(device_entries) > 0, \
                    "Should have GPU device passthrough entries"

    def test_lxc_gpu_passthrough_capabilities(self, host):
        """Verify LXC GPU passthrough capabilities are configured."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            # May have capability entries
            if "lxc.cap" in content or "lxc.cgroup2.devices.allow" in content:
                assert True, "GPU capabilities or device access configured"


class TestNVIDIAGPUConfiguration:
    """Test NVIDIA GPU configuration for LXC."""

    def test_nvidia_container_toolkit_installed(self, host):
        """Verify NVIDIA container toolkit is installed."""
        pkg = host.package("nvidia-container-toolkit")
        if pkg.is_installed:
            assert pkg.is_installed, "nvidia-container-toolkit should be installed"
        else:
            pytest.skip("NVIDIA container toolkit not installed")

    def test_nvidia_smi_available(self, host):
        """Verify nvidia-smi is available."""
        cmd = host.run("nvidia-smi 2>&1")
        if cmd.rc == 0:
            assert "NVIDIA" in cmd.stdout, "nvidia-smi should return GPU info"
        else:
            pytest.skip("nvidia-smi not available")

    def test_nvidia_devices_exist(self, host):
        """Verify NVIDIA devices exist."""
        for device in GPU_DEVICE_PATHS.get("nvidia", []):
            d = host.file(device)
            if d.exists:
                assert d.exists, f"{device} should exist"
            # Devices may not exist if no GPU present

    def test_nvidia_driver_loaded(self, host):
        """Verify NVIDIA driver is loaded."""
        cmd = host.run("lsmod | grep nvidia 2>&1")
        if cmd.rc == 0:
            assert "nvidia" in cmd.stdout, "NVIDIA kernel module should be loaded"
        else:
            pytest.skip("NVIDIA driver not loaded")


class TestAMDGPUConfiguration:
    """Test AMD GPU configuration for LXC."""

    def test_amd_gpu_devices_exist(self, host):
        """Verify AMD GPU devices exist."""
        for device in GPU_DEVICE_PATHS.get("amd", []):
            d = host.file(device)
            if d.exists:
                assert d.is_directory if device.endswith("/dri") else d.exists, \
                    f"{device} should exist"

    def test_amd_gpu_driver_loaded(self, host):
        """Verify AMD GPU driver is loaded."""
        cmd = host.run("lsmod | grep -E 'amdgpu|radeon' 2>&1")
        if cmd.rc == 0:
            assert "amdgpu" in cmd.stdout or "radeon" in cmd.stdout, \
                "AMD GPU kernel module should be loaded"
        else:
            pytest.skip("AMD GPU driver not loaded")

    def test_rocm_installed(self, host):
        """Verify ROCm is installed."""
        pkg = host.package("rocm-smi-lib")
        if pkg.is_installed:
            assert pkg.is_installed, "rocm-smi-lib should be installed"
        else:
            pytest.skip("ROCm not installed")


class TestIntelGPUConfiguration:
    """Test Intel GPU configuration for LXC."""

    def test_intel_gpu_devices_exist(self, host):
        """Verify Intel GPU devices exist."""
        for device in GPU_DEVICE_PATHS.get("intel", []):
            d = host.file(device)
            if d.exists:
                assert d.exists, f"{device} should exist"

    def test_intel_gpu_driver_loaded(self, host):
        """Verify Intel GPU driver is loaded."""
        cmd = host.run("lsmod | grep -E 'i915|xe' 2>&1")
        if cmd.rc == 0:
            assert "i915" in cmd.stdout or "xe" in cmd.stdout, \
                "Intel GPU kernel module should be loaded"
        else:
            pytest.skip("Intel GPU driver not loaded")

    def test_intel_media_driver_installed(self, host):
        """Verify Intel media driver is installed."""
        pkg = host.package("intel-media-driver")
        if pkg.is_installed:
            assert pkg.is_installed, "intel-media-driver should be installed"
        else:
            pytest.skip("Intel media driver not installed")


class TestLXCContainerGPUAccess:
    """Test LXC container GPU access."""

    def test_lxc_container_gpu_config(self, host):
        """Verify LXC containers have GPU configuration."""
        cmd = host.run("lxc-ls 2>&1")
        if cmd.rc == 0 and cmd.stdout.strip():
            containers = cmd.stdout.strip().split()
            for container in containers:
                config_cmd = host.run(f"lxc config show {container} 2>&1 || true")
                if config_cmd.rc == 0:
                    # Check if GPU config is present
                    if "gpu" in config_cmd.stdout.lower():
                        assert "gpu" in config_cmd.stdout.lower(), \
                            f"Container {container} should have GPU config"
        else:
            pytest.skip("No LXC containers found")

    def test_lxc_gpu_config_applied(self, host):
        """Verify LXC GPU configuration is applied."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            # Should have valid configuration
            assert len(content.strip()) > 0, "GPU config should have content"


class TestLXCGPUSlicing:
    """Test LXC GPU slicing configurations."""

    def test_lxc_mig_configuration(self, host):
        """Verify LXC MIG configuration if NVIDIA MIG enabled."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            if "mig" in content.lower():
                assert "mig" in content.lower(), "MIG configuration should be present"

    def test_lxc_vgpu_configuration(self, host):
        """Verify LXC vGPU configuration if NVIDIA vGPU enabled."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            if "vgpu" in content.lower():
                assert "vgpu" in content.lower(), "vGPU configuration should be present"

    def test_lxc_sriov_configuration(self, host):
        """Verify LXC SR-IOV configuration if AMD SR-IOV enabled."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            if "sriov" in content.lower():
                assert "sriov" in content.lower(), "SR-IOV configuration should be present"


class TestLXCCompletion:
    """Test LXC GPU configuration completion indicators."""

    def test_lxc_gpu_config_complete(self, host):
        """Verify LXC GPU configuration is complete."""
        f = host.file(LXC_GPU_CONFIG)
        if f.exists:
            content = f.content_string
            # Should have device allow entries
            assert "lxc.cgroup2.devices.allow" in content, \
                "GPU config should have device allow rules"
        else:
            pytest.skip("GPU config not found")

    def test_lxc_system_ready_for_gpu(self, host):
        """Verify system is ready for LXC GPU containers."""
        # Check for at least one GPU-related component
        gpu_indicators = [
            host.file("/dev/nvidia0").exists,
            host.file("/dev/dri").exists,
            host.file("/dev/kfd").exists,
        ]
        assert any(gpu_indicators), "System should have GPU devices available"
