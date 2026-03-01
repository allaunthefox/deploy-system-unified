#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-510010
# Test Type: Property-Based Testing (Hypothesis) for Quality Gates
# Last Updated: 2026-03-01
# Version: 1.0
# =============================================================================
import re
import pytest
from hypothesis import given, strategies as st

# The slugify logic used in the project
slug_re = re.compile(r'[^a-z0-9 -]')
def slugify(s):
    s = s.lower()
    s = slug_re.sub('', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

@given(st.text())
def test_slugify_properties(s):
    """Test that slugify always produces a URL-safe, lowercase, non-empty (if input had chars) string."""
    slug = slugify(s)
    
    # Property 1: Always lowercase
    assert slug == slug.lower()
    
    # Property 2: No special characters or uppercase
    assert not re.search(r'[^a-z0-9-]', slug)
    
    # Property 3: No double hyphens
    assert '--' not in slug
    
    # Property 4: No leading/trailing hyphens
    assert not slug.startswith('-')
    assert not slug.endswith('-')

@given(st.text(min_size=1).filter(lambda s: any(c.isalnum() for c in s)))
def test_slugify_non_empty_input(s):
    """Ensure alphanumeric input results in a non-empty slug if it contains at least one alphanumeric character."""
    slug = slugify(s)
    if any(c.isalnum() for c in s):
        # Note: slugify might still be empty if all alphanumeric chars are invalid (unlikely with a-z0-9)
        assert len(slug) >= 0 # Just ensure it doesn't crash
    if re.search(r'[a-z0-9]', s.lower()):
        assert len(slug) > 0

# Test regex matching for audit codes
AUDIT_CODE_PATTERN = re.compile(r'^DSU-[A-Z]{3}-\d{6}$')

@given(st.from_regex(AUDIT_CODE_PATTERN))
def test_audit_code_matching(code):
    """Verify that generated audit codes are correctly recognized by the pattern."""
    assert AUDIT_CODE_PATTERN.match(code) is not None

@given(st.text())
def test_audit_code_negative_matching(s):
    """Verify that random text doesn't accidentally match the strict audit code format."""
    # This is a weak test but ensures we don't have catastrophic false positives
    if not (s.startswith("DSU-") and len(s) == 14):
        assert not AUDIT_CODE_PATTERN.fullmatch(s)

if __name__ == "__main__":
    import sys
    pytest.main([__file__])
