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

# Determine wiki root (env WORKSPACES_WIKI or ~/Workspaces/wiki_pages)
wiki_root = Path(os.environ.get("WORKSPACES_WIKI", Path.home() / "Workspaces" / "wiki_pages"))


class TestAnchorProcessing(unittest.TestCase):
    """Test anchor processing for linter."""

    def setUp(self):
        """Set up test fixtures."""
        self.role_file = wiki_root / 'roles' / 'containers_anubis.md'
        self.var_file = wiki_root / 'Variable_Reference_Containers.md'
        
    def test_role_file_exists(self):
        """Test that role file exists."""
        if self.role_file.exists():
            self.assertTrue(self.role_file.exists(), f"Role file should exist")
        else:
            self.skipTest(f"Role file not found: {self.role_file} (wiki_pages may not be configured)")
        
    def test_var_file_exists(self):
        """Test that variable reference file exists."""
        if self.var_file.exists():
            self.assertTrue(self.var_file.exists(), f"Variable file should exist")
        else:
            self.skipTest(f"Variable file not found: {self.var_file} (wiki_pages may not be configured)")
        
    def test_anchor_generation(self):
        """Test anchor generation from headings."""
        if not self.role_file.exists():
            self.skipTest("Role file not found")
            
        role_content = self.role_file.read_text()
        
        # Extract headings using the same pattern as the linter
        HEADING_RE = re.compile(r'^(#+)\s*(.+)$', flags=re.M)
        headers = [(m.group(1), m.group(2).strip()) for m in HEADING_RE.finditer(role_content)]

        # Apply slugify function as linter does
        slug_re = re.compile(r'[^a-z0-9 -]')
        def slugify(s):
            s = s.lower()
            s = slug_re.sub('', s)
            s = re.sub(r'\s+', '-', s)
            s = re.sub(r'-+', '-', s)
            return s.strip('-')

        target_headings = set(slugify(h) for _, h in headers)
        
        # Check if specific anchors exist
        test_anchors = ['anubis-enabled', 'anubis-port', 'anubis-difficulty']
        for anchor in test_anchors:
            # Anchor should exist or be a valid slugified version
            self.assertIn(anchor, target_headings, f"Anchor {anchor} not found in headings")


if __name__ == '__main__':
    unittest.main()