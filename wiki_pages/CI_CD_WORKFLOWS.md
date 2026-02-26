# CI_CD_WORKFLOWS

The Deploy-System-Unified project utilizes a comprehensive suite of CI/CD workflows to ensure security, style compliance, and functional integrity.

## 🚀 GitHub Actions

Located in `.github/workflows/`, these workflows are triggered on push and pull requests to the `main` branch.

### 🔒 Security & Integrity
- **`detect-secrets.yml`**: Scans the codebase for hardcoded secrets and credentials using `detect-secrets`.
- **`negative-tests.yml`**: Executes negative security tests to verify that roles fail gracefully (and securely) when secrets are missing or misconfigured.
- **`ssh-policy-tests.yml`**: Validates SSH configuration against project-defined security policies.
- **`sshd-idempotence.yml`**: Specifically tests the idempotency of SSH daemon configurations.

### 🛠 Linting & Style
- **`style-enforcement.yml`**: Runs `enforce_style_guide.sh` to ensure all YAML, shell, and Ansible files adhere to project standards.
- **`wiki-lint.yml`**: Validates wiki Markdown files for broken links, header consistency, and structure.

### 📖 Wiki Management
- **`wiki-publish.yml` / `wiki-publish-auto.yml`**: Automates the synchronization of the `wiki_pages/` directory with the repository's GitHub/Codeberg wiki.
- **`wiki-pr-check.yml`**: Validates wiki changes within Pull Requests.
- **`test-wiki-pat.yml`**: Utility to verify the Personal Access Token (PAT) used for wiki publishing.

## 🏗 Woodpecker CI

The project also supports **Woodpecker CI** (via `.woodpecker.yml`) for self-hosted or alternative CI environments, paralleling the primary GitHub Actions checks.

## 🧪 Molecule Testing

Molecule is used for role-level integration testing.
- **Converge**: Ensures the role can be applied to a clean instance.
- **Idempotence**: Verifies that a second run results in zero changes.
- **Verify**: Uses `testinfra` or Ansible assertions to validate the final state.

---
*See [Testing_Negative_IMPLEMENTATION](Testing_Negative_IMPLEMENTATION) for deep-dives into security failure testing.*
