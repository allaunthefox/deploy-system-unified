# Local ansiblelint extension package for project-specific rules
# Re-export selected submodules from the installed 'ansiblelint' package so
# local rule modules can import ansiblelint.errors, file_utils, etc. during
# tests without needing to modify existing test imports.
import importlib

try:
    errors = importlib.import_module('ansiblelint.errors')
    file_utils = importlib.import_module('ansiblelint.file_utils')
    rules = importlib.import_module('ansiblelint.rules')
except Exception:
    # If installed ansiblelint is not available in the environment, tests that
    # rely on its classes should import directly or handle the missing pieces.
    pass

__all__ = ['rules', 'errors', 'file_utils']
