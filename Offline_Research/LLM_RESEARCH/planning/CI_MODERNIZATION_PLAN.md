# CI Modernization and Remediation Plan

## Objective
Establish a strict, modern, and reliable CI/CD pipeline that enforces project standards (Style Guide, Security, and Functional Correctness).

## Status Overview
- **CI Parsing & Execution**: ✅ FIXED (Root workflows modernized)
- **Secret Detection**: ✅ FIXED (Audited baseline implemented)
- **Style Enforcement**: ⚠️ PARTIAL (Workflows active; 12 manual fixes pending)
- **GitHub Pages**: ⚠️ PARTIAL (CI fixed; deployment awaiting Settings change)

## Completed Modernization
- **Strict Standards**: Defined `permissions`, `timeout-minutes`, and specific Action versions (`@v4`, `@v5`).
- **Secret Baseline**: Audited `.secrets.baseline` to ignore known false positives while catching new exposures.
- **Workflow Isolation**: Fixed location mismatch; workflows now reside and run from `.github/workflows/`.
- **Pages Optimization**: Implemented staging area to exclude heavy binary research data from web deployment.

## Planned Remediations (Backlog)

### 1. Style Guide Violations (Manual Fixes Required)
The following 12 issues were identified by the `enforce_style_guide.sh` tool:
- [ ] **FQCN Compliance**: 52 non-FQCN module calls across Ansible roles.
- [ ] **YAML Refinement**: Final manual review of line lengths in `detect-secrets.yml`.
- [ ] **Ansible Lint**: Review `community.general` and `ansible.posix` collection versions in the runner environment.

### 2. Infrastructure Configuration
- [ ] **GitHub Pages**: User must enable GitHub Pages deployment in Repository Settings.
- [ ] **Runners**: Periodically verify Python 3.11+ availability on standard Ubuntu runners.

### 3. CI/CD Evolution
- [ ] **Pre-commit Integration**: Integrate `enforce_style_guide.sh` as a local pre-commit hook.
- [ ] **Security Scanning**: Add `gitleaks` as a secondary safety check for non-baseline patterns.

## Performance Metrics
- **Detect Secrets**: ~40s
- **Style Enforcement**: ~25s
- **Deploy Pages (Upload)**: ~15s (Optimized from 0s failure)
