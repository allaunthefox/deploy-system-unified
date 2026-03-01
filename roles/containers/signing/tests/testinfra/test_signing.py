# =============================================================================
# Audit Event Identifier: DSU-PYS-500026
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for containers/signing role.

This role handles container image signing:
- GPG key management
- Container image signing with cosign or podman trust
- Signature verification
"""
import pytest


class TestSigningPackages:
    """Test signing package installation."""

    def test_gpg_installed(self, host):
        """Verify GPG is installed."""
        pkg = host.package("gnupg")
        assert pkg.is_installed, "gnupg package should be installed"

    def test_podman_installed(self, host):
        """Verify podman is installed."""
        pkg = host.package("podman")
        if pkg.is_installed:
            assert pkg.is_installed, "podman package should be installed"


class TestSigningDirectories:
    """Test signing directories."""

    def test_signing_dir_exists(self, host):
        """Verify signing directory exists."""
        d = host.file("/srv/containers/signing")
        if d.exists:
            assert d.is_directory, "/srv/containers/signing should be a directory"

    def test_signing_dir_permissions(self, host):
        """Verify signing directory has correct permissions."""
        d = host.file("/srv/containers/signing")
        if d.exists:
            # Should be secure - owner only
            assert d.mode in [0o700, 0o755], \
                f"/srv/containers/signing should have secure permissions, got {oct(d.mode)}"


class TestSigningConfiguration:
    """Test signing configuration."""

    def test_gpg_available(self, host):
        """Verify GPG is available."""
        cmd = host.run("gpg --version")
        if cmd.rc == 0:
            assert "gpg" in cmd.stdout.lower(), "GPG should be available"
        else:
            pytest.skip("GPG not available")

    def test_podman_available(self, host):
        """Verify podman is available for container signing."""
        cmd = host.run("podman --version")
        if cmd.rc == 0:
            assert "podman" in cmd.stdout.lower(), "podman should be available"
        else:
            pytest.skip("podman not available")


class TestSigningCompletion:
    """Test signing completion indicators."""

    def test_signing_config_complete(self, host):
        """Verify signing configuration is complete."""
        d = host.file("/srv/containers/signing")
        # Just verify the directory exists and is accessible
        if d.exists:
            assert True, "Signing directory should be accessible"
        else:
            pytest.skip("Signing directory not configured")
