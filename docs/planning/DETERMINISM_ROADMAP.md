# Determinism & Hardening Roadmap

> This document captures the gaps identified in the sterile reassessment and outlines the path to full environment determinism and supply-chain hardening.

## Current State (Feb 2026)

| Category | Status | Notes |
|----------|--------|-------|
| Collection versions | ✅ Pinned | Exact versions in requirements.yml |
| CI Actions | ✅ Pinned | @v4, @v6, @v2 |
| Secrets scanning | ✅ Active | gitleaks + detect-secrets |
| Structure | ✅ Coherent | Runtime/validation separation |
| .ansible/ | ✅ Ignored | No vendored collections |

## Gaps Identified

### 1. Python Dependency Pinning

**Current**: Unknown if pip dependencies are pinned
**Gap**: No hash verification for Python packages
**Impact**: Non-deterministic CI environment

**Action Items**:
- [ ] Audit `requirements.txt` for pinned versions
- [ ] Consider adding `requirements-lock.txt` with hashes
- [ ] Or use `pip-compile` with `--generate-hashes`

### 2. Action SHA Pinning

**Current**: `@v4`, `@v6` (major version pins)
**Gap**: Not immutable - floats within major version
**Impact**: Potential supply-chain compromise within tag

**Action Items**:
- [ ] Pin actions to commit SHA in CI workflows
- Example: `uses: actions/checkout@8c317e8c4f0ebdd1dd8cb1d17ffe186c2bf1a4e9`

### 3. Branch Protection & Governance

**Current**: Unknown if branch protection rules exist
**Gap**: CI presence ≠ enforcement
**Impact**: PRs could be merged without required checks

**Action Items**:
- [ ] Verify branch protection rules on `main`
- [ ] Ensure required status checks are enforced
- [ ] Require admin bypass be disabled

### 4. Execution Isolation

**Current**: No documented guards
**Gap**: Risk of misconfigured play running against unintended hosts
**Impact**: Accidental production modifications

**Action Items**:
- [ ] Verify no implicit `all` hosts in playbooks
- [ ] Add safety confirmations for production runs
- [ ] Document inventory separation strategy

### 5. Coverage & Idempotence

**Current**: Molecule tests exist
**Gap**: No coverage thresholds, no idempotence gating
**Impact**: Incomplete validation

**Action Items**:
- [ ] Add `molecule --coverage` to CI
- [ ] Set minimum coverage threshold
- [ ] Add idempotence test step in CI

### 6. Threat Model Documentation

**Current**: Not documented
**Gap**: Blind spot in adversarial evaluation
**Impact**: Undefined trust boundaries

**Action Items**:
- [ ] Document trust boundary between CI and targets
- [ ] Define who can modify playbooks
- [ ] Document credential model (SSH, vault, etc.)
- [ ] Document vault password management

## Priority Recommendations

### High Priority (Immediate)
1. Verify branch protection rules exist
2. Add idempotence to CI gates
3. Document inventory isolation

### Medium Priority (This Quarter)
4. Pin CI actions to SHA
5. Add coverage thresholds
6. Create threat model document

### Low Priority (Backlog)
7. Python dependency hash locking
8. Artifact retention policy
9. Semantic versioning strategy

## Maturity Targets

| Level | Description | Target Date |
|-------|-------------|--------------|
| Current | Structurally competent | - |
| Next | Governance confirmed | Q2 2026 |
| Target | Adversarially evaluated | Q3 2026 |

---

*Last Updated: 2026-02-15*
