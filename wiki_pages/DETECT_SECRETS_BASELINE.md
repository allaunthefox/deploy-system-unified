# DETECT_SECRETS_BASELINE

Purpose
- Keep CI actionable by recording *benign* findings so Detect‑Secrets only blocks on real secrets.

When to add entries to `.secrets.baseline`
- Test fixtures, molecule scenarios, sample or example credential values used only in CI or tests.
- Generated or placeholder values in charts/templates/docs (examples, sample env files).
- Static artifacts that are provably non‑secret (e.g., intentionally mocked values used by tests).

When NOT to add entries
- Any file that contains production credentials, private keys, passwords, or secrets used by real systems (e.g. `inventory/group_vars/*`, `roles/*/defaults` that map to production values unless provably safe).
- Files that could contain real customer data or secrets.

Required PR process for baseline changes
1. Add the baseline update (commit or generated file) to your branch.
2. In the PR description include:
   - The `filename` and `hashed_secret` values you added.
   - A short justification why the finding is benign (e.g. "molecule fixture, not used in production").
   - A code snippet or link showing the affected lines.
3. Request review from a maintainer or security approver; **do not** merge until a reviewer confirms the justification.

Best practices
- Prefer workflow excludes (directory/file) for clearly non‑secret folders (e.g. `branch_templates/`, `molecule/negative/`) instead of adding many individual hashes.
- If a baseline entry later becomes a real secret, remove it from the baseline and rotate the secret immediately.

Commands / troubleshooting
- Run a fresh scan locally:
  detect-secrets scan --all-files > .secrets.baseline
- To diff a temporary baseline against the committed baseline:
  detect-secrets scan --baseline /tmp/baseline && jq -r '.results | keys' .secrets.baseline

Template PR justification (copy into your PR body)
```
Triage: added hashed entry `HASH` for `path/to/file` to .secrets.baseline.
Justification: molecule test fixture / placeholder value; not used in production.
Reviewer: @maintainer
```

Questions? Ping the repo maintainers or open an issue titled "Detect‑Secrets baseline: <short reason>".
