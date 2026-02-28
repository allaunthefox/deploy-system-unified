#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-TST-1000101
# File Type: Python Test Script
# Test Type: Debug/Validation
# Description: Test script to debug linter anchor processing
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
"""Test script to debug the linter's anchor processing."""

import os
import re
import unittest
from pathlib import Path

# Determine wiki root - use project wiki_pages directory
repo_root = Path(__file__).resolve().parent.parent
wiki_root = repo_root / 'wiki_pages'


class TestAnchorProcessing(unittest.TestCase):
    """Test anchor processing for linter."""

    def setUp(self):
        """Set up test fixtures."""
        self.role_file = wiki_root / 'roles' / 'containers_anubis.md'
        self.var_file = wiki_root / 'REF_VARS_CONTAINERS.md'
        
    def test_role_file_exists(self):
        """Test that role file exists."""
        self.assertTrue(self.role_file.exists(), f"Role file should exist at {self.role_file}")
        
    def test_var_file_exists(self):
        """Test that variable reference file exists."""
        self.assertTrue(self.var_file.exists(), f"Variable file should exist at {self.var_file}")
        
    def test_anchor_generation(self):
        """Test anchor generation from headings."""
        role_content = self.role_file.read_text()
        
        # Extract anchors from HTML-style anchor tags: <a id="anchor-name"></a>
        ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')
        anchors = ANCHOR_RE.findall(role_content)
        
        # Check if specific anchors exist
        test_anchors = ['anubis-enabled', 'anubis-port', 'anubis-difficulty']
        for anchor in test_anchors:
            self.assertIn(anchor, anchors, f"Anchor {anchor} should exist in file")


if __name__ == '__main__':
    unittest.main()