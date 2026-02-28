#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-TST-1000107
# File Type: Python Test Script
# Test Type: Script Logic Validation
# Description: Test the exact logic from the linter script
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
"""Test the exact logic from the linter script."""

import os
import re
import unittest
from pathlib import Path


class TestScriptLogic(unittest.TestCase):
    """Test linter script logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).resolve().parent.parent
        self.wiki_pages = self.repo_root / 'wiki_pages'
        self.var_file = self.wiki_pages / 'REF_VARS_CONTAINERS.md'

    def test_slugify_function(self):
        """Test slugify function for anchor generation."""
        slug_re = re.compile(r'[^a-z0-9 -]')
        
        def slugify(s):
            s = s.lower()
            s = slug_re.sub('', s)
            s = re.sub(r'\s+', '-', s)
            s = re.sub(r'-+', '-', s)
            return s.strip('-')
        
        # Test cases
        self.assertEqual(slugify("Anubis Enabled"), "anubis-enabled")
        self.assertEqual(slugify("anubis_enabled"), "anubisenabled")
        self.assertEqual(slugify("GPU Settings"), "gpu-settings")
        self.assertEqual(slugify("Test--Double--Dash"), "test-double-dash")

    def test_role_header_pattern(self):
        """Test role header pattern matching."""
        pattern = r'^###+ `([^`]+)`'
        
        # Valid role headers
        self.assertIsNotNone(re.match(pattern, "### `containers/anubis`"))
        self.assertIsNotNone(re.match(pattern, "### `security/vault`"))
        
        # Invalid patterns
        self.assertIsNone(re.match(pattern, "## Regular Header"))
        self.assertIsNone(re.match(pattern, "### No Backticks"))

    def test_variable_line_pattern(self):
        """Test variable line pattern matching."""
        # Pattern for: - `[varname](path#anchor)`
        # Breaking down: whitespace-dash-backtick-bracket-varname-bracket-bracket-paren-hash-anchor-paren
        pattern = r'^\s*-\s+`\[([a-zA-Z0-9_]+)\]\([^)]*#([a-zA-Z0-9_]+)\)`'
        
        # Valid variable line
        line = "- `[anubis_enabled](roles/containers_anubis.md#anubis_enabled)`"
        match = re.match(pattern, line)
        self.assertIsNotNone(match, "Should match variable line format")
        
        if match:
            varname, anchor = match.groups()
            self.assertEqual(varname, "anubis_enabled")
            self.assertEqual(anchor, "anubis_enabled")

    def test_var_file_processing(self):
        """Test processing of variable reference file."""
        with open(self.var_file, 'r') as f:
            content = f.read()
        
        lines = content.splitlines()
        current_role_file = None
        
        # Process first 20 lines to verify logic
        processed = 0
        for line in lines[:20]:
            # Match role header
            m_role = re.match(r'^###+ `([^`]+)`', line)
            if m_role:
                role_name = m_role.group(1)
                current_role_file = f"roles/{role_name.replace('/', '_')}.md"
                processed += 1
                continue
                
            # Match variable line
            m_var = re.match(r'^(\s*-\s+`)(\[)([a-zA-Z0-9_]+)(\])(\].*#)([a-zA-Z0-9_]+)(\).*)$', line)
            if m_var and current_role_file:
                processed += 1
                
        self.assertGreater(processed, 0, "Should process at least some lines")


if __name__ == '__main__':
    unittest.main()
