# =============================================================================
# Audit Event Identifier: DSU-PYS-500054
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for core/bootstrap role.

This role handles system initialization and base configuration including:
- Installing base packages (curl, wget, git, sudo, vim, htop, net-tools, pciutils)
- Creating standard system directories
- Detecting virtualization environment
"""
import pytest


# Base packages that should be installed on all systems
BASE_PACKAGES = [
    "curl",
    "wget",
    "git",
    "sudo",
    "vim",
    "htop",
    "net-tools",
    "pciutils",
]

# Distribution-specific packages
DEBIAN_PACKAGES = [
    "python3-apt",
    "software-properties-common",
    "build-essential",
    "gnupg2",
]

REDHAT_PACKAGES = [
    "python3-dnf",
    "epel-release",
    "tar",
]

ARCH_PACKAGES = [
    "base-devel",
    "python",
]

ALPINE_PACKAGES = [
    "python3",
    "shadow",
    "bash",
]

# Standard directories that should exist
STANDARD_DIRECTORIES = [
    "/etc/ansible",
    "/usr/local/bin",
    "/var/log/custom_ops",
]


class TestBootstrapPackages:
    """Test base package installation."""

    @pytest.mark.parametrize("package", BASE_PACKAGES)
    def test_base_packages_installed(self, host, package):
        """Verify base packages are installed."""
        pkg = host.package(package)
        assert pkg.is_installed, f"Base package '{package}' should be installed"


class TestBootstrapDistributionPackages:
    """Test distribution-specific package installation."""

    def test_debian_packages(self, host):
        """Verify Debian-specific packages are installed on Debian systems."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            for package in DEBIAN_PACKAGES:
                pkg = host.package(package)
                assert pkg.is_installed, f"Debian package '{package}' should be installed"

    def test_redhat_packages(self, host):
        """Verify RedHat-specific packages are installed on RedHat systems."""
        if host.system_info.distribution in ["centos", "fedora", "redhat", "rocky", "almalinux"]:
            for package in REDHAT_PACKAGES:
                pkg = host.package(package)
                assert pkg.is_installed, f"RedHat package '{package}' should be installed"

    def test_arch_packages(self, host):
        """Verify Arch-specific packages are installed on Arch systems."""
        if host.system_info.distribution == "arch":
            for package in ARCH_PACKAGES:
                pkg = host.package(package)
                assert pkg.is_installed, f"Arch package '{package}' should be installed"

    def test_alpine_packages(self, host):
        """Verify Alpine-specific packages are installed on Alpine systems."""
        if host.system_info.distribution == "alpine":
            for package in ALPINE_PACKAGES:
                pkg = host.package(package)
                assert pkg.is_installed, f"Alpine package '{package}' should be installed"


class TestBootstrapDirectories:
    """Test standard system directories."""

    @pytest.mark.parametrize("directory", STANDARD_DIRECTORIES)
    def test_standard_directories_exist(self, host, directory):
        """Verify standard system directories exist."""
        d = host.file(directory)
        assert d.exists, f"Directory '{directory}' should exist"
        assert d.is_directory, f"'{directory}' should be a directory"
        assert d.mode == 0o755, f"Directory '{directory}' should have mode 0755"


class TestBootstrapSystemState:
    """Test system state and configuration."""

    def test_package_manager_available(self, host):
        """Verify package manager is available."""
        # Check for common package managers
        package_managers = ["apt", "dnf", "yum", "pacman", "apk"]
        has_package_manager = False
        for pm in package_managers:
            if host.exists(pm):
                has_package_manager = True
                break
        assert has_package_manager, "At least one package manager should be available"

    def test_root_user_exists(self, host):
        """Verify root user exists."""
        user = host.user("root")
        assert user.exists, "Root user should exist"
        assert user.gid == 0, "Root user should have GID 0"

    def test_etc_directory_exists(self, host):
        """Verify /etc directory exists and is accessible."""
        d = host.file("/etc")
        assert d.exists, "/etc directory should exist"
        assert d.is_directory, "/etc should be a directory"

    def test_tmp_directory_exists(self, host):
        """Verify /tmp directory exists."""
        d = host.file("/tmp")
        assert d.exists, "/tmp directory should exist"
        assert d.is_directory, "/tmp should be a directory"

    def test_var_log_directory_exists(self, host):
        """Verify /var/log directory exists."""
        d = host.file("/var/log")
        assert d.exists, "/var/log directory should exist"
        assert d.is_directory, "/var/log should be a directory"


class TestBootstrapNetwork:
    """Test network configuration."""

    def test_localhost_resolves(self, host):
        """Verify localhost resolves correctly."""
        cmd = host.run("getent hosts localhost")
        assert cmd.rc == 0, "localhost should resolve"

    def test_network_tools_available(self, host):
        """Verify network diagnostic tools are available."""
        # net-tools should provide these commands
        network_commands = ["ifconfig", "netstat", "ip"]
        has_network_tool = False
        for cmd in network_commands:
            if host.exists(cmd):
                has_network_tool = True
                break
        assert has_network_tool, "At least one network diagnostic tool should be available"
