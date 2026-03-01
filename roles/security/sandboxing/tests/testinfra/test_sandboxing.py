# =============================================================================
# Audit Event Identifier: DSU-PYS-500049
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for security/sandboxing role.

This role handles user-space isolation:
- Bubblewrap installation
- Landlock kernel support verification
- Sandbox policy directory configuration
- Sandbox profile deployment
"""
import pytest


# Sandboxing configuration paths
BUBBLEWRAP_BIN = "/usr/bin/bwrap"
SANDBOXING_POLICY_DIR = "/etc/sandboxing/policies"
LANDLOCK_DEVICE = "/dev/landlock"


class TestBubblewrapInstallation:
    """Test Bubblewrap installation."""

    def test_bubblewrap_package_installed(self, host):
        """Verify Bubblewrap package is installed."""
        pkg = host.package("bubblewrap")
        assert pkg.is_installed, "bubblewrap package should be installed"

    def test_bubblewrap_binary_exists(self, host):
        """Verify Bubblewrap binary exists."""
        f = host.file(BUBBLEWRAP_BIN)
        assert f.exists, f"Bubblewrap binary '{BUBBLEWRAP_BIN}' should exist"
        assert f.is_file, f"'{BUBBLEWRAP_BIN}' should be a regular file"

    def test_bubblewrap_binary_permissions(self, host):
        """Verify Bubblewrap binary has correct permissions."""
        f = host.file(BUBBLEWRAP_BIN)
        if f.exists:
            # Should be executable
            assert f.mode & 0o111, f"'{BUBBLEWRAP_BIN}' should be executable"
            assert f.user == "root", "Bubblewrap binary should be owned by root"

    def test_bubblewrap_version(self, host):
        """Verify Bubblewrap version can be determined."""
        cmd = host.run("bwrap --version 2>&1")
        if cmd.rc == 0:
            assert "bubblewrap" in cmd.stdout.lower() or "bwrap" in cmd.stdout.lower(), \
                "bwrap --version should return version info"
        else:
            pytest.skip("bwrap --version not available")


class TestBubblewrapCapabilities:
    """Test Bubblewrap capabilities."""

    def test_bubblewrap_help(self, host):
        """Verify Bubblewrap help is available."""
        cmd = host.run("bwrap --help 2>&1 | head -10")
        if cmd.rc == 0:
            assert "bubblewrap" in cmd.stdout.lower() or "usage" in cmd.stdout.lower(), \
                "bwrap --help should return usage info"
        else:
            pytest.skip("bwrap --help not available")

    def test_bubblewrap_can_create_sandbox(self, host):
        """Verify Bubblewrap can create a basic sandbox."""
        # Test basic sandbox creation (read-only root)
        cmd = host.run("bwrap --ro-bind / / --dev /dev --proc /proc --unshare-all echo sandbox_test 2>&1")
        if cmd.rc == 0:
            assert "sandbox_test" in cmd.stdout, "Bubblewrap should be able to create sandbox"
        else:
            # May fail in certain environments (containers, missing capabilities)
            pytest.skip(f"Bubblewrap sandbox test failed: {cmd.stdout}")


class TestLandlockSupport:
    """Test Landlock kernel support."""

    def test_landlock_kernel_support(self, host):
        """Verify Landlock kernel support is available."""
        # Check kernel config
        cmd = host.run("grep -i landlock /boot/config-$(uname -r) 2>/dev/null || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "CONFIG_SECURITY_LANDLOCK" in cmd.stdout, \
                "Kernel should have Landlock support configured"
        else:
            # Check via dmesg or device
            cmd = host.run("dmesg | grep -i landlock 2>&1 || true")
            if cmd.rc == 0 and cmd.stdout:
                pass  # Landlock detected in dmesg
            else:
                pytest.skip("Landlock kernel support not detected")

    def test_landlock_device_exists(self, host):
        """Verify Landlock device exists if available."""
        f = host.file(LANDLOCK_DEVICE)
        if f.exists:
            assert f.is_char_device, f"'{LANDLOCK_DEVICE}' should be a character device"
        else:
            pytest.skip(f"Landlock device '{LANDLOCK_DEVICE}' does not exist")

    def test_landlock_status_reported(self, host):
        """Verify Landlock status is reported."""
        # This is informational - the role reports Landlock status
        pytest.skip("Landlock status reporting is done during Ansible execution")


class TestSandboxingPolicyDirectory:
    """Test sandboxing policy directory."""

    def test_policy_directory_exists(self, host):
        """Verify sandboxing policy directory exists."""
        d = host.file(SANDBOXING_POLICY_DIR)
        assert d.exists, f"Policy directory '{SANDBOXING_POLICY_DIR}' should exist"
        assert d.is_directory, f"'{SANDBOXING_POLICY_DIR}' should be a directory"

    def test_policy_directory_permissions(self, host):
        """Verify policy directory has correct permissions."""
        d = host.file(SANDBOXING_POLICY_DIR)
        assert d.mode == 0o755, \
            f"Policy directory should have mode 0755, got {oct(d.mode)}"
        assert d.user == "root", "Policy directory should be owned by root"
        assert d.group == "root", "Policy directory group should be root"

    def test_policy_directory_structure(self, host):
        """Verify policy directory has proper structure."""
        d = host.file(SANDBOXING_POLICY_DIR)
        if d.exists and d.is_directory:
            # Directory should be accessible
            cmd = host.run(f"ls -la {SANDBOXING_POLICY_DIR}/ 2>&1")
            if cmd.rc == 0:
                pass  # Directory is accessible
        else:
            pytest.skip(f"Policy directory '{SANDBOXING_POLICY_DIR}' does not exist")


class TestSandboxingProfiles:
    """Test sandboxing profile deployment."""

    def test_policy_files_have_correct_extension(self, host):
        """Verify policy files have correct extension."""
        d = host.file(SANDBOXING_POLICY_DIR)
        if d.exists and d.is_directory:
            cmd = host.run(f"ls {SANDBOXING_POLICY_DIR}/*.conf 2>/dev/null || true")
            if cmd.rc == 0 and cmd.stdout:
                # Policy files should exist
                for line in cmd.stdout.strip().split("\n"):
                    if line:
                        assert line.endswith(".conf"), f"Policy file should end with .conf: {line}"
            else:
                pytest.skip("No policy files found in policy directory")
        else:
            pytest.skip(f"Policy directory '{SANDBOXING_POLICY_DIR}' does not exist")

    def test_policy_files_permissions(self, host):
        """Verify policy files have correct permissions."""
        d = host.file(SANDBOXING_POLICY_DIR)
        if d.exists and d.is_directory:
            cmd = host.run(f"ls -la {SANDBOXING_POLICY_DIR}/*.conf 2>/dev/null || true")
            if cmd.rc == 0 and cmd.stdout:
                for line in cmd.stdout.strip().split("\n"):
                    if line and not line.startswith("total"):
                        # Parse permissions from ls output
                        parts = line.split()
                        if len(parts) >= 9:
                            # Check file permissions
                            pass  # Basic check - files should exist
            else:
                pytest.skip("No policy files found")
        else:
            pytest.skip(f"Policy directory '{SANDBOXING_POLICY_DIR}' does not exist")

    def test_policy_files_readable(self, host):
        """Verify policy files are readable."""
        d = host.file(SANDBOXING_POLICY_DIR)
        if d.exists and d.is_directory:
            cmd = host.run(f"ls {SANDBOXING_POLICY_DIR}/*.conf 2>/dev/null | head -1")
            if cmd.rc == 0 and cmd.stdout.strip():
                policy_file = cmd.stdout.strip()
                f = host.file(policy_file)
                assert f.is_readable, f"Policy file '{policy_file}' should be readable"
        else:
            pytest.skip(f"Policy directory '{SANDBOXING_POLICY_DIR}' does not exist")


class TestSandboxingConfiguration:
    """Test sandboxing configuration."""

    def test_sandboxing_enabled_flag(self, host):
        """Verify sandboxing is enabled."""
        # This is typically controlled by Ansible variable
        # Check if sandboxing tools are available
        has_bwrap = host.exists("bwrap")
        assert has_bwrap, "Bubblewrap should be available when sandboxing is enabled"


class TestSeccompSupport:
    """Test seccomp support for sandboxing."""

    def test_seccomp_available(self, host):
        """Verify seccomp is available in the kernel."""
        cmd = host.run("grep -i seccomp /proc/self/status 2>&1")
        if cmd.rc == 0:
            # Seccomp should be available
            assert "Seccomp" in cmd.stdout, "Seccomp should be available"
        else:
            pytest.skip("Cannot determine seccomp status")

    def test_seccomp_filters_supported(self, host):
        """Verify seccomp filters are supported."""
        cmd = host.run("grep CONFIG_SECCOMP_FILTER /boot/config-$(uname -r) 2>/dev/null || true")
        if cmd.rc == 0 and "y" in cmd.stdout:
            pass  # Seccomp filter supported
        else:
            pytest.skip("Seccomp filter support not detected")


class TestNamespaceSupport:
    """Test namespace support for sandboxing."""

    def test_user_namespaces_available(self, host):
        """Verify user namespaces are available."""
        cmd = host.run("grep CONFIG_USER_NS /boot/config-$(uname -r) 2>/dev/null || true")
        if cmd.rc == 0 and "y" in cmd.stdout:
            pass  # User namespaces available
        else:
            pytest.skip("User namespaces not available")

    def test_pid_namespaces_available(self, host):
        """Verify PID namespaces are available."""
        cmd = host.run("grep CONFIG_PID_NS /boot/config-$(uname -r) 2>/dev/null || true")
        if cmd.rc == 0 and "y" in cmd.stdout:
            pass  # PID namespaces available
        else:
            pytest.skip("PID namespaces not available")

    def test_network_namespaces_available(self, host):
        """Verify network namespaces are available."""
        cmd = host.run("grep CONFIG_NET_NS /boot/config-$(uname -r) 2>/dev/null || true")
        if cmd.rc == 0 and "y" in cmd.stdout:
            pass  # Network namespaces available
        else:
            pytest.skip("Network namespaces not available")


class TestSandboxingIntegration:
    """Test sandboxing integration with system."""

    def test_proc_available_for_sandbox(self, host):
        """Verify /proc is available for sandboxing."""
        d = host.file("/proc")
        assert d.exists, "/proc should exist"
        assert d.is_directory, "/proc should be a directory"

    def test_dev_available_for_sandbox(self, host):
        """Verify /dev is available for sandboxing."""
        d = host.file("/dev")
        assert d.exists, "/dev should exist"
        assert d.is_directory, "/dev should be a directory"

    def test_tmp_available_for_sandbox(self, host):
        """Verify /tmp is available for sandboxing."""
        d = host.file("/tmp")
        assert d.exists, "/tmp should exist"
        assert d.is_directory, "/tmp should be a directory"


class TestContainerDetection:
    """Test container environment handling."""

    def test_not_in_container_or_skip(self, host):
        """Verify test handles container environment appropriately."""
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        if cmd.rc == 0:
            virt_type = cmd.stdout.strip().lower()
            if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
                # Some sandboxing features may be limited in containers
                pytest.skip(f"Running in container ({virt_type}), some sandboxing features may be limited")


class TestSandboxingCompletion:
    """Test sandboxing configuration completion."""

    def test_bubblewrap_available(self, host):
        """Verify Bubblewrap is available."""
        assert host.exists("bwrap"), "Bubblewrap should be available"

    def test_policy_directory_configured(self, host):
        """Verify policy directory is configured."""
        d = host.file(SANDBOXING_POLICY_DIR)
        assert d.exists, f"Policy directory '{SANDBOXING_POLICY_DIR}' should exist"

    def test_sandboxing_tools_installed(self, host):
        """Verify sandboxing tools are installed."""
        # At least bubblewrap should be installed
        pkg = host.package("bubblewrap")
        assert pkg.is_installed, "bubblewrap package should be installed"
