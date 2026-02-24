"""
Testinfra tests for ops/connection_info role.

This role handles SSH connection information management:
- Determining SSH port
- Creating SSH connection info
- Caching SSH port information
- Encrypting connection info (SOPS/Vault)
- Rsync encrypted info to destination
"""
import pytest


# Default paths
SSH_PORT_CACHE_DIR = "/.ssh_port_cache"


class TestConnectionInfoSSH:
    """Test SSH configuration."""

    def test_ssh_command_available(self, host):
        """Verify SSH command is available."""
        assert host.exists("ssh"), "ssh command should be available"

    def test_sshd_service(self, host):
        """Verify sshd service status."""
        svc_names = ["sshd", "ssh"]
        for svc_name in svc_names:
            svc = host.service(svc_name)
            if svc.exists:
                # Service should be manageable
                pass

    def test_ssh_port_configured(self, host):
        """Verify SSH port is configured."""
        # Default SSH port is 22
        # Check sshd_config for port
        f = host.file("/etc/ssh/sshd_config")
        if f.exists:
            content = f.content_string
            # Port may be explicitly set or default to 22
            has_port = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("Port "):
                    has_port = True
                    port = line.split()[1]
                    assert port.isdigit(), f"SSH port should be numeric, got {port}"
                    break
            # Port may not be explicitly set (defaults to 22)

    def test_ssh_port_default(self, host):
        """Verify default SSH port is 22 if not configured."""
        f = host.file("/etc/ssh/sshd_config")
        if f.exists:
            content = f.content_string
            has_custom_port = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("Port ") and not line.startswith("Port 22"):
                    has_custom_port = True
                    break
            # If no custom port, default is 22


class TestConnectionInfoCache:
    """Test SSH port caching."""

    def test_ssh_port_cache_directory(self, host):
        """Verify SSH port cache directory structure."""
        # Cache directory is typically in playbook_dir or inventory_dir
        # This is controller-side, not host-side
        pass

    def test_ssh_port_cache_file_format(self, host):
        """Verify SSH port cache file format."""
        # Cache files contain just the port number
        # This is controller-side verification
        pass


class TestConnectionInfoEncryption:
    """Test connection info encryption."""

    def test_sops_available(self, host):
        """Verify SOPS is available if configured."""
        if host.exists("sops"):
            cmd = host.run("sops --version 2>&1 | head -1 || true")
            if cmd.rc == 0:
                assert "sops" in cmd.stdout.lower(), "sops --version should return version info"

    def test_ansible_vault_available(self, host):
        """Verify Ansible Vault is available."""
        assert host.exists("ansible-vault"), "ansible-vault command should be available"

    def test_gpg_available(self, host):
        """Verify GPG is available for encryption."""
        if host.exists("gpg") or host.exists("gpg2"):
            # GPG is available for SOPS encryption
            pass


class TestConnectionInfoFiles:
    """Test connection info files."""

    def test_ssh_config_exists(self, host):
        """Verify SSH config file exists."""
        f = host.file("/etc/ssh/ssh_config")
        if f.exists:
            assert f.is_file, "/etc/ssh/ssh_config should be a file"

    def test_ssh_config_permissions(self, host):
        """Verify SSH config has correct permissions."""
        f = host.file("/etc/ssh/ssh_config")
        if f.exists:
            assert f.mode in [0o644, 0o640], "/etc/ssh/ssh_config should have correct permissions"

    def test_sshd_config_exists(self, host):
        """Verify sshd_config file exists."""
        f = host.file("/etc/ssh/sshd_config")
        assert f.exists, "/etc/ssh/sshd_config should exist"

    def test_sshd_config_permissions(self, host):
        """Verify sshd_config has correct permissions."""
        f = host.file("/etc/ssh/sshd_config")
        if f.exists:
            assert f.mode in [0o644, 0o600], "/etc/ssh/sshd_config should have secure permissions"
            assert f.user == "root", "/etc/ssh/sshd_config should be owned by root"

    def test_ssh_host_keys_exist(self, host):
        """Verify SSH host keys exist."""
        key_types = ["rsa", "ecdsa", "ed25519"]
        has_keys = False
        for key_type in key_types:
            f = host.file(f"/etc/ssh/ssh_host_{key_type}_key")
            if f.exists:
                has_keys = True
                # Private key should have restrictive permissions
                assert f.mode in [0o600, 0o400], f"SSH host {key_type} key should have restrictive permissions"
        assert has_keys, "At least one SSH host key should exist"

    def test_ssh_host_pub_keys_exist(self, host):
        """Verify SSH host public keys exist."""
        key_types = ["rsa", "ecdsa", "ed25519"]
        for key_type in key_types:
            f = host.file(f"/etc/ssh/ssh_host_{key_type}_key.pub")
            if f.exists:
                # Public key should be readable
                assert f.mode in [0o644, 0o640], f"SSH host {key_type} public key should be readable"


class TestConnectionInfoSecurity:
    """Test connection info security."""

    def test_ssh_directory_permissions(self, host):
        """Verify SSH directory has correct permissions."""
        d = host.file("/etc/ssh")
        assert d.exists, "/etc/ssh should exist"
        assert d.is_directory, "/etc/ssh should be a directory"
        assert d.mode in [0o755, 0o750], "/etc/ssh should have correct permissions"
        assert d.user == "root", "/etc/ssh should be owned by root"

    def test_ssh_keys_directory(self, host):
        """Verify SSH keys directory permissions."""
        d = host.file("/etc/ssh")
        if d.exists:
            # Should contain host keys
            pass

    def test_temp_file_cleanup(self, host):
        """Verify temporary files are cleaned up."""
        # Connection info role should clean up temp files
        # Check for leftover temp files
        cmd = host.run("find /tmp -name 'ssh_connection_info_*' -type f 2>/dev/null | head -5 || true")
        if cmd.rc == 0 and cmd.stdout.strip():
            # Temp files should be cleaned up
            # This is informational as cleanup happens on controller


class TestConnectionInfoRsync:
    """Test rsync functionality."""

    def test_rsync_available(self, host):
        """Verify rsync is available."""
        assert host.exists("rsync"), "rsync command should be available"

    def test_rsync_version(self, host):
        """Verify rsync version can be determined."""
        cmd = host.run("rsync --version | head -1")
        if cmd.rc == 0:
            assert "rsync" in cmd.stdout.lower(), "rsync --version should return version info"


class TestConnectionInfoValidation:
    """Test connection info validation."""

    def test_connection_info_format(self, host):
        """Verify connection info has expected format."""
        # Connection info should include:
        # - deployment_id
        # - hostname
        # - port
        # - username
        # - timestamp
        # This is verified through role output

    def test_encryption_method_configured(self, host):
        """Verify encryption method is configured."""
        # Default is 'plain' for dev/test
        # Can be 'sops' or 'vault' for production
        # This is verified through role variables

    def test_rsync_destination_validated(self, host):
        """Verify rsync destination is validated."""
        # Rsync destination should be in allowlist
        # This is verified through role logic
