# Repository Security & Best Practices Checklist

This document outlines all items that should be scanned and potentially removed from a GitHub repository for security and best practices.

---

## 1. Authentication Credentials

### Must Never Be in Repo
| Pattern | Description | Action |
|---------|------------|--------|
| `password=*` | Password assignments | REMOVE immediately |
| `api_key=*` | API keys | REMOVE immediately |
| `apikey=*` | API keys (alternate) | REMOVE immediately |
| `token=*` | Auth tokens | REMOVE immediately |
| `secret=*` | Secrets | REMOVE immediately |
| `private_key` | SSH private keys | REMOVE immediately |
| `-----BEGIN RSA PRIVATE KEY-----` | RSA keys | REMOVE immediately |
| `AWS_ACCESS_KEY_ID` | AWS credentials | REMOVE immediately |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials | REMOVE immediately |
| `GITHUB_TOKEN` | GitHub tokens | REMOVE immediately |
| `GITHUB_API_TOKEN` | GitHub tokens | REMOVE immediately |

### Check These Files
- `.env` - Environment variables
- `.env.local` - Local environment
- `config.py` - Configuration files
- `settings.py` - Django/settings files
- `credentials.json` - Service account files
- `*.pem` - Certificate files

---

## 2. Editor & IDE Settings

### Should Be Gitignored
| Directory/File | Description |
|---------------|-------------|
| `.vscode/` | Visual Studio Code settings |
| `.idea/` | IntelliJ/PyCharm settings |
| `.atom/` | Atom editor settings |
| `.sublime*` | Sublime Text settings |
| `*.swp` | Vim swap files |
| `*~` | Backup files |
| `.clinerules/` | AI personal settings |

---

## 3. Python Build & Cache Files

### Must Be Gitignored
| Pattern | Description |
|---------|-------------|
| `__pycache__/` | Python bytecode cache |
| `*.py[cod]` | Compiled Python files |
| `*.so` | Compiled extensions |
| `*.egg-info/` | Package metadata |
| `dist/` | Distribution builds |
| `build/` | Build outputs |
| `.pytest_cache/` | Pytest cache |
| `.mypy_cache/` | Mypy cache |
| `.ruff_cache/` | Ruff cache |
| `.hypothesis/` | Hypothesis test cache |

---

## 4. Sensitive Project Files

### Should Not Be Committed
| File | Reason |
|------|--------|
| `*.log` | May contain sensitive data |
| `*.db` | Local databases |
| `*.sqlite` | SQLite databases |
| `*.sqlite3` | SQLite databases |
| `secrets.toml` | Secret configurations |
| `credentials.json` | Service credentials |
| `serviceAccount.json` | GCP credentials |

---

## 5. CI/CD Sensitive Data

### Check Workflows (.github/workflows/)
- Never hardcode secrets in YAML
- Use GitHub Secrets

---

## 6. Git-Specific Files

### Should Not Be Committed
| File | Reason |
|------|--------|
| `.git/` (in repo) | Never commit .git directory |
| `*.rbc` | Ruby bytecode |
| `.gitignore` | Check it's comprehensive |

---

## 7. Large Binary Files

### Should Not Be Committed
| Type | Recommendation |
|------|----------------|
| Images >1MB | Use Git LFS |
| Videos | Use Git LFS |
| Datasets | Use external storage |
| Model weights | Use external storage |

---

## 8. Pre-Commit Security Scan Commands

### Quick Scan
```bash
grep -r "password\s*=" --include="*.py" .
grep -r "api_key\s*=" --include="*.py" .
grep -r "token\s*=" --include="*.py" .
grep -r "secret\s*=" --include="*.py" .
```

---

## 9. If Compromised - Recovery Steps

### Immediate Actions
1. **Revoke exposed credentials** - Reset all exposed API keys/passwords
2. **Force push clean history** - Use git-filter-repo:
   ```bash
   git filter-repo --replace-text patterns.txt --force
   ```

---

## 10. Recommended .gitignore Template

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Environments
.env
.env.local
.venv
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Logs & Databases
*.log
*.db
*.sqlite
*.sqlite3

# Project specific
output/
.coverage
coverage.xml
```

---

---

# Audit Log - Completed Actions

## 2026-02-16 Actions Taken
1. ✅ Cleaned NoDupeLabs - removed .vscode, .clinerules, scrubbed git history
2. ✅ Audited all GitHub repos (allaunthefox account)
3. ✅ Cleaned SystemBackups - removed database files from git history

## 2026-02-19 Actions Taken
1. ✅ **Ansible Configuration Hardening**: Isolated collections to `.collections` via `ansible.cfg` and resolved duplicate keys in YAML that crashed security linters.
2. ✅ **Lint Enforcement**: Achieved 100% clean pass for `ansible-lint` and `ruff` on all active codebase paths.
3. ✅ **Logic Verification**: Reached 100% test coverage for critical security logic files (`validator_logic.py`, `codes.py`).
4. ✅ **Pipeline Stability**: Fixed deadlocks in `time_sync` background tests that were blocking security gating in CI.

## Repos Audited
- NoDupeLabs: ✅ SECURE
- deploy-system-unified: ✅ SECURE (uses SOPS encryption)
- lastingfirst-infra: ✅ SECURE
- lastingfirst-website: ✅ SECURE
- nix-template: ✅ SECURE
- RpiZero-Scale: ✅ SECURE
- SystemBackups: ✅ NOW CLEANED

## Security Gates Added
| Feature | NoDuPeLabs | deploy-system | lastingfirst | nix | SystemBackups | RpiZero | website |
|---------|-------------|--------------|-------------|-----|---------------|----------|---------|
| TruffleHog | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Secret Scanning | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Dependabot | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Super-Linter | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| OSSF Scorecard | ✅ | - | - | - | - | - | - |
| SecureStack SBOM | ✅ | - | - | - | - | - | - |
| Vault Integration | - | ✅(branch) | - | - | - | - | - |

**Last Updated**: 2026-02-19
