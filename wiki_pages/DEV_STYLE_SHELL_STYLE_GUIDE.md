# Shell_Style_Guide

To maintain consistency and ensure clean linting for shell scripts in the Deploy-System-Unified project, all contributions must adhere to the following style requirements.

## Shell Script Standards

* **Shebang**: Always start shell scripts with appropriate shebang (e.g., `#!/bin/bash`).
* **ShellCheck**: All shell scripts must pass ShellCheck linting without warnings.
* **Quoting**: Always quote variables to prevent word splitting and pathname expansion.
* **Variables**: Use lowercase for local variables and UPPERCASE for environment variables.
* **Functions**: Use functions to organize code and avoid repetition.
* **Error Handling**: Implement proper error handling with `set -euo pipefail` when appropriate.
* **Portability**: Write portable shell scripts when possible, avoiding bashisms unless necessary.

## Best Practices

* **Comments**: Include comments to explain complex logic.
* **Parameter Expansion**: Use parameter expansion instead of external commands when possible.
* **Security**: Validate inputs and avoid injection vulnerabilities.
* **Performance**: Optimize for performance where critical.

## Linting

These standards are enforced via the `make lint` suite. All shell scripts must pass linting checks before acceptance.