# Contributing to Deploy-System-Unified

Thank you for your interest in contributing to Deploy-System-Unified! We welcome contributions from the community to help make this project better.

## Getting Started

1.  **Fork the repository** on GitHub/Codeberg.
2.  **Clone your fork** locally.
3.  **Create a new branch** for your feature or fix: `git checkout -b feat/my-feature`.

## Development Guidelines

### Code Style
- **Ansible**: We follow `ansible-lint` strict rules. Run `ansible-lint` before submitting.
- **Python**: Scripts should follow PEP 8.
- **Markdown**: Documentation should be clear and follow GFM (GitHub Flavored Markdown).

### Testing
- **Idempotence**: All roles must be idempotent. Run `scripts/verify_idempotence.sh` to verify.
- **Preflight**: Changes must pass `playbooks/preflight_validate.yml`.
- **Secrets**: Never commit secrets. Use SOPS/Age for secret management.

## Pull Request Process

1.  Ensure your code passes all local tests.
2.  Update documentation if you are changing behavior.
3.  Submit a Pull Request with a clear description of the change.
4.  Link to any relevant issues (e.g., `Closes #123`).

## Reporting Issues

- Use the Issue Tracker to report bugs or request features.
- Provide clear reproduction steps for bugs.
- Include relevant logs and environment details.

## License

By contributing, you agree that your contributions will be licensed under the project's license (MIT/Apache 2.0).
