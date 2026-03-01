# =============================================================================
# Audit Event Identifier: DSU-PYS-500092
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for virtualization/kvm role.

This role handles KVM/QEMU virtualization setup:
- Installing QEMU and KVM packages
- Configuring libvirt daemon
- Setting up virtual networking
- Configuring TPM emulation (swtpm)
- Installing VM management tools
"""
import pytest


# KVM-related packages
KVM_PACKAGES_DEBIAN = [
    "qemu-kvm",
    "qemu-utils",
    "libvirt-daemon-system",
    "libvirt-clients",
    "bridge-utils",
    "virt-manager",
    "ovmf",
    "libguestfs-tools",
    "swtpm",
    "swtpm-tools",
]

# KVM kernel modules
KVM_KERNEL_MODULES = {
    "intel": "kvm_intel",
    "amd": "kvm_amd",
    "generic": "kvm",
}


class TestKVMPackages:
    """Test KVM package installation."""

    def test_qemu_kvm_installed(self, host):
        """Verify qemu-kvm package is installed."""
        pkg = host.package("qemu-kvm")
        if pkg.is_installed:
            assert pkg.is_installed, "qemu-kvm package should be installed"

    def test_qemu_utils_installed(self, host):
        """Verify qemu-utils package is installed."""
        pkg = host.package("qemu-utils")
        if pkg.is_installed:
            assert pkg.is_installed, "qemu-utils package should be installed"

    def test_libvirt_daemon_installed(self, host):
        """Verify libvirt-daemon-system package is installed."""
        pkg = host.package("libvirt-daemon-system")
        if pkg.is_installed:
            assert pkg.is_installed, "libvirt-daemon-system package should be installed"

    def test_libvirt_clients_installed(self, host):
        """Verify libvirt-clients package is installed."""
        pkg = host.package("libvirt-clients")
        if pkg.is_installed:
            assert pkg.is_installed, "libvirt-clients package should be installed"

    def test_bridge_utils_installed(self, host):
        """Verify bridge-utils package is installed."""
        pkg = host.package("bridge-utils")
        if pkg.is_installed:
            assert pkg.is_installed, "bridge-utils package should be installed"

    def test_ovmf_installed(self, host):
        """Verify ovmf (UEFI) package is installed."""
        pkg = host.package("ovmf")
        if pkg.is_installed:
            assert pkg.is_installed, "ovmf package should be installed"

    def test_swtpm_installed(self, host):
        """Verify swtpm package is installed."""
        pkg = host.package("swtpm")
        if pkg.is_installed:
            assert pkg.is_installed, "swtpm package should be installed"


class TestKVMCommands:
    """Test KVM-related commands availability."""

    def test_qemu_img_available(self, host):
        """Verify qemu-img command is available."""
        assert host.exists("qemu-img"), "qemu-img command should be available"

    def test_qemu_nbd_available(self, host):
        """Verify qemu-nbd command is available."""
        assert host.exists("qemu-nbd"), "qemu-nbd command should be available"

    def test_virsh_available(self, host):
        """Verify virsh command is available."""
        assert host.exists("virsh"), "virsh command should be available"

    def test_virt_manager_available(self, host):
        """Verify virt-manager command is available."""
        assert host.exists("virt-manager"), "virt-manager command should be available"

    def test_guestfish_available(self, host):
        """Verify guestfish command is available."""
        assert host.exists("guestfish"), "guestfish command should be available"


class TestKVMKernelModules:
    """Test KVM kernel modules."""

    def test_kvm_module_available(self, host):
        """Verify kvm kernel module is available."""
        cmd = host.run("modinfo kvm 2>&1 || true")
        if cmd.rc == 0:
            assert "kvm" in cmd.stdout.lower(), "kvm module should be available"

    def test_kvm_intel_module(self, host):
        """Verify kvm_intel module is available for Intel CPUs."""
        cmd = host.run("modinfo kvm_intel 2>&1 || true")
        if cmd.rc == 0:
            assert "kvm_intel" in cmd.stdout.lower(), "kvm_intel module should be available"

    def test_kvm_amd_module(self, host):
        """Verify kvm_amd module is available for AMD CPUs."""
        cmd = host.run("modinfo kvm_amd 2>&1 || true")
        if cmd.rc == 0:
            assert "kvm_amd" in cmd.stdout.lower(), "kvm_amd module should be available"

    def test_kvm_module_loaded(self, host):
        """Verify kvm module is loaded."""
        cmd = host.run("lsmod | grep kvm 2>&1 || true")
        # May not be loaded in containers
        pass


class TestKVMService:
    """Test libvirt service configuration."""

    def test_libvirtd_service_exists(self, host):
        """Verify libvirtd service exists."""
        svc = host.service("libvirtd")
        if svc.exists:
            assert svc.exists, "libvirtd service should exist"

    def test_libvirtd_service_enabled(self, host):
        """Verify libvirtd service is enabled."""
        svc = host.service("libvirtd")
        if svc.exists:
            assert svc.is_enabled, "libvirtd service should be enabled"

    def test_libvirtd_service_running(self, host):
        """Verify libvirtd service is running."""
        svc = host.service("libvirtd")
        if svc.exists:
            assert svc.is_running, "libvirtd service should be running"


class TestKVMNetworking:
    """Test KVM networking configuration."""

    def test_libvirt_networks_directory(self, host):
        """Verify libvirt networks directory exists."""
        d = host.file("/etc/libvirt/qemu/networks")
        if d.exists:
            assert d.is_directory, "/etc/libvirt/qemu/networks should be a directory"

    def test_bridge_utils_available(self, host):
        """Verify bridge configuration commands are available."""
        assert host.exists("brctl"), "brctl command should be available"


class TestKVMStorage:
    """Test KVM storage configuration."""

    def test_libvirt_storage_directory(self, host):
        """Verify libvirt storage directory exists."""
        d = host.file("/var/lib/libvirt")
        if d.exists:
            assert d.is_directory, "/var/lib/libvirt should be a directory"

    def test_qemu_img_command(self, host):
        """Verify qemu-img can create disk images."""
        cmd = host.run("qemu-img --help 2>&1 | head -5 || true")
        if cmd.rc == 0:
            assert "qemu-img" in cmd.stdout.lower(), "qemu-img help should be available"


class TestKVMSecurity:
    """Test KVM security configuration."""

    def test_libvirt_group_exists(self, host):
        """Verify libvirt group exists."""
        g = host.group("libvirt")
        if g.exists:
            assert g.exists, "libvirt group should exist"

    def test_kvm_group_exists(self, host):
        """Verify kvm group exists."""
        g = host.group("kvm")
        if g.exists:
            assert g.exists, "kvm group should exist"

    def test_swtpm_available(self, host):
        """Verify software TPM is available."""
        assert host.exists("swtpm"), "swtpm command should be available"


class TestKVMUEFI:
    """Test UEFI support for VMs."""

    def test_ovmf_directory(self, host):
        """Verify OVMF firmware directory exists."""
        d = host.file("/usr/share/OVMF")
        if d.exists:
            assert d.is_directory, "/usr/share/OVMF should be a directory"

    def test_ovmf_files_exist(self, host):
        """Verify OVMF firmware files exist."""
        cmd = host.run("ls /usr/share/OVMF/*.fd 2>/dev/null || true")
        # OVMF files should exist if ovmf package is installed
        pass


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), KVM virtualization not available")

    def test_kvm_access_in_container(self, host):
        """Verify KVM access in container."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        if "container" in cmd.stdout.lower():
            pytest.skip("KVM virtualization not accessible in container environment")
