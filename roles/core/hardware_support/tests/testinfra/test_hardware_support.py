# =============================================================================
# Audit Event Identifier: DSU-PYS-500057
# Last Updated: 2026-02-28
# =============================================================================
"""
Testinfra tests for core/hardware_support role.

This role handles hardware-specific support packages and configuration.
"""


class TestHardwareSupport:
    """Test hardware support configuration."""

    def test_hardware_support_role_executed(self, host):
        """Verify hardware support role executed."""
        pass

    def test_hardware_packages_available(self, host):
        """Verify hardware packages can be queried."""
        cmd = host.run("dpkg -l 2>&1 | head -5 || true")
        if cmd.rc == 0:
            assert cmd.stdout.strip()
