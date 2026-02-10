# CONTRIBUTING

We welcome contributions to Deploy-System-Unified! This document outlines the process for contributing code, documentation, and other improvements.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct.

## How Can I Contribute?

### Reporting Bugs

- Ensure the bug was not already reported
- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps

### Pull Requests

- Fill in the pull request template
- Follow the existing code style
- Update documentation as needed
- Add tests if applicable

### Branch Templates

- When creating profile deployments, consider using the templates in `branch_templates/`
- Copy the appropriate template to your own deployment directory (separate from this repository)
- These templates provide starting points for different use cases (ephemeral, production, development)
- Remember that the main repository serves as a base layer with roles and base functionality
- **Policy:** `projects/deploy-system-unified/main.yml` must remain a pristine base and **must not** include a top-level `roles:` list. Use `branch_templates/` for role-based deployments; CI will enforce this policy.

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Development Setup

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Submit a pull request
