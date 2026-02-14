"""Adaptive shim for `ansiblelint` test imports.

This package lives inside the repository so local rule modules can do
`from ansiblelint.rules import AnsibleLintRule` and similar during unit tests.

Behaviour:
- If a real `ansiblelint` installation exposes the expected submodules
  (`errors`, `file_utils`, `rules`) we re-export them.
- Otherwise we provide small, compatible fallback implementations that
  expose the symbols the repository's unit tests and local rule modules
  expect (e.g. `MatchError`, `Lintable`, `AnsibleLintRule`, `RulesCollection`).

The shim is intentionally minimal but broadly compatible so tests run
consistently in CI and local dev environments.
"""
from __future__ import annotations

import importlib
import sys
import types
import logging
import inspect
import os
import re
from pathlib import Path
from typing import Any

# Helper to create a minimal module and register it in sys.modules
def _make_module(name: str) -> types.ModuleType:
    m = types.ModuleType(name)
    sys.modules[name] = m
    return m

# Attempt to import real submodules, but fall back to lightweight shims
_errors = None
_file_utils = None
_rules = None

def _safe_import(name: str, required_attrs: tuple[str, ...]) -> Any | None:
    """Import a submodule and verify it exposes required attributes.

    Return the module only if all required_attrs are present; otherwise None.
    """
    try:
        mod = importlib.import_module(name)
        for a in required_attrs:
            if not hasattr(mod, a):
                return None
        return mod
    except Exception:
        return None

_errors = _safe_import('ansiblelint.errors', ('MatchError',))
_file_utils = _safe_import('ansiblelint.file_utils', ('Lintable',))
_rules = _safe_import('ansiblelint.rules', ('AnsibleLintRule', 'RulesCollection'))

# If any submodule is missing, create a compatible fallback — but only when
# it is safe (local repo tests / CI). This prevents accidental use of the
# test-only shim in other contexts and closes potential attack vectors.
from pathlib import Path
import os
import inspect

_repo_root = Path(__file__).resolve().parents[1]

def _import_originates_from_repo() -> bool:
    """Return True if any frame in the import stack originates from this repo.

    This restricts fallback activation to test runs or code importing from the
    repository itself (prevents global/third-party usage of the shim).
    """
    try:
        for fr in inspect.stack():
            fn = getattr(fr, 'filename', None)
            if not fn:
                continue
            try:
                p = Path(fn).resolve()
            except Exception:
                continue
            # If the importing frame is inside the repository root, allow fallback
            if _repo_root == p or _repo_root in p.parents:
                return True
    except Exception:
        # Be conservative if stack inspection fails
        return False
    return False

# Allow fallback if any of these are true (explicit env toggle OR running tests/CI)
_ALLOW_FALLBACK = bool(os.environ.get('DSU_ALLOW_ANSIBLELINT_SHIM'))
_ALLOW_FALLBACK = _ALLOW_FALLBACK or _import_originates_from_repo() or ('pytest' in sys.modules) or ('PYTEST_CURRENT_TEST' in os.environ) or ('CI' in os.environ)

if not _ALLOW_FALLBACK and (_errors is None or _file_utils is None or _rules is None):
    # Safety: do not create fallback modules outside test/repo/CI contexts.
    # Leave the missing submodules as None so normal imports fail fast.
    pass
else:
    # Provision minimal, safe fallbacks only when allowed and needed.
    if _errors is None:
        _errors = _make_module('ansiblelint.errors')

        class MatchError(Exception):
            """Minimal stand-in for ansiblelint.errors.MatchError."""

            def __init__(self, lintable: Any = None, rule: Any = None, message: str = ''):
                super().__init__(message)
                self.lintable = lintable
                self.rule = rule
                self.message = message

        _errors.MatchError = MatchError
        _errors.__dsu_shim__ = True

    if _file_utils is None:
        _file_utils = _make_module('ansiblelint.file_utils')

        class Lintable:
            """Lightweight Lintable stand-in used by local rules/tests."""

            def __init__(self, path: str = '', data: Any = None):
                self.path = path
                self.data = data

        _file_utils.Lintable = Lintable
        _file_utils.__dsu_shim__ = True

    if _rules is None:
        _rules = _make_module('ansiblelint.rules')

        class AnsibleLintRule:
            """Minimal base class so local rule classes can subclass."""

            id: str = ''
            shortdesc: str = ''
            description: str = ''
            severity: str = ''
            tags: list[str] = []

            def __init__(self, *args, **kwargs) -> None:  # pragma: no cover - trivial
                super().__init__()

        class RulesCollection(list):
            """Tiny RulesCollection compatible with test imports."""

            def __init__(self, *items):
                super().__init__(items)

        _rules.AnsibleLintRule = AnsibleLintRule
        _rules.RulesCollection = RulesCollection
        _rules.__dsu_shim__ = True

# Expose as package attributes so `from ansiblelint.rules import ...` works
rules = _rules
errors = _errors
file_utils = _file_utils

# If we created any test-only fallbacks, emit an auditable, tagged log entry
# following project audit/logging conventions (non-sensitive, structured).
try:
    _created_shims = [
        name for name, mod in (
            ('errors', _errors), ('file_utils', _file_utils), ('rules', _rules)
        )
        if getattr(mod, '__dsu_shim__', False)
    ]

    if _created_shims:
        # Determine activation reason(s)
        _reasons = []
        if os.environ.get('DSU_ALLOW_ANSIBLELINT_SHIM'):
            _reasons.append('env_override')
        if 'pytest' in sys.modules or os.environ.get('PYTEST_CURRENT_TEST'):
            _reasons.append('pytest')
        if os.environ.get('CI'):
            _reasons.append('ci')
        if _import_originates_from_repo():
            _reasons.append('repo_import')
        if not _reasons:
            _reasons.append('unknown')

        # Find the first repo-local caller frame (if any)
        _origin = None
        for fr in inspect.stack():
            fn = getattr(fr, 'filename', None)
            if not fn:
                continue
            try:
                p = Path(fn).resolve()
            except Exception:
                continue
            if _repo_root == p or _repo_root in p.parents:
                _origin = str(p)
                break

        # Gather DSU rule ids present in ansiblelint/rules (for auditability)
        _affected_rules: list[str] = []
        try:
            _rules_dir = Path(__file__).resolve().parent / 'rules'
            if _rules_dir.exists():
                for _f in _rules_dir.glob('*.py'):
                    try:
                        _txt = _f.read_text(encoding='utf-8')
                    except Exception:
                        continue
                    m = re.search(r"id\s*=\s*['\"](DSU\d+)['\"]", _txt)
                    if m:
                        _affected_rules.append(m.group(1))
        except Exception:
            _affected_rules = []

        # Structured, non-sensitive audit log message
        _logger = logging.getLogger('dsu.ansiblelint_shim')
        _logger.info(
            f"DSU-SHIM: ansiblelint shim activated; shims={_created_shims}; "
            f"reason={','.join(sorted(set(_reasons)))}; origin={_origin}; "
            f"affected_rules={sorted(_affected_rules)}; tag=DSU-SHIM"
        )
except Exception:
    # Never let logging/audit attempt raise during import — keep shim robust.
    pass

# Only re-export convenience symbols when available (avoid leaking stubs)
AnsibleLintRule = getattr(rules, 'AnsibleLintRule', None)
RulesCollection = getattr(rules, 'RulesCollection', None)
MatchError = getattr(errors, 'MatchError', None)
Lintable = getattr(file_utils, 'Lintable', None)

# Harden __all__ to list only available/public symbols
__all__ = [
    name for name in (
        'rules', 'errors', 'file_utils', 'AnsibleLintRule',
        'RulesCollection', 'MatchError', 'Lintable',
    )
    if globals().get(name) is not None
]
