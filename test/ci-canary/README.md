# CI Canary Test Directory

This directory contains intentionally bad files to verify that CI workflows correctly detect issues.

## Files

| File | Purpose |
|------|---------|
| `bad_style_and_secrets.yml` | Triggers yamllint errors + detect-secrets |
| `bad_script.sh` | Triggers shellcheck violations + detect-secrets |
| `bad_playbook.yml` | Triggers ansible-lint violations |

## Expected CI Failures

After pushing these files, the following workflows should fail:

1. **Detect Secrets**: Should find fake AWS keys, API tokens, passwords
2. **Style Enforcement**: Should find yamllint and ansible-lint violations
3. **ShellCheck** (if enabled): Should find shell script issues

## Cleanup

Once CI detection is verified, remove this directory:
```bash
git rm -rf test/ci-canary
git commit -m "test: remove CI canary files after verification"
git push
```
