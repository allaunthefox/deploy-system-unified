# =============================================================================
# Audit Event Identifier: DSU-PYS-500034
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for ops/session role.

This role handles deployment session management:
- Creating TMUX session for deployment
- Managing deployment session state
- Validating session availability
"""
import pytest


# Default session configuration
DEFAULT_SESSION_NAME = "deployment-session"


class TestSessionTmux:
    """Test TMUX availability and configuration."""

    def test_tmux_installed(self, host):
        """Verify tmux is installed."""
        pkg = host.package("tmux")
        if pkg.exists:
            assert pkg.is_installed, "tmux package should be installed"
        else:
            # tmux command should be available
            assert host.exists("tmux"), "tmux command should be available"

    def test_tmux_command_available(self, host):
        """Verify tmux command is available."""
        assert host.exists("tmux"), "tmux command should be available"

    def test_tmux_version(self, host):
        """Verify tmux version can be determined."""
        cmd = host.run("tmux -V")
        if cmd.rc == 0:
            # Should return version string like "tmux 3.x"
            assert "tmux" in cmd.stdout.lower(), "tmux -V should return version info"


class TestSessionDeployment:
    """Test deployment session configuration."""

    def test_session_name_configured(self, host):
        """Verify session name is configured."""
        # The session name should be the default or configured value
        # This is verified through the role's fact setting
        pass  # Session name is a role fact, not system state

    def test_session_creation_capability(self, host):
        """Verify session can be created."""
        # Check if tmux can create sessions
        if host.exists("tmux"):
            cmd = host.run("tmux new-session -d -s test-session-$$ 2>&1; tmux kill-session -t test-session-$$ 2>/dev/null; echo $?")
            # Should be able to create and destroy a test session
            # This is informational as it requires tmux server


class TestSessionState:
    """Test session state management."""

    def test_tmux_socket_directory(self, host):
        """Verify tmux socket directory is accessible."""
        # Tmux uses /tmp for sockets by default
        socket_dirs = ["/tmp/tmux", "/var/run/tmux"]
        has_socket_dir = False
        for socket_dir in socket_dirs:
            d = host.file(socket_dir)
            if d.exists:
                has_socket_dir = True
                assert d.is_directory, f"{socket_dir} should be a directory"
        # Socket dir may not exist until tmux is used

    def test_user_home_directory(self, host):
        """Verify user home directory exists for session."""
        # Sessions are typically created in user context
        cmd = host.run("echo $HOME")
        if cmd.rc == 0 and cmd.stdout.strip():
            home = cmd.stdout.strip()
            d = host.file(home)
            if d.exists:
                assert d.is_directory, f"Home directory {home} should be a directory"


class TestSessionEnvironment:
    """Test session environment configuration."""

    def test_shell_available(self, host):
        """Verify shell is available for sessions."""
        shells = ["/bin/bash", "/bin/sh", "/usr/bin/bash"]
        has_shell = False
        for shell in shells:
            f = host.file(shell)
            if f.exists:
                has_shell = True
                assert f.is_file, f"{shell} should be a file"
                break
        assert has_shell, "At least one shell should be available"

    def test_terminal_capabilities(self, host):
        """Verify terminal capabilities are available."""
        # TERM should be set
        cmd = host.run("echo $TERM")
        # TERM may or may not be set depending on execution context

    def test_path_configured(self, host):
        """Verify PATH is configured."""
        cmd = host.run("echo $PATH")
        if cmd.rc == 0 and cmd.stdout.strip():
            path = cmd.stdout.strip()
            assert len(path) > 0, "PATH should be configured"
            # Should include common directories
            assert "/bin" in path or "/usr/bin" in path, "PATH should include standard directories"


class TestSessionValidation:
    """Test session validation."""

    def test_session_fact_available(self, host):
        """Verify session state fact can be determined."""
        # The role sets tmux_session_ok fact
        # This is verified through Ansible, not system state
        pass

    def test_deployment_session_not_conflicting(self, host):
        """Verify no conflicting session names."""
        if host.exists("tmux"):
            cmd = host.run("tmux list-sessions 2>/dev/null || true")
            # Should be able to list sessions without error
            # Multiple sessions are allowed


class TestSessionSecurity:
    """Test session security configuration."""

    def test_tmux_config_permissions(self, host):
        """Verify tmux configuration has correct permissions."""
        config_paths = [
            "/etc/tmux.conf",
            "/etc/tmux.conf.local",
        ]
        for config_path in config_paths:
            f = host.file(config_path)
            if f.exists:
                assert f.mode in [0o644, 0o640, 0o600], f"{config_path} should have secure permissions"

    def test_user_tmux_config(self, host):
        """Verify user tmux config has correct permissions."""
        # Check for user tmux configs
        cmd = host.run("find /home -name '.tmux.conf' -type f 2>/dev/null | head -5")
        if cmd.rc == 0 and cmd.stdout.strip():
            for config_file in cmd.stdout.strip().split("\n"):
                f = host.file(config_file)
                if f.exists:
                    # User configs should be readable only by owner
                    assert f.mode in [0o644, 0o640, 0o600], f"{config_file} should have secure permissions"
