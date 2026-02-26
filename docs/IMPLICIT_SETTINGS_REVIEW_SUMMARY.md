# Implicit Settings Review Summary

**Date**: 2026-02-25  
**Review Type**: Security & Determinism Audit  
**Scope**: Deploy-System-Unified configuration patterns

---

## Executive Summary

A comprehensive review of implicit settings in Deploy-System-Unified identified **10 distinct patterns** of implicit configuration that create audit complexity, potential security gaps, and non-deterministic deployments.

**Key Findings**:
- **1 CRITICAL** security gap (empty checksums with verification enabled)
- **2 HIGH** risk patterns (cascading overrides, profile-based logic)
- **5 MEDIUM** risk patterns (inheritance chains, container modes, etc.)
- **2 LOW** risk patterns (auto-detection, network assumptions)

**Recommendation**: Implement 3-phase remediation plan (Q2-Q4 2026)

---

## Review Findings

### Critical Findings

#### 1. Empty Checksum "Verification" 🔴 CRITICAL

**Location**: `inventory/group_vars/all/hardened_supply_chain.yml`

**Issue**: Multiple GPG verification toggles set to `true` but checksums are empty strings (`""`)

```yaml
# Verification enabled but checksums empty
rpmfusion_verify_checksum: true
rpmfusion_free_sha256: ""
rpmfusion_nonfree_sha256: ""

nvidia_gpg_key_verify: true
nvidia_gpg_key_sha256: ""

amd_rocm_gpg_key_verify: true
amd_rocm_gpg_key_sha256: ""
```

**Risk**: False sense of security - verification logic may pass with empty checksums

**Remediation**: 
- Immediate: Populate checksums OR set verification to `false`
- Long-term: Add CI check to prevent empty checksum + verify contradictions

---

### High Risk Findings

#### 2. Cascading Variable Overrides

**Example**: SSH Port Configuration

```yaml
# os_settings.yml
system_ssh_port: "{{ 2222 if system_enable_endlessh | default(false) else 22 }}"
ssh_effective_port: "{{ advanced_security_hardening_random_ssh_port | default(system_ssh_port) | default(22) }}"

# vps.yml (overrides)
system_ssh_port: 2222  # Hard-coded override
```

**Risk**: Effective value depends on variable precedence and file load order

**Locations**:
- `inventory/group_vars/all/os_settings.yml`
- `inventory/group_vars/all/vps.yml`
- `inventory/group_vars/hardened.yml`

**Remediation**: Create variable precedence diagram, consolidate to single source

---

#### 3. Profile-Based Implicit Logic

**Example**: `deployment_profile: hardened` implicitly enables:

```yaml
# From os_settings.yml - computed based on profile
system_storage_dedupe_btrfs: "{{ true if deployment_profile in ['hardened', 'production'] else false }}"
system_storage_restic_archival: "{{ true if deployment_profile in ['hardened', 'production'] else false }}"

# From roles/containers/caddy/defaults/main.yml
containers_caddy_use_unix_sockets: "{{ true if deployment_profile in ['hardened', 'production'] else false }}"

# From roles/storage/dedupe/defaults/main.yml
storage_dedupe_ephemeral_skip: "{{ true if deployment_profile == 'ephemeral' and not system_storage_archival_ephemeral_allow else false }}"
```

**Risk**: 10+ features enabled/disabled based on single variable without explicit declaration

**Remediation**: Move profile conditionals to explicit `profiles/` directory

---

### Medium Risk Findings

#### 4. Fail-Secure Inheritance Chains

**Pattern**: 99 `fail_secure` references across 50+ files

```
core_security_fail_secure (global)
  └─→ containers_fail_secure (container roles)
       └─→ containers_caddy_fail_secure (service-specific)
       └─→ containers_media_fail_secure
       └─→ containers_monitoring_fail_secure
       └─→ containers_vaultwarden_fail_secure
```

**Risk**: Complex inheritance makes it difficult to audit effective security posture

**Remediation**: Simplify to 2-level inheritance, add preflight assertions

---

#### 5. Container Runtime Implicit Modes

**Example**: Rootless Podman determines 6+ system configurations

```yaml
# roles/containers/runtime/defaults/main.yml
podman_rootless_enabled: false  # Default: ROOTFUL

# This IMPLICITLY determines:
containers_systemd_dir: "/etc/containers/systemd"  # vs ~/.config/containers/systemd
containers_secrets_dir: "/etc/containers/secrets"  # vs ~/.config/containers/secrets
containers_systemd_scope: "system"                 # vs "user"
containers_caddy_http_port: 80                     # vs 8080
containers_caddy_https_port: 443                   # vs 8443
containers_caddy_network_mode: "host"              # vs "bridge"
```

**Risk**: Container networking and paths change based on single boolean

**Remediation**: Add explicit assertions in preflight checks

---

#### 6. Secrets Provider Selection

**Pattern**: `secrets_provider_mode` implicitly disables validation

```yaml
# inventory/group_vars/all/secrets_config.yml
secrets_provider_mode: "sops"  # Implicitly disables Ansible Vault enforcement

# Roles may have implicit assumptions about which provider is active
```

**Risk**: Roles may fail silently or use wrong provider

**Remediation**: Add explicit validation per provider mode in preflight

---

#### 7. Ephemeral Profile Guards

**Pattern**: 5+ features implicitly disabled unless explicitly allowed

```yaml
# os_settings.yml
system_storage_archival_ephemeral_allow: false
system_security_scanning_ephemeral_allow: false
system_security_ips_ephemeral_allow: false
storage_nfs_ephemeral_allow: false
ops_rsync_ephemeral_allow: false

# Complex conditional logic
storage_dedupe_ephemeral_skip: "{{ true if (deployment_profile == 'ephemeral' and not system_storage_archival_ephemeral_allow) else false }}"
```

**Risk**: Features silently disabled in ephemeral profile

**Remediation**: Document all guards in single reference, add warnings

---

#### 8. TCP Forwarding Logic

**Pattern**: Contradictory variable names create confusion

```yaml
# vps.yml
sshd_allow_tcp_forwarding: false              # Seems to disable
sshd_enable_trusted_group_exceptions: true    # But this re-enables for groups
sshd_trusted_groups: ['ssh-trusted']          # For these groups
```

**Risk**: Operators may think TCP forwarding is fully disabled when it's not

**Remediation**: Rename variables for clarity, add documentation

---

### Low Risk Findings

#### 9. Architecture Auto-Detection

**Example**: GPU slicing strategy auto-resolves

```yaml
# roles/containers/runtime/defaults/main.yml
containers_gpu_slicing:
  strategy: "auto"  # IMPLICITLY resolves to:
    # bare_metal → "mig"
    # virtual_host → "sriov"
    # virtual_guest → "passthrough"
```

**Risk**: May not match operator intent in edge cases

**Remediation**: Document auto-detection logic, allow explicit override

---

#### 10. Network Attachment Assumptions

**Example**: Caddy attached to all container networks

```yaml
# roles/containers/caddy/defaults/main.yml
containers_caddy_network: "proxy_net"
containers_caddy_extra_networks: ['media_net', 'ops_net', 'monitoring_net', 'anubis_net']

# Comment: "For simplicity with Quadlets, we can attach multiple networks"
```

**Risk**: Caddy has access to all container traffic (security boundary)

**Remediation**: Add explicit network configuration documentation

---

## Remediation Plan

A comprehensive **3-phase remediation plan** has been created:

📄 **See**: [`../wiki_pages/PLAN_IMPLICIT_SETTINGS_REMEDIATION.md`](../wiki_pages/PLAN_IMPLICIT_SETTINGS_REMEDIATION.md)

### Phase 1: Audit & Document (Q2 2026)
- Create variable precedence diagram
- Document profile-based implicit behaviors
- Generate dependency graph
- **CRITICAL**: Audit empty checksums

### Phase 2: Consolidate (Q3 2026)
- Move profile conditionals to `profiles/` directory
- Simplify fail-secure inheritance
- Expand preflight assertions
- Populate missing checksums

### Phase 3: Enforce (Q4 2026)
- Add CI checks for implicit dependencies
- Generate configuration effective value reports
- Runtime validation framework

---

## Integration with Existing Plans

This review integrates with:

1. **[../wiki_pages/PLAN_DETERMINISM_ROADMAP.md](../wiki_pages/PLAN_DETERMINISM_ROADMAP.md)** - Updated with implicit settings section
2. **[../wiki_pages/PLAN_ROLE_ENHANCEMENT_EXECUTION_PLAN_2026.md](../wiki_pages/PLAN_ROLE_ENHANCEMENT_EXECUTION_PLAN_2026.md)** - Cross-referenced
3. **[../wiki_pages/PLAN_STABILITY_PLAN.md](../wiki_pages/PLAN_STABILITY_PLAN.md)** - Added explicit configuration goal

---

## Success Metrics

| Metric | Current | Q2 2026 | Q3 2026 | Q4 2026 |
|--------|---------|---------|---------|---------|
| Empty checksums with verify=true | 6 | 0 | 0 | 0 |
| Inline profile conditionals | 50+ | 50+ | 10 | 0 |
| Variables with >3 levels inheritance | 15 | 15 | 5 | 0 |
| Undocumented implicit dependencies | Unknown | Documented | 10 | 0 |
| Preflight assertions | 0 | 5 | 20 | 50+ |

---

## Governance

- **Weekly**: Core team sync on Phase progress
- **Monthly**: Security review of remediation effectiveness
- **Quarterly**: Architecture review board approval

---

## Approval

**Security Team**: _________________  Date: _________

**Architecture Team**: _____________  Date: _________

**CTO/Security Officer**: __________  Date: _________

---

*Last Updated: 2026-02-25*
