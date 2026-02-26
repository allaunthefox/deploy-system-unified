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

---

## Updating the Wiki

Before editing wiki content or sidebar files, run the wiki linter locally to catch regressions and style issues:

```sh
python3 .scripts/wiki_wiki_lint.py --json
```

- To auto-fix H1 mismatches and create placeholders for referenced YAMLs, use:

```sh
python3 .scripts/wiki_wiki_lint.py --fix-h1 --create-placeholders
```

- Open a PR with your changes and include the linter output (JSON or summary) in the PR description. The repository has a GitHub Action (`.github/workflows/wiki-lint.yml`) that enforces wiki hygiene on PRs and pushes.

Guidelines:
- Don't change H1s without reviewer consent if it's a content/title-sensitive page.
- Use placeholder pages under `wiki_pages/` when linking to repo YAMLs or non-wiki resources.
- Use `wiki_pages/UPDATING.md` for detailed wiki-specific guidance.

## 🎓 Training & Learning

To master the orchestration patterns used in this project, we recommend completing the **Interactive Learning Lab** tutorials. These Jupyter notebooks provide hands-on experience with:
- **Test Harness Pattern**: Building verifiable AI agents.
- **Audit Event Identifier System**: Forensic naming and traceability.
- **Multi-Agent Workflows**: Orchestrating complex deployments.

👉 **[Launch Interactive Lab (14 Tutorials)](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/blob/main/tutorials/README.md)**

## Development Setup

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Submit a pull request
