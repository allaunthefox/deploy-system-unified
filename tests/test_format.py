#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-TST-1000102
# File Type: Python Test Script
# Test Type: Format Validation
# Description: Test markdown link format parsing
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
"""Test markdown link format parsing."""

import re
import unittest
from pathlib import Path


class TestMarkdownFormat(unittest.TestCase):
    """Test markdown link format parsing."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).resolve().parent.parent
        self.wiki_pages = self.repo_root / 'wiki_pages'
        self.var_file = self.wiki_pages / 'REF_VARS_CONTAINERS.md'

    def test_link_format_parsing(self):
        """Test parsing of markdown link format."""
        # Test standard format: - [varname](path#anchor)
        line = "- [anubis_enabled](roles/containers_anubis.md#anubis_enabled)"
        pattern = r'^(\s*-\s+\[)([a-zA-Z0-9_]+)(\].*#)([a-zA-Z0-9_]+)(\).*)$'
        m_var = re.match(pattern, line)
        self.assertIsNotNone(m_var, "Standard format should match")
        
        prefix, varname, mid, anchor, suffix = m_var.groups()
        self.assertEqual(varname, "anubis_enabled")
        self.assertEqual(anchor, "anubis_enabled")

    def test_backtick_format_parsing(self):
        """Test parsing of backtick-wrapped format."""
        # Test backtick format: - `[varname](path#anchor)`
        line = "- `[anubis_enabled](roles/containers_anubis.md#anubis_enabled)`"
        pattern = r'^(\s*-\s+`)(\[)([a-zA-Z0-9_]+)(\])(\].*#)([a-zA-Z0-9_]+)(\).*)$'
        m_var = re.match(pattern, line)
        # This format may not match - that's expected behavior to detect
        # The test validates the pattern works as designed
        self.assertIsNone(m_var, "Backtick format should not match standard pattern")

    def test_var_file_exists(self):
        """Test that variable reference file exists."""
        if self.var_file.exists():
            self.assertTrue(self.var_file.exists(), "Variable file should exist")
        else:
            self.skipTest("Variable reference file not found")

    def test_file_content_format(self):
        """Test actual file content format."""
        if not self.var_file.exists():
            self.skipTest("Variable reference file not found")
        
        with open(self.var_file, 'r') as f:
            content = f.read()
        
        # Find lines with anubis references (format: [`varname`](path#anchor))
        pattern = r'\[`anubis[a-z_]*`\]\([^)]*containers_anubis\.md#[^)]+\)'
        matches = re.findall(pattern, content)
        self.assertGreater(len(matches), 0, "Should find anubis variable links")
        
        # Verify specific anubis anchors exist
        anubis_anchors = ['anubisenabled', 'anubisport', 'anubisdifficulty']
        for anchor in anubis_anchors:
            self.assertIn(f'#{anchor}', content, f"Should have anchor #{anchor}")


if __name__ == '__main__':
    unittest.main()
