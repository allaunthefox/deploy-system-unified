import importlib
import logging
import sys
import os

import pytest


def test_shim_activation_is_logged(caplog, monkeypatch):
    """When the fallback shim activates, it must emit a tagged audit log."""
    # Ensure shim is allowed and force a fresh import
    monkeypatch.setenv('DSU_ALLOW_ANSIBLELINT_SHIM', '1')
    for k in list(sys.modules.keys()):
        if k.startswith('ansiblelint'):
            del sys.modules[k]

    caplog.set_level(logging.INFO)

    # Import the package (triggers shim)
    mod = importlib.import_module('ansiblelint')

    # If the shim produced fallback modules, we expect an audit log entry
    created_shims = [
        name for name in ('ansiblelint.errors', 'ansiblelint.file_utils', 'ansiblelint.rules')
        if name in sys.modules and getattr(sys.modules[name], '__dsu_shim__', False)
    ]

    if not created_shims:
        pytest.skip('Fallback shim not created in this environment; skipping log assertion')

    # Verify an INFO log entry with the DSU-SHIM tag exists
    msgs = [r.getMessage() for r in caplog.records if r.levelno == logging.INFO]
    assert any('DSU-SHIM' in m and 'ansiblelint shim activated' in m for m in msgs), msgs

    # Ensure affected_rules metadata is present (helps auditors find impacted rules)
    assert any('affected_rules' in m for m in msgs)
