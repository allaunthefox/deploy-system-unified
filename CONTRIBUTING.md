# Contributing to deploy-system-unified

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

Please read and follow my [Code of Conduct](CODE_OF_CONDUCT.md) to maintain a welcoming and inclusive community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/deploy-system-unified.git`
3. Create a branch: `git checkout -b feature/your-feature-name`

## How to Contribute

### Reporting Bugs

- Use the bug report issue template
- Include steps to reproduce
- Provide environment details (Ansible version, OS, etc.)
- Attach relevant logs if applicable

### Suggesting Features

- Use the feature request issue template
- Describe the use case
- Explain why this feature would be useful

### Submitting Code

- Follow existing code style and conventions
- Write clear commit messages
- Include tests where applicable
- Update documentation as needed

## Development Setup

### Prerequisites

- Ansible >= 2.9
- Python 3.8+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/allaunthefox/deploy-system-unified.git
cd deploy-system-unified

# Install dependencies (if any)
pip install -r requirements.txt

# Set up Ansible configuration
export ANSIBLE_CONFIG=$(pwd)/ansible.cfg
```

## Testing

Before submitting changes, please ensure your code passes all tests:

```bash
# Run Ansible lint
ansible-lint

# Run syntax check
ansible-playbook --syntax-check your_playbook.yml

# Run tests (if test suite exists)
./run_tests.sh
```

## Submitting Changes

1. Ensure your code follows the style guidelines
2. Run all tests and verify they pass
3. Update documentation if needed
4. Commit your changes with clear messages
5. Push to your fork
6. Open a Pull Request

## Commit Guidelines

We follow conventional commit messages:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Maintenance tasks

Example:
```
feat: add new hardening role for web servers

- Implement CIS benchmark compliance checks
- Add firewall configuration
- Include security headers for nginx
```

## Pull Request Process

1. **Create PR**: Open a pull request with a clear title and description
2. **Link Issues**: Reference any related issues
3. **Review**: I will review your PR as soon as possible
4. **Address Feedback**: Make any requested changes
5. **Approval**: Once approved, I will merge your PR

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear and descriptive
- [ ] Changes are tested and working

## Questions?

If you have questions, please:
- Check existing issues and documentation
- Open a new issue for discussion

Thank you for contributing to this project!
