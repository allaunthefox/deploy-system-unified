# Python Accessibility Standards

This document establishes accessibility standards for Python code in this project, ensuring consistency, maintainability, and reliability across all modules and test files.

## Table of Contents

1. [Module Imports and Dependencies](#module-imports-and-dependencies)
2. [Circular Imports and Type Checking](#circular-imports-and-type-checking)
3. [Mocking Best Practices](#mocking-best-practices)
4. [Type Hinting Requirements](#type-hinting-requirements)
5. [Documentation Standards](#documentation-standards)
6. [Accessibility Implementation](#accessibility-implementation)
7. [Error Handling Standards](#error-handling-standards)
8. [Test Accessibility Guidelines](#test-accessibility-guidelines)

---

## Module Imports and Dependencies

### Import Order

Imports must follow this strict order (per PEP 8):

```python
# 1. Standard library imports
import os
import sys
import json
from typing import List, Dict, Optional

# 2. Third-party imports
import pytest
from unittest.mock import Mock, patch, MagicMock

# 3. Local application imports
from mymodule import MyClass, my_function
```

### Relative vs Absolute Imports

- **Always use absolute imports** for better readability and maintainability:
  ```python
  # ✓ Good
  from deploy_system_unified.module import function_name
  
  # ✗ Avoid (unless in package __init__.py)
  from .module import function_name
  ```

### Handling Missing Dependencies

When a module may not be available, use conditional imports with clear error messages:

```python
def get_optional_dependency():
    """Get optional dependency or raise informative error."""
    try:
        import optional_module
        return optional_module
    except ImportError:
        raise ImportError(
            "optional_module is required for this feature. "
            "Install with: pip install optional-package"
        )

---

## Circular Imports and Type Checking

When two modules need each other for type hints but not at runtime, use the `TYPE_CHECKING` guard:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .other_module import OtherClass

def process(obj: 'OtherClass'):
    pass
```

This prevents runtime circular dependencies while allowing static analysis tools like `mypy` and `ruff` to verify types.

---

## Mocking Best Practices

### Using unittest.mock Properly

Always import from the correct module location:

```python
# ✓ Correct - unittest.mock is the standard
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from unittest.mock import mock_open, call, ANY

# ✗ Incorrect - wrong module path
from mock import Mock  # External mock package
```

### Common Mock Patterns

```python
# Mocking a function
with patch('module.path.function_name') as mock_func:
    mock_func.return_value = expected_result
    # test code...

# Mocking a class
with patch('module.path.ClassName') as MockClass:
    instance = MockClass.return_value
    instance.method.return_value = 'mocked'
    # test code...

# Mocking async functions
with patch('module.path.async_function', new_callable=AsyncMock) as mock_async:
    await mock_async()
    # test code...

# Mocking multiple items
with patch('module.func1'), patch('module.func2'), patch('module.Class'):
    # test code...
```

### Mock Return Values

```python
# Simple return value
mock_obj = Mock()
mock_obj.method.return_value = 'result'

# Raising exceptions
mock_obj = Mock()
mock_obj.method.side_effect = ValueError("Invalid input")

# Iterating return values
mock_obj = Mock()
mock_obj.method.side_effect = ['first', 'second', 'third']
```

---

## Type Hinting Requirements

### Basic Type Hints

All function parameters and return values must have type hints:

```python
# ✓ Good
def process_data(items: List[str], config: Dict[str, int]) -> Optional[str]:
    pass

def calculate(x: float, y: float) -> float:
    pass

# ✗ Bad - missing type hints
def process_data(items, config):
    pass
```

### Complex Type Hints

Use appropriate typing constructs for complex scenarios:

```python
from typing import List, Dict, Optional, Union, Callable, TypeVar, Any

# Optional (can be None)
name: Optional[str] = None

# Union types
result: Union[str, int, None] = None

# TypeVar for generics
T = TypeVar('T')

def get_first(items: List[T]) -> Optional[T]:
    return items[0] if items else None

# Callable types
callback: Callable[[int, str], bool] = lambda x, y: True

# Any for untyped code
unknown: Any = "can be anything"
```

---

## Documentation Standards

### Docstring Format

Use Google-style or NumPy-style docstrings consistently:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short one-line summary.

    Longer description if needed. Can span multiple lines.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param2 is negative.
        TypeError: When param1 is not a string.

    Example:
        >>> result = function_name("hello", 5)
        >>> print(result)
        True
    """
```

### Module-Level Documentation

Every Python file should have a module docstring:

```python
"""Module name and brief description.

This module provides functionality for...
"""

# Module constants/variables (if any)
__version__ = "1.0.0"
__all__ = ["public_function", "PublicClass"]

---

## Accessibility Implementation

### AccessibleTool Interface

All tools requiring user interaction or output must inherit from `AccessibleTool` and implement its methods:

- `announce_to_assistive_tech`: Direct output to screen readers.
- `format_for_accessibility`: Convert complex data to clear textual descriptions.
- `get_accessible_status`: Provide a concise summary of the tool's health.

### UI Component Accessibility (WCAG 2.2 AA Compliant)

TUI components (Menu, Form, List, etc.) MUST be navigable by keyboard only and provide clear focus indicators. Avoid relying solely on color to convey information.

### 2025/2026 Accessibility Enhancements

#### WCAG 2.2 AA Requirements
- **Focus Appearance (2.4.11)**: Focus indicator must have minimum 3:1 contrast ratio and cover at least 1px border area
- **Focus Not Obscured (2.4.12)**: Focused element must not be fully hidden by other content
- **Target Size Minimum (2.5.8)**: Interactive elements must be at least 24x24 CSS pixels
- **Draggable Movements (2.5.4)**: Provide alternative for drag operations

#### ARIA Live Regions for CLI/TUI
```python
# Dynamic output should announce to assistive technology
def announce_to_assistive_tech(self, message: str, priority: str = "polite"):
    """Announce message to screen readers.
    
    Args:
        message: The message to announce
        priority: 'polite' (waits for silence) or 'assertive' (interrupts)
    """
    # For TUI: use terminal escape sequences
    # For CLI: print to stderr with appropriate markers
    print(f"\033[{priority}_announce:{message}\033[/announce]", file=sys.stderr)
```

#### Keyboard Navigation Requirements
- All interactive elements accessible via Tab
- Arrow keys for menu navigation
- Enter/Space for activation
- Escape for cancellation/close
- Home/End for list navigation

#### Color and Visual Accessibility
- Color contrast minimum 4.5:1 for normal text
- Color contrast minimum 3:1 for large text (18pt+ or 14pt bold)
- Never use color alone to convey information
- Provide text labels for all icon-only buttons

---

## Error Handling Standards

### Exception Handling

```python
# ✓ Good - specific exception handling
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise CustomError("Operation failed") from e
except (IOError, OSError) as e:
    logger.error(f"IO error: {e}")
    raise

# ✗ Bad - bare except (never do this)
try:
    result = risky_operation()
except:
    pass
```

### Custom Exceptions

```python
class DeploymentError(Exception):
    """Base exception for deployment-related errors."""
    pass

class ConfigurationError(DeploymentError):
    """Raised when configuration is invalid."""
    pass

class ValidationError(DeploymentError):
    """Raised when validation fails."""
    def __init__(self, message: str, field: str = ""):
        super().__init__(message)
        self.field = field
```

---

## Test Accessibility Guidelines

### Test File Structure

```python
"""Tests for module_name module.

These tests verify the functionality of...
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestFunctionName:
    """Tests for function_name."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_data = {"key": "value"}

    def teardown_method(self):
        """Clean up after tests."""
        pass

    def test_basic_case(self):
        """Test basic functionality."""
        # Arrange
        expected = "result"

        # Act
        result = function_to_test("input")

        # Assert
        assert result == expected

    def test_edge_case(self):
        """Test edge case handling."""
        # Test with empty input
        result = function_to_test("")
        assert result is None

    @patch('module.function')
    def test_with_mock(self, mock_func):
        """Test with mocked function."""
        mock_func.return_value = "mocked"
        result = function_to_test("test")
        assert result == "mocked"
        mock_func.assert_called_once_with("test")
```

### Test Naming

- Use descriptive test names: `test_function_name_scenario`
- Group related tests in classes
- Include docstrings explaining what's being tested

### Avoiding Common Pitfalls

```python
# ✗ Don't import from wrong locations
# Wrong - may not exist or be outdated
from mock import Mock  

# ✓ Correct - standard library
from unittest.mock import Mock


# ✗ Don't forget to patch at the correct location
# Wrong - patches where it's imported, not where it's used
from module import function_to_test

@patch('function_to_test')  # Wrong!
def test_something(mock_func):
    pass

# ✓ Correct - patch where it's used
@patch('module.function_to_test')  # Correct!
def test_something(mock_func):
    pass
```

---

## Code Style Guidelines

### General Rules (PEP 8)

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Whitespace**: Around operators, after commas
- **Naming**: 
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

### Pre-commit Hooks

Configure pre-commit to catch issues early:

```yaml
# .pre-commit-config.yaml
# Updated: 2026-02-24 with 2025/2026 tooling

repos:
  # ===== PYTHON LINTING =====
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120, --ignore=E501,W503]

  # ===== PYTHON FORMATTING =====
  - repo: https://github.com/psf/black
    rev: 25.1.0
    hooks:
      - id: black
        args: [--line-length=120]

  # ===== IMPORT SORTING =====
  - repo: https://github.com/pycqa/isort
    rev: 5.14.0
    hooks:
      - id: isort
        args: [--profile=black, --line-length=120]

  # ===== YAML/JSON LINTING =====
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: detect-private-key
      - id: trailing-whitespace
      - id: end-of-file-fixer

  # ===== SECRET DETECTION =====
  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.93.3
    hooks:
      - id: trufflehog
        args: [--only-verified]

  # ===== SHELL SCRIPT LINTING =====
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.10.0.1
    hooks:
      - id: shellcheck

  # ===== IaC SECURITY SCANNING =====
  - repo: https://github.com/checkov/checkov
    rev: 3.2.300
    hooks:
      - id: checkov
        args: [--directory, ., --framework, ansible]

  # ===== VULNERABILITY DETECTION =====
  - repo: https://github.com/google/osv-scanner
    rev: v1.9.0
    hooks:
      - id: osv-scanner
        args: [--recursive, .]
```

---

## Summary

Following these standards ensures:

1. **Consistency**: All code follows the same patterns
2. **Maintainability**: Clear structure makes code easier to modify
3. **Reliability**: Proper mocking and error handling prevents test failures
4. **Accessibility**: Type hints and documentation make code approachable

When writing new code or fixing existing issues, always reference this document to ensure compliance with project standards.

---

*Last Updated: 2026-02-24*
*Version: 1.2.0*
