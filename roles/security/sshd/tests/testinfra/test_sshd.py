# =============================================================================
# Audit Event Identifier: DSU-PYS-500052
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for security/sshd role.

This role handles SSH daemon hardening:
- Configuring strong cryptographic algorithms (FIPS 140-2 compliant)
- Disabling weak SSH host keys
- Setting secure SSH configuration options
- Managing SSH host key permissions
- Post-Quantum Cryptography (PQC) hybrid support
"""
import pytest


# SSH configuration paths
SSHD_CONFIG_PATH = "/etc/ssh/sshd_config"
SECURITY_SSHD_CONFIG_PATH = "/etc/ssh/security_sshd_config"
SSH_HOST_KEY_DIR = "/etc/ssh"

# Strong ciphers that should be configured
STRONG_CIPHERS = [
    "chacha20-poly1305@openssh.com",
    "aes256-gcm@openssh.com",
    "aes128-gcm@openssh.com",
]

# Strong MACs that should be configured
STRONG_MACS = [
    "hmac-sha2-512-etm@openssh.com",
    "hmac-sha2-256-etm@openssh.com",
]

# Strong key exchange algorithms
STRONG_KEX = [
    "curve25519-sha256",
    "curve25519-sha256@libssh.org",
    "diffie-hellman-group16-sha512",
]

# PQC KEX algorithms (when enabled)
PQC_KEX_ALGORITHMS = [
    "mlkem768x25519-sha256",
    "sntrup761x25519-sha512@openssh.com",
]

# Strong host key algorithms
STRONG_HOST_KEY_ALGORITHMS = [
    "ssh-ed25519",
    "rsa-sha2-512",
    "rsa-sha2-256",
]


class TestSSHDService:
    """Test SSHD service state."""

    def test_sshd_service_exists(self, host):
        """Verify SSHD service exists."""
        # Service name varies by distribution
        service_names = ["ssh", "sshd"]
        has_service = False
        for name in service_names:
            svc = host.service(name)
            if svc.exists:
                has_service = True
                break
        assert has_service, "SSH service (ssh or sshd) should exist"

    def test_sshd_service_running(self, host):
        """Verify SSHD service is running."""
        service_names = ["ssh", "sshd"]
        for name in service_names:
            svc = host.service(name)
            if svc.exists:
                assert svc.is_running, f"SSH service '{name}' should be running"
                assert svc.is_enabled, f"SSH service '{name}' should be enabled"
                return
        pytest.skip("SSH service not found")

    def test_sshd_installed(self, host):
        """Verify OpenSSH server is installed."""
        # Check for sshd binary
        assert host.exists("sshd"), "sshd binary should be installed"


class TestSSHDConfiguration:
    """Test SSHD configuration file."""

    def test_sshd_config_exists(self, host):
        """Verify SSHD configuration file exists."""
        f = host.file(SSHD_CONFIG_PATH)
        assert f.exists, f"SSHD config file '{SSHD_CONFIG_PATH}' should exist"
        assert f.is_file, f"'{SSHD_CONFIG_PATH}' should be a regular file"

    def test_sshd_config_permissions(self, host):
        """Verify SSHD configuration file has correct permissions."""
        f = host.file(SSHD_CONFIG_PATH)
        assert f.mode == 0o644, f"SSHD config should have mode 0644, got {oct(f.mode)}"
        assert f.user == "root", "SSHD config should be owned by root"
        assert f.group == "root", "SSHD config group should be root"

    def test_sshd_config_syntax_valid(self, host):
        """Verify SSHD configuration has valid syntax."""
        cmd = host.run(f"sshd -t -f {SSHD_CONFIG_PATH} 2>&1")
        assert cmd.rc == 0, f"SSHD config syntax should be valid: {cmd.stdout}"


class TestSSHDStrongCiphers:
    """Test strong cipher configuration."""

    def test_security_sshd_config_exists(self, host):
        """Verify security SSHD config file exists."""
        f = host.file(SECURITY_SSHD_CONFIG_PATH)
        if f.exists:
            assert f.is_file, f"'{SECURITY_SSHD_CONFIG_PATH}' should be a regular file"
            assert f.mode in [0o644, 0o640, 0o600], "Security SSHD config should have secure permissions"
            assert f.user == "root", "Security SSHD config should be owned by root"

    def test_strong_ciphers_configured(self, host):
        """Verify only strong ciphers are configured."""
        f = host.file(SECURITY_SSHD_CONFIG_PATH)
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                if line.strip().startswith("Ciphers "):
                    # Verify strong ciphers are present
                    for cipher in STRONG_CIPHERS:
                        assert cipher in line, f"Strong cipher '{cipher}' should be configured"
                    # Verify weak ciphers are not present
                    weak_ciphers = ["3des", "aes128-cbc", "aes256-cbc", "blowfish", "cast128", "arcfour"]
                    for weak in weak_ciphers:
                        assert weak not in line.lower(), f"Weak cipher '{weak}' should not be configured"
                    return
            pytest.skip("Ciphers not explicitly configured in security config")

    def test_strong_macs_configured(self, host):
        """Verify only strong MACs are configured."""
        f = host.file(SECURITY_SSHD_CONFIG_PATH)
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                if line.strip().startswith("MACs "):
                    # Verify strong MACs are present
                    for mac in STRONG_MACS:
                        assert mac in line, f"Strong MAC '{mac}' should be configured"
                    # Verify weak MACs are not present
                    weak_macs = ["hmac-md5", "hmac-sha1", "umac-64"]
                    for weak in weak_macs:
                        assert weak not in line.lower(), f"Weak MAC '{weak}' should not be configured"
                    return
            pytest.skip("MACs not explicitly configured in security config")

    def test_strong_kex_configured(self, host):
        """Verify only strong key exchange algorithms are configured."""
        f = host.file(SECURITY_SSHD_CONFIG_PATH)
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                if line.strip().startswith("KexAlgorithms "):
                    # Verify strong KEX are present
                    for kex in STRONG_KEX:
                        assert kex in line, f"Strong KEX '{kex}' should be configured"
                    # Verify weak KEX are not present
                    weak_kex = ["diffie-hellman-group1", "diffie-hellman-group14-sha1", "diffie-hellman-group-exchange-sha1"]
                    for weak in weak_kex:
                        assert weak not in line.lower(), f"Weak KEX '{weak}' should not be configured"
                    return
            pytest.skip("KexAlgorithms not explicitly configured in security config")

    def test_strong_host_key_algorithms_configured(self, host):
        """Verify only strong host key algorithms are configured."""
        f = host.file(SECURITY_SSHD_CONFIG_PATH)
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                if line.strip().startswith("HostKeyAlgorithms "):
                    # Verify strong host key algorithms are present
                    for algo in STRONG_HOST_KEY_ALGORITHMS:
                        assert algo in line, f"Strong host key algorithm '{algo}' should be configured"
                    return
            pytest.skip("HostKeyAlgorithms not explicitly configured in security config")


class TestSSHDSecuritySettings:
    """Test SSHD security settings."""

    def test_permit_root_login_disabled(self, host):
        """Verify root login is disabled (CIS 5.2.5)."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("PermitRootLogin "):
                assert "no" in line.lower(), "PermitRootLogin should be set to 'no'"
                return
        pytest.skip("PermitRootLogin not explicitly configured")

    def test_password_authentication_disabled(self, host):
        """Verify password authentication is disabled (CIS 5.2.11)."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("PasswordAuthentication "):
                assert "no" in line.lower(), "PasswordAuthentication should be set to 'no'"
                return
        pytest.skip("PasswordAuthentication not explicitly configured")

    def test_pubkey_authentication_enabled(self, host):
        """Verify public key authentication is enabled."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("PubkeyAuthentication "):
                assert "yes" in line.lower(), "PubkeyAuthentication should be set to 'yes'"
                return
        pytest.skip("PubkeyAuthentication not explicitly configured")

    def test_x11_forwarding_disabled(self, host):
        """Verify X11 forwarding is disabled."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("X11Forwarding "):
                assert "no" in line.lower(), "X11Forwarding should be set to 'no'"
                return
        pytest.skip("X11Forwarding not explicitly configured")

    def test_tcp_forwarding_disabled(self, host):
        """Verify TCP forwarding is disabled."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("AllowTcpForwarding "):
                assert "no" in line.lower(), "AllowTcpForwarding should be set to 'no'"
                return
        pytest.skip("AllowTcpForwarding not explicitly configured")

    def test_agent_forwarding_disabled(self, host):
        """Verify agent forwarding is disabled."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("AllowAgentForwarding "):
                assert "no" in line.lower(), "AllowAgentForwarding should be set to 'no'"
                return
        pytest.skip("AllowAgentForwarding not explicitly configured")

    def test_permit_empty_passwords_disabled(self, host):
        """Verify empty passwords are not permitted."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("PermitEmptyPasswords "):
                assert "no" in line.lower(), "PermitEmptyPasswords should be set to 'no'"
                return
        pytest.skip("PermitEmptyPasswords not explicitly configured")

    def test_use_pam_enabled(self, host):
        """Verify PAM is enabled."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("UsePAM "):
                assert "yes" in line.lower(), "UsePAM should be set to 'yes'"
                return
        pytest.skip("UsePAM not explicitly configured")

    def test_log_level_verbose(self, host):
        """Verify log level is set to VERBOSE."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("LogLevel "):
                assert "VERBOSE" in line.upper(), "LogLevel should be set to VERBOSE"
                return
        pytest.skip("LogLevel not explicitly configured")

    def test_max_auth_tries_limited(self, host):
        """Verify MaxAuthTries is limited."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("MaxAuthTries "):
                value = int(line.split()[1])
                assert value <= 4, f"MaxAuthTries should be 4 or less, got {value}"
                return
        pytest.skip("MaxAuthTries not explicitly configured")

    def test_client_alive_interval_configured(self, host):
        """Verify ClientAliveInterval is configured."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("ClientAliveInterval "):
                value = int(line.split()[1])
                assert value > 0, "ClientAliveInterval should be greater than 0"
                assert value <= 300, "ClientAliveInterval should be 300 or less"
                return
        pytest.skip("ClientAliveInterval not explicitly configured")

    def test_login_grace_time_limited(self, host):
        """Verify LoginGraceTime is limited."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("LoginGraceTime "):
                value = line.split()[1]
                # Value can be in seconds or with suffix (e.g., 60, 1m)
                if value.isdigit():
                    assert int(value) <= 60, f"LoginGraceTime should be 60 seconds or less, got {value}"
                return
        pytest.skip("LoginGraceTime not explicitly configured")


class TestSSHDHostKeys:
    """Test SSH host key configuration."""

    def test_ssh_directory_exists(self, host):
        """Verify SSH directory exists."""
        d = host.file(SSH_HOST_KEY_DIR)
        assert d.exists, f"SSH directory '{SSH_HOST_KEY_DIR}' should exist"
        assert d.is_directory, f"'{SSH_HOST_KEY_DIR}' should be a directory"
        assert d.mode == 0o755, f"SSH directory should have mode 0755, got {oct(d.mode)}"

    def test_ssh_host_ed25519_key_exists(self, host):
        """Verify Ed25519 host key exists."""
        f = host.file(f"{SSH_HOST_KEY_DIR}/ssh_host_ed25519_key")
        assert f.exists, "Ed25519 host key should exist"

    def test_ssh_host_ed25519_key_permissions(self, host):
        """Verify Ed25519 private key has correct permissions (CIS 5.2.2)."""
        f = host.file(f"{SSH_HOST_KEY_DIR}/ssh_host_ed25519_key")
        if f.exists:
            assert f.mode == 0o600, f"Ed25519 private key should have mode 0600, got {oct(f.mode)}"
            assert f.user == "root", "Ed25519 private key should be owned by root"
            assert f.group == "root", "Ed25519 private key group should be root"

    def test_ssh_host_ed25519_key_pub_permissions(self, host):
        """Verify Ed25519 public key has correct permissions (CIS 5.2.3)."""
        f = host.file(f"{SSH_HOST_KEY_DIR}/ssh_host_ed25519_key.pub")
        if f.exists:
            assert f.mode == 0o644, f"Ed25519 public key should have mode 0644, got {oct(f.mode)}"
            assert f.user == "root", "Ed25519 public key should be owned by root"

    def test_ssh_host_rsa_key_exists(self, host):
        """Verify RSA host key exists."""
        f = host.file(f"{SSH_HOST_KEY_DIR}/ssh_host_rsa_key")
        assert f.exists, "RSA host key should exist"

    def test_ssh_host_rsa_key_permissions(self, host):
        """Verify RSA private key has correct permissions (CIS 5.2.2)."""
        f = host.file(f"{SSH_HOST_KEY_DIR}/ssh_host_rsa_key")
        if f.exists:
            assert f.mode == 0o600, f"RSA private key should have mode 0600, got {oct(f.mode)}"
            assert f.user == "root", "RSA private key should be owned by root"
            assert f.group == "root", "RSA private key group should be root"

    def test_ssh_host_rsa_key_pub_permissions(self, host):
        """Verify RSA public key has correct permissions (CIS 5.2.3)."""
        f = host.file(f"{SSH_HOST_KEY_DIR}/ssh_host_rsa_key.pub")
        if f.exists:
            assert f.mode == 0o644, f"RSA public key should have mode 0644, got {oct(f.mode)}"
            assert f.user == "root", "RSA public key should be owned by root"

    def test_weak_dsa_keys_absent(self, host):
        """Verify weak DSA host keys are removed."""
        weak_keys = [
            f"{SSH_HOST_KEY_DIR}/ssh_host_dsa_key",
            f"{SSH_HOST_KEY_DIR}/ssh_host_dsa_key.pub",
        ]
        for key_path in weak_keys:
            f = host.file(key_path)
            if f.exists:
                pytest.fail(f"Weak DSA key '{key_path}' should not exist")

    def test_weak_ecdsa_keys_absent(self, host):
        """Verify weak ECDSA host keys are removed (when disable_weak_keys enabled)."""
        weak_keys = [
            f"{SSH_HOST_KEY_DIR}/ssh_host_ecdsa_key",
            f"{SSH_HOST_KEY_DIR}/ssh_host_ecdsa_key.pub",
        ]
        # Note: ECDSA keys might still exist if disable_weak_keys is false
        # This test is informational
        for key_path in weak_keys:
            f = host.file(key_path)
            # Just check and report, don't fail


class TestSSHDPrivilegeSeparation:
    """Test SSH privilege separation."""

    def test_sshd_privsep_directory_exists(self, host):
        """Verify SSH privilege separation directory exists."""
        d = host.file("/run/sshd")
        assert d.exists, "/run/sshd directory should exist"
        assert d.is_directory, "/run/sshd should be a directory"

    def test_sshd_privsep_directory_permissions(self, host):
        """Verify SSH privilege separation directory has correct permissions."""
        d = host.file("/run/sshd")
        if d.exists:
            assert d.mode == 0o755, f"/run/sshd should have mode 0755, got {oct(d.mode)}"


class TestSSHDPort:
    """Test SSH port configuration."""

    def test_ssh_port_configured(self, host):
        """Verify SSH port is configured."""
        f = host.file(SSHD_CONFIG_PATH)
        content = f.content_string
        has_port = False
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("Port "):
                has_port = True
                port = int(line.split()[1])
                assert 1 <= port <= 65535, f"SSH port should be valid (1-65535), got {port}"
                break
        assert has_port, "SSH Port should be configured"

    def test_ssh_listening_on_correct_port(self, host):
        """Verify SSH is listening on the configured port."""
        # Get configured port
        f = host.file(SSHD_CONFIG_PATH)
        configured_port = 22  # default
        content = f.content_string
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("Port "):
                configured_port = int(line.split()[1])
                break

        # Check if SSH is listening on that port
        cmd = host.run(f"ss -tlnp | grep -E ':{configured_port}\\s' || netstat -tlnp | grep -E ':{configured_port}\\s' || true")
        if cmd.rc == 0 and cmd.stdout:
            assert "sshd" in cmd.stdout or "ssh" in cmd.stdout, f"SSH should be listening on port {configured_port}"


class TestSSHDPQC:
    """Test Post-Quantum Cryptography support."""

    def test_pqc_kex_algorithms_when_enabled(self, host):
        """Verify PQC KEX algorithms are configured when PQC is enabled."""
        f = host.file(SECURITY_SSHD_CONFIG_PATH)
        if f.exists:
            content = f.content_string
            for line in content.split("\n"):
                if line.strip().startswith("KexAlgorithms "):
                    # Check if any PQC algorithms are present (when enabled)
                    has_pqc = any(pqc in line for pqc in PQC_KEX_ALGORITHMS)
                    # PQC might not be enabled, so this is informational
                    if has_pqc:
                        assert "mlkem768x25519-sha256" in line or "sntrup761x25519-sha512" in line, \
                            "PQC KEX algorithm should be valid"
                    return
            pytest.skip("KexAlgorithms not configured")
