# Implicit Settings Remediation Plan

**Created**: 2026-02-25  
**Status**: Planning  
**Priority**: High (Security & Determinism)

---

## Executive Summary

Deploy-System-Unified currently relies extensively on **implicit settings** through variable cascades, profile-based conditionals, and inheritance chains. While this provides flexibility, it creates:

- **Audit complexity** - Difficult to determine effective configuration values
- **Security gaps** - Defaults may not match operator expectations
- **Non-deterministic deployments** - Behavior depends on variable precedence and execution order
- **Operator confusion** - Implicit behavior not obvious from documentation

This plan outlines a phased approach to make settings **explicit where appropriate** while preserving necessary flexibility.

---

## Identified Implicit Patterns

### CRITICAL Risk

| # | Pattern | Example | Files Affected | Remediation |
|---|---------|---------|----------------|-------------|
| 1 | **Empty Checksum "Verification"** | GPG verification enabled but checksums empty (`""`) | `inventory/group_vars/all/hardened_supply_chain.yml` | Populate checksums OR set verification to `false` |

### HIGH Risk

| # | Pattern | Example | Files Affected | Remediation |
|---|---------|---------|----------------|-------------|
| 2 | **Cascading Variable Overrides** | `system_ssh_port` defined in multiple files with different precedence | `inventory/group_vars/all/os_settings.yml`, `inventory/group_vars/all/vps.yml` | Create precedence diagram, consolidate to single source |
| 3 | **Profile-Based Implicit Logic** | `deployment_profile: hardened` implicitly enables 10+ features | `inventory/group_vars/all/os_settings.yml`, 20+ role defaults files | Move to explicit `profiles/` directory with clear mappings |

### MEDIUM Risk

| # | Pattern | Example | Files Affected | Remediation |
|---|---------|---------|----------------|-------------|
| 4 | **Fail-Secure Inheritance Chains** | 99 `fail_secure` references across codebase with complex inheritance | 50+ files across all roles | Create single source of truth, simplify inheritance |
| 5 | **Container Runtime Implicit Modes** | Rootful vs rootless determines 6+ system paths and ports | `roles/containers/runtime/defaults/main.yml`, 10+ container roles | Add explicit assertions in preflight checks |
| 6 | **Secrets Provider Selection** | `secrets_provider_mode` implicitly disables vault/sops validation | `inventory/group_vars/all/secrets_config.yml`, preflight checks | Add explicit validation per provider mode |
| 7 | **Ephemeral Profile Guards** | 5+ features implicitly disabled unless explicitly allowed | `inventory/group_vars/all/os_settings.yml`, multiple role defaults | Document all guards in single reference |
| 8 | **TCP Forwarding Logic** | `sshd_allow_tcp_forwarding: false` but trusted groups allowed | `inventory/group_vars/all/vps.yml`, `roles/security/sshd/defaults/main.yml` | Rename variables for clarity, add documentation |

### LOW Risk

| # | Pattern | Example | Files Affected | Remediation |
|---|---------|---------|----------------|-------------|
| 9 | **Architecture Auto-Detection** | GPU slicing strategy auto-resolves based on virtualization | `roles/containers/runtime/defaults/main.yml` | Document auto-detection logic, allow explicit override |
| 10 | **Network Attachment Assumptions** | Caddy implicitly attached to all container networks | `roles/containers/caddy/defaults/main.yml` | Add explicit network configuration documentation |

---

## Phase 1: Audit & Document (Q2 2026)

### Objective
Create comprehensive documentation of all implicit settings and their effective values.

### Tasks

#### 1.1 Variable Precedence Diagram
**Owner**: Architecture Team  
**Effort**: 2 weeks

- [ ] Map all variable definition locations
- [ ] Document Ansible variable precedence rules as applied to project
- [ ] Create visual diagram showing override chains
- [ ] Identify circular dependencies or conflicting defaults

**Deliverable**: `docs/variable_precedence.md` with diagrams

#### 1.2 Profile Behavior Reference
**Owner**: Security Team  
**Effort**: 3 weeks

- [ ] Document all features enabled by each `deployment_profile` value
- [ ] Create matrix showing profile → feature mapping
- [ ] Identify features with complex conditional logic
- [ ] Document all `ephemeral_allow` style guard variables

**Deliverable**: `wiki_pages/Profile_Behavior_Reference.md`

#### 1.3 Variable Dependency Graph
**Owner**: DevOps Team  
**Effort**: 2 weeks

- [ ] Generate automated dependency graph for cascading variables
- [ ] Identify variables with >3 levels of inheritance
- [ ] Flag variables with conditional defaults based on other variables
- [ ] Create searchable index of variable dependencies

**Deliverable**: `docs/variable_dependencies.json` + visualization

#### 1.4 Checksum Audit
**Owner**: Security Team  
**Effort**: 1 week (CRITICAL - prioritize immediately)

- [ ] Audit all `*_verify: true` settings with empty checksums
- [ ] Populate missing checksums from upstream sources
- [ ] OR set verification toggles to `false` with documentation
- [ ] Add CI check to prevent future empty checksum + verify contradictions

**Deliverable**: Fixed `hardened_supply_chain.yml` + CI guard

---

## Phase 2: Consolidate (Q3 2026)

### Objective
Reduce implicit behavior by consolidating configuration logic into explicit, auditable structures.

### Tasks

#### 2.1 Profile Conditionals Consolidation
**Owner**: Architecture Team  
**Effort**: 4 weeks

- [ ] Create `profiles/` directory structure:
  ```
  profiles/
    ├── ephemeral.yml
    ├── dev.yml
    ├── vps.yml
    ├── hardened.yml
    ├── production.yml
    └── backup.yml
  ```
- [ ] Move all profile-based conditionals from role defaults to profile files
- [ ] Replace inline Jinja2 conditionals with explicit variable definitions
- [ ] Add profile validation schema

**Example Before**:
```yaml
# roles/containers/caddy/defaults/main.yml
containers_caddy_use_unix_sockets: "{{ true if deployment_profile | default('standard') in ['hardened', 'production'] else false }}"
```

**Example After**:
```yaml
# profiles/hardened.yml
containers_caddy_use_unix_sockets: true
containers_caddy_fail_secure: true
# ... all hardened-specific overrides

# profiles/dev.yml
containers_caddy_use_unix_sockets: false
containers_caddy_fail_secure: false
# ... all dev-specific overrides
```

**Deliverable**: Consolidated `profiles/` directory, removed inline conditionals

#### 2.2 Fail-Secure Chain Simplification
**Owner**: Security Team  
**Effort**: 3 weeks

- [ ] Document current inheritance: `core_security_fail_secure` → `containers_fail_secure` → service-specific
- [ ] Evaluate if 3-level inheritance is necessary
- [ ] Consider flattening to 2 levels: `global_fail_secure` → `role_fail_secure`
- [ ] Add explicit assertions in preflight checks

**Deliverable**: Simplified fail-secure logic, updated documentation

#### 2.3 Preflight Assertions Expansion
**Owner**: QA Team  
**Effort**: 3 weeks

- [ ] Add assertions for all critical implicit settings
- [ ] Require explicit declaration of effective values
- [ ] Add "configuration effective value" report at playbook start
- [ ] Fail deployment if implicit settings conflict

**Example Addition to `preflight_validate.yml`**:
```yaml
- name: Assert effective SSH port is explicitly known
  ansible.builtin.assert:
    that:
      - ssh_effective_port is defined
      - ssh_effective_port | int > 0
    fail_msg: >
      CRITICAL: ssh_effective_port must be explicitly determined.
      Current value: {{ ssh_effective_port | default('UNDEFINED') }}
      Check: system_ssh_port, advanced_security_hardening_random_ssh_port
```

**Deliverable**: Enhanced `playbooks/preflight_validate.yml`

#### 2.4 Checksum Population
**Owner**: Security Team  
**Effort**: 2 weeks

- [ ] Populate all empty checksums in `hardened_supply_chain.yml`
- [ ] Add automated checksum update workflow (dependabot-style)
- [ ] Document process for obtaining checksums from upstream
- [ ] Add checksum rotation schedule

**Deliverable**: Fully populated checksums, automated update process

---

## Phase 3: Enforce (Q4 2026)

### Objective
Enforce explicit configuration through CI/CD gates and runtime validation.

### Tasks

#### 3.1 CI Check for Implicit Dependencies
**Owner**: DevOps Team  
**Effort**: 2 weeks

- [ ] Add CI check to detect undocumented implicit variable dependencies
- [ ] Fail PRs that add new implicit conditionals without documentation
- [ ] Require explicit declaration of variable precedence in role metadata

**Example CI Check**:
```yaml
- name: Check for undocumented implicit conditionals
  run: |
    # Search for new inline conditionals in defaults files
    if grep -r "deployment_profile.*in \[" roles/*/defaults/main.yml; then
      echo "ERROR: Inline profile conditionals must be moved to profiles/"
      exit 1
    fi
```

**Deliverable**: CI workflow `.github/workflows/explicit_config_check.yml`

#### 3.2 Configuration Effective Value Report
**Owner**: DevOps Team  
**Effort**: 2 weeks

- [ ] Create playbook that runs before deployment
- [ ] Outputs all effective configuration values
- [ ] Highlights values that differ from defaults
- [ ] Generates audit log for compliance

**Example Output**:
```yaml
# Effective Configuration Report - 2026-02-25T12:00:00Z
# Profile: hardened

SSH Configuration:
  system_ssh_port: 2222 (overridden in vps.yml)
  ssh_effective_port: 2222 (computed)
  security_sshd_permit_root_login: "no" (default)

Container Runtime:
  podman_rootless_enabled: false (default)
  containers_systemd_dir: /etc/containers/systemd (computed from rootless=false)
  containers_caddy_http_port: 80 (computed from rootless=false)
```

**Deliverable**: `playbooks/report_effective_config.yml`

#### 3.3 Runtime Validation
**Owner**: Security Team  
**Effort**: 3 weeks

- [ ] Add runtime validation that effective values match expected
- [ ] Fail deployment if validation fails
- [ ] Log all implicit value resolutions for audit

**Deliverable**: Runtime validation framework

---

## Success Metrics

| Metric | Baseline | Q2 Target | Q3 Target | Q4 Target |
|--------|----------|-----------|-----------|-----------|
| Empty checksums with verify=true | 6 | 0 | 0 | 0 |
| Inline profile conditionals | 50+ | 50+ | 10 | 0 |
| Variables with >3 levels inheritance | 15 | 15 | 5 | 0 |
| Undocumented implicit dependencies | Unknown | Documented | 10 | 0 |
| Preflight assertions for implicit settings | 0 | 5 | 20 | 50+ |
| CI checks for implicit configuration | 0 | 0 | 1 | 3 |

---

## Risk Mitigation

### Risk: Breaking Changes
**Mitigation**: 
- Deprecation warnings in Q2 before enforcement in Q4
- Backward compatibility layer for existing deployments
- Clear migration guide for each phase

### Risk: Increased Complexity
**Mitigation**:
- Consolidate conditionals rather than duplicate
- Automated tooling to generate documentation
- Keep profile files simple and readable

### Risk: Operator Resistance
**Mitigation**:
- Document benefits: auditability, security, determinism
- Provide migration tooling and scripts
- Phased rollout with feedback loops

---

## Governance

### Review Cadence
- **Weekly**: Core team sync on Phase progress
- **Monthly**: Security review of remediation effectiveness
- **Quarterly**: Architecture review board approval for major changes

### Approval Requirements
- Phase 1 deliverables: Security team sign-off
- Phase 2 deliverables: Architecture team sign-off
- Phase 3 deliverables: CTO/Security Officer approval

---

## Related Documents

- [`Plan_DETERMINISM_ROADMAP.md`](Plan_DETERMINISM_ROADMAP.md) - Overall determinism strategy
- [`inventory/group_vars/all/hardened_supply_chain.yml`](inventory/group_vars/all/hardened_supply_chain.yml) - Checksum configuration
- [`inventory/group_vars/all/os_settings.yml`](inventory/group_vars/all/os_settings.yml) - Profile definitions
- [`playbooks/preflight_validate.yml`](playbooks/preflight_validate.yml) - Validation logic

---

*Last Updated: 2026-02-25*
