#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-TST-1000109
# File Type: Python Test Script
# Test Type: Handler Naming Convention Test
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
import re
from pathlib import Path

handler_files = list(Path('deploy-system-unified').rglob('roles/*/handlers/main.yml'))
assert handler_files, 'No handler files found in roles'

snake_re = re.compile(r'^[a-z0-9_]+$')

bad = []
for hf in handler_files:
    text = hf.read_text()
    for line in text.splitlines():
        m = re.match(r"^\s*-\s*name:\s*['"]?(.*)['"]?\s*$", line)
        if m:
            name = m.group(1)
            if not snake_re.match(name):
                bad.append(f"{hf}: '{name}'")

if bad:
    msg = '
'.join(bad)
    raise AssertionError('Handler name convention violations (use lowercase_snake_case):
' + msg)
