# Strict Compliance Remediation Checklist

This document tracks compliance with strict production-grade standards for POSIX shell, container security, deterministic builds, and least-privilege enforcement.

## Compliance Status

| Category | Status | Last Validated |
|----------|--------|----------------|
| POSIX Shell | ✅ Compliant | 2026-02-27 |
| Deterministic Docker Build | ✅ Compliant | 2026-02-27 |
| Container Logging | ✅ Compliant | 2026-02-27 |
| Docker Security Hardening | ✅ Compliant | 2026-02-27 |
| Init System Portability | ✅ Compliant | 2026-02-27 |
| Idempotent Deployment | ✅ Compliant | 2026-02-27 |
| FHS | ✅ Compliant | 2026-02-27 |
| Centralized Configuration | ✅ Compliant | 2026-02-27 |
| Least Privilege | ✅ Compliant | 2026-02-27 |

---

## POSIX Shell Compliance

### Requirements
- [x] Shebang: `#!/bin/sh` (not `#!/bin/bash`)
- [x] No `set -o pipefail` (use `set -eu`)
- [x] No `[[ ... ]]` (use `[ ... ]`)
- [x] No `==` in test (use `=`)
- [x] No `function name()` (use `name()`)
- [x] No `echo -e` (use `printf`)
- [x] No `&>` redirection (use `> file 2>&1`)
- [x] No arrays, `$RANDOM`, or bash-specific features

### Validated Files
- [x] `scripts/*.sh` - All POSIX compliant
- [x] `tasks/*.sh` - All POSIX compliant

### Validation Command
```bash
for script in scripts/*.sh; do
  dash "$script" && echo "PASS: $script" || echo "FAIL: $script"
done
```

---

## Deterministic Docker Build Compliance

### Requirements
- [x] Base image pinned to digest (not tag)
- [x] Non-root USER directive
- [x] HEALTHCHECK instruction
- [x] Version-pinned dependencies
- [x] `--no-install-recommends` for apt
- [x] Cache cleanup in same RUN layer

### Helm Chart Security (Kubernetes)
- [x] `securityContext.runAsNonRoot: true`
- [x] `securityContext.allowPrivilegeEscalation: false`
- [x] `capabilities.drop: [ALL]`
- [x] Resource requests and limits
- [x] Liveness and readiness probes
- [x] Secrets via secretKeyRef (not plaintext)

### Validated Files
- [x] `charts/database-stack/templates/postgresql-deployment.yaml`

---

## Container Logging Compliance

### Requirements
- [x] Logs to stdout/stderr (not files)
- [x] No file-based logs inside container
- [x] 12-factor logging principles

### Configuration
```yaml
access_log /dev/stdout;
error_log /dev/stderr;
```

---

## Docker Security Hardening

### Requirements
- [x] No `/var/run/docker.sock` mount
- [x] `restart: unless-stopped` policy
- [x] Resource limits (memory, CPU)
- [x] `read_only: true` where feasible
- [x] `userns-remap` enabled
- [x] No privileged containers

### Validation
```bash
grep -r "docker.sock" charts/ roles/containers/
# Should return nothing
```

---

## Init System Portability

### Requirements
- [x] Detect init system before writing service files
- [x] Support systemd detection
- [x] Fail gracefully on unsupported init
- [x] EUID check before privileged operations

### Implementation
```sh
if command -v systemctl >/dev/null 2>&1; then
  # systemd installation
else
  echo "Unsupported init system"
  exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
  echo "Must run as root"
  exit 1
fi
```

---

## Idempotency Compliance

### Requirements
- [x] `mkdir -p` (not `mkdir`)
- [x] Conditional file overwrites
- [x] Service reinstallation checks
- [x] Safe re-runnable scripts

### Validation
```bash
# Run playbook twice, assert zero changes
ansible-playbook site.yml --check --diff | grep -c '"changed": true'
# Should be 0 on second run
```

---

## Configuration Centralization

### Requirements
- [x] Single source of truth for paths
- [x] No hardcoded `/opt/deploy-system`
- [x] Use variables: `INSTALL_DIR=${INSTALL_DIR:-/opt/deploy-system}`

### Implementation
```sh
# Top of script
INSTALL_DIR="${INSTALL_DIR:-/opt/deploy-system}"
CONFIG_DIR="$INSTALL_DIR/config"
LOG_DIR="$INSTALL_DIR/logs"

# Replace all occurrences
sed -i "s|/opt/deploy-system|\"\$INSTALL_DIR\"|g" script.sh
```

---

## Least Privilege Compliance

### Requirements
- [x] No host Docker socket exposure
- [x] No root container execution
- [x] Explicit umask setting
- [x] Explicit file permission setting
- [x] No unvalidated external input
- [x] Explicit PATH validation

### Implementation
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 999
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

---

## Filesystem Hierarchy Standard (FHS)

### Status: ✅ Compliant

| Path | Usage | FHS Compliant |
|------|-------|---------------|
| `/opt/deploy-system` | Application installation | ✅ Yes |
| `/usr/local/bin` | Local binaries | ✅ Yes |
| `/etc/systemd/system` | Service files | ✅ Yes |
| `/var/log` | Log files | ✅ Yes |
| `/var/lib` | State data | ✅ Yes |

---

## Reproducibility Compliance

### Requirements
- [x] Pinned image digests
- [x] Pinned dependency versions
- [x] No "latest" tags
- [x] No implicit environment dependence
- [x] Lock file for dependencies

### Validation
```bash
# Check for unpinned images
grep -r ":latest" charts/ roles/containers/
# Should return nothing

# Check for version ranges
grep -r ">=.*<" requirements.yml
# Should show upper bounds
```

---

## Validation Commands

### Full Compliance Check
```bash
# Run compliance validation task
ansible-playbook playbooks/preflight_assertions.yml \
  -e "compliance_validation_enabled=true"
```

### Individual Checks
```bash
# POSIX compliance
dash scripts/*.sh

# Docker socket
grep -r "docker.sock" charts/ roles/

# Image tags
grep -E "image.*:.*latest" charts/*/values.yaml

# Hardcoded paths
grep -v "^#" scripts/*.sh | grep "/opt/deploy-system"

# Idempotency
ansible-playbook site.yml && ansible-playbook site.yml --check
```

---

## Remediation History

| Date | Issue | Remediation | Status |
|------|-------|-------------|--------|
| 2026-02-27 | POSIX shell compliance | Converted all scripts to #!/bin/sh | ✅ Complete |
| 2026-02-27 | Container security | Added securityContext to Helm charts | ✅ Complete |
| 2026-02-27 | Resource limits | Added requests/limits to deployments | ✅ Complete |
| 2026-02-27 | Health checks | Added liveness/readiness probes | ✅ Complete |
| 2026-02-27 | Secret management | Changed to secretKeyRef | ✅ Complete |

---

## Next Steps

1. **Quarterly Compliance Review** - Re-run validation tasks
2. **Dependency Updates** - Review pinned versions quarterly
3. **Security Scanning** - Integrate Trivy/Clair in CI
4. **CIS Benchmark Alignment** - Map to CIS Docker Benchmark

---

**Overall Compliance Status: ✅ COMPLIANT**

Last validated: 2026-02-27  
Next review: 2026-05-27
