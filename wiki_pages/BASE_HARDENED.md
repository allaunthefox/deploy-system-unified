# BASE_HARDENED

The **BASE_HARDENED** profile serves as the primary security baseline for all production hosts within the project. it implements a rigorous set of security configurations, including kernel hardening, strict access controls, and forensic logging readiness.

### Canonical Reference
The source YAML for this profile is located at:
- `projects/deploy-system-unified/BASE_HARDENED.yml`
- `projects/deploy-system-unified/branch_templates/BASE_HARDENED.yml`

### Core Features
- Mandatory kernel sysctl hardening.
- Automated security patching and repository management.
- Enhanced SSH daemon security.
- Forensic-ready log aggregation.
