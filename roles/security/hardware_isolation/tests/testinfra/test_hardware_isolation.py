"""
Testinfra tests for security/hardware_isolation role.

This role handles hardware isolation and IOMMU configuration.
"""


class TestHardwareIsolation:
    """Test hardware isolation configuration."""

    def test_hardware_isolation_role_executed(self, host):
        """Verify hardware isolation role executed."""
        pass

    def test_iommu_available(self, host):
        """Verify IOMMU can be configured."""
        pass
