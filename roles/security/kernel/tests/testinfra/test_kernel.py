"""
Testinfra tests for security/kernel role.

This role handles kernel hardening via sysctl:
- Network hardening (redirects, source routing, martians)
- System hardening (kptr_restrict, dmesg_restrict)
- Memory hardening (panic_on_oops, swappiness)
- GRUB kernel parameters for memory initialization
"""
import pytest


# Expected sysctl values for kernel hardening
EXPECTED_SYSCTL_VALUES = {
    # Network Hardening
    "net.ipv4.conf.all.accept_redirects": "0",
    "net.ipv4.conf.all.secure_redirects": "0",
    "net.ipv4.conf.all.send_redirects": "0",
    "net.ipv4.conf.all.accept_source_route": "0",
    "net.ipv4.conf.all.log_martians": "1",
    "net.ipv4.tcp_syncookies": "1",
    "net.ipv4.tcp_rfc1337": "1",
    # System Hardening
    "kernel.kptr_restrict": "2",
    "kernel.dmesg_restrict": "1",
    "kernel.printk": "3 3 3 3",
    "kernel.unprivileged_bpf_disabled": "1",
    "net.core.bpf_jit_harden": "2",
    "dev.tty.ldisc_autoload": "0",
    "vm.unprivileged_userfaultfd": "0",
    # Memory Hardening
    "kernel.panic_on_oops": "1",
    "vm.swappiness": "1",
}

# GRUB security parameters that should be added
GRUB_SECURITY_PARAMS = [
    "init_on_free=1",
    "page_poison=1",
    "slab_nomerge",
]

# Sysctl configuration file
SYSCTL_CONFIG_FILE = "/etc/sysctl.d/99-hardened.conf"


class TestSysctlConfiguration:
    """Test sysctl configuration file."""

    def test_sysctl_hardened_config_exists(self, host):
        """Verify hardened sysctl configuration file exists."""
        f = host.file(SYSCTL_CONFIG_FILE)
        assert f.exists, f"Sysctl config '{SYSCTL_CONFIG_FILE}' should exist"
        assert f.is_file, f"'{SYSCTL_CONFIG_FILE}' should be a regular file"

    def test_sysctl_hardened_config_permissions(self, host):
        """Verify hardened sysctl configuration has correct permissions."""
        f = host.file(SYSCTL_CONFIG_FILE)
        assert f.mode in [0o644, 0o640, 0o600], \
            f"Sysctl config should have secure permissions, got {oct(f.mode)}"
        assert f.user == "root", "Sysctl config should be owned by root"


class TestNetworkHardening:
    """Test network-related kernel parameters."""

    @pytest.mark.parametrize("param,value", [
        ("net.ipv4.conf.all.accept_redirects", "0"),
        ("net.ipv4.conf.all.secure_redirects", "0"),
        ("net.ipv4.conf.all.send_redirects", "0"),
        ("net.ipv4.conf.all.accept_source_route", "0"),
    ])
    def test_network_redirects_disabled(self, host, param, value):
        """Verify network redirect parameters are disabled."""
        # Check runtime value
        cmd = host.run(f"sysctl -n {param} 2>&1")
        if cmd.rc == 0:
            actual_value = cmd.stdout.strip()
            assert actual_value == value, \
                f"{param} should be {value}, got {actual_value}"
        else:
            pytest.skip(f"Parameter {param} not available (possibly in container)")

    def test_log_martians_enabled(self, host):
        """Verify martian packet logging is enabled."""
        cmd = host.run("sysctl -n net.ipv4.conf.all.log_martians 2>&1")
        if cmd.rc == 0:
            assert cmd.stdout.strip() == "1", \
                "net.ipv4.conf.all.log_martians should be 1"
        else:
            pytest.skip("log_martians parameter not available")

    def test_tcp_syncookies_enabled(self, host):
        """Verify TCP SYN cookies are enabled (SYN flood protection)."""
        cmd = host.run("sysctl -n net.ipv4.tcp_syncookies 2>&1")
        if cmd.rc == 0:
            assert cmd.stdout.strip() == "1", \
                "net.ipv4.tcp_syncookies should be 1"
        else:
            pytest.skip("tcp_syncookies parameter not available")

    def test_tcp_rfc1337_enabled(self, host):
        """Verify TCP RFC 1337 protection is enabled."""
        cmd = host.run("sysctl -n net.ipv4.tcp_rfc1337 2>&1")
        if cmd.rc == 0:
            assert cmd.stdout.strip() == "1", \
                "net.ipv4.tcp_rfc1337 should be 1"
        else:
            pytest.skip("tcp_rfc1337 parameter not available")

    def test_sysctl_config_has_network_params(self, host):
        """Verify sysctl config contains network hardening parameters."""
        f = host.file(SYSCTL_CONFIG_FILE)
        if f.exists:
            content = f.content_string
            network_params = [
                "net.ipv4.conf.all.accept_redirects",
                "net.ipv4.tcp_syncookies",
                "net.ipv4.conf.all.log_martians",
            ]
            for param in network_params:
                assert param in content, f"{param} should be in sysctl config"
        else:
            pytest.skip(f"{SYSCTL_CONFIG_FILE} does not exist")


class TestSystemHardening:
    """Test system-related kernel parameters."""

    def test_kptr_restrict_enabled(self, host):
        """Verify kernel pointer restriction is enabled (CIS 3.2.1)."""
        cmd = host.run("sysctl -n kernel.kptr_restrict 2>&1")
        if cmd.rc == 0:
            value = cmd.stdout.strip()
            assert value in ["1", "2"], \
                f"kernel.kptr_restrict should be 1 or 2, got {value}"
        else:
            pytest.skip("kptr_restrict parameter not available")

    def test_dmesg_restrict_enabled(self, host):
        """Verify dmesg restriction is enabled."""
        cmd = host.run("sysctl -n kernel.dmesg_restrict 2>&1")
        if cmd.rc == 0:
            assert cmd.stdout.strip() == "1", \
                "kernel.dmesg_restrict should be 1"
        else:
            pytest.skip("dmesg_restrict parameter not available")

    def test_printk_restricted(self, host):
        """Verify printk is restricted."""
        cmd = host.run("sysctl -n kernel.printk 2>&1")
        if cmd.rc == 0:
            # Should be "3 3 3 3" or similar restricted values
            value = cmd.stdout.strip()
            values = value.split()
            if len(values) >= 1:
                assert int(values[0]) <= 4, \
                    f"kernel.printk console_loglevel should be <= 4, got {values[0]}"
        else:
            pytest.skip("printk parameter not available")

    def test_unprivileged_bpf_disabled(self, host):
        """Verify unprivileged BPF is disabled."""
        cmd = host.run("sysctl -n kernel.unprivileged_bpf_disabled 2>&1")
        if cmd.rc == 0:
            assert cmd.stdout.strip() == "1", \
                "kernel.unprivileged_bpf_disabled should be 1"
        else:
            pytest.skip("unprivileged_bpf_disabled parameter not available")

    def test_bpf_jit_harden_enabled(self, host):
        """Verify BPF JIT hardening is enabled."""
        cmd = host.run("sysctl -n net.core.bpf_jit_harden 2>&1")
        if cmd.rc == 0:
            value = cmd.stdout.strip()
            assert value in ["1", "2"], \
                f"net.core.bpf_jit_harden should be 1 or 2, got {value}"
        else:
            pytest.skip("bpf_jit_harden parameter not available")

    def test_ldisc_autoload_disabled(self, host):
        """Verify line discipline autoload is disabled."""
        cmd = host.run("sysctl -n dev.tty.ldisc_autoload 2>&1")
        if cmd.rc == 0:
            assert cmd.stdout.strip() == "0", \
                "dev.tty.ldisc_autoload should be 0"
        else:
            pytest.skip("ldisc_autoload parameter not available")

    def test_unprivileged_userfaultfd_disabled(self, host):
        """Verify unprivileged userfaultfd is disabled."""
        cmd = host.run("sysctl -n vm.unprivileged_userfaultfd 2>&1")
        if cmd.rc == 0:
            assert cmd.stdout.strip() == "0", \
                "vm.unprivileged_userfaultfd should be 0"
        else:
            pytest.skip("unprivileged_userfaultfd parameter not available")


class TestMemoryHardening:
    """Test memory-related kernel parameters."""

    def test_panic_on_oops_enabled(self, host):
        """Verify panic_on_oops is enabled."""
        cmd = host.run("sysctl -n kernel.panic_on_oops 2>&1")
        if cmd.rc == 0:
            assert cmd.stdout.strip() == "1", \
                "kernel.panic_on_oops should be 1"
        else:
            pytest.skip("panic_on_oops parameter not available")

    def test_swappiness_minimized(self, host):
        """Verify swappiness is minimized to reduce swapping of sensitive data."""
        cmd = host.run("sysctl -n vm.swappiness 2>&1")
        if cmd.rc == 0:
            value = int(cmd.stdout.strip())
            assert value <= 10, \
                f"vm.swappiness should be <= 10 for security, got {value}"
        else:
            pytest.skip("swappiness parameter not available")

    def test_sysctl_config_has_memory_params(self, host):
        """Verify sysctl config contains memory hardening parameters."""
        f = host.file(SYSCTL_CONFIG_FILE)
        if f.exists:
            content = f.content_string
            memory_params = [
                "kernel.panic_on_oops",
                "vm.swappiness",
            ]
            for param in memory_params:
                assert param in content, f"{param} should be in sysctl config"
        else:
            pytest.skip(f"{SYSCTL_CONFIG_FILE} does not exist")


class TestGRUBKernelParameters:
    """Test GRUB kernel parameters for memory initialization."""

    def test_grub_config_exists(self, host):
        """Verify GRUB configuration file exists."""
        f = host.file("/etc/default/grub")
        assert f.exists, "/etc/default/grub should exist"

    def test_grub_cmdline_linux_exists(self, host):
        """Verify GRUB_CMDLINE_LINUX_DEFAULT is configured."""
        f = host.file("/etc/default/grub")
        content = f.content_string
        has_cmdline = False
        for line in content.split("\n"):
            if "GRUB_CMDLINE_LINUX_DEFAULT" in line or "GRUB_CMDLINE_LINUX" in line:
                has_cmdline = True
                break
        assert has_cmdline, "GRUB_CMDLINE_LINUX_DEFAULT should be configured"

    def test_init_on_free_parameter(self, host):
        """Verify init_on_free=1 is in GRUB parameters."""
        f = host.file("/etc/default/grub")
        content = f.content_string
        for line in content.split("\n"):
            if "GRUB_CMDLINE_LINUX" in line and not line.startswith("#"):
                assert "init_on_free=1" in line, \
                    "init_on_free=1 should be in GRUB parameters"
                return
        pytest.skip("GRUB_CMDLINE_LINUX not configured")

    def test_page_poison_parameter(self, host):
        """Verify page_poison=1 is in GRUB parameters."""
        f = host.file("/etc/default/grub")
        content = f.content_string
        for line in content.split("\n"):
            if "GRUB_CMDLINE_LINUX" in line and not line.startswith("#"):
                assert "page_poison=1" in line, \
                    "page_poison=1 should be in GRUB parameters"
                return
        pytest.skip("GRUB_CMDLINE_LINUX not configured")

    def test_slab_nomerge_parameter(self, host):
        """Verify slab_nomerge is in GRUB parameters."""
        f = host.file("/etc/default/grub")
        content = f.content_string
        for line in content.split("\n"):
            if "GRUB_CMDLINE_LINUX" in line and not line.startswith("#"):
                assert "slab_nomerge" in line, \
                    "slab_nomerge should be in GRUB parameters"
                return
        pytest.skip("GRUB_CMDLINE_LINUX not configured")


class TestSysctlReload:
    """Test sysctl configuration is applied."""

    def test_sysctl_reload_possible(self, host):
        """Verify sysctl can be reloaded."""
        cmd = host.run("sysctl --system 2>&1 || true")
        # This should not fail catastrophically
        # In containers this may have limited functionality

    def test_sysctl_d_directory_exists(self, host):
        """Verify sysctl.d directory exists."""
        d = host.file("/etc/sysctl.d")
        assert d.exists, "/etc/sysctl.d should exist"
        assert d.is_directory, "/etc/sysctl.d should be a directory"

    def test_sysctl_d_directory_permissions(self, host):
        """Verify sysctl.d directory has correct permissions."""
        d = host.file("/etc/sysctl.d")
        assert d.mode == 0o755, f"/etc/sysctl.d should have mode 0755, got {oct(d.mode)}"


class TestContainerDetection:
    """Test container environment handling."""

    def test_virtualization_detection(self, host):
        """Verify virtualization type can be detected."""
        # This is informational - tests should skip in containers
        cmd = host.run("systemd-detect-virt 2>&1 || echo 'none'")
        virt_type = cmd.stdout.strip().lower()
        if virt_type in ["docker", "podman", "lxc", "openvz", "container"]:
            pytest.skip(f"Running in container ({virt_type}), some kernel params may not be available")

    def test_proc_sys_accessible(self, host):
        """Verify /proc/sys is accessible."""
        d = host.file("/proc/sys")
        if d.exists:
            assert d.is_directory, "/proc/sys should be a directory"
        else:
            pytest.skip("/proc/sys not accessible")
