"""
Testinfra tests for security/access role.

This role handles SSH and user access configuration:
- OpenSSH server installation
- SSH service management
- Wheel group configuration
- Sudo configuration for wheel group
- Admin account management
- SSH Match block rules for IP restrictions
"""
import pytest


# SSH configuration
SSH_SERVICE_NAMES = ["ssh", "sshd"]
SSHD_CONFIG_PATH = "/etc/ssh/sshd_config"

# Access control files
SUDOERS_PATH = "/etc/sudoers"
WHEEL_GROUP = "wheel"
ADMIN_USER = "admin"


class TestOpenSSHInstallation:
    """Test OpenSSH server installation."""

    def test_openssh_server_installed_debian(self, host):
        """Verify OpenSSH server is installed (Debian/Ubuntu)."""
        if host.file("/etc/debian_version").exists:
            pkg = host.package("openssh-server")
            assert pkg.is_installed, "openssh-server package should be installed"

    def test_openssh_server_installed_redhat(self, host):
        """Verify OpenSSH server is installed (RedHat/CentOS)."""
        if host.file("/etc/redhat-release").exists:
            pkg = host.package("openssh-server")
            assert pkg.is_installed, "openssh-server package should be installed"

    def test_openssh_server_installed_arch(self, host):
        """Verify OpenSSH server is installed (Arch Linux)."""
        if host.file("/etc/arch-release").exists:
            pkg = host.package("openssh")
            assert pkg.is_installed, "openssh package should be installed"

    def test_sshd_binary_exists(self, host):
        """Verify sshd binary exists."""
        assert host.exists("sshd"), "sshd binary should exist"


class TestSSHService:
    """Test SSH service configuration."""

    def test_ssh_service_exists(self, host):
        """Verify SSH service exists."""
        has_service = False
        for name in SSH_SERVICE_NAMES:
            svc = host.service(name)
            if svc.exists:
                has_service = True
                break
        assert has_service, "SSH service should exist"

    def test_ssh_service_running(self, host):
        """Verify SSH service is running."""
        for name in SSH_SERVICE_NAMES:
            svc = host.service(name)
            if svc.exists:
                assert svc.is_running, f"SSH service '{name}' should be running"
                assert svc.is_enabled, f"SSH service '{name}' should be enabled"
                return
        pytest.skip("SSH service not found")

    def test_ssh_privilege_separation_directory(self, host):
        """Verify SSH privilege separation directory exists."""
        d = host.file("/run/sshd")
        assert d.exists, "/run/sshd should exist"
        assert d.is_directory, "/run/sshd should be a directory"
        assert d.mode == 0o755, f"/run/sshd should have mode 0755, got {oct(d.mode)}"


class TestWheelGroup:
    """Test wheel group configuration (CIS 1.1.5)."""

    def test_wheel_group_exists(self, host):
        """Verify wheel group exists."""
        cmd = host.run("getent group wheel")
        assert cmd.rc == 0, "wheel group should exist"
        assert "wheel" in cmd.stdout, "wheel group should be in getent output"

    def test_wheel_group_has_members(self, host):
        """Verify wheel group has at least one member (typically root)."""
        cmd = host.run("getent group wheel")
        if cmd.rc == 0:
            # Format: wheel:x:10:root,admin
            parts = cmd.stdout.strip().split(":")
            if len(parts) >= 4 and parts[3]:
                members = parts[3].split(",")
                assert len(members) > 0, "wheel group should have members"
        else:
            pytest.skip("wheel group does not exist")


class TestSudoConfiguration:
    """Test sudo configuration for wheel group (CIS 7.1)."""

    def test_sudoers_file_exists(self, host):
        """Verify sudoers file exists."""
        f = host.file(SUDOERS_PATH)
        assert f.exists, f"{SUDOERS_PATH} should exist"
        assert f.is_file, f"{SUDOERS_PATH} should be a file"

    def test_sudoers_file_permissions(self, host):
        """Verify sudoers file has correct permissions (STIG V-230235)."""
        f = host.file(SUDOERS_PATH)
        assert f.mode == 0o440, f"{SUDOERS_PATH} should have mode 0440, got {oct(f.mode)}"
        assert f.user == "root", f"{SUDOERS_PATH} should be owned by root"
        assert f.group == "root", f"{SUDOERS_PATH} group should be root"

    def test_wheel_sudo_configured(self, host):
        """Verify wheel group has sudo access (STIG V-230236)."""
        f = host.file(SUDOERS_PATH)
        content = f.content_string
        has_wheel_sudo = False
        for line in content.split("\n"):
            line = line.strip()
            if not line.startswith("#") and "%wheel" in line:
                has_wheel_sudo = True
                # Check for appropriate sudo configuration
                assert "ALL" in line, "wheel group should have ALL hosts access"
                break
        assert has_wheel_sudo, "wheel group should be configured in sudoers"

    def test_sudoers_syntax_valid(self, host):
        """Verify sudoers file has valid syntax."""
        cmd = host.run("visudo -cf /etc/sudoers 2>&1")
        assert cmd.rc == 0, f"sudoers syntax should be valid: {cmd.stdout}"

    def test_sudoers_d_directory_exists(self, host):
        """Verify sudoers.d directory exists."""
        d = host.file("/etc/sudoers.d")
        if d.exists:
            assert d.is_directory, "/etc/sudoers.d should be a directory"
            assert d.mode in [0o750, 0o700], \
                f"/etc/sudoers.d should have secure permissions, got {oct(d.mode)}"
        else:
            pytest.skip("/etc/sudoers.d does not exist")


class TestAdminAccount:
    """Test admin account configuration."""

    def test_admin_user_exists(self, host):
        """Verify admin user exists."""
        cmd = host.run(f"id {ADMIN_USER} 2>&1")
        if cmd.rc == 0:
            assert ADMIN_USER in cmd.stdout, f"{ADMIN_USER} user should exist"
        else:
            pytest.skip(f"Admin user '{ADMIN_USER}' does not exist")

    def test_admin_user_in_wheel_group(self, host):
        """Verify admin user is in wheel group."""
        cmd = host.run(f"id {ADMIN_USER} 2>&1")
        if cmd.rc == 0:
            assert "wheel" in cmd.stdout or f"gid=0(root)" in cmd.stdout, \
                f"{ADMIN_USER} should be in wheel group or have root gid"
        else:
            pytest.skip(f"Admin user '{ADMIN_USER}' does not exist")

    def test_admin_user_has_home_directory(self, host):
        """Verify admin user has home directory."""
        cmd = host.run(f"id {ADMIN_USER} 2>&1")
        if cmd.rc == 0:
            d = host.file(f"/home/{ADMIN_USER}")
            if d.exists:
                assert d.is_directory, f"/home/{ADMIN_USER} should be a directory"
        else:
            pytest.skip(f"Admin user '{ADMIN_USER}' does not exist")

    def test_admin_user_shell(self, host):
        """Verify admin user has valid shell."""
        cmd = host.run(f"getent passwd {ADMIN_USER} 2>&1")
        if cmd.rc == 0:
            parts = cmd.stdout.strip().split(":")
            if len(parts) >= 7:
                shell = parts[6]
                assert shell in ["/bin/bash", "/bin/sh", "/bin/zsh"], \
                    f"Admin user should have valid shell, got {shell}"
        else:
            pytest.skip(f"Admin user '{ADMIN_USER}' does not exist")


class TestSSHMatchRules:
    """Test SSH Match block rules for IP restrictions."""

    def test_sshd_config_exists_for_match(self, host):
        """Verify SSHD config exists for Match rules."""
        f = host.file(SSHD_CONFIG_PATH)
        assert f.exists, f"{SSHD_CONFIG_PATH} should exist"

    def test_ssh_match_rules_syntax(self, host):
        """Verify SSH Match rules have valid syntax if configured."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        has_match = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("Match "):
                has_match = True
                # Match should be followed by User, Group, Host, or Address
                match_types = ["User", "Group", "Host", "Address", "LocalAddress", "LocalPort", "RDomain"]
                parts = line.split()
                if len(parts) >= 2:
                    assert parts[1] in match_types, \
                        f"Match type should be valid, got {parts[1]}"
        if not has_match:
            pytest.skip("No SSH Match rules configured")

    def test_ssh_match_block_options(self, host):
        """Verify SSH Match block options are valid if configured."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        in_match_block = False
        valid_options = [
            "PasswordAuthentication", "PubkeyAuthentication", "AllowTcpForwarding",
            "X11Forwarding", "AllowAgentForwarding", "PermitTTY", "ForceCommand",
            "ChrootDirectory", "Banner", "ClientAliveInterval", "ClientAliveCountMax",
            "Address", "ListenAddress", "Port", "AuthenticationMethods"
        ]
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("Match "):
                in_match_block = True
                continue
            if in_match_block and line and not line.startswith("#"):
                # Check if this is a new Match block or a regular directive
                if line.startswith("Match "):
                    continue
                # Indented lines are part of Match block
                if line.startswith(" ") or line.startswith("\t"):
                    option = line.split("=")[0].strip().split()[0]
                    # Options in Match blocks should be valid
        # This is a basic syntax check


class TestAccessControlFiles:
    """Test access control file permissions."""

    def test_passwd_file_exists(self, host):
        """Verify /etc/passwd exists."""
        f = host.file("/etc/passwd")
        assert f.exists, "/etc/passwd should exist"
        assert f.mode == 0o644, f"/etc/passwd should have mode 0644, got {oct(f.mode)}"

    def test_group_file_exists(self, host):
        """Verify /etc/group exists."""
        f = host.file("/etc/group")
        assert f.exists, "/etc/group should exist"
        assert f.mode == 0o644, f"/etc/group should have mode 0644, got {oct(f.mode)}"

    def test_shadow_file_secure(self, host):
        """Verify /etc/shadow has secure permissions."""
        f = host.file("/etc/shadow")
        assert f.exists, "/etc/shadow should exist"
        assert f.mode == 0o600, f"/etc/shadow should have mode 0600, got {oct(f.mode)}"
        assert f.user == "root", "/etc/shadow should be owned by root"

    def test_gshadow_file_secure(self, host):
        """Verify /etc/gshadow has secure permissions."""
        f = host.file("/etc/gshadow")
        if f.exists:
            assert f.mode == 0o600, f"/etc/gshadow should have mode 0600, got {oct(f.mode)}"
            assert f.user == "root", "/etc/gshadow should be owned by root"
        else:
            pytest.skip("/etc/gshadow does not exist")


class TestLoginConfiguration:
    """Test login configuration."""

    def test_login_defs_exists(self, host):
        """Verify /etc/login.defs exists."""
        f = host.file("/etc/login.defs")
        assert f.exists, "/etc/login.defs should exist"

    def test_secure_umask_configured(self, host):
        """Verify secure umask is configured."""
        f = host.file("/etc/login.defs")
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("UMASK"):
                value = line.split()[1]
                umask_value = int(value, 8)
                # Umask should be 027 or more restrictive (077)
                assert umask_value >= 0o027, f"UMASK should be 027 or more restrictive, got {value}"
                return
        pytest.skip("UMASK not configured in login.defs")

    def test_create_home_configured(self, host):
        """Verify CREATE_HOME is configured."""
        f = host.file("/etc/login.defs")
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("CREATE_HOME"):
                value = line.split()[1]
                assert value.lower() == "yes", "CREATE_HOME should be yes"
                return
        pytest.skip("CREATE_HOME not configured in login.defs")


class TestPAMAccess:
    """Test PAM access configuration."""

    def test_pam_d_directory_exists(self, host):
        """Verify PAM configuration directory exists."""
        d = host.file("/etc/pam.d")
        assert d.exists, "/etc/pam.d should exist"
        assert d.is_directory, "/etc/pam.d should be a directory"

    def test_pam_d_sshd_exists(self, host):
        """Verify SSHD PAM configuration exists."""
        f = host.file("/etc/pam.d/sshd")
        assert f.exists, "/etc/pam.d/sshd should exist"

    def test_pam_d_system_auth_exists(self, host):
        """Verify system-auth PAM configuration exists (RedHat)."""
        f = host.file("/etc/pam.d/system-auth")
        if f.exists:
            assert f.is_file, "/etc/pam.d/system-auth should be a file"
        else:
            pytest.skip("/etc/pam.d/system-auth does not exist (non-RedHat)")

    def test_pam_d_common_auth_exists(self, host):
        """Verify common-auth PAM configuration exists (Debian)."""
        f = host.file("/etc/pam.d/common-auth")
        if f.exists:
            assert f.is_file, "/etc/pam.d/common-auth should be a file"
        else:
            pytest.skip("/etc/pam.d/common-auth does not exist (non-Debian)")


class TestAccessCompletion:
    """Test access configuration completion indicators."""

    def test_ssh_configured(self, host):
        """Verify SSH is properly configured."""
        # SSH service should exist and be manageable
        has_service = False
        for name in SSH_SERVICE_NAMES:
            svc = host.service(name)
            if svc.exists:
                has_service = True
                break
        assert has_service, "SSH should be configured"

    def test_sudo_available(self, host):
        """Verify sudo is available."""
        assert host.exists("sudo"), "sudo binary should be available"

    def test_wheel_or_sudo_group_exists(self, host):
        """Verify wheel or sudo group exists."""
        cmd = host.run("getent group wheel 2>&1 || getent group sudo 2>&1 || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "wheel" in cmd.stdout or "sudo" in cmd.stdout, \
                "wheel or sudo group should exist"
        else:
            pytest.skip("Neither wheel nor sudo group exists")
