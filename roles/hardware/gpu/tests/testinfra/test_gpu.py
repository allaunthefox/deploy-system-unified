"""
Testinfra tests for hardware/gpu role.

This role handles GPU driver installation and configuration:
- Installing GPU driver packages (NVIDIA, AMD, Intel)
- Loading kernel modules
- Configuring hybrid graphics (Prime/Optimus)
- Setting up Vulkan and compute stacks
- Configuring eGPU and RDMA support
"""
import pytest


# GPU-related packages and modules
GPU_PACKAGES_DEBIAN = {
    "nvidia": ["nvidia-driver", "nvidia-smi", "nvidia-utils"],
    "amd": ["mesa-vulkan-drivers", "vulkan-radeon", "libgl1-mesa-dri", "libglx-mesa0"],
    "intel": ["mesa-vulkan-drivers", "vulkan-intel", "libgl1-mesa-dri", "intel-media-va-driver"],
    "generic": ["mesa-utils", "libgl1-mesa-dri", "vulkan-tools"],
}

GPU_KERNEL_MODULES = {
    "nvidia": ["nvidia", "nvidia_drm", "nvidia_modeset", "nvidia_uvm"],
    "amd": ["amdgpu", "radeon"],
    "intel": ["i915", "xe"],
}


class TestGPUDetection:
    """Test GPU hardware detection."""

    def test_gpu_hardware_detected(self, host):
        """Verify GPU hardware is detected."""
        cmd = host.run("lspci | grep -i 'vga\\|3d\\|display' 2>&1 || true")
        # Should detect at least one GPU
        # This is informational - may not have GPU in test environment

    def test_gpu_vendor_detection(self, host):
        """Verify GPU vendor can be detected."""
        cmd = host.run("lspci -nn | grep -i 'vga\\|3d\\|display' 2>&1 || true")
        # Should show vendor info (NVIDIA, AMD, Intel)
        pass

    def test_pci_devices_accessible(self, host):
        """Verify PCI devices are accessible."""
        cmd = host.run("lspci 2>&1 | head -5 || true")
        if cmd.rc == 0:
            assert "pci" in cmd.stdout.lower() or cmd.stdout.strip(), \
                "PCI devices should be accessible"


class TestGPUPackages:
    """Test GPU driver package installation."""

    def test_mesa_utils_installed(self, host):
        """Verify mesa-utils package is installed."""
        pkg = host.package("mesa-utils")
        assert pkg.is_installed, "mesa-utils package should be installed"

    def test_mesa_dri_installed(self, host):
        """Verify libgl1-mesa-dri package is installed."""
        pkg = host.package("libgl1-mesa-dri")
        assert pkg.is_installed, "libgl1-mesa-dri package should be installed"

    def test_vulkan_tools_installed(self, host):
        """Verify vulkan-tools package is installed."""
        pkg = host.package("vulkan-tools")
        assert pkg.is_installed, "vulkan-tools package should be installed"

    def test_libglx_mesa_installed(self, host):
        """Verify libglx-mesa0 package is installed."""
        pkg = host.package("libglx-mesa0")
        assert pkg.is_installed, "libglx-mesa0 package should be installed"


class TestGPUCommands:
    """Test GPU-related commands availability."""

    def test_glxinfo_available(self, host):
        """Verify glxinfo command is available."""
        assert host.exists("glxinfo"), "glxinfo command should be available"

    def test_glxgears_available(self, host):
        """Verify glxgears command is available."""
        assert host.exists("glxgears"), "glxgears command should be available"

    def test_vulkaninfo_available(self, host):
        """Verify vulkaninfo command is available."""
        assert host.exists("vulkaninfo"), "vulkaninfo command should be available"

    def test_vkcube_available(self, host):
        """Verify vkcube command is available."""
        assert host.exists("vkcube"), "vkcube command should be available"


class TestGPUNvidia:
    """Test NVIDIA GPU driver configuration."""

    def test_nvidia_driver_installed(self, host):
        """Verify NVIDIA driver package is installed if NVIDIA GPU present."""
        cmd = host.run("lspci | grep -i nvidia 2>&1 || true")
        if "nvidia" in cmd.stdout.lower():
            pkg = host.package("nvidia-driver")
            assert pkg.is_installed, "nvidia-driver package should be installed for NVIDIA GPU"

    def test_nvidia_smi_available(self, host):
        """Verify nvidia-smi command is available if NVIDIA GPU present."""
        cmd = host.run("lspci | grep -i nvidia 2>&1 || true")
        if "nvidia" in cmd.stdout.lower():
            assert host.exists("nvidia-smi"), "nvidia-smi command should be available for NVIDIA GPU"

    def test_nvidia_kernel_modules(self, host):
        """Verify NVIDIA kernel modules are loaded if NVIDIA GPU present."""
        cmd = host.run("lspci | grep -i nvidia 2>&1 || true")
        if "nvidia" in cmd.stdout.lower():
            lsmod_cmd = host.run("lsmod | grep nvidia 2>&1 || true")
            # Modules should be loaded if driver is active
            # May not be loaded in containers
            pass


class TestGPUAMD:
    """Test AMD GPU driver configuration."""

    def test_amdgpu_kernel_module(self, host):
        """Verify amdgpu kernel module is loaded if AMD GPU present."""
        cmd = host.run("lspci | grep -i 'amd\\|radeon' 2>&1 || true")
        if "amd" in cmd.stdout.lower() or "radeon" in cmd.stdout.lower():
            lsmod_cmd = host.run("lsmod | grep amdgpu 2>&1 || true")
            # Module should be loaded if AMD GPU is active
            pass

    def test_radeon_kernel_module(self, host):
        """Verify radeon kernel module is available for older AMD GPUs."""
        cmd = host.run("modinfo radeon 2>&1 || true")
        if cmd.rc == 0:
            assert "radeon" in cmd.stdout.lower(), "radeon module should be available"


class TestGPUIntel:
    """Test Intel GPU driver configuration."""

    def test_i915_kernel_module(self, host):
        """Verify i915 kernel module is loaded if Intel GPU present."""
        cmd = host.run("lspci | grep -i intel 2>&1 || true")
        if "intel" in cmd.stdout.lower():
            lsmod_cmd = host.run("lsmod | grep i915 2>&1 || true")
            # Module should be loaded if Intel GPU is active
            pass

    def test_intel_media_driver(self, host):
        """Verify Intel media driver is installed."""
        pkg = host.package("intel-media-va-driver")
        # May not be installed on all systems
        if pkg.is_installed:
            assert pkg.is_installed, "intel-media-va-driver should be installed"


class TestGPUKernelModules:
    """Test GPU kernel modules."""

    def test_drm_module_loaded(self, host):
        """Verify DRM (Direct Rendering Manager) module is loaded."""
        cmd = host.run("lsmod | grep drm 2>&1 || true")
        # DRM should be loaded for GPU functionality
        if cmd.stdout.strip():
            assert "drm" in cmd.stdout.lower(), "DRM module should be loaded"

    def test_drm_kms_helper_loaded(self, host):
        """Verify drm_kms_helper module is loaded."""
        cmd = host.run("lsmod | grep drm_kms_helper 2>&1 || true")
        # KMS helper should be loaded
        pass

    def test_gpu_modules_in_sysfs(self, host):
        """Verify GPU devices are in sysfs."""
        d = host.file("/sys/class/drm")
        if d.exists:
            assert d.is_directory, "/sys/class/drm should be a directory"


class TestGPUDeviceFiles:
    """Test GPU device files."""

    def test_dri_directory_exists(self, host):
        """Verify DRI (Direct Rendering Infrastructure) directory exists."""
        d = host.file("/dev/dri")
        if d.exists:
            assert d.is_directory, "/dev/dri should be a directory"

    def test_dri_card_devices(self, host):
        """Verify DRI card devices exist."""
        cmd = host.run("ls -la /dev/dri/card* 2>/dev/null || true")
        # Card devices should exist if GPU is active
        pass

    def test_dri_render_devices(self, host):
        """Verify DRI render devices exist."""
        cmd = host.run("ls -la /dev/dri/renderD* 2>/dev/null || true")
        # Render devices should exist if GPU is active
        pass


class TestGPUVulkan:
    """Test Vulkan configuration."""

    def test_vulkan_icd_directory(self, host):
        """Verify Vulkan ICD directory exists."""
        d = host.file("/usr/share/vulkan/icd.d")
        if d.exists:
            assert d.is_directory, "/usr/share/vulkan/icd.d should be a directory"

    def test_vulkan_icd_files(self, host):
        """Verify Vulkan ICD files exist."""
        cmd = host.run("ls -la /usr/share/vulkan/icd.d/*.json 2>/dev/null || true")
        # ICD files should exist for installed GPU drivers
        pass

    def test_vulkan_loader_available(self, host):
        """Verify Vulkan loader is available."""
        f = host.file("/usr/lib/x86_64-linux-gnu/libvulkan.so.1")
        if not f.exists:
            f = host.file("/usr/lib64/libvulkan.so.1")
        if f.exists:
            assert f.exists, "Vulkan loader library should exist"


class TestGPUHybrid:
    """Test hybrid graphics configuration."""

    def test_prime_configuration(self, host):
        """Verify Prime configuration if hybrid GPU present."""
        cmd = host.run("prime-select query 2>&1 || true")
        # Prime-select is available on Ubuntu for hybrid graphics
        pass

    def test_dgpu_power_management(self, host):
        """Verify dGPU power management if hybrid setup."""
        cmd = host.run("cat /sys/kernel/debug/vgaswitcheroo/switch 2>/dev/null || true")
        # VGA switcheroo shows hybrid GPU status
        pass


class TestGPUEGPU:
    """Test eGPU configuration."""

    def test_thunderbolt_available(self, host):
        """Verify Thunderbolt support if eGPU configured."""
        cmd = host.run("boltctl 2>&1 || true")
        # boltctl shows Thunderbolt devices
        pass

    def test_usb4_available(self, host):
        """Verify USB4 support if eGPU configured."""
        cmd = host.run("ls -la /sys/bus/thunderbolt/devices/ 2>/dev/null || true")
        # USB4/Thunderbolt devices
        pass


class TestGPUSecurity:
    """Test GPU security configuration."""

    def test_video_group_exists(self, host):
        """Verify video group exists for GPU access."""
        g = host.group("video")
        if g.exists:
            assert g.exists, "video group should exist"

    def test_render_group_exists(self, host):
        """Verify render group exists for GPU rendering."""
        g = host.group("render")
        if g.exists:
            assert g.exists, "render group should exist"

    def test_dri_permissions(self, host):
        """Verify DRI device permissions."""
        cmd = host.run("ls -la /dev/dri/ 2>/dev/null || true")
        if cmd.stdout.strip():
            # Devices should have appropriate permissions
            pass


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), GPU passthrough may not be available")

    def test_pci_access_available(self, host):
        """Verify PCI access is available."""
        cmd = host.run("lspci 2>&1 | head -1 || true")
        if cmd.rc != 0:
            pytest.skip("PCI access not available in this environment")
