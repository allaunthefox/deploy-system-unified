# DETERMINISM_ROADMAP

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

### 7. Implicit Settings Remediation (NEW - Feb 2026)

**Current**: Extensive use of implicit defaults, cascading variables, and profile-based conditionals
**Gap**: Configuration behavior depends on execution order, variable precedence, and inherited defaults
**Impact**: Audit complexity, potential security gaps, operator confusion, non-deterministic deployments

**Identified Implicit Patterns**:

| Pattern | Example | Risk Level |
|---------|---------|------------|
| **Cascading Variable Overrides** | `system_ssh_port` defined in multiple files with different precedence | HIGH |
| **Profile-Based Implicit Logic** | `deployment_profile: hardened` implicitly enables 10+ features | HIGH |
| **Fail-Secure Inheritance Chains** | 99 `fail_secure` references across codebase with complex inheritance | MEDIUM |
| **Empty Checksum "Verification"** | GPG verification enabled but checksums empty (`""`) | CRITICAL |
| **Container Runtime Implicit Modes** | Rootful vs rootless determines 6+ system paths and ports | MEDIUM |
| **Architecture Auto-Detection** | GPU slicing strategy auto-resolves based on virtualization | LOW |
| **Secrets Provider Selection** | `secrets_provider_mode` implicitly disables vault/sops validation | MEDIUM |
| **Ephemeral Profile Guards** | 5+ features implicitly disabled unless explicitly allowed | MEDIUM |
| **Network Attachment Assumptions** | Caddy implicitly attached to all container networks | LOW |
| **TCP Forwarding Logic** | `sshd_allow_tcp_forwarding: false` but trusted groups allowed | MEDIUM |

**Action Items**:
- [ ] **Phase 1: Audit & Document** (Q2 2026)
  - [ ] Create variable precedence diagram showing override chains
  - [ ] Document all profile-based implicit behaviors in a single reference
  - [ ] Generate dependency graph for cascading variables
  - [ ] Audit all empty checksums and resolve contradictions
- [ ] **Phase 2: Consolidate** (Q3 2026)
  - [ ] Move profile-based conditionals to `profiles/` directory with explicit mappings
  - [ ] Create single source of truth for `fail_secure` inheritance chain
  - [ ] Replace cascading defaults with explicit assertions in preflight checks
  - [ ] Populate missing checksums or disable verification toggles
- [ ] **Phase 3: Enforce** (Q4 2026)
  - [ ] Add preflight assertions for all critical implicit settings
  - [ ] Require explicit declaration of effective values in deployment logs
  - [ ] Create "configuration effective value" report at playbook start
  - [ ] Add CI check for undocumented implicit variable dependencies

## Priority Recommendations

### High Priority (Immediate)
1. Verify branch protection rules exist
2. Add idempotence to CI gates
3. Document inventory isolation
4. **NEW: Audit empty checksums in `hardened_supply_chain.yml` (CRITICAL security gap)**

### Medium Priority (This Quarter)
4. Pin CI actions to SHA
5. Add coverage thresholds
6. Create threat model document
7. **NEW: Create variable precedence documentation**
8. **NEW: Document all profile-based implicit behaviors**

### Low Priority (Backlog)
7. Python dependency hash locking
8. Artifact retention policy
9. Semantic versioning strategy
10. **NEW: Consolidate profile conditionals to explicit mappings**
11. **NEW: Add preflight assertions for implicit settings**
12. **NEW: Generate configuration effective value reports**

## Maturity Targets

| Level | Description | Target Date |
|-------|-------------|--------------|
| Current | Structurally competent | - |
| Next | Governance confirmed | Q2 2026 |
| Target | Adversarially evaluated | Q3 2026 |
| **Enhanced** | **Explicit configuration (all implicit settings documented)** | **Q4 2026** |
| **Hardened** | **Explicit configuration (all implicit settings enforced via assertions)** | **Q1 2027** |

---

*Last Updated: 2026-02-25*
