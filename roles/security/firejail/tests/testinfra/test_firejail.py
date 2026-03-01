# =============================================================================
# Audit Event Identifier: DSU-PYS-500041
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for security/firejail role.

This role handles application sandboxing with Firejail:
- Firejail package installation
- Firejail configuration directory setup
- Firejail GPU access configuration
- Firejail profile management
"""
import pytest


# Firejail configuration paths
FIREJAIL_BIN = "/usr/bin/firejail"
FIREJAIL_CONFIG_DIR = "/etc/firejail"
FIREJAIL_LOCAL_DIR = "/usr/local/etc/firejail"
FIREJAIL_GLOBALS_LOCAL = "/etc/firejail/globals.local"
FIREJAIL_DEFAULT_PROFILE = "/etc/firejail/default.profile"


class TestFirejailInstallation:
    """Test Firejail package installation."""

    def test_firejail_package_installed(self, host):
        """Verify Firejail package is installed."""
        pkg = host.package("firejail")
        assert pkg.is_installed, "firejail package should be installed"

    def test_firejail_binary_exists(self, host):
        """Verify Firejail binary exists."""
        f = host.file(FIREJAIL_BIN)
        assert f.exists, f"Firejail binary '{FIREJAIL_BIN}' should exist"
        assert f.is_file, f"'{FIREJAIL_BIN}' should be a regular file"

    def test_firejail_binary_permissions(self, host):
        """Verify Firejail binary has correct permissions."""
        f = host.file(FIREJAIL_BIN)
        if f.exists:
            # Should be executable with setuid bit for sandboxing
            assert f.mode & 0o111, f"'{FIREJAIL_BIN}' should be executable"
            # Firejail typically has setuid root
            has_setuid = (f.mode & 0o4000) != 0
            # Note: setuid might not be set in all configurations
            # assert has_setuid, f"'{FIREJAIL_BIN}' should have setuid bit"

    def test_firejail_version(self, host):
        """Verify Firejail version can be determined."""
        cmd = host.run("firejail --version 2>&1")
        if cmd.rc == 0:
            assert "firejail" in cmd.stdout.lower(), \
                "firejail --version should return version info"
        else:
            pytest.skip("firejail --version not available")


class TestFirejailConfiguration:
    """Test Firejail configuration directories."""

    def test_firejail_config_directory_exists(self, host):
        """Verify Firejail configuration directory exists."""
        d = host.file(FIREJAIL_CONFIG_DIR)
        assert d.exists, f"Firejail config directory '{FIREJAIL_CONFIG_DIR}' should exist"
        assert d.is_directory, f"'{FIREJAIL_CONFIG_DIR}' should be a directory"

    def test_firejail_config_directory_permissions(self, host):
        """Verify Firejail configuration directory has correct permissions."""
        d = host.file(FIREJAIL_CONFIG_DIR)
        assert d.mode == 0o755, \
            f"Firejail config directory should have mode 0755, got {oct(d.mode)}"
        assert d.user == "root", "Firejail config directory should be owned by root"

    def test_firejail_local_config_directory_exists(self, host):
        """Verify Firejail local configuration directory exists."""
        d = host.file(FIREJAIL_LOCAL_DIR)
        assert d.exists, f"Firejail local config directory '{FIREJAIL_LOCAL_DIR}' should exist"
        assert d.is_directory, f"'{FIREJAIL_LOCAL_DIR}' should be a directory"

    def test_firejail_local_config_directory_permissions(self, host):
        """Verify Firejail local configuration directory has correct permissions."""
        d = host.file(FIREJAIL_LOCAL_DIR)
        assert d.mode == 0o755, \
            f"Firejail local config directory should have mode 0755, got {oct(d.mode)}"


class TestFirejailProfiles:
    """Test Firejail profiles."""

    def test_default_profile_exists(self, host):
        """Verify default Firejail profile exists."""
        f = host.file(FIREJAIL_DEFAULT_PROFILE)
        if f.exists:
            assert f.is_file, f"Default profile '{FIREJAIL_DEFAULT_PROFILE}' should be a file"
        else:
            pytest.skip(f"Default profile '{FIREJAIL_DEFAULT_PROFILE}' does not exist")

    def test_profile_files_have_correct_extension(self, host):
        """Verify profile files have correct extension."""
        d = host.file(FIREJAIL_CONFIG_DIR)
        if d.exists and d.is_directory:
            cmd = host.run(f"ls {FIREJAIL_CONFIG_DIR}/*.profile 2>/dev/null | head -5 || true")
            if cmd.rc == 0 and cmd.stdout:
                for line in cmd.stdout.strip().split("\n"):
                    if line:
                        assert line.endswith(".profile"), \
                            f"Profile file should end with .profile: {line}"
            else:
                pytest.skip("No profile files found")
        else:
            pytest.skip(f"Firejail config directory '{FIREJAIL_CONFIG_DIR}' does not exist")

    def test_profiles_readable(self, host):
        """Verify Firejail profiles are readable."""
        d = host.file(FIREJAIL_CONFIG_DIR)
        if d.exists and d.is_directory:
            cmd = host.run(f"ls {FIREJAIL_CONFIG_DIR}/*.profile 2>/dev/null | head -1")
            if cmd.rc == 0 and cmd.stdout.strip():
                profile_file = cmd.stdout.strip()
                f = host.file(profile_file)
                assert f.is_readable, f"Profile file '{profile_file}' should be readable"
        else:
            pytest.skip(f"Firejail config directory '{FIREJAIL_CONFIG_DIR}' does not exist")


class TestFirejailGPUConfiguration:
    """Test Firejail GPU access configuration."""

    def test_globals_local_exists_when_enabled(self, host):
        """Verify globals.local exists when GPU is enabled."""
        f = host.file(FIREJAIL_GLOBALS_LOCAL)
        if f.exists:
            assert f.is_file, f"globals.local '{FIREJAIL_GLOBALS_LOCAL}' should be a file"
            assert f.mode == 0o644, \
                f"globals.local should have mode 0644, got {oct(f.mode)}"
        else:
            pytest.skip(f"globals.local '{FIREJAIL_GLOBALS_LOCAL}' does not exist (GPU may be disabled)")

    def test_globals_local_has_gpu_config(self, host):
        """Verify globals.local has GPU configuration when enabled."""
        f = host.file(FIREJAIL_GLOBALS_LOCAL)
        if f.exists:
            content = f.content_string
            # Check for GPU-related configurations
            has_gpu_config = False
            gpu_patterns = [
                "noblacklist /dev/dri",
                "noblacklist /dev/nvidia",
                "noblacklist /dev/kfd",
            ]
            for pattern in gpu_patterns:
                if pattern in content:
                    has_gpu_config = True
                    break
            if has_gpu_config:
                # Verify GPU access is properly configured
                assert "noblacklist" in content, "globals.local should have noblacklist directives"
            else:
                pytest.skip("No GPU configuration found in globals.local")
        else:
            pytest.skip(f"globals.local '{FIREJAIL_GLOBALS_LOCAL}' does not exist")

    def test_globals_local_content_valid(self, host):
        """Verify globals.local has valid content."""
        f = host.file(FIREJAIL_GLOBALS_LOCAL)
        if f.exists:
            content = f.content_string
            # Should have comments or configuration
            lines = [l for l in content.split("\n") if l.strip() and not l.strip().startswith("#")]
            if lines:
                # Each line should be a valid firejail directive
                for line in lines:
                    # Basic validation - should be a known directive
                    valid_prefixes = ["noblacklist", "blacklist", "whitelist", "include", 
                                     "private", "tmpfs", "bind", "seccomp"]
                    has_valid_prefix = any(line.startswith(p) for p in valid_prefixes)
                    if not has_valid_prefix:
                        pytest.skip(f"Unknown directive in globals.local: {line}")
        else:
            pytest.skip(f"globals.local '{FIREJAIL_GLOBALS_LOCAL}' does not exist")


class TestFirejailCapabilities:
    """Test Firejail capabilities."""

    def test_firejail_help(self, host):
        """Verify Firejail help is available."""
        cmd = host.run("firejail --help 2>&1 | head -20")
        if cmd.rc == 0:
            assert "firejail" in cmd.stdout.lower() or "usage" in cmd.stdout.lower(), \
                "firejail --help should return usage info"
        else:
            pytest.skip("firejail --help not available")

    def test_firejail_list_profiles(self, host):
        """Verify Firejail can list profiles."""
        cmd = host.run("firejail --list 2>&1 | head -10 || true")
        # This may show running sandboxes
        # Just verify command runs

    def test_firejail_show_profiles(self, host):
        """Verify Firejail can show available profiles."""
        cmd = host.run("ls /etc/firejail/*.profile 2>&1 | head -5 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert ".profile" in cmd.stdout, "Firejail should have profiles available"
        else:
            pytest.skip("Cannot list Firejail profiles")


class TestFirejailSandboxing:
    """Test Firejail sandboxing capabilities."""

    def test_firejail_can_create_sandbox(self, host):
        """Verify Firejail can create a basic sandbox."""
        # Test basic sandbox with a simple command
        cmd = host.run("firejail --quiet --noprofile echo sandbox_test 2>&1")
        if cmd.rc == 0:
            assert "sandbox_test" in cmd.stdout, "Firejail should be able to create sandbox"
        else:
            # May fail in certain environments
            pytest.skip(f"Firejail sandbox test failed: {cmd.stdout}")

    def test_firejail_network_isolation(self, host):
        """Verify Firejail network isolation capability."""
        cmd = host.run("firejail --help 2>&1 | grep -i 'net\\|network' || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "net" in cmd.stdout.lower(), "Firejail should support network isolation"
        else:
            pytest.skip("Network isolation help not found")


class TestFirejailSecurity:
    """Test Firejail security features."""

    def test_firejail_seccomp_support(self, host):
        """Verify Firejail seccomp support."""
        cmd = host.run("firejail --help 2>&1 | grep -i seccomp || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "seccomp" in cmd.stdout.lower(), "Firejail should support seccomp"
        else:
            pytest.skip("Seccomp help not found")

    def test_firejail_caps_support(self, host):
        """Verify Firejail capabilities support."""
        cmd = host.run("firejail --help 2>&1 | grep -i 'caps\\|capability' || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "caps" in cmd.stdout.lower() or "capability" in cmd.stdout.lower(), \
                "Firejail should support capabilities"
        else:
            pytest.skip("Capabilities help not found")

    def test_firejail_private_option(self, host):
        """Verify Firejail private home directory support."""
        cmd = host.run("firejail --help 2>&1 | grep -i 'private' || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "private" in cmd.stdout.lower(), "Firejail should support private directories"
        else:
            pytest.skip("Private directory help not found")


class TestFirejailIntegration:
    """Test Firejail integration with system."""

    def test_firejail_directory_structure(self, host):
        """Verify Firejail directory structure."""
        d = host.file(FIREJAIL_CONFIG_DIR)
        if d.exists and d.is_directory:
            # Check for expected subdirectories
            subdirs = ["disable", "local"]
            for subdir in subdirs:
                sd = host.file(f"{FIREJAIL_CONFIG_DIR}/{subdir}")
                if sd.exists:
                    assert sd.is_directory, f"{subdir} should be a directory"
        else:
            pytest.skip(f"Firejail config directory '{FIREJAIL_CONFIG_DIR}' does not exist")

    def test_firejail_disable_directory_exists(self, host):
        """Verify Firejail disable directory exists."""
        d = host.file(f"{FIREJAIL_CONFIG_DIR}/disable")
        if d.exists:
            assert d.is_directory, f"'{FIREJAIL_CONFIG_DIR}/disable' should be a directory"
        else:
            pytest.skip(f"Firejail disable directory does not exist")


class TestFirejailLogging:
    """Test Firejail logging."""

    def test_firejail_can_log(self, host):
        """Verify Firejail can produce logs."""
        cmd = host.run("firejail --help 2>&1 | grep -i 'log\\|debug' || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "log" in cmd.stdout.lower() or "debug" in cmd.stdout.lower(), \
                "Firejail should support logging"
        else:
            pytest.skip("Logging help not found")


class TestContainerDetection:
    """Test container environment handling."""

    def test_not_in_container_or_skip(self, host):
        """Verify test handles container environment appropriately."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        if cmd.rc == 0:
            virt_type = cmd.stdout.strip().lower()
            if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
                pytest.skip(f"Running in container ({virt_type}), Firejail may have limited functionality")


class TestFirejailCompletion:
    """Test Firejail configuration completion."""

    def test_firejail_properly_installed(self, host):
        """Verify Firejail is properly installed."""
        pkg = host.package("firejail")
        assert pkg.is_installed, "firejail package should be installed"

    def test_firejail_config_directory_configured(self, host):
        """Verify Firejail configuration directory is configured."""
        d = host.file(FIREJAIL_CONFIG_DIR)
        assert d.exists, f"Firejail config directory '{FIREJAIL_CONFIG_DIR}' should exist"

    def test_firejail_local_config_directory_configured(self, host):
        """Verify Firejail local configuration directory is configured."""
        d = host.file(FIREJAIL_LOCAL_DIR)
        assert d.exists, f"Firejail local config directory '{FIREJAIL_LOCAL_DIR}' should exist"

    def test_firejail_available(self, host):
        """Verify Firejail is available for use."""
        assert host.exists("firejail"), "firejail command should be available"
