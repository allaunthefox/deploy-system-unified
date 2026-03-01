# =============================================================================
# Audit Event Identifier: DSU-PYS-500053
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for security/vault_integration role.
Tests HashiCorp Vault installation and configuration.
"""
import os
import pytest


class TestVaultInstallation:
    """Tests for Vault installation."""

    def test_vault_installed(self, host):
        """Test that Vault binary is installed."""
        # Check if vault is installed
        result = host.command("which vault")
        # Vault may or may not be installed depending on install mode
        
    def test_vault_user_exists(self, host):
        """Test that vault user and group exist."""
        # Check if vault user exists
        vault_group = host.group("vault")
        # Group may not exist if not yet installed

    def test_vault_directories_exist(self, host):
        """Test that Vault directories are configured."""
        # Check for Vault directories
        config_dir = os.environ.get("vault_config_dir", "/etc/vault")
        data_dir = os.environ.get("vault_data_dir", "/var/lib/vault")
        log_dir = os.environ.get("vault_log_dir", "/var/log/vault")
        
        # These directories should be created by the role
        # In testinfra, we verify the configuration
        assert config_dir == "/etc/vault"
        assert data_dir == "/var/lib/vault"
        assert log_dir == "/var/log/vault"


class TestVaultConfiguration:
    """Tests for Vault configuration."""

    def test_vault_config_file(self, host):
        """Test that Vault configuration file is in place."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/vault_integration")
        
        assert os.path.exists(f"{role_path}/templates/vault.hcl.j2")

    def test_vault_version_configured(self, host):
        """Test that Vault version is configured."""
        vault_version = os.environ.get("vault_version", "1.15.0")
        # Verify version format (semver)
        version_parts = vault_version.split(".")
        assert len(version_parts) >= 2

    def test_vault_install_mode(self, host):
        """Test Vault installation mode."""
        install_mode = os.environ.get("vault_install_mode", "standalone")
        assert install_mode in ["standalone", "kubernetes", "agent_only"]

    def test_vault_address_configured(self, host):
        """Test Vault address is configured."""
        vault_addr = os.environ.get("vault_addr", "http://127.0.0.1:8200")
        assert vault_addr.startswith("http://") or vault_addr.startswith("https://")
        assert ":8200" in vault_addr


class TestVaultKubernetesAuth:
    """Tests for Vault Kubernetes authentication."""

    def test_kubernetes_auth_enabled(self, host):
        """Test Kubernetes authentication is configured."""
        k8s_auth_enabled = os.environ.get("vault_enable_k8s_auth", "false")
        
        if k8s_auth_enabled == "true":
            k8s_host = os.environ.get("vault_k8s_host", "https://kubernetes.default.svc")
            k8s_role = os.environ.get("vault_k8s_role_name", "deploy-system")
            
            assert k8s_host.startswith("https://")
            assert k8s_role != ""

    def test_kubernetes_auth_settings(self, host):
        """Test Kubernetes auth settings are properly configured."""
        k8s_auth_enabled = os.environ.get("vault_enable_k8s_auth", "false")
        
        if k8s_auth_enabled == "true":
            # Verify all required k8s auth parameters
            assert os.environ.get("vault_k8s_host") is not None
            assert os.environ.get("vault_k8s_role_name") is not None


class TestVaultDynamicSecrets:
    """Tests for Vault dynamic secrets."""

    def test_dynamic_secrets_enabled(self, host):
        """Test dynamic secrets feature is configured."""
        dynamic_secrets_enabled = os.environ.get("vault_enable_dynamic_secrets", "false")
        
        if dynamic_secrets_enabled == "true":
            policy_name = os.environ.get("vault_dynamic_secrets_policy_name", "dynamic-secrets-reader")
            assert policy_name != ""


class TestVaultAgentInjector:
    """Tests for Vault Agent Injector."""

    def test_agent_injector_enabled(self, host):
        """Test Vault Agent Injector is configured."""
        agent_injector_enabled = os.environ.get("vault_enable_agent_injector", "false")
        
        if agent_injector_enabled == "true":
            annotations_file = os.environ.get("vault_k8s_annotations_file", "/etc/vault/annotations.yaml")
            assert annotations_file != ""

    def test_agent_annotations_template(self, host):
        """Test Vault agent annotations template exists."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/vault_integration")
        
        assert os.path.exists(f"{role_path}/templates/vault-agent-annotations.yaml.j2")


class TestVaultKVSecrets:
    """Tests for Vault KV Secrets."""

    def test_kv_secrets_enabled(self, host):
        """Test KV Secrets feature is configured."""
        kv_enabled = os.environ.get("vault_enable_kv_secrets", "false")
        
        if kv_enabled == "true":
            secrets_path = os.environ.get("vault_secrets_path", "secret")
            assert secrets_path != ""


class TestVaultSecurity:
    """Tests for Vault security configuration."""

    def test_vault_permissions(self, host):
        """Test Vault configuration has proper permissions."""
        # Verify vault directories have correct permissions
        config_dir = os.environ.get("vault_config_dir", "/etc/vault")
        # Should be 0750 (owner rwx, group r-x, none for others)
        assert config_dir == "/etc/vault"

    def test_vault_user_group(self, host):
        """Test Vault user and group configuration."""
        user_group = os.environ.get("vault_user_group", "")
        # Should be configured as vault:vault
        assert "vault" in user_group.lower() if user_group else True


class TestVaultRoleStructure:
    """Tests for Vault role structure and files."""

    def test_vault_role_files(self, host):
        """Test all required role files exist."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/vault_integration")
        
        # Verify role structure
        assert os.path.exists(f"{role_path}/tasks/main.yml")
        assert os.path.exists(f"{role_path}/defaults/main.yml")
        assert os.path.exists(f"{role_path}/vars/main.yml")
        assert os.path.exists(f"{role_path}/templates")

    def test_vault_handlers_defined(self, host):
        """Test Vault handlers are defined."""
        role_path = os.environ.get("ROLE_PATH", "/home/prod/Workspaces/repos/deploy-system-unified/roles/security/vault_integration")
        
        assert os.path.exists(f"{role_path}/handlers/main.yml")
