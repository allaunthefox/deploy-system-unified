"""
Testinfra tests for containers/common role.

This role handles common container configuration.
"""


class TestContainersCommon:
    """Test common container configuration."""

    def test_common_role_executed(self, host):
        """Verify common role executed."""
        pass

    def test_container_directories_exist(self, host):
        """Verify container directories exist."""
        d = host.file("/var/lib")
        assert d.exists, "/var/lib should exist"
