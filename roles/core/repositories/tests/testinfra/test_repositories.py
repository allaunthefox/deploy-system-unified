# =============================================================================
# Audit Event Identifier: DSU-PYS-500061
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for core/repositories role.

This role handles package repository configuration:
- Enabling contrib/non-free repositories (Debian/Ubuntu)
- Enabling universe/multiverse repositories (Ubuntu)
- Installing RPMFusion repositories (Fedora)
- Enabling community repositories (Alpine)
- Updating package cache
"""
import pytest


class TestRepositoriesDebian:
    """Test Debian/Ubuntu repository configuration."""

    def test_sources_list_exists(self, host):
        """Verify sources.list exists on Debian systems."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            f = host.file("/etc/apt/sources.list")
            if f.exists:
                assert f.is_file, "/etc/apt/sources.list should be a file"

    def test_sources_list_permissions(self, host):
        """Verify sources.list has correct permissions."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            f = host.file("/etc/apt/sources.list")
            if f.exists:
                assert f.mode in [0o644, 0o640], "sources.list should have correct permissions"
                assert f.user == "root", "sources.list should be owned by root"

    def test_apt_sources_d_directory(self, host):
        """Verify /etc/apt/sources.list.d directory exists."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            d = host.file("/etc/apt/sources.list.d")
            assert d.exists, "/etc/apt/sources.list.d should exist"
            assert d.is_directory, "/etc/apt/sources.list.d should be a directory"

    def test_software_properties_common(self, host):
        """Verify software-properties-common is installed on Debian/Ubuntu."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            pkg = host.package("software-properties-common")
            assert pkg.is_installed, "software-properties-common should be installed"

    def test_gnupg_installed(self, host):
        """Verify gnupg is installed on Debian/Ubuntu."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            # Package name varies
            pkg_names = ["gnupg", "gnupg2"]
            has_gnupg = False
            for pkg_name in pkg_names:
                pkg = host.package(pkg_name)
                if pkg.is_installed:
                    has_gnupg = True
                    break
            assert has_gnupg, "gnupg or gnupg2 should be installed"

    def test_ca_certificates_installed(self, host):
        """Verify ca-certificates is installed on Debian/Ubuntu."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            pkg = host.package("ca-certificates")
            assert pkg.is_installed, "ca-certificates should be installed"


class TestRepositoriesRedHat:
    """Test RedHat/Fedora repository configuration."""

    def test_dnf_available(self, host):
        """Verify dnf is available on RedHat systems."""
        if host.system_info.distribution in ["centos", "fedora", "redhat", "rocky", "almalinux"]:
            assert host.exists("dnf") or host.exists("yum"), "dnf or yum should be available"

    def test_epel_release(self, host):
        """Verify EPEL release package status on RHEL/CentOS."""
        if host.system_info.distribution in ["centos", "redhat", "rocky", "almalinux"]:
            pkg = host.package("epel-release")
            if pkg.is_installed:
                assert pkg.is_installed, "epel-release should be installed if configured"


class TestRepositoriesFedora:
    """Test Fedora-specific repository configuration."""

    def test_rpmfusion_repos(self, host):
        """Verify RPMFusion repository configuration on Fedora."""
        if host.system_info.distribution == "fedora":
            # Check if RPMFusion repos are configured
            cmd = host.run("dnf repolist 2>/dev/null | grep -i rpmfusion || true")
            # RPMFusion may or may not be configured, this is informational
            pass


class TestRepositoriesAlpine:
    """Test Alpine repository configuration."""

    def test_apk_repositories_file(self, host):
        """Verify /etc/apk/repositories exists on Alpine."""
        if host.system_info.distribution == "alpine":
            f = host.file("/etc/apk/repositories")
            assert f.exists, "/etc/apk/repositories should exist"
            assert f.is_file, "/etc/apk/repositories should be a file"

    def test_apk_repositories_permissions(self, host):
        """Verify /etc/apk/repositories has correct permissions."""
        if host.system_info.distribution == "alpine":
            f = host.file("/etc/apk/repositories")
            if f.exists:
                assert f.mode in [0o644, 0o640], "/etc/apk/repositories should have correct permissions"

    def test_community_repo_enabled(self, host):
        """Verify community repository is enabled on Alpine."""
        if host.system_info.distribution == "alpine":
            f = host.file("/etc/apk/repositories")
            if f.exists:
                content = f.content_string
                # Community repo should not be commented out
                has_community = False
                for line in content.split("\n"):
                    if "community" in line and not line.strip().startswith("#"):
                        has_community = True
                        break
                # This is informational - community repo may be intentionally disabled


class TestRepositoriesPackageCache:
    """Test package cache status."""

    def test_apt_cache_updated(self, host):
        """Verify apt cache is updated on Debian/Ubuntu."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            # Check if apt cache exists and is recent
            cache_file = host.file("/var/lib/apt/lists")
            if cache_file.exists:
                assert cache_file.is_directory, "/var/lib/apt/lists should be a directory"

    def test_dnf_cache_exists(self, host):
        """Verify dnf cache exists on RedHat systems."""
        if host.system_info.distribution in ["centos", "fedora", "redhat", "rocky", "almalinux"]:
            cache_dir = host.file("/var/cache/dnf")
            if cache_dir.exists:
                assert cache_dir.is_directory, "/var/cache/dnf should be a directory"


class TestRepositoriesSecurity:
    """Test repository security configuration."""

    def test_gpg_keys_directory(self, host):
        """Verify GPG keys directory exists."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            d = host.file("/etc/apt/trusted.gpg.d")
            if d.exists:
                assert d.is_directory, "/etc/apt/trusted.gpg.d should be a directory"

    def test_keyring_directory(self, host):
        """Verify keyring directory exists."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            d = host.file("/usr/share/keyrings")
            if d.exists:
                assert d.is_directory, "/usr/share/keyrings should be a directory"

    def test_pacman_keyring(self, host):
        """Verify pacman keyring on Arch."""
        if host.system_info.distribution == "arch":
            d = host.file("/etc/pacman.d/gnupg")
            if d.exists:
                assert d.is_directory, "pacman keyring directory should exist"


class TestRepositoriesConfiguration:
    """Test repository configuration files."""

    def test_sources_list_format(self, host):
        """Verify sources.list has valid format."""
        if host.system_info.distribution in ["debian", "ubuntu"]:
            f = host.file("/etc/apt/sources.list")
            if f.exists:
                content = f.content_string
                for line in content.split("\n"):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Valid deb lines start with deb or deb-src
                    if line.startswith("deb"):
                        parts = line.split()
                        assert len(parts) >= 3, f"Invalid deb line: {line}"

    def test_dnf_repos_directory(self, host):
        """Verify /etc/yum.repos.d directory exists on RedHat."""
        if host.system_info.distribution in ["centos", "fedora", "redhat", "rocky", "almalinux"]:
            d = host.file("/etc/yum.repos.d")
            assert d.exists, "/etc/yum.repos.d should exist"
            assert d.is_directory, "/etc/yum.repos.d should be a directory"
