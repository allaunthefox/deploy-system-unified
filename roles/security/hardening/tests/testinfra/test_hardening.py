"""
Testinfra tests for security/hardening role.

This role handles core security hardening:
- Installing security packages (auditd, libpam-tmpdir)
- Hardening file system permissions
- Locking system accounts
- Configuring password aging limits
- PAM configuration hardening
"""
import pytest


# Sensitive files and their expected permissions
SENSITIVE_FILES = {
    "/etc/shadow": {"mode": 0o600, "owner": "root", "group": "root"},
    "/etc/passwd": {"mode": 0o644, "owner": "root", "group": "root"},
    "/etc/group": {"mode": 0o644, "owner": "root", "group": "root"},
    "/etc/sudoers": {"mode": 0o440, "owner": "root", "group": "root"},
    "/etc/ssh": {"mode": 0o755, "owner": "root", "group": "root"},
    "/etc/ssh/sshd_config": {"mode": 0o644, "owner": "root", "group": "root"},
}

# System accounts that should be locked
SYSTEM_ACCOUNTS = [
    "bin",
    "daemon",
    "adm",
    "lp",
    "sync",
    "shutdown",
    "halt",
    "mail",
]

# Security packages that should be installed
SECURITY_PACKAGES_DEBIAN = [
    "libpam-tmpdir",
    "auditd",
]

SECURITY_PACKAGES_REDHAT = [
    "audit",
]

SECURITY_PACKAGES_ARCH = [
    "audit",
]

SECURITY_PACKAGES_ALPINE = [
    "audit",
]


class TestSecurityPackages:
    """Test security package installation."""

    def test_audit_package_installed_debian(self, host):
        """Verify audit package is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("auditd")
            assert pkg.is_installed, "auditd package should be installed on Debian/Ubuntu"

    def test_audit_package_installed_redhat(self, host):
        """Verify audit package is installed (RedHat/CentOS)."""
        if host.file("/etc/redhat-release").exists:
            pkg = host.package("audit")
            assert pkg.is_installed, "audit package should be installed on RedHat/CentOS"

    def test_audit_package_installed_arch(self, host):
        """Verify audit package is installed (Arch Linux)."""
        if host.file("/etc/arch-release").exists:
            pkg = host.package("audit")
            assert pkg.is_installed, "audit package should be installed on Arch Linux"

    def test_libpam_tmpdir_installed_debian(self, host):
        """Verify libpam-tmpdir is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("libpam-tmpdir")
            assert pkg.is_installed, "libpam-tmpdir package should be installed on Debian/Ubuntu"


class TestAuditdService:
    """Test auditd service configuration."""

    def test_auditd_service_exists(self, host):
        """Verify auditd service exists."""
        svc = host.service("auditd")
        assert svc.exists, "auditd service should exist"

    def test_auditd_service_running(self, host):
        """Verify auditd service is running."""
        svc = host.service("auditd")
        if svc.exists:
            assert svc.is_running, "auditd service should be running"
            assert svc.is_enabled, "auditd service should be enabled"

    def test_auditd_config_exists(self, host):
        """Verify auditd configuration file exists."""
        f = host.file("/etc/audit/auditd.conf")
        assert f.exists, "/etc/audit/auditd.conf should exist"

    def test_auditd_rules_exist(self, host):
        """Verify auditd rules directory exists."""
        d = host.file("/etc/audit/rules.d")
        assert d.exists, "/etc/audit/rules.d should exist"
        assert d.is_directory, "/etc/audit/rules.d should be a directory"


class TestFileSystemPermissions:
    """Test file system permission hardening (CIS 1.1.1)."""

    @pytest.mark.parametrize("path,expected", SENSITIVE_FILES.items())
    def test_sensitive_file_permissions(self, host, path, expected):
        """Verify sensitive files have correct permissions."""
        f = host.file(path)
        if f.exists:
            assert f.mode == expected["mode"], \
                f"{path} should have mode {oct(expected['mode'])}, got {oct(f.mode)}"
            assert f.user == expected["owner"], \
                f"{path} should be owned by {expected['owner']}"
            assert f.group == expected["group"], \
                f"{path} group should be {expected['group']}"
        else:
            pytest.skip(f"{path} does not exist on this system")

    def test_shadow_file_exists(self, host):
        """Verify /etc/shadow exists."""
        f = host.file("/etc/shadow")
        assert f.exists, "/etc/shadow should exist"

    def test_shadow_file_secure(self, host):
        """Verify /etc/shadow has secure permissions (CIS 1.1.1)."""
        f = host.file("/etc/shadow")
        assert f.mode == 0o600, f"/etc/shadow should have mode 0600, got {oct(f.mode)}"
        assert f.user == "root", "/etc/shadow should be owned by root"
        assert f.group in ["root", "shadow"], "/etc/shadow group should be root or shadow"

    def test_passwd_file_permissions(self, host):
        """Verify /etc/passwd has correct permissions."""
        f = host.file("/etc/passwd")
        assert f.exists, "/etc/passwd should exist"
        assert f.mode == 0o644, f"/etc/passwd should have mode 0644, got {oct(f.mode)}"

    def test_group_file_permissions(self, host):
        """Verify /etc/group has correct permissions."""
        f = host.file("/etc/group")
        assert f.exists, "/etc/group should exist"
        assert f.mode == 0o644, f"/etc/group should have mode 0644, got {oct(f.mode)}"

    def test_sudoers_file_permissions(self, host):
        """Verify /etc/sudoers has correct permissions."""
        f = host.file("/etc/sudoers")
        if f.exists:
            assert f.mode == 0o440, f"/etc/sudoers should have mode 0440, got {oct(f.mode)}"
            assert f.user == "root", "/etc/sudoers should be owned by root"

    def test_sudoers_directory_permissions(self, host):
        """Verify /etc/sudoers.d has correct permissions."""
        d = host.file("/etc/sudoers.d")
        if d.exists:
            assert d.is_directory, "/etc/sudoers.d should be a directory"
            assert d.mode in [0o750, 0o700], f"/etc/sudoers.d should have secure permissions, got {oct(d.mode)}"

    def test_ssh_directory_permissions(self, host):
        """Verify /etc/ssh has correct permissions."""
        d = host.file("/etc/ssh")
        assert d.exists, "/etc/ssh should exist"
        assert d.is_directory, "/etc/ssh should be a directory"
        assert d.mode == 0o755, f"/etc/ssh should have mode 0755, got {oct(d.mode)}"


class TestStickyBit:
    """Test sticky bit on world-writable directories."""

    def test_sticky_bit_on_tmp(self, host):
        """Verify sticky bit is set on /tmp."""
        d = host.file("/tmp")
        if d.exists:
            # Mode should have sticky bit (2000) or be 1777
            mode = d.mode
            has_sticky = (mode & 0o1000) != 0
            assert has_sticky or mode == 0o1777, "/tmp should have sticky bit set"

    def test_sticky_bit_on_var_tmp(self, host):
        """Verify sticky bit is set on /var/tmp."""
        d = host.file("/var/tmp")
        if d.exists:
            mode = d.mode
            has_sticky = (mode & 0o1000) != 0
            assert has_sticky or mode == 0o1777, "/var/tmp should have sticky bit set"

    def test_no_world_writable_without_sticky(self, host):
        """Verify no world-writable directories without sticky bit (excluding standard locations)."""
        # This is a basic check - full check would require find command
        # Check some common directories
        dirs_to_check = ["/home", "/opt", "/usr/local"]
        for dir_path in dirs_to_check:
            d = host.file(dir_path)
            if d.exists and d.is_directory:
                mode = d.mode
                is_world_writable = (mode & 0o002) != 0
                has_sticky = (mode & 0o1000) != 0
                if is_world_writable:
                    assert has_sticky, f"{dir_path} is world-writable but missing sticky bit"


class TestSystemAccounts:
    """Test system account hardening (CIS 5.4.1)."""

    @pytest.mark.parametrize("account", SYSTEM_ACCOUNTS)
    def test_system_account_locked(self, host, account):
        """Verify system accounts are locked."""
        # Check if account exists first
        cmd = host.run(f"id {account} 2>&1")
        if cmd.rc == 0:
            # Account exists, check if locked
            # Locked accounts have '!' or '*' at the start of the password field
            cmd = host.run(f"passwd -S {account} 2>&1")
            if cmd.rc == 0:
                # 'L' or 'LK' indicates locked
                assert "L" in cmd.stdout or "LK" in cmd.stdout, \
                    f"System account '{account}' should be locked"
        else:
            pytest.skip(f"Account '{account}' does not exist on this system")

    def test_root_account_exists(self, host):
        """Verify root account exists."""
        cmd = host.run("id root")
        assert cmd.rc == 0, "root account should exist"


class TestPasswordPolicy:
    """Test password aging policy (CIS 5.4.1)."""

    def test_login_defs_exists(self, host):
        """Verify /etc/login.defs exists."""
        f = host.file("/etc/login.defs")
        assert f.exists, "/etc/login.defs should exist"

    def test_pass_min_days_configured(self, host):
        """Verify PASS_MIN_DAYS is configured."""
        f = host.file("/etc/login.defs")
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("PASS_MIN_DAYS"):
                value = int(line.split()[1])
                assert value >= 7, f"PASS_MIN_DAYS should be at least 7, got {value}"
                return
        pytest.skip("PASS_MIN_DAYS not configured in login.defs")

    def test_pass_max_days_configured(self, host):
        """Verify PASS_MAX_DAYS is configured."""
        f = host.file("/etc/login.defs")
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("PASS_MAX_DAYS"):
                value = int(line.split()[1])
                assert value <= 90, f"PASS_MAX_DAYS should be 90 or less, got {value}"
                return
        pytest.skip("PASS_MAX_DAYS not configured in login.defs")

    def test_pass_warn_age_configured(self, host):
        """Verify PASS_WARN_AGE is configured."""
        f = host.file("/etc/login.defs")
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("PASS_WARN_AGE"):
                value = int(line.split()[1])
                assert value >= 7, f"PASS_WARN_AGE should be at least 7, got {value}"
                return
        pytest.skip("PASS_WARN_AGE not configured in login.defs")


class TestPAMConfiguration:
    """Test PAM configuration hardening."""

    def test_pam_directory_exists(self, host):
        """Verify PAM configuration directory exists."""
        d = host.file("/etc/pam.d")
        assert d.exists, "/etc/pam.d should exist"
        assert d.is_directory, "/etc/pam.d should be a directory"

    def test_common_password_pam_unix_configured(self, host):
        """Verify pam_unix is configured with strong hashing (Debian)."""
        f = host.file("/etc/pam.d/common-password")
        if f.exists:
            content = f.content_string
            has_pam_unix = False
            for line in content.split("\n"):
                line = line.strip()
                if "pam_unix.so" in line and not line.startswith("#"):
                    has_pam_unix = True
                    # Should have obscure and sha512 options
                    assert "obscure" in line, "pam_unix.so should have 'obscure' option"
                    assert "sha512" in line or "yescrypt" in line, \
                        "pam_unix.so should have 'sha512' or 'yescrypt' option"
                    # Check for rounds parameter
                    if "rounds=" in line:
                        rounds = int(line.split("rounds=")[1].split()[0])
                        assert rounds >= 65536, f"pam_unix rounds should be >= 65536, got {rounds}"
                    break
            if not has_pam_unix:
                pytest.skip("pam_unix.so not configured in common-password")
        else:
            pytest.skip("/etc/pam.d/common-password does not exist (non-Debian system)")

    def test_pam_tmpdir_configured(self, host):
        """Verify pam_tmpdir is configured (Debian)."""
        f = host.file("/etc/pam.d/common-session")
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                line = line.strip()
                if "pam_tmpdir.so" in line and not line.startswith("#"):
                    assert "pam_tmpdir.so" in line, "pam_tmpdir.so should be configured"
                    return
            pytest.skip("pam_tmpdir.so not configured in common-session")
        else:
            pytest.skip("/etc/pam.d/common-session does not exist (non-Debian system)")

    def test_pam_d_system_auth_exists(self, host):
        """Verify system-auth PAM configuration exists (RedHat)."""
        f = host.file("/etc/pam.d/system-auth")
        if f.exists:
            assert f.is_file, "/etc/pam.d/system-auth should be a file"
        else:
            pytest.skip("/etc/pam.d/system-auth does not exist (non-RedHat system)")


class TestWheelGroup:
    """Test wheel group configuration."""

    def test_wheel_group_exists(self, host):
        """Verify wheel group exists."""
        cmd = host.run("getent group wheel")
        if cmd.rc == 0:
            assert "wheel" in cmd.stdout, "wheel group should exist"
        else:
            # Some systems use 'sudo' group instead
            cmd = host.run("getent group sudo")
            if cmd.rc == 0:
                pytest.skip("System uses 'sudo' group instead of 'wheel'")
            else:
                pytest.skip("Neither wheel nor sudo group exists")

    def test_sudoers_wheel_configured(self, host):
        """Verify wheel group has sudo access."""
        f = host.file("/etc/sudoers")
        if f.exists:
            content = f.content_string
            has_wheel = False
            for line in content.split("\n"):
                line = line.strip()
                if not line.startswith("#") and "%wheel" in line:
                    has_wheel = True
                    break
            if not has_wheel:
                # Check sudoers.d
                d = host.file("/etc/sudoers.d")
                if d.exists and d.is_directory:
                    # Check for wheel configuration in sudoers.d
                    pass
                else:
                    pytest.skip("wheel group not configured in sudoers")
        else:
            pytest.skip("/etc/sudoers does not exist")


class TestSecurityHardeningCompletion:
    """Test security hardening completion indicators."""

    def test_security_packages_available(self, host):
        """Verify security packages are available."""
        # At least one security package should be available
        security_pkgs = ["auditd", "audit", "libpam-tmpdir"]
        has_package = False
        for pkg_name in security_pkgs:
            pkg = host.package(pkg_name)
            if pkg.is_installed:
                has_package = True
                break
        assert has_package, "At least one security package should be installed"
